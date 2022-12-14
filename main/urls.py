from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('binance_get_price.urls')),
    path('', include('site_helper.urls')),
]
