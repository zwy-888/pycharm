from django.db import models

# Create your models here.


class Article(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    cate = models.ForeignKey('Course', models.DO_NOTHING, blank=True, null=True)
    issue_time = models.DateField(blank=True, null=True)
    reading = models.IntegerField(blank=True, null=True)
    one_course = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    two_course = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article'


class Course(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'



