from django.shortcuts import render
from .models import Student, Rating, ClassTeam, Phase
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from .filters import TeamFilter
from .models import get_raw_rating

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
    team_filter = TeamFilter(request.GET, queryset=team_list)
    team = team_filter.qs
    students = Student.objects.filter(class_team=team[0])
    phases = Phase.objects.all()

    return render(request, 'main/search/team_list.html', {
        'phases': phases,
        'filter': team_filter,
        'students': students,
        'cs': len(students) * 2
    })


# decorator
def toggle(func):
    def inner_toggle(*args, **kwargs):
        r = func(*args, **kwargs)
        if r.use:
            r.use = False
        else:
            r.use = True
        r.save()
        return r
    return inner_toggle


# decorator
def toggle_off(func):
    def inner_toggle_off(*args, **kwargs):
        r = func(*args, **kwargs)
        if r.use:
            r.use = False
            r.save()
        return r
    return inner_toggle_off


def rating(student=None, allocator=None, phase_pk=None, r_pk=None):
    if not r_pk:
        phase = Phase.objects.get(pk=phase_pk)
        r = Rating.objects.filter(
            student=student,
            allocator=allocator,
            phase=phase,
        ).latest()
    else:
        r = Rating.objects.get(pk=r_pk)
    return r


def toggle_total_alloc(request):
    std_pk = request.GET.get('pk', '')
    phase_pk = request.GET.get('phase', '')

    phase = Phase.objects.get(pk=int(phase_pk))

    student = Student.objects.get(pk=std_pk)
    team_members = Student.objects.filter(class_team=student.class_team)

    rating_off = toggle_off(rating)

    # first ever use of decorator
    [rating_off(tm, student, phase.pk) for tm in team_members]

    return team_search(request)


def toggle_single_alloc(request):
    # Decorate the rating function
    toggle_rating = toggle(rating)

    # The rating after it being toggled
    toggled_rating = toggle_rating(r_pk=request.GET.get('pk', ''))
    student = toggled_rating.student
    students = Student.objects.filter(class_team=student.class_team)

    return render(request, 'main/search/table.html', {
        'students': students,
        'cs': (len(students) * 2)
    })
