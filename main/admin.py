from django.contrib import admin
from .models import CSVUpload, Student, Rating, ClassTeam, ClassNo
from django.forms.models import BaseInlineFormSet



class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'given_name', 'pref_name')# 'team',
                    #'proposal', 'interface', 'database', 'function', 'final')

    list_filter = ('class_no', )
    ordering = ('class_no',)

    def team(self, student):
        return student.class_team.team_letter

    team.admin_order_field = 'class_team__team_letter'


class TeamMembersTabularInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ['student_code', 'password', 'paf', 'sapa', 'ratios',]# 'scores',]
    readonly_fields = ['paf', 'sapa', 'ratios']# 'scores',]


class ClassTeamAdmin(admin.ModelAdmin):
    list_display = ('team_letter', 'class_no',)

    list_filter = ('class_no', 'team_letter',)
    ordering = ('class_no', 'team_letter')

    inlines = [
        TeamMembersTabularInline,
    ]

    @staticmethod
    def team_members(team):
        return "".join([s.sus_name() for s in Student.objects.filter(class_team=team)])[:-2]


class RatingAdmin(admin.ModelAdmin):
    list_display = ('student', 'phase', 'allocation')
    list_filter = ('student__class_no', 'student__class_team__team_letter',)
    ordering = ('-created_at',)


admin.site.register(Student, StudentAdmin)
admin.site.register(ClassTeam, ClassTeamAdmin)
admin.site.register(CSVUpload)
admin.site.register(Rating, RatingAdmin)
admin.site.register(ClassNo)
