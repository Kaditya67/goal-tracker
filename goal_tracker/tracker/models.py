from django.db import models

from django.db import models
import re

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
            return cls.objects.create(playlist_id=playlist_id, playlist_url=playlist_url, title=title)
        return None

    @staticmethod
    def extract_playlist_id(url):
        match = re.search(r'list=([^&]+)', url)
        return match.group(1) if match else None




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
