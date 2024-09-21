from django.shortcuts import render, redirect, get_object_or_404
from .models import YouTubePlaylist, YouTubeVideo, VideoFeedback, ProjectIdea
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotAllowed

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required
def dashboard(request):
    videos = YouTubeVideo.objects.select_related('playlist').all()

    processed_playlists = {}

    for video in videos[::-1]:
        playlist = video.playlist  
        
        if playlist.id not in processed_playlists:
            processed_playlists[playlist.id] = {
                'title': playlist.title,
                'next_video_to_watch': None
            }

        if not video.watched:
            if processed_playlists[playlist.id]['next_video_to_watch'] is None:
                processed_playlists[playlist.id]['next_video_to_watch'] = video

    processed_playlists_list = list(processed_playlists.values())

    context = {
        'playlists': processed_playlists_list
    }
    return render(request, 'dashboard.html', context)

@login_required
def mark_as_watched(request, video_id):
    # Ensure the request is a POST request
    if request.method == 'POST':
        # Fetch the video by ID and mark it as watched
        video = get_object_or_404(YouTubeVideo, id=video_id)
        video.watched = True
        video.save()  # Save the change to the database
        # Redirect back to the playlists view (or wherever appropriate)
        return redirect(reverse('playlists_view'))
    else:
        # If it's not a POST request, return a 405 Method Not Allowed response
        return HttpResponseNotAllowed(['POST'])

@login_required
def mark_unwatched(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(YouTubeVideo, id=video_id)
        video.watched = False
        video.save()
        return redirect('playlists_view')  # Redirect back to the playlists view

@login_required
def playlists_view(request):
    # Fetch all videos and related playlists in one query
    videos = YouTubeVideo.objects.select_related('playlist').all()

    # Debug: Print fetched videos
    # print("Fetched Videos:", videos)

    # Dictionary to hold playlist data
    processed_playlists = {}

    for video in videos:
        playlist = video.playlist  # Get the playlist of the current video
        
        # Initialize playlist data if it's not already in the processed_playlists dict
        if playlist.id not in processed_playlists:
            processed_playlists[playlist.id] = {
                'title': playlist.title,
                'watched_videos': [],
                'next_video_to_watch': None,
                'upcoming_videos': []
            }

        # Determine if the video has been watched and categorize accordingly
        if video.watched:
            processed_playlists[playlist.id]['watched_videos'].append(video)
        else:
            # If the next video to watch hasn't been set, set this video
            if processed_playlists[playlist.id]['next_video_to_watch'] is None:
                processed_playlists[playlist.id]['next_video_to_watch'] = video
            
            processed_playlists[playlist.id]['upcoming_videos'].append(video)

    # Convert processed_playlists dict to a list of playlist data for template rendering
    processed_playlists_list = list(processed_playlists.values())

    # Debug: Print the final processed playlists data
    # print("Processed Playlists Data:", processed_playlists_list)

    for playlist_data in processed_playlists.values():
        playlist_data['watched_videos'].reverse()
        playlist_data['upcoming_videos'].reverse()
        playlist_data['next_video_to_watch'] = playlist_data['upcoming_videos'][0] if playlist_data['upcoming_videos'] else None

    context = {
        'playlists': processed_playlists_list
    }

    # Debug: Print the final context being sent to the template
    # print("Final Context:", context)

    return render(request, 'playlist_list.html', context)

@login_required
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

