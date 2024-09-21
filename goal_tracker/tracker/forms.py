from django import forms
from .models import YouTubePlaylist, YouTubeVideo

from django import forms

class YouTubePlaylistForm(forms.Form):
    playlist_url = forms.URLField(label='YouTube Playlist URL')



class YouTubeVideoForm(forms.ModelForm):
    class Meta:
        model = YouTubeVideo
        fields = ['title', 'url', 'watched', 'thumbnail_url']  # Make sure these fields exist in the model

