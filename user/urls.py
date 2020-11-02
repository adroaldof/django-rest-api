from django.urls import path

from .views import CreateUserView, LoginView, ManageUserView

app_name = "user"  # pylint: disable=C0103

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="me"),
]
