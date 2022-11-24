from django.urls import include, path
from amino_json_responder import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'get_via_serializer', views.ContainingFoodsViewSet)
router.register(r'optimize_mixing_ratio', views.GetOptimizedMixingRatioViewSet, basename='Dummy')

urlpatterns = [
    path("", include(router.urls)),
    path("get_nutrients_list/", views.get_nutrients_list, name="get_nutrients_list"),
    path("get_foods/<restriction>", views.get_foods, name="get_foods"),
    path("get_containing_foods/<searched_food>", views.get_containing_foods, name="get_containing_foods"),
    path("get_nutrients_info/<exact_food_key_string>", views.get_nutrients_info, name="get_nutrients_info"),
    path("get_recommended_foods/", views.get_recommended_foods, name="get_recommended_foods"),
    #path("GetOptimizedMixingRatio/", views.GetOptimizedMixingRatioAPIView.as_view(), name="test_name"),
]