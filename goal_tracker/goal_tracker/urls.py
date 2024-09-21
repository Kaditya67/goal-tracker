from django.urls import path
from tracker.views import (
    playlists_view, 
    add_playlist, 
    video_detail, 
    mark_video_watched, 
    submit_feedback,
    project_idea_list,
    add_project_idea,
    update_project_idea,
    project_detail
)
from django.contrib import admin
from tracker.views import display_youtube_playlist_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playlists/', playlists_view, name='playlists_view'),
    path('add_playlist/', add_playlist, name='add_playlist'),
    path('youtube-playlist/', display_youtube_playlist_data, name='youtube_playlist'),
    # path('videos/<int:video_id>/mark_watched/', mark_video_watched, name='mark_video_watched'),
    # path('videos/<int:video_id>/', video_detail, name='video_detail'),
    # path('videos/<int:video_id>/submit_feedback/', submit_feedback, name='submit_feedback'),
    # path('projects/', project_idea_list, name='project_idea_list'),
    # path('projects/add/', add_project_idea, name='add_project_idea'),
    # path('projects/<int:project_id>/edit/', update_project_idea, name='update_project_idea'),
    # path('projects/<int:project_id>/', project_detail, name='project_detail'),
]
