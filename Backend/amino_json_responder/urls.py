from django.urls import path
from amino_json_responder import views

urlpatterns = [
    path("getNutrientsList/", views.get_nutrients_list, name="get_nutrients_list"),
    path("getContainingFoods/<searched_food>", views.get_containing_foods, name="get_containing_foods"),
    path("getNutrientsInfo/<exact_food_key_string>", views.get_nutrients_info, name="get_nutrients_info"),
    path("getRecommendedFoods/<url_param>", views.get_recommended_foods, name="get_recommended_foods"),
]