from rest_framework import serializers
from .models import CustomUser, Report
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['user_type'] = user.user_type
        return token

#user  
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    phone_number = serializers.CharField(max_length=17, required=True)
    sex = serializers.ChoiceField(choices=CustomUser.SEX_CHOICES, required=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, default='STANDARD_USER')
    first_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'phone_number', 'sex', 'user_type','first_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number'),
            sex=validated_data.get('sex'),
            user_type=validated_data.get('user_type')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

    #end user



class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'











class ProfileSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name' ,'email', 'phone_number', 'sex', 'user_type','reports')