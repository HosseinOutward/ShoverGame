from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import render
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .models import ScoreBoardEntry
from lobby.models import MapLayout, Lobby


def home(request):
    return render(request, r"base_site/Home.html", context={"user": request.user})
def about_us(request):
    return render(request, r"base_site/about-us.html", context={"user": request.user})
def contact(request):
    return render(request, r"base_site/contact.html", context={"user": request.user})
def explanation(request):
    return render(request, r"base_site/explanation.html", context={"user": request.user})

@login_required
def mylobby(request):
    return render(request, r"base_site/mylobby.html", context={"user": request.user})
@login_required
def createGame(request):
    return render(request, r"base_site/choose map.html", context={"maps": MapLayout.objects.all()})


def registration(request):
    if request.user.is_anonymous:
        return render(request, 'register.html')
    else: return home(request)


@login_required
def game(request): return render(request, r"game.html")
@login_required
def coop(request): return render(request, r"coop.html")


class UserAPIView(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    queryset=User.objects.all()

    def get_serializer_class(self):
        serializer_class = CreateUserSerializer
        if self.request.method != 'POST':
            serializer_class = ProfileSerializer
            self.permission_classes = [IsAuthenticated]
        return serializer_class

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'POST':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return super(UserAPIView, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)


class PasswordChangeAPIView(generics.UpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PasswordSerializer

    def get_object(self):
        return self.request.user


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class ScoreBoardAPIView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ScoreBoardSerializer

    def get_queryset(self):
        return ScoreBoardEntry.objects.filter(user_score=self.request.user)

    def create(self, request, *args, **kwargs):
        time_played = float(request.POST["time_played"])*10/6
        return super(ScoreBoardAPIView, self).create(request, *args, **kwargs)


@login_required
@api_view(['GET'])
def get_highscore(request):
    from django.db.models import Max
    queryset = ScoreBoardEntry.objects.filter(user_score=request.user)
    boxout = queryset.aggregate(Max('highScore_score'))['highScore_score__max']
    fortune = queryset.aggregate(Max('highFortune_score'))['highFortune_score__max']
    return Response({"highScore": boxout, "highFortune": fortune}, status=status.HTTP_200_OK)


