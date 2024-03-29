from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404

import thrall.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('thrall.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('bag/', include('bag.urls')),
    path('contact/', include('contact.urls')),
    path('blog/', include('blog.urls')),
    path('products/', include('products.urls')),
    path('profile/', include('profiles.urls')),
    path('checkout/', include('checkout.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'django_thrall.views.handler404'
