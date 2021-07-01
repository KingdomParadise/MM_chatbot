from django.db import models 

class ChatTracker(models.Model): 
    chatid = models.CharField(max_length=5000,default="", blank=True,) 

    init_message = models.CharField(max_length=5000,default="", blank=True,)
 
    zipcode = models.CharField(max_length=100,default="", blank=True)
     
    email = models.CharField(max_length=100,default="", blank=True)
    
     
    def __str__(self):
        return str(self.chatid)+"__"+str(self.zipcode)
    
class UserConfiguration(models.Model):
    Token = models.CharField(max_length=100,default="", blank=True)
    FirstName = models.CharField(max_length=100,default="", blank=True)
    LastName = models.CharField(max_length=100,default="", blank=True)
    ZipFilePassword = models.CharField(max_length=100,default="", blank=True)
    RequirePhoneNumber = models.BooleanField(default="", blank=True)
    RequireEmailAddress = models.BooleanField(default="", blank=True)
    ReservationApiVersion = models.CharField(max_length=100,default="", blank=True)
    ReservationUserCode = models.CharField(max_length=100,default="", blank=True)
    ReservationAgentCode = models.CharField(max_length=100,default="", blank=True)
    ReservationClientCode = models.CharField(max_length=100,default="", blank=True)
    ReservationVenderCode = models.CharField(max_length=100,default="", blank=True)
    ECommCaliforniaFlow = models.CharField(max_length=100,default="", blank=True)
    Status = models.CharField(max_length=100,default="", blank=True)
    #Message = models.CharField(max_length=100,default="", blank=True)
    
    def __str__(self):
        return str(self.FirstName)+"__"+str(self.LastName)
    
class StartOrder(models.Model):
    Token = models.CharField(max_length=100,default="", blank=True)
    SerialNumber = models.CharField(max_length=100,default="", blank = True)
    Platform = models.CharField(max_length=100,default="", blank=True)
    AppVersion = models.CharField(max_length=100,default="", blank=True)
    State = models.CharField(max_length=100,default="", blank=True)
    SaleTypeId = models.IntegerField(default=0,blank = True)
    Latitude = models.FloatField(default=0, blank=True)
    Longitude = models.FloatField(default=0, blank=True)   
    
    Result = models.BooleanField(default="", blank=True)
    OrderNumber = models.IntegerField(default=0, blank=True) 
    OrderDate = models.DateTimeField(default="", blank=True)
    PackageID = models.CharField(max_length=100, default="", blank=True)
    Status = models.CharField(max_length=100, default="", blank=True)
    Message = models.CharField(max_length=100, default="", blank=True)
    
    def __str__(self):
        return str(self.Message)