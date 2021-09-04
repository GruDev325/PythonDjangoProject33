from django.contrib.auth import get_user_model
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
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "user_role",
            "email",
            "password",
            "first_name",
            "last_name",
            "age",
            "phone_number",
        )
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "email": {
                "required": True,
                "allow_blank": False,
            },
            "user_role": {"required": True},
        }

    def _get_request(self):
        request = self.context.get("request")
        if (
            request
            and not isinstance(request, HttpRequest)
            and hasattr(request, "_request")
        ):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address.")
                )
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get("email"),
            name=validated_data.get("name"),
            username=generate_unique_username(
                [validated_data.get("name"), validated_data.get("email"), "user"]
            ),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            age=validated_data.get("age"),
            user_role=validated_data.get("user_role"),
            phone_number=validated_data.get("phone_number"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        if (user.user_role == 2):
            Restaurant.objects.create(location_id=None, name='', img_url='', user_id=user.id)
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "user_role",
            "email",
            "name",
            "first_name",
            "last_name",
            "age",
            "phone_number",
        ]


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""

    password_reset_form_class = ResetPasswordForm


class LocationSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = Location
        geo_field = "point"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('id', 'address', 'city', 'state')
class RestaurantSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False, read_only=False)
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "location",
            "name",
            "img_url"
        )

    def create(self, validated_data):
        location = validated_data.get("location")
        restaurant = Restaurant(
            location = Location.objects.create(address=location.get("address"), city=location.get("city"), state=location.get("state"), point=location.get("point")),
            name=validated_data.get("name"),
            img_url=validated_data.get("img_url"),
            user_id = self.context['request'].user.id,
        )
        restaurant.save()
        return restaurant

    def update(self, instance, validated_data):
        location = validated_data.get('location', instance.location)
        location = Location(address=location.get("address"), city=location.get("city"), state=location.get("state"), point=location.get("point"))
        location.save()
        instance.location = location
        instance.name = validated_data.get('name', instance.name)
        instance.img_url = validated_data.get('img_url', instance.img_url)
        instance.user_id = self.context['request'].user.id
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class DealSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Deal
        fields = (
            "category",
            "img_url",
            "name",
            "price",
            "reduced_price",
            "category",
            "special_offer",
        )

    def create(self, validated_data):
        deal = Deal(
            category_id=self.data['category'],
            name=validated_data.get("name"),
            price=validated_data.get("price"),
            reduced_price=validated_data.get("reduced_price"),
            category=validated_data.get("category"),
            special_offer=validated_data.get("special_offer"),
            img_url=validated_data.get("img_url"),
            user_id = self.context['request'].user.id,
            restaurant_id = Restaurant.objects.get(user_id=self.context['request'].user.id).id
        )
        deal.save()
        return deal

class DealGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    restaurant = RestaurantSerializer(many=False, read_only=True)
    class Meta:
        model = Deal
        fields = "__all__"


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = "__all__"


class User_BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Badge
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class BadgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badges
        fields = "__all__"


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = "__all__"


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = "__all__"
