from django.db import models
import datetime

from django.utils import timezone
# Create your models here.

class Question(models.Model):
    question_text =models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published')

    def __str__(self):
        return self.question_text

    #自定义一个模型方法，用于判断问卷是否近期发布过
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    #使用ForeignKey 定义外健关系  外键写在多的一方
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return  self.choice_text