from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# Ensure 'community_updates' is imported here!
from core.views import home, dashboard, admin_dashboard, community_updates,common_gallery 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dept-admin/', admin_dashboard, name='admin_dashboard'),
    
    # ADD THIS MISSING LINE:
    path('community/', community_updates, name='community'), 
    
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('gallery/', common_gallery, name='common_gallery'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)