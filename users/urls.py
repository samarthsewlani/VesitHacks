from django.urls import path
#from .views import home
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [

	path( 'login/',  views.login, name= 'login' ),
	path( 'logout/', views.logout, name = 'logout' )
    
]
if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)