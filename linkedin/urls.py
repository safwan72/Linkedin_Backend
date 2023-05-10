from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("auth_api.urls")),
    path("api/profile/", include("Profile.urls")),
    path("api/connection/", include("network.urls")),
    # path("api/notification/", include("notification.urls")),
    path("api/post/", include("post.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/organizations/", include("Job.urls")),
    re_path(r"^auth/", include("drf_social_oauth2.urls", namespace="drf")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
