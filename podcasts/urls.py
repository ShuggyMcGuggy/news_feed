from django.urls import path

from .views import HomePageView, NewsView

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path('news/', NewsView.as_view(), name='news'),
]