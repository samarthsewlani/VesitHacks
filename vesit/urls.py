from django.urls import path
from .views import home,index, create_event, event,approve_events,approve_level

urlpatterns = [
    path('',home, name = 'home' ),
    path('index/',index,name='index'),
    path('create_event', create_event, name = 'create_event' ),
    path('events/',event,name='events'),
    path( 'approve_events', approve_events, name='approve_events' ),
    path( 'approve_level\<int:eid>\<int:approved>\<int:level>', approve_level, name='approve-level' ),

]