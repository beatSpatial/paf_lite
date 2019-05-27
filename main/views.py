from django.shortcuts import render
from .models import Student, Rating, ClassTeam, Phase
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from .filters import TeamFilter

import ast


def pp(request):
    return render(request, 'main/phases/PP.html')


def id(request):
    return render(request, 'main/phases/ID.html')


def dd(request):
    return render(request, 'main/phases/DD.html')


def fi(request):
    return render(request, 'main/phases/IF.html')


def fs(request):
    return render(request, 'main/phases/PP.html')


def get_team_options(request):
    password = request.GET.get('pass', '')
    s = Student.objects.get(password=password.upper())

    class_team = s.class_team

    team_members = Student.objects.filter(class_team=class_team)

    starting_prop = 10.0 / len(team_members)

    peers = [
        {
            'value': i * starting_prop,
            'type': str(student.pk)
        } for i, student in enumerate(team_members)]

    lookup = {}
    for student in team_members:
        lookup[str(student.pk)] = str(student)

    return JsonResponse([peers, lookup], safe=False)


def tp(num):
    return num / 10 * 100


def create_rating(student, allocator, phase, allocation):
    return Rating.objects.create(
        student=student,
        allocator=allocator,
        phase=phase,
        allocation=allocation
    )


def set_team_alloc(request):
    password = request.GET.get('pass', '')
    alloc = request.GET.get('alloc', '')
    phase = request.GET.get('phase', '')
    alloc = ast.literal_eval(alloc)

    allocator = Student.objects.get(password=password.upper())
    team_members = Student.objects.filter(class_team=allocator.class_team)
    phase = Phase.objects.get(phase=phase)

    paf_alloc = list(zip([student.pk for student in team_members], alloc))

    for i, (pk, score) in enumerate(paf_alloc):
        student = Student.objects.get(pk=pk)

        try:
            rating = create_rating(student=student,
                                   allocator=allocator,
                                   phase=phase,
                                   allocation=tp(paf_alloc[i + 1][1] - score))

        except IndexError:
            rating = create_rating(student=student,
                                   allocator=allocator,
                                   phase=phase,
                                   allocation=tp(10 - score))

        rating.save()

    return JsonResponse('cool', safe=False)


def team_search(request):
    team_list = ClassTeam.objects.all()
    print(request)
    team_filter = TeamFilter(request.GET, queryset=team_list)
    print('FUCK6')
    print(request.GET)
    print('FK7')
    team = team_filter.qs
    students = Student.objects.filter(class_team=team[0])
    phases = Phase.objects.all()
    #print(list((student, student.paf()) for student in students))

    return render(request, 'main/search/team_list.html', {
        'phases': phases,
        'filter': team_filter,
        'students': students,
        'cs': len(students)
    })


