from rest_framework import viewsets
from home.models import (
    Badges,
    Category,
    CheckIn,
    Deal,
    Description,
    Location,
    Notification,
    Restaurant,
    Timeline,
    User_Badge,
)
from .serializers import (
    BadgesSerializer,
    CategorySerializer,
    CheckInSerializer,
    DealGetSerializer,
    DealSerializer,
    DescriptionSerializer,
    LocationSerializer,
    NotificationSerializer,
    RestaurantSerializer,
    TimelineSerializer,
    User_BadgeSerializer,
)
from rest_framework import authentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import json

class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        restaurant = Restaurant.objects.filter(user=user)
        if (restaurant):
            restaurant_serializer = RestaurantSerializer(restaurant, many=True)
            return Response({"token": token.key, "user": user_serializer.data, "restaurant": restaurant_serializer.data})
        else:
            return Response({"token": token.key, "user": user_serializer.data})


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['address']

class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Restaurant.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['name']


    def create(self, request, *args, **kwargs):
        restaurant=None
        user_id=request.user.id
        if user_id:
            restaurant=Restaurant.objects.get(user_id=user_id)

        if restaurant:
            kwarg_field: str = self.lookup_url_kwarg or self.lookup_field
            self.kwargs[kwarg_field] = restaurant.id
            return self.update(request, *args, **kwargs)
        else:
            return self.create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        img_url = Restaurant.objects.create(image=file)
        return Response(json.dumps({'message': "Uploaded"}), status=200)

class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Deal.objects.all()

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        img_url = Restaurant.objects.create(image=file)



class DealSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('name_only'):
            return ['name']
        return super(DealSearchFilter, self).get_search_fields(view, request)

class DealGetViewSet(viewsets.ModelViewSet):
    serializer_class = DealGetSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Deal.objects.all()
    filter_backends = [DealSearchFilter, filters.OrderingFilter]
    # filter_fields = ('name', 'category')
    search_fields = ['name', 'restaurant__location__address', 'restaurant__location__state', 'restaurant__location__city', 'restaurant__location__point', 'category__name']
    ordering_fields = ['name']
    ordering = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()


class TimelineViewSet(viewsets.ModelViewSet):
    serializer_class = TimelineSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Timeline.objects.all()


class User_BadgeViewSet(viewsets.ModelViewSet):
    serializer_class = User_BadgeSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = User_Badge.objects.all()



class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()


class BadgesViewSet(viewsets.ModelViewSet):
    serializer_class = BadgesSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Badges.objects.all()

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        img_url = Restaurant.objects.create(image=file)


class CheckInViewSet(viewsets.ModelViewSet):
    serializer_class = CheckInSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = CheckIn.objects.all()


class GetCheckInByCurrentCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CheckInSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return CheckIn.objects.filter(user=user)

class DescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = DescriptionSerializer
    authentication_classes = (
        # authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    queryset = Description.objects.all()
