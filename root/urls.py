
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('mazamamedia_chatbotapi/', index, name='index'),       
    path('submit_info/<str:id>', submit_info, name='submit_info'),       
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

