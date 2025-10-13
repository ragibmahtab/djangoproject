from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.generic import RedirectView

urlpatterns = [
    path('task', RedirectView.as_view(url='/task/')),
    path('admin/', admin.site.urls),
    path('',include('task.urls'))

] + debug_toolbar_urls()
