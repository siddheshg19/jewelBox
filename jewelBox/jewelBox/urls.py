from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontEnd.urls')),  # Frontend pages
   # path('jewelBoxDbServices/', include('jewelBoxDbServices.urls')),  # Backend services
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)