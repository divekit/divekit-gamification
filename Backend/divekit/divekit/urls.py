from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include



admin.site.site_header = 'DivekitBadge'
admin.site.index_title = 'Divekit Admin'
# admin.site.site_title = 'HTML title from adminsitration' 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/', include('badges.urls')),
    path('api/v1/', include('authentication.urls')),
    path("api/v1/",include("bot.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


