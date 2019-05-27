
from django.urls import include, path
from django.contrib import admin
from main import views
from django_filters.views import FilterView
from .filters import TeamFilter

urlpatterns = [
  path('admin/', admin.site.urls),
  path('pp', views.pp, name='pp'),
  path('id', views.id, name='id'),
  path('dd', views.dd, name='dd'),
  path('fi', views.fi, name='fi'),
  path('fs', views.fs, name='fs'),
  path('get_team_options', views.get_team_options, name='get-team-options'),
  path('set_team_alloc', views.set_team_alloc, name='set-team-alloc'),
  path('teams/', views.team_search, name='teams')
]
