from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import views, profile_images
from .views import ProfileViewSet
from .preferences import PreferenceViewSet
from .questions import QuestionViewSet
from .locations import LocationViewSet
from .tags import TagManageViewSet


urlpatterns = [
    path("user/login/", ObtainAuthToken.as_view(), name='api_token_auth'),
    path("user/auth/google/", views.google_login_and_signup, name='google_login_and_signup'),
    path("user/signup/", views.sign_up, name='sign_up'),
    path("user/verify/", views.otp_verification, name='otp_verification'),
    path("cookie/csrf/", views.set_csrf_token, name="set_csrf_token"),
    path("user/profile/", ProfileViewSet.as_view({
        "get" : "profile_details",
        "post" : "update",
        "put" : "update",
        "delete" : "destroy",
    }), name="profile_view_set"),

    path("user/preference/", PreferenceViewSet.as_view({
        "get" : "preference_details",
        "post" : "update",
        "put" : "update",
        "delete" : "destroy",
    }), name="preference_view_set"),

    path("user/question/", QuestionViewSet.as_view({
        "get" : "question_details",
        "post" : "update",
        "put" : "update",
        "delete" : "destroy",
    }), name="question_view_set"),

    path("user/location/", LocationViewSet.as_view({
        "get" : "location_details",
        "post" : "update",
        "put" : "update",
        "delete" : "destroy",
    }), name="location_view_set"),

    path('user/image/dp/', profile_images.profile_pic_upload, name="profile_pic_upload"),
    path('user/image/pic/', profile_images.profile_image_upload, name="profile_image_upload"),
    path('user/image/<str:id>/delete/', profile_images.profile_image_delete, name="profile_image_delete"),    

    path('user/profile/tags/', TagManageViewSet.as_view({
        "post" : "create",
        "delete" : "destroy"
    }),name="tags_update_view_set")
] 

