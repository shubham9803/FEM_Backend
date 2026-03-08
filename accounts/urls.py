from django.urls import path
from .views import RegisterView,LogoutView,me
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CreateFamilyView,
    JoinFamilyView,
    MyFamilyView,
    FamilyMembersView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/me/', me),
    path('family/create/', CreateFamilyView.as_view()),
    path('family/join/', JoinFamilyView.as_view()),
    path('family/me/', MyFamilyView.as_view()),
    path('family/members/', FamilyMembersView.as_view()),
]