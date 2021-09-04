from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    BadgesViewSet,
    CategoryViewSet,
    CheckInViewSet,
    DealGetViewSet,
    DealViewSet,
    DescriptionViewSet,
    GetCheckInByCurrentCustomerViewSet,
    LocationViewSet,
    NotificationViewSet,
    RestaurantViewSet,
    TimelineViewSet,
    User_BadgeViewSet,
)

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("restaurant", RestaurantViewSet)
router.register("location", LocationViewSet)
router.register("deal", DealViewSet)
router.register("deal-get", DealGetViewSet)
router.register("category", CategoryViewSet)
router.register("timeline", TimelineViewSet)
router.register("user_badge", User_BadgeViewSet)
router.register("notification", NotificationViewSet)
router.register("badges", BadgesViewSet)
router.register("checkin", CheckInViewSet)
router.register("my-checkin", GetCheckInByCurrentCustomerViewSet, basename="myCheckin")
router.register("description", DescriptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
