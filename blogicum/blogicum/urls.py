from django.conf import settings
from django.contrib import admin
from django.urls import path, include


handler404 = 'pages.views.page_not_found_view'
handler500 = 'pages.views.server_error_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
