from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views


app_name = 'users'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('login/', views.CreateTokenJwtUserView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
