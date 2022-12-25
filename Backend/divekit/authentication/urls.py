from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import ObtainTokenPairView, UserDetailView,UserCreate,UserListView,UserListViewMinified,UserBadgeListView,UserActivationView,CustomTokenRefreshView

urlpatterns = [
    path('token/obtain/', ObtainTokenPairView.as_view(),
         name='token_create'),  # override sjwt stock token
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/create/', UserCreate.as_view(), name="create_user"),
    path('users/<int:user_id>/', UserDetailView.as_view(), name="user"),
    path("users/",UserListView.as_view(), name="users"),
    path("users/minified/",UserListViewMinified.as_view(),name="users_minified"),
    path("users/confirmation/",UserActivationView.as_view(),name="confirmation")
]
