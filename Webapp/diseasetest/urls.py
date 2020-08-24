from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('heart', views.heart, name="heart"),
    path('diabetes', views.diabetes, name="diabetes"),
    path('breast', views.breast, name="breast"),
    path('home', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('', views.login, name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)