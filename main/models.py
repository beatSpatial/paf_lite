from django.db import models

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save

from .signals import csv_uploaded
from .validators import csv_file_validator
import io
import csv

FEB = "IT.f"
AUG = "IT.a"
MAY = "IT.m"
OCT = "IT.o"
STEM = "IT.s"

GROUP_CHOICES = (
    (FEB, "February Standard"),
    (AUG, "August Standard"),
    (MAY, "May Express"),
    (OCT, "October Express"),
    (STEM, "STEM High achievers"),
)

TEAM_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
)

CLASS_CHOICES = ((str(i), str(i)) for i in range(1, 11))

PHASE_CHOICES = (
    ('PP', 'Proposal'),
    ('ID', 'Interface'),
    ('DD', 'Database'),
    ('IF', 'Functionality'),
    ('FS', 'Final'),
)


def upload_csv_file(instance, filename):
    qs = instance.__class__.objects.filter(user=instance.user)
    if qs.exists():
        num_ = qs.last().id + 1
    else:
        num_ = 1
    return f'csv/{num_}/{instance.user.username}/{filename}'


class Phase(models.Model):
    phase = models.CharField(max_length=2, choices=PHASE_CHOICES)

    def __str__(self):
        return self.get_phase_display()


class Group(models.Model):
    month = models.CharField(max_length=4, choices=GROUP_CHOICES)
    year = models.PositiveSmallIntegerField(
        default=18,
        validators=[MaxValueValidator(30), MinValueValidator(18)]
    )

    def __str__(self):
        return "{} {}".format(self.get_month_display(), self.year)


