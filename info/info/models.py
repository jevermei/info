from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    admin = models.BooleanField(default= False)
    
    def __str__(self):
        return self.firstname + ' ' + self.lastname

class Stop(models.Model):
    stopname = models.CharField(max_length = 30)
    order = models.IntegerField(null=True)
    stop_line = models.ForeignKey('line',on_delete=models.CASCADE)

    def __str__(self):
        return self.stopname

class Line(models.Model):
    line_number = models.CharField(max_length = 30 , default="")

    def __str__(self):
        return "Line number :" + self.line_number

class Report(models.Model):
    user = models.ForeignKey('user', on_delete=models.CASCADE)
    reportstop = models.ForeignKey('stop', on_delete=models.CASCADE) 
    reportline = models.ForeignKey('line', on_delete=models.CASCADE)

    def __str__(self):
        return  self.reportstop.stopname + " " + self.reportline.line_number
