from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    
    #Authentication
path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
path('register/', RegisterView.as_view(), name='auth_register'),
path('logout/', LogoutView.as_view(), name='logout'),

#Profile
path('profile/', getProfile, name='profile'),
path('profile/update/', updateProfile, name='update-profile'),
    

    path('super-resolution/', SuperResolutionAPI, name='Super Resolution Api'),
    path('detect-fractures/', FractureDetectionAPI, name='Detect Fracture Api')
]