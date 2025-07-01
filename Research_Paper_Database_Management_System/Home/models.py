from django.db import models

# Create your models here.

class users_Model(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    role_here = models.CharField(max_length=100)

    class Meta:
        db_table="users"
        

class research_Model(models.Model):
    research_id = models.IntegerField(primary_key=True)
    publisher_id = models.IntegerField()
    institute_id = models.IntegerField()
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    views = models.IntegerField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    publish_date = models.DateField()

    class Meta:
        db_table="research"
