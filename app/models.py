from django.db import models

# Create your models here.

class Employee(models.Model):
    emp_id = models.IntegerField()
    first_name = models.CharField(max_length = 1000)
    last_name = models.CharField(max_length = 1000)
    age = models.IntegerField()
    sex = models.CharField(max_length = 100)
    department = models.CharField(max_length = 1000)
    designation = models.CharField(max_length = 1000)

    def __str__(self):
        return self.first_name

class Blog(models.Model):
    name = models.CharField(max_length = 1000)
    author = models.CharField(max_length = 1000)
    price = models.CharField(max_length = 1000)

    def __str__(self):
        return self.name
