"""TestCarRenting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url

import CarRentals.views as car_rentals

urlpatterns = [
    url(r'^car-rentals/', include('CarRentals.urls')),
    path('admin/', admin.site.urls),
    path('api/', car_rentals.AllTech.as_view()),
    re_path(r'^api/(?P<pk>\d+)', car_rentals.TechView.as_view()),

    # Sign Up, Sign Verify
    path('api/sign-up', car_rentals.SignUpView.as_view()),
    path('api/sign-verify', car_rentals.SignVerifyView.as_view()),
]
