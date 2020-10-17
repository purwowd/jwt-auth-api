from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views


app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/', views.CreateTokenJwtUserView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
