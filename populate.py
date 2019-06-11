import os
import csv

if __name__ == '__main__':

    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'main.settings')
    django.setup()
    from main.models import Group, Student, Rating, ClassTeam, ClassNo, Phase

    def create_rating(student, allocator, phase, allocation):
        return Rating.objects.get_or_create(
            student=student,
            allocator=allocator,
            phase=phase,
            allocation=allocation
        )[0]

    def assign_team(students):

        base_path = os.path.dirname(os.path.realpath(__file__))
        csv_file = os.path.join(base_path, 'Team_allocation.csv')
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            lookup = {item[0]: item[1] for item in reader}

        # Create teams and assign students to them
        for student in students:
            team_letter = lookup[student.student_code]
            class_team = ClassTeam.objects.get_or_create(team_letter=team_letter, class_no=student.class_no)[0]
            class_team.save()
            student.class_team = class_team
            student.save()

    def populate_base_ratings(students):

        for phase in ['ID', 'DD']:# 'DD', 'IF', 'FS']:
            phase = Phase.objects.get_or_create(phase=phase)[0]
            for student in students:
                team = ClassTeam.objects.get(
                    class_no=student.class_no,
                    team_letter=student.class_team.team_letter)

                team_members = Student.objects.filter(class_team=team)
                split = int(100/len(team_members))

                for team_member in team_members:
                    r = create_rating(student, team_member, phase, split)
                    r.save()

    #students = Student.objects.all()

    #assign_team(students)

    students_in_teams = Student.objects.all()

    populate_base_ratings(students_in_teams)

