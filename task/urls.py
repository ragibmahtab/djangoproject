from django.urls import path
from task.views import Homepage,Dashboard,create_event,create_catagory,detail_View,update_event,delete_event,update_catagory,search,admin_dashboard,organizer_dashboard,participant_dashboard,rsvp_event,event_detail
from .auth_views import signup_view,login_view,logout_view,activate_account
from . import auth_views


urlpatterns = [
    path('',Homepage,name="homepage"),
    path('Dashboard/',Dashboard,name="Dashboard"),
    path('create_event/',create_event,name="create_event"),
    path('update_event/<int:id>/',update_event,name="update_event"),
    path('delete_event/<int:id>/',delete_event,name="delete-event"),

    # path('create_participant/',create_participant,name="create-participant"),
    

    path('create_catagory/',create_catagory,name="create_catagory"),
    path('update_catagory/<int:id>/',update_catagory,name="update_catagory"),

    # path('detail_View/<int:id>/',detail_View,name="detail_View"),
    path('search/',search,name="search"),
    path('event_detail/<int:id>/',event_detail,name="event_detail"),

    path("signup/",signup_view,name="signup"),
    path("login/",login_view,name="login"),
    path("logout/",logout_view,name="logout"),
    path("activate/<uidb64>/<token>/",activate_account,name="activate"),

    path("admin-dashboard/",admin_dashboard,name="admin_dashboard"),
    path("organizer-dashboard/",organizer_dashboard,name="organizer_dashboard"),
    path("participant-dashboard/",participant_dashboard,name="participant_dashboard"),

    path("rsvp/<int:id>/",rsvp_event,name="rsvp_event"),
    path("activate/<uidb64>/<token>/", auth_views.activate_account, name="activate"),

]

