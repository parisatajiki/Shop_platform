from django.urls import path
from .views import HomeView


app_name = 'home_app'
urlpatterns = [
    path('',HomeView.as_view(),name='home' ),
]