class ClassNo(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    class_no = models.CharField(max_length=2, choices=CLASS_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(self.class_no)


class ClassTeam(models.Model):
    team_letter = models.CharField('Team', max_length=1, choices=TEAM_CHOICES, null=True, blank=True)
    class_no = models.ForeignKey(ClassNo, on_delete=models.CASCADE, blank=True, null=True)
    limit = models.PositiveSmallIntegerField(
        default=15,
        validators=[MaxValueValidator(5), MinValueValidator(30)]
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['team_letter', 'class_no'], name='unique_team'), ]
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def __str__(self):
        return f'Team {str(self.team_letter)} in class {str(self.class_no)}.'


def sapa_calc(ss, ts, ns):
    # self score, total score & number of scores
    # Getting back None from ss causing an exception
    try:
        return "{0:.2f}".format(ss / ((ts - ss) / (ns - 1)))
    except ZeroDivisionError:
        return "{0:.2f}".format(1)


def paf_calc(ts, ntm, ns):
    # total score, no of team members, no of scores
    return "{0:.2f}".format((ts / 100) * (ntm / ns))


# TODO Decorator experiment
def get_score_from_rating(func, *args, **kwargs):
    return


def get_score(student, allocator, phase):
    # Returns 1 number the rating given to a student by an allocator

    phase = Phase.objects.get(phase=phase)
    score = Rating.objects.filter(
        student=student,
        allocator=allocator,
        phase=phase,
    ).latest()

    if score.use:
        return score.allocation
    else:
        return None


def get_raw_rating(student, allocator, phase):
    phase = Phase.objects.get(phase=phase)
    rating = Rating.objects.filter(
        student=student,
        allocator=allocator,
        phase=phase,
    ).latest()

    return rating


def get_team_scores(student, phase='PP'):

    # a queryset of team members
    team_members = Student.objects.filter(class_team=student.class_team)
    no_team_members = len(team_members)
    score_list = list(filter(None, [get_score(student, member, phase) for member in team_members]))
    no_scores = len(score_list)
    total_score = sum(score_list)
    return total_score, no_team_members, no_scores


def get_limit(self, tm, limit):
    self_score = get_score(self, self, 'PP')
    if self_score is None:
        return False
    else:
        total_score, _, no_scores = get_team_scores(tm, 'PP')
        # probs

        ratio = sapa_calc(self_score, total_score, no_scores)

        return abs(float(ratio) - 1.00) > (float(limit/100))


class Student(models.Model):
    student_code = models.CharField(max_length=8, null=True, blank=True)
    password = models.CharField(max_length=8, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    class_no = models.ForeignKey(ClassNo, on_delete=models.CASCADE, null=True, blank=True)
    class_team = models.ForeignKey(ClassTeam, on_delete=models.CASCADE, blank=True, null=True)
    surname = models.CharField(max_length=75, null=True, blank=True)
    given_name = models.CharField(max_length=50, null=True, blank=True)
    pref_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=70, blank=True, null=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def save(self, *args, **kwargs):
        self.student_code = self.student_code.upper()
        super(Student, self).save(*args, **kwargs)

    def sus_name(self):
        p = self.pref_name
        g = self.given_name
        s = self.surname
        given = p if p is None else g
        return f" {given} {s}, "

    def paf(self, phase='PP'):

        if self.class_team.team_letter is not None:

            # Get team score adds the scores from other team members
            total_score, no_team_members, no_scores = get_team_scores(self, phase)
            try:
                # total score, no_team_members, no_scores
                return paf_calc(total_score, no_team_members, no_scores)

            except ZeroDivisionError:
                return None
        else:
            return None

    def sapa(self, phase='PP'):
        if self.class_team.team_letter is not None:
            total_score, _, no_scores = get_team_scores(self, phase)

            self_score = get_score(self, self, phase)
            # Self score is not being used
            if self_score is not None:
                return sapa_calc(self_score, total_score, no_scores)
            else:
                return "SA not Justified"

    def ratios(self):
        class_team = self.class_team
        limit = class_team.limit

        team_members = Student.objects.filter(class_team=class_team)
        total_score, _, no_scores = get_team_scores(self, 'PP')
        collector = []
        for tm in team_members:
            self_score = get_score(self, tm, 'PP')

            if self_score is not None:
                ratio = sapa_calc(self_score, total_score, no_scores)
            else:
                ratio = ""
            try:
                collector.append((ratio, abs(float(ratio) - 1.00) > (float(limit/100))))
            except ValueError:
                # "ratio is "SA not Justified" so
                collector.append((ratio, False))

        return collector

    def raw_score(self):
        """

        :return: A list of tuples.
         tuple with index 0 is the score given regardless of whether it is used or not,
         and a Bool indicating whether the score exceeds the limit
        """

        class_team = self.class_team
        team_members = Student.objects.filter(class_team=class_team)
        limit = class_team.limit

        return [(get_raw_rating(self, team_member, 'PP'),
                 get_limit(self, team_member, limit)) for team_member in team_members]

    def __str__(self):
        return f"{self.surname}, {self.given_name} {'({})'.format(self.pref_name) if self.pref_name is not None else ''}"


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    allocator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='allocator')
    use = models.BooleanField(default=True)
    allocation = models.PositiveSmallIntegerField(
        default=33,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ['created_at', ]

    def __str__(self):
        return f"{self.allocator},  {self.allocation} points " \
            f" for {self.phase}"


# Create your models here.
class CSVUpload(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_csv_file, validators=[csv_file_validator])
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file)


def convert_header(csvHeader):
    header_ = csvHeader[0]
    cols = [x.replace(' ', '_').lower() for x in header_.split(",")]
    return cols


def csv_upload_post_save(sender, instance, created, *args, **kwargs):
    if not instance.completed:
        csv_file = instance.file
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=';', quotechar='|')
        header_ = next(reader)
        header_cols = convert_header(header_)
        parsed_items = []

        '''
        if using a custom signal
        '''
        for line in reader:
            parsed_row_data = {}
            i = 0
            row_item = line[0].split(',')
            for item in row_item:
                key = header_cols[i]
                parsed_row_data[key] = item
                i += 1

            parsed_items.append(parsed_row_data)

        for item in parsed_items:
            try:
                month = item['group10'][:4]
                class_no = item['group10'][-2:]
            except KeyError:
                month = item['group'][:4]
                class_no = item['group'][-2:]
            g = Group.objects.get_or_create(
                month=month, year=19
            )[0]
            g.save()

            try:
                cn = ClassNo.objects.get_or_create(group=g, class_no=int(class_no))[0]
                cn.save()
                fyid = item['username'].upper()

                s = Student.objects.get_or_create(
                    student_code=fyid,
                    password=item['password'].upper(),
                    group=g,
                    class_no=cn,
                    surname=item['lastname'],
                    given_name=item['firstname'],
                    pref_name=item['preferredname'],
                    email=item['email']
                )[0]
                s.save()
            except ValueError:
                print('excepting out cause no class no')
                pass

        csv_uploaded.send(sender=instance, user=instance.user, csv_file_list=parsed_items)
        instance.completed = True
        instance.save()


post_save.connect(csv_upload_post_save, sender=CSVUpload)
