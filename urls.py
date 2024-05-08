from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("Upload.html", views.Upload, name="Upload"),
	       path("SongPlay", views.SongPlay, name="SongPlay"),
	       path("basic.html", views.basic, name="basic"),
	       path("WebCam", views.WebCam, name="WebCam"),
	       path("DetectEmotion", views.DetectEmotion, name="DetectEmotion"),
]