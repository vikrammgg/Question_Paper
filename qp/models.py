from django.db import models

# Create your models here.
class Question(models.Model):
    
    id = models.AutoField(primary_key=True)
    Level = models.CharField(max_length=50)
    Topic = models.CharField(max_length=100)
    Sub_Topic = models.CharField(max_length=100)
    Question = models.TextField()
    Options = models.TextField(max_length=255)
    OptionA = models.CharField(max_length=255)
    OptionB = models.CharField(max_length=255)
    OptionC = models.CharField(max_length=255)
    OptionD = models.CharField(max_length=255)
    Answer_Option = models.CharField(max_length=255)
    Answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
