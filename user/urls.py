from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import *


rout=DefaultRouter()
rout.register('user', UserAPIView, basename='user')

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('registration/', registration, name='User-create'),

    path('', home, name='base-home'),
    path('contact/', contact, name='base-contact'),
    path('about_us/', about_us, name='base-about_us'),
    path('explanation/', explanation, name='base-expl'),
    path('lobby/', mylobby, name='mylobby'),
    path('createGame/', createGame, name='createGame'),

    path('game/', game, name='game'),
    path('coop/', coop, name='coop'),

    path('_api/', include(rout.urls)),
    path('_api/HighScore/', get_highscore),
    path('_api/ScoreBoard/', ScoreBoardAPIView.as_view()),

    path('_api/profileUpdate/', ProfileUpdateAPIView.as_view(), name='Profile-Update'),
    path('_api/PassUpdate/', PasswordChangeAPIView.as_view(), name='Pass-Update'),
]
