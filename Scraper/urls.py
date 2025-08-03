from django.urls import path
from .views import FacebookPostScraperView
urlpatterns = [
    path('',FacebookPostScraperView.as_view(), name='fb_scraper'),
]