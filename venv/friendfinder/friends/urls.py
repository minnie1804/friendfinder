from django.contrib import admin
from django.urls import path
from . import views

app_name = "friendfinder"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home")
]
