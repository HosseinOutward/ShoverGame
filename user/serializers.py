from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, ScoreBoardEntry


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
            'password2': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'image_profile', 'highscore_profile', 'email', 'first_name', 'last_name']
        related_fields=['userprofile']
        extra_kwargs = {
            'pk': {'read_only': True},
        }
    image_profile = serializers.ImageField(source='userprofile.image_profile')
    highscore_profile = serializers.IntegerField(source='userprofile.highscore_profile')

    def update(self, instance, validated_data):
        # Handle related objects
        for related_obj_name in self.Meta.related_fields:
            try:
                # Validated data will show the nested structure
                data = validated_data.pop(related_obj_name)
                related_instance = getattr(instance, related_obj_name)

                # Same as default update implementation
                for attr_name, value in data.items():
                    setattr(related_instance, attr_name, value)
                related_instance.save()
            except KeyError: pass

        return super(ProfileSerializer,self).update(instance, validated_data)


class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password', 'password2']
        extra_kwargs = {
            'password': {'required': True},
            'password2': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return attrs


class ScoreBoardSerializer(serializers.ModelSerializer):
    highScore = serializers.IntegerField(source="highScore_score")
    highFortune = serializers.IntegerField(source="highFortune_score")
    time_played = serializers.FloatField(source="time_played_score")
    # start_time = serializers.DateTimeField(source="start_time_score")

    class Meta:
        model = ScoreBoardEntry
        fields = ['highScore', 'highFortune', 'time_played', 'user_score']
        read_only_fields = ('user_score',)

    def create(self, validated_data):
        validated_data['user_score'] = self.context['request'].user
        return super().create(validated_data)
