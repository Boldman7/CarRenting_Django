from django.db import models

# Create your models here.
import datetime
from django.utils import timezone

class Question(models.Model):
   question_text = models.CharField(max_length=200)
   pub_date = models.DateTimeField('date published')

   def __str__(self):
       return self.question_text

   def was_published_recently(self):
       now = timezone.now()
       return now - datetime.timedelta(days=1) <= self.pub_date <= now

   was_published_recently.admin_order_field = 'pub_date'
   was_published_recently.boolean = True
   was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING,)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Tech(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=200)

class User(models.Model):
    user_id = models.CharField(max_length=200)
    mobile = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    namespace = models.CharField(max_length=200)
    confirmation_hash = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    href = models.CharField(max_length=200)
    target_id = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    updated_at = models.DateTimeField()

    access_token = models.CharField(max_length=200)
    client_id = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    endpoints_http = models.CharField(max_length=200)
    endpoints_mqtt = models.CharField(max_length=200)
    endpoints_uploader = models.CharField(max_length=200)
    expires = models.CharField(max_length=200)
    grant_type = models.CharField(max_length=200)
    owner_id = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    scope_1 = models.CharField(max_length=200)
    scope_2 = models.CharField(max_length=200)

class ParseUser(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    mobile = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    namespace = models.CharField(max_length=200)
    confirmation_hash = models.CharField(max_length=200)
    created = models.DateTimeField()
    href = models.CharField(max_length=200)
    target_id = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    updated = models.DateTimeField()