from django.db import models

from django.db import models
import re

import requests
from django.conf import settings

class YouTubePlaylist(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    playlist_id = models.CharField(max_length=100, unique=True)
    playlist_url = models.URLField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title or self.playlist_url

    @classmethod
    def create_playlist(cls, playlist_url, title=None):
        playlist_id = cls.extract_playlist_id(playlist_url)
        if playlist_id:
            # Create a playlist object
            playlist = cls.objects.create(playlist_id=playlist_id, playlist_url=playlist_url, title=title)
            # Fetch and store videos for this playlist
            playlist.fetch_and_store_videos()
            return playlist
        return None

    @staticmethod
    def extract_playlist_id(url):
        match = re.search(r'list=([^&]+)', url)
        return match.group(1) if match else None

    def fetch_and_store_videos(self):
        api_key = settings.YOUTUBE_API_KEY  # YouTube API key should be stored in Django settings
        base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
        params = {
            'part': 'snippet',
            'playlistId': self.playlist_id,
            'maxResults': 200,  # Fetch up to 50 videos at a time
            'key': api_key
        }

        # Make the request to YouTube API to fetch videos in this playlist
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            videos_data = response.json().get('items', [])
            for video_data in videos_data:
                self.store_video(video_data['snippet'])

    def store_video(self, snippet):
        """Store a video in the YouTubeVideo model."""
        video_title = snippet.get('title')
        video_url = f"https://www.youtube.com/watch?v={snippet['resourceId']['videoId']}"
        thumbnail_url = snippet['thumbnails']['high']['url']

        # Create a new YouTubeVideo entry linked to this playlist
        YouTubeVideo.objects.create(
            title=video_title,
            url=video_url,
            thumbnail_url=thumbnail_url,
            playlist=self
        )




class YouTubeVideo(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    thumbnail_url = models.URLField()
    watched = models.BooleanField(default=False)
    playlist = models.ForeignKey(YouTubePlaylist, related_name='videos', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']  # Order videos by most recently added

    def __str__(self):
        return self.title


class VideoFeedback(models.Model):
    video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField()  # Assume rating is out of 5
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Feedback for {self.video.title} - Rating: {self.rating}'


class ProjectIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    progress = models.CharField(max_length=100)  # e.g., "In Progress", "Completed"
    messages = models.TextField(blank=True, null=True)  # Optional messages

    def __str__(self):
        return self.title
