from django.urls import include, path
from amino_json_responder import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'get_via_serializer', views.ContainingFoodsViewSet)
router.register(r'get_optimized_mixing_ratio', views.GetOptimizedMixingRatioViewSet, basename='Dummy1')
router.register(r'get_recommendations', views.GetRecommendationsViewSet, basename='Dummy2')
router.register(r'get_high_scores', views.GetHighScoresViewSet, basename='Dummy3')
router.register(r'get_who_requirements', views.GetWhoRequirementsViewSet, basename='Dummy4')
router.register(r'get_who_100_g_coverage', views.GetWho100gCoverageViewSet, basename='Dummy5')
router.register(r'get_foods', views.GetFoodsViewSet, basename='Dummy6')

urlpatterns = [
    path("", include(router.urls)),
    path("get_nutrients_list/", views.get_nutrients_list, name="get_nutrients_list"),
    path("get_containing_foods/<searched_food>", views.get_containing_foods, name="get_containing_foods"),
    path("get_nutrients_info/<exact_food_key_string>", views.get_nutrients_info, name="get_nutrients_info"),
    path("get_recommended_foods/", views.get_recommended_foods, name="get_recommended_foods"),
    #path("GetOptimizedMixingRatio/", views.GetOptimizedMixingRatioAPIView.as_view(), name="test_name"),
]