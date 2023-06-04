from django.urls import path
from .views import LeftSwipeViewSet, RightSwipeViewSet, TagViewSet
from .recomender import RecommendProfiles


urlpatterns = [

    path("swipe/left/", LeftSwipeViewSet.as_view({
        "get" : "swipe_details",
        "post" : "perform_create",
        "put" : "update",
        "delete" : "destroy",
    }), name="left_swipe_view_set"),

    path("swipe/right/", RightSwipeViewSet.as_view({
        "get" : "swipe_details",
        "post" : "perform_create",
        "put" : "update",
        "delete" : "destroy",
    }), name="right_swipe_view_set"),

    path("recommend/", RecommendProfiles.as_view({
        "get" : "get_recommendations",
        "post" : "get_recommendations",
    }), name="recommend_profiles"),

    path("tags/", TagViewSet.as_view({
        'get' : 'get_tags'
    }), name="tags_view_set"),
]