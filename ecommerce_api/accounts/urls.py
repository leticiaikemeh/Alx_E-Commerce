
from django.urls import path
from .views import RegisterView, MeView, UserAdminListCreate, UserAdminDetail

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("users/", UserAdminListCreate.as_view(), name="users"),
    path("users/<int:pk>/", UserAdminDetail.as_view(), name="user-detail"),
]
