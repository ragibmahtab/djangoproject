from django.urls import path
from task.views_cbv import (
    HomeView, EventDashboardView, CreateEventView, UpdateEventView, 
    DeleteEventView, EventDetailView, EventSearchView, CreateCategoryView,
    UpdateCategoryView, AdminDashboardView, OrganizerDashboardView,
    ParticipantDashboardView, RSVPEventView, UserProfileView, EditProfileView,
    PasswordChangeViewCustom, PasswordChangeDoneView, PasswordResetViewCustom,
    PasswordResetDoneView, PasswordResetConfirmViewCustom, PasswordResetCompleteView
)

from .auth_views import signup_view, login_view, logout_view, activate_account
from . import auth_views


urlpatterns = [
    # ===== HOMEPAGE & EVENTS =====
    path('', HomeView.as_view(), name="homepage"),
    path('dashboard/', EventDashboardView.as_view(), name="Dashboard"),
    
    # ===== EVENT CRUD =====
    path('create_event/', CreateEventView.as_view(), name="create_event"),
    path('update_event/<int:id>/', UpdateEventView.as_view(), name="update_event"),
    path('delete_event/<int:id>/', DeleteEventView.as_view(), name="delete-event"),
    path('event_detail/<int:id>/', EventDetailView.as_view(), name="event_detail"),
    path('search/', EventSearchView.as_view(), name="search"),
    
    # ===== CATEGORY CRUD =====
    path('create_category/', CreateCategoryView.as_view(), name="create_catagory"),
    path('update_category/<int:id>/', UpdateCategoryView.as_view(), name="update_catagory"),
    
    # ===== AUTHENTICATION =====
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("activate/<uidb64>/<token>/", activate_account, name="activate"),
    
    # ===== PROFILE MANAGEMENT =====
    path('profile/', UserProfileView.as_view(), name="user_profile"),
    path('profile/edit/', EditProfileView.as_view(), name="edit_profile"),
    
    # ===== PASSWORD MANAGEMENT =====
    path('password-change/', PasswordChangeViewCustom.as_view(), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset/', PasswordResetViewCustom.as_view(), name="password_reset"),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmViewCustom.as_view(), name="password_reset_confirm"),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    # ===== DASHBOARDS =====
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("organizer-dashboard/", OrganizerDashboardView.as_view(), name="organizer_dashboard"),
    path("participant-dashboard/", ParticipantDashboardView.as_view(), name="participant_dashboard"),
    
    # ===== RSVP =====
    path("rsvp/<int:id>/", RSVPEventView.as_view(), name="rsvp_event"),
]

