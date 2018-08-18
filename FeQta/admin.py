from django.contrib import admin
from . import models

admin.site.register(models.Topic)
admin.site.register(models.Question)
admin.site.register(models.Answer)
# Register your models here.
