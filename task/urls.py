from django.urls import path
from task.views import Homepage,Dashboard,create_event,create_participant,create_catagory,detail_View,update_event,delete_event,update_catagory,search


urlpatterns = [
    path('',Homepage,name="homepage"),
    path('Dashboard/',Dashboard,name="Dashboard"),
    path('create_event/',create_event,name="create_event"),
    path('update_event/<int:id>/',update_event,name="update_event"),
    path('delete_event/<int:id>/',delete_event,name="delete-event"),

    path('create_participant/',create_participant,name="create-participant"),
    

    path('create_catagory/',create_catagory,name="create_catagory"),
    path('update_catagory/<int:id>/',update_catagory,name="update_catagory"),

    path('detail_View/<int:id>/',detail_View,name="detail_View"),
    path('search/',search,name="search")
]

