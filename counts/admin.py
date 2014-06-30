from django.contrib import admin
from counts import models as count_models

# Register your models here.
admin.site.register(count_models.Messages)
