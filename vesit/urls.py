from django.urls import path
from .views import (home,index, create_event, event,approve_events,approve_level,CouncilStudentCreateView, 
CouncilStudentListView,
CouncilStudentDetailView, 
TeamStudentCreateView,
TeamStudentListView,
TeamStudentDetailView
)

urlpatterns = [
    path('',home, name = 'home' ),
    path('index/',index,name='index'),
    path('create_event', create_event, name = 'create_event' ),
    path('events/',event,name='events'),
    path( 'approve_events', approve_events, name='approve_events' ),
    path( 'approve_level\<int:eid>\<int:approved>\<int:level>', approve_level, name='approve-level' ),

    path('council_student_create/', CouncilStudentCreateView.as_view(), name="council_student_create"),
    path('council_student_list/', CouncilStudentListView.as_view(), name="council_student_list"),
    path('<int:pk>/council_student_detail/', CouncilStudentDetailView.as_view(), name="council_student_detail"),

    path('team_student_create/', TeamStudentCreateView.as_view(), name="team_student_create"),
    path('team_student_list/', TeamStudentListView.as_view(), name="team_student_list"),
    path('<int:pk>/team_student_detail/', TeamStudentDetailView.as_view(), name="team_student_detail"),


]