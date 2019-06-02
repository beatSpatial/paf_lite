from django.shortcuts import render
from .models import Student, Rating, ClassTeam, Phase
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .filters import TeamFilter

import ast


def landing(request, phase):
    # create context from request
    context = {'phase': phase}
    return render(request, 'main/index.html', context)


def get_team_options(request):
    password = request.GET.get('pass', '')
    class_team = Student.objects.get(password=password.upper()).class_team
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
            new_rating = create_rating(student=student,
                                       allocator=allocator,
                                       phase=phase,
                                       allocation=tp(paf_alloc[i + 1][1] - score))

        except IndexError:
            new_rating = create_rating(student=student,
                                       allocator=allocator,
                                       phase=phase,
                                       allocation=tp(10 - score))

        new_rating.save()

    return JsonResponse('cool', safe=False)


def team_search(request):
    team_filter = TeamFilter(request.GET, queryset=ClassTeam.objects.all())
    team = team_filter.qs
    students = Student.objects.filter(class_team=team[0])

    if request.method == "POST":
        print('post FUCK')
        phase = request.GET.get('limit', '')

    if request.method == "GET":
        limit = request.GET.get('limit', '')
        print(limit)

    return render(request, 'main/search/team_list.html', {
        'phases': Phase.objects.all(),
        'filter': team_filter,
        'team': team,
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


def rating(student=None, allocator=None, phase=None, r_pk=None):
    if not r_pk:
        r = Rating.objects.filter(
            student=student,
            allocator=allocator,
            phase=phase,
        ).latest()
    else:
        r = Rating.objects.get(pk=r_pk)
    return r


def toggle_total_alloc(request):
    phase = Phase.objects.get(pk=int(request.GET.get('phase', '')))
    student = Student.objects.get(pk=request.GET.get('pk', ''))
    team_members = Student.objects.filter(class_team=student.class_team)

    # decorate rating
    rating_off = toggle_off(rating)

    # Don't use any of the ratings
    [rating_off(tm, student, phase) for tm in team_members]

    # return team_search(request)

    return render(request, 'main/search/table.html', {
        'students': team_members,
        'cs': (len(team_members) * 2)
    })


def toggle_single_alloc(request):
    # Decorate the rating function
    toggle_rating = toggle(rating)

    # The rating after it being toggled
    toggled_rating = toggle_rating(r_pk=request.GET.get('pk', ''))
    student = toggled_rating.student
    team_members = Student.objects.filter(class_team=student.class_team)

    return render(request, 'main/search/table.html', {
        'students': team_members,
        'cs': (len(team_members) * 2)
    })
