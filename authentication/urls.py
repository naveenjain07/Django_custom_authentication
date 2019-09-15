from django.contrib import admin
from django.urls import path, include
from authentication import views as authViews

urlpatterns = [
    path('', authViews.signup),
    path('<int:userId>/', authViews.updateUserDetails),
    path('login', authViews.login),
    path('confirm-user', authViews.confirmUser),
    path('generate-link', authViews.generateLink),
    path('reset-password', authViews.resetPassword),
]
