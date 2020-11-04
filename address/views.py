from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Address
from .serializers import AddressSerializer


class AddressBaseView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressCreateListView(ListCreateAPIView, AddressBaseView):
    pass


class AddressRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView, AddressBaseView):
    pass
