from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('habits/', include('habits.urls')),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('achievements/', include('achievements.urls')),
    path('about/', include('about.urls')),
    path('', include('main.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)