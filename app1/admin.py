from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Socity)
admin.site.register(models.Post)
admin.site.register(models.Socity_officer)
admin.site.register(models.branch_officer)