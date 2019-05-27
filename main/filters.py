from .models import ClassTeam
import django_filters

"""
team_letter = models.CharField('Team', max_length=1, choices=TEAM_CHOICES, null=True, blank=True)
    class_no = models.ForeignKey(ClassNo, on_delete=models.CASCADE, blank=True, null=True)


"""


class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = ClassTeam
        fields = ['class_no', 'team_letter', ]