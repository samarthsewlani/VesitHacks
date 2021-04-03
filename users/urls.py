from django.urls import path
#from .views import home
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import DepartmentCreateView,DepartmentDetailView,DepartmentListView,StudentCreateView,StudentDetailView,StudentListView

urlpatterns = [

	path( 'login/',  views.login, name= 'login' ),
	path( 'logout/', views.logout, name = 'logout' ),
	path( 'department/new',DepartmentCreateView.as_view(),name='new-department'),
	path( 'department/<int:pk>',DepartmentDetailView.as_view(),name="department-detail"),
    path( 'department/all',DepartmentListView.as_view(),name='department-list'),
	path( 'student/new',StudentCreateView.as_view(),name='new-student'),
	path( 'student/<int:pk>',StudentDetailView.as_view(),name="student-detail"),
    path( 'student/all',StudentListView.as_view(),name='student-list'),
    
]
if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)