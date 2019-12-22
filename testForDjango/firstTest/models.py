from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class reporter(models.Model):
    c = (
        ("writer","writer"),
        ("author","author")
    )
    reporterKind = models.CharField("reporter kind",max_length=10,choices=c,default="select kind")
    reporterName = models.CharField("first name", max_length=60)
    reporterLast = models.CharField("last name", max_length=60)
    reporterEmail = models.CharField("email", max_length=60)
    
    def __str__(self):
        return self.reporterName+" "+self.reporterLast


class article(models.Model):
    articleMain = models.CharField("article body", max_length=3000)
    articleContent = models.CharField("article header", max_length=100)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    likerUsers = models.ManyToManyField(User, related_name="likerUsers")
    likes = models.IntegerField(default=0)


    def __str__(self):
        return self.articleContent

    def getLikes(self):
        return len(self.likerUsers.all())


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=300, default="hey i am using this site!")
    location = models.CharField(max_length=300,blank=True)
    phonenumber = models.CharField(max_length=300,blank=True)
    image = models.ImageField(upload_to='firstTest/static/firstTest/img/profiles/',blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
