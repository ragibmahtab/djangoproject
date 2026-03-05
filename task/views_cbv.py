from django.views import View
from django.views.generic import TemplateView, UpdateView, FormView, DetailView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q, Count
from datetime import date
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from user.form import (
    UserProfileForm, 
    CustomPasswordChangeForm, 
    CustomPasswordResetForm, 
    CustomSetPasswordForm,
    customregistrationform
)
from task.models import event, catagory
from .decorators import role_required

User = get_user_model()


# ============= PROFILE VIEWS (NEW) =============

class UserProfileView(LoginRequiredMixin, DetailView):
    """Display user profile"""
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile_user'
    login_url = 'login'
    
    def get_object(self):
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Edit user profile"""
    model = User
    form_class = UserProfileForm
    template_name = 'edit_profile.html'
    login_url = 'login'
    success_url = reverse_lazy('user_profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully!")
        return response


class PasswordChangeViewCustom(LoginRequiredMixin, PasswordChangeView):
    """Change password"""
    form_class = CustomPasswordChangeForm
    template_name = 'change_password.html'
    login_url = 'login'
    success_url = reverse_lazy('password_change_done')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully!")
        return response


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """Password change success"""
    template_name = 'password_change_done.html'
    login_url = 'login'


class PasswordResetViewCustom(PasswordResetView):
    """Reset password via email"""
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, "Password reset link has been sent to your email!")
        return response


class PasswordResetDoneView(TemplateView):
    """Password reset email sent"""
    template_name = 'password_reset_done.html'


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    """Confirm password reset"""
    form_class = CustomSetPasswordForm
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(TemplateView):
    """Password reset complete"""
    template_name = 'password_reset_complete.html'


# ============= EVENT VIEWS (CBV CONVERSIONS) =============

class HomeView(ListView):
    """Homepage - List all events"""
    model = event
    template_name = 'homepage.html'
    context_object_name = 'events'
    paginate_by = 10
    
    def get_queryset(self):
        return event.objects.select_related("catagory").all()


class EventDashboardView(TemplateView):
    """Dashboard with event statistics"""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_filter = self.request.GET.get("type")
        
        events = event.objects.select_related("catagory").all()
        
        count_event = events.aggregate(
            total=Count('id'),
            upcoming=Count('id', filter=Q(date__gt=date.today())),
            past=Count('id', filter=Q(date__lt=date.today())),
            todays=Count('id', filter=Q(date=date.today())),
        )
        
        if type_filter == 'UPcoming Events':
            events = events.filter(date__gt=date.today())
        elif type_filter == 'Past Events':
            events = events.filter(date__lt=date.today())
        elif type_filter == 'Todays Events':
            events = events.filter(date=date.today())
        
        context['events'] = events
        context['counts'] = count_event
        return context


class CreateEventView(LoginRequiredMixin, CreateView):
    """Create new event - for Organizers"""
    model = event
    template_name = 'event_form.html'
    fields = ['name', 'description', 'date', 'time', 'location', 'catagory', 'image']
    login_url = 'login'
    success_url = reverse_lazy('homepage')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__iexact="Organizer").exists():
            messages.error(request, "Only organizers can create events")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Event created successfully!")
        return response


class UpdateEventView(LoginRequiredMixin, UpdateView):
    """Update event"""
    model = event
    template_name = 'event_form.html'
    fields = ['name', 'description', 'date', 'time', 'location', 'catagory', 'image']
    login_url = 'login'
    pk_url_kwarg = 'id'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__iexact="Organizer").exists():
            messages.error(request, "Only organizers can update events")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, "Event updated successfully!")
        return reverse_lazy('update_event', kwargs={'id': self.object.id})


class DeleteEventView(LoginRequiredMixin, DeleteView):
    """Delete event"""
    model = event
    template_name = 'event_confirm_delete.html'
    login_url = 'login'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('homepage')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__iexact="Organizer").exists():
            messages.error(request, "Only organizers can delete events")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event deleted successfully!")
        return super().delete(request, *args, **kwargs)


class EventDetailView(DetailView):
    """View event details"""
    model = event
    template_name = 'event_detail.html'
    context_object_name = 'event'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countt'] = self.object.rsvp_users.count()
        return context


class EventSearchView(ListView):
    """Search events"""
    model = event
    template_name = 'search.html'
    context_object_name = 'eventss'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return event.objects.filter(
                Q(name__icontains=query) | Q(location__icontains=query)
            )
        return event.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class CreateCategoryView(LoginRequiredMixin, CreateView):
    """Create category - for Organizers"""
    model = catagory
    template_name = 'category_form.html'
    fields = ['name', 'description']
    login_url = 'login'
    success_url = reverse_lazy('homepage')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__iexact="Organizer").exists():
            messages.error(request, "Only organizers can create categories")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category created successfully!")
        return response


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    """Update category"""
    model = catagory
    template_name = 'category_form.html'
    fields = ['name', 'description']
    login_url = 'login'
    pk_url_kwarg = 'id'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__iexact="Organizer").exists():
            messages.error(request, "Only organizers can update categories")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, "Category updated successfully!")
        return reverse_lazy('update_category', kwargs={'id': self.object.id})


# ============= DASHBOARD VIEWS (CBV) =============

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """Admin dashboard"""
    template_name = 'admin_dashboard.html'
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.groups.filter(name__iexact="Admin").exists()):
            messages.error(request, "Access denied")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = event.objects.all()
        context['users'] = User.objects.all()
        context['categories'] = catagory.objects.all()
        return context


class OrganizerDashboardView(LoginRequiredMixin, TemplateView):
    """Organizer dashboard"""
    template_name = 'organizer_dashboard.html'
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__iexact="Organizer").exists():
            messages.error(request, "Access denied")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = event.objects.all()
        context['categories'] = catagory.objects.all()
        return context


class ParticipantDashboardView(LoginRequiredMixin, TemplateView):
    """Participant dashboard"""
    template_name = 'participant_dashboard.html'
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__iexact="Participant").exists():
            messages.error(request, "Access denied")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = self.request.user.rsvp_events.all()
        return context


class RSVPEventView(LoginRequiredMixin, View):
    """RSVP for an event"""
    login_url = 'login'
    
    def post(self, request, id):
        event_obj = get_object_or_404(event, id=id)
        
        if request.user not in event_obj.rsvp_users.all():
            event_obj.rsvp_users.add(request.user)
            
            send_mail(
                "RSVP Confirmation",
                f"You successfully RSVP'd for {event_obj.name}",
                "admin@example.com",
                [request.user.email],
            )
            messages.success(request, "You've successfully RSVP'd for this event!")
        else:
            messages.warning(request, "You've already RSVP'd for this event")
        
        return redirect("participant_dashboard")
    
    def get(self, request, id):
        return self.post(request, id)
