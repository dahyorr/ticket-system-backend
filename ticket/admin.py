from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Ticket)
admin.site.register(models.Queue)
admin.site.register(models.Reply)
