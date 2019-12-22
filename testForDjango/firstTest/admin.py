from django.contrib import admin
from .models import reporter, article, profile
# Register your models here.
admin.site.register(reporter)
admin.site.register(article)
admin.site.register(profile)