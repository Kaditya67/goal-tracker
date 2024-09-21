from django.contrib import admin

# Register your models here.
from .models import YouTubePlaylist,YouTubeVideo

admin.site.register(YouTubePlaylist)
admin.site.register(YouTubeVideo)

