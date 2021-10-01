from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    image_profile = models.ImageField(default=r'profile_pic/default.jpg', upload_to='profile_pic')
    color_profile = models.CharField(max_length=7, default=r'#FFFFFF')
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        from PIL.Image import open as open_image
        if self.image_profile.name!=r'profile_pic/default.jpg':
            img = open_image(self.image_profile.file)
            img.thumbnail((256, 256))
            img.save(self.image_profile.path)


class ScoreBoardEntry(models.Model):
    highScore_score = models.IntegerField(default=-1)
    highFortune_score = models.IntegerField(default=-1)
    time_played_score = models.FloatField(default=-1)
    start_time_score = models.DateTimeField(default=None, blank=True, null=True)
    end_time_score = models.DateTimeField(default=timezone.now)

    user_score = models.OneToOneField(User, on_delete=models.CASCADE)
