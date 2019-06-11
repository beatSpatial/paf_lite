
from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('get_team_options', views.get_team_options, name='get-team-options'),
  path('set_team_alloc', views.set_team_alloc, name='set-team-alloc'),
  path('teams/', views.team_search, name='teams'),
  #path('toggle_total_alloc', views.toggle_total_alloc, name='toggle-total-alloc'),
  path('toggle_single_alloc', views.toggle_single_alloc, name='toggle-single-alloc'),
  path('<str:phase>', views.landing, name='landing'),
]
