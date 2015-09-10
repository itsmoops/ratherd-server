from django.contrib import admin
from .models import Rather

# Register your models here.

class RatherAdmin(admin.ModelAdmin):
	list_display = ('id', 'rather_text', 'wins', 'losses', 'ratio', 'date_submitted', 'date_updated')
	search_fields = ['id', 'rather_text']
	list_filter = ['is_pair', 'date_submitted']

admin.site.register(Rather, RatherAdmin)