from django.urls import path, include
from . import views
from django.views.generic import TemplateView, RedirectView
from base.views import ChatApp, AllTeams, SingleTeam

# urlpatterns = [
#    path('', views.home )
# ]s

# using the CBVs
# 1. Templateviews 
urlpatterns =[
    path('', TemplateView.as_view(template_name="base/home.html", extra_context={'title':'Custom Title'})),
    path('chat/', ChatApp.as_view(), name='chat'),
    #redirectView
    path('rdt', RedirectView.as_view(url='https://github.com/Clinton-John'), name='redirect_user'),
    ## redrict users from all the pages to a single post page
    path('viewteams/<str:pk>', AllTeams.as_view(), name='redirect_all_teams'),
    path('viewSingleTeam/<str:pk>', SingleTeam.as_view(), name='redirect_single_team'),


     
]
