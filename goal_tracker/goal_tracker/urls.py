from django.contrib import admin
from django.urls import path
from tracker.views import (
    playlists_view, 
    add_playlist, 
    mark_as_watched,mark_unwatched, dashboard,
    signup_view, login_view, logout_view
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('my-playlists/', playlists_view, name='playlists_view'),
    path('mark-watched/<int:video_id>/', mark_as_watched, name='mark_watched'),
    path('mark_unwatched/<int:video_id>/', mark_unwatched, name='mark_unwatched'),
    path('add_playlist/', add_playlist, name='add_playlist'),

    path('dashboard/', dashboard, name='dashboard'),
]
