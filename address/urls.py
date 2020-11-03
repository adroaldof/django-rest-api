from django.urls import path

from .views import AddressCreateListView, AddressRetrieveUpdateDestroyView

app_name = "address"  # pylint: disable=C0103

urlpatterns = [
    path("", AddressCreateListView.as_view(), name="list_create"),
    path(
        "<int:pk>/",
        AddressRetrieveUpdateDestroyView.as_view(),
        name="retrieve_update_destroy",
    ),
]
