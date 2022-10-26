from django.urls import path
from amino_json_responder import views

urlpatterns = [
    path("get_nutrients_list/", views.get_nutrients_list, name="get_nutrients_list"),
    path("get_containing_foods/<searched_food>", views.get_containing_foods, name="get_containing_foods"),
    path("get_nutrients_info/<exact_food_key_string>", views.get_nutrients_info, name="get_nutrients_info"),
    path("get_recommended_foods/<url_param>", views.get_recommended_foods, name="get_recommended_foods"),
]