from django.contrib import admin
from .models import Rather
from django.contrib.auth.models import User

# Register your models here.

class RatherAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'rather_text', 'wins', 'losses', 'ratio', 'this_sucks', 'date_submitted', 'date_updated')
	search_fields = ['id', 'rather_text']
	list_filter = ['this_sucks', 'date_submitted']

admin.site.register(Rather, RatherAdmin)
