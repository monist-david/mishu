from django.urls import path
from .views import HomeView

app_name = 'personality'
urlpatterns = [
    path('', HomeView.as_view(), name='personality'),
]