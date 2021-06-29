from django.db import models 

class ChatTracker(models.Model): 
    chatid = models.CharField(max_length=5000,default="", blank=True,) 

    init_message = models.CharField(max_length=5000,default="", blank=True,)
 
    zipcode = models.CharField(max_length=100,default="", blank=True)
     
    email = models.CharField(max_length=100,default="", blank=True)
     
    def __str__(self):
        return str(self.chatid)+"__"+str(self.zipcode)