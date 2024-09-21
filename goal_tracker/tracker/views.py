from django.shortcuts import render, redirect, get_object_or_404
from .models import YouTubePlaylist, YouTubeVideo, VideoFeedback, ProjectIdea
from .forms import YouTubePlaylistForm, YouTubeVideoForm
import requests
from django.conf import settings
from django.contrib import messages

def dashboard(request):
    return render(request, 'dashboard.html')

import requests
from django.shortcuts import render

# Replace with your YouTube playlist ID
playlist_id = "PLwgFb6VsUj_l3XGLgZTf5lXq9rPAQ9COu"

import requests
from django.shortcuts import render
from decouple import config

def display_youtube_playlist_data(request):
    playlists = YouTubePlaylist.objects.all()
    # Get all playlist_ids
    playlist_ids = YouTubePlaylist.objects.values_list('playlist_id', flat=True)

# Convert the queryset to a list if needed
    playlist_ids_list = list(playlist_ids)

# Now you can print or use the list of IDs
    print(playlist_ids_list)


    print(playlists)
    api_key = config('YOUTUBE_API_KEY')
    api_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=PLwgFb6VsUj_l3XGLgZTf5lXq9rPAQ9COu&key={api_key}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get('items', []):
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
                'video_url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
            }
            videos.append(video_data)

        context = {
            'videos': videos,
        }
        return render(request, 'youtube_playlist.html', context)

    except requests.exceptions.RequestException as e:
        print("Error fetching data from YouTube API:", e)
        return render(request, 'youtube_playlist.html', {'error': 'Failed to fetch data from the YouTube API'})



def fetch_youtube_playlist_videos(playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={settings.YOUTUBE_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for non-200 codes
        data = response.json()
        videos = []
        for item in data.get('items', []):
            video_data = item['snippet']
            videos.append({
                'title': video_data.get('title'),
                'url': f"https://www.youtube.com/watch?v={video_data['resourceId']['videoId']}",
                'thumbnail_url': video_data['thumbnails']['default']['url'],  # Thumbnail URL
                'watched': False,  # Set based on your logic
            })
        return videos
    except requests.RequestException as e:
        # Log the error and handle gracefully
        print(f"Error fetching YouTube playlist videos: {e}")
        return []


def extract_video_id(video_url):
    import re
    match = re.search(r'(v=|youtu.be/)([a-zA-Z0-9_-]+)', video_url)
    return match.group(2) if match else None


def playlists_view(request):
    playlists = YouTubePlaylist.objects.prefetch_related('videos').all()
    
    # Debug: Print playlists
    print("Fetched Playlists:", playlists)

    processed_playlists = []

    for playlist in playlists:
        # Debug: Print each playlist's videos
        print(f"Processing Playlist: {playlist.title}")
        print(f"Videos in playlist: {playlist.videos.all()}")

        watched_videos = []
        upcoming_videos = []
        next_video_to_watch = None

        for video in playlist.videos.all():
            print(f"Video: {video.title} - Watched: {video.watched}")
            if video.watched:
                watched_videos.append(video)
            else:
                if next_video_to_watch is None:
                    next_video_to_watch = video
                upcoming_videos.append(video)

        playlist_data = {
            'title': playlist.title,
            'watched_videos': watched_videos,
            'next_video_to_watch': next_video_to_watch,
            'upcoming_videos': upcoming_videos
        }

        # Debug: Print the processed playlist data
        print("Processed Playlist Data:", playlist_data)

        processed_playlists.append(playlist_data)

    context = {
        'playlists': processed_playlists
    }

    # Debug: Print the final context being sent to the template
    print("Final Context:", context)

    return render(request, 'playlist_list.html', context)


def add_videos_to_playlist(videos, playlist):
    for video in videos:
        if not YouTubeVideo.objects.filter(url=video['url']).exists():
            YouTubeVideo.objects.create(
                title=video['title'],
                url=video['url'],
                thumbnail_url=video['thumbnail_url'],
                watched=video['watched'],
                playlist=playlist
            )


import re
from django.shortcuts import render, redirect
from .models import YouTubePlaylist
from .forms import YouTubePlaylistForm

def add_playlist(request):
    if request.method == 'POST':
        playlist_url = request.POST.get('playlist_url')  # Get the URL from form
        title = request.POST.get('title')  # Get the optional title from form
        playlist = YouTubePlaylist.create_playlist(playlist_url, title=title)  # Pass title to the method

        if playlist:
            return redirect('playlists_view')  # Redirect to the list of playlists
        else:
            error_message = "Invalid playlist URL. Please try again."
            return render(request, 'add_playlist.html', {'error': error_message})

    return render(request, 'add_playlist.html')




def extract_playlist_id(url):
    match = re.search(r'list=([^&]+)', url)
    return match.group(1) if match else None



def mark_video_watched(request, video_id):
    video = get_object_or_404(YouTubeVideo, id=video_id)
    video.watched = True
    video.save()
    messages.success(request, f'Video "{video.title}" marked as watched.')
    return redirect('playlists_view')


def video_detail(request, video_id):
    video = get_object_or_404(YouTubeVideo, id=video_id)
    return render(request, 'video_detail.html', {'video': video})


def submit_feedback(request, video_id):
    video = get_object_or_404(YouTubeVideo, id=video_id)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating'))
        except ValueError:
            messages.error(request, 'Invalid rating provided.')
            return redirect('video_detail', video_id=video_id)

        comments = request.POST.get('comments')
        if 1 <= rating <= 5:
            VideoFeedback.objects.create(video=video, rating=rating, comments=comments)
            messages.success(request, 'Feedback submitted successfully.')
        else:
            messages.error(request, 'Rating must be between 1 and 5.')
        return redirect('video_detail', video_id=video_id)
    return render(request, 'submit_feedback.html', {'video': video})


def project_idea_list(request):
    projects = ProjectIdea.objects.all()
    return render(request, 'project_idea_list.html', {'projects': projects})


def add_project_idea(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        progress = request.POST.get('progress')

        if title and description and progress:
            ProjectIdea.objects.create(title=title, description=description, progress=progress)
            messages.success(request, 'Project idea added successfully.')
        else:
            messages.error(request, 'All fields are required.')
        return redirect('project_idea_list')
    return render(request, 'add_project_idea.html')


def update_project_idea(request, project_id):
    project = get_object_or_404(ProjectIdea, id=project_id)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.progress = request.POST.get('progress')
        project.save()
        messages.success(request, 'Project idea updated successfully.')
        return redirect('project_idea_list')
    return render(request, 'update_project_idea.html', {'project': project})


def project_detail(request, project_id):
    project = get_object_or_404(ProjectIdea, id=project_id)
    return render(request, 'project_detail.html', {'project': project})
