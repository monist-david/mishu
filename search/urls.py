from django.urls import path
from .views import HomeView

app_name = 'search'
urlpatterns = [
    path('', HomeView.as_view(), name='search'),
]