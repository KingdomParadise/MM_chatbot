
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('', index, name='index'),  
    path('', index, name='userConfigurate'),  
    path('', index, name='orderStatement')       
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

