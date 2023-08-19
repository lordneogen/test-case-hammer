from . import views_cbf , views_dbf
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

# from .views_cbf import RegisterView

urlpatterns = [
    path('', views_cbf.R_Users.as_view(), name='main'),

    # Просмотр, обновление и удаление пользователя по указанному id
    path('<int:id>/', views_cbf.RUD_Users.as_view(), name='get id'),

    # Создание нового пользователя - первая часть процесса
    path('create/', views_cbf.C_1_Users.as_view(), name='create user pr1'),

    # Создание нового пользователя - вторая часть процесса с указанием доступа
    path('create/access/<int:id>', views_cbf.C_2_Users.as_view(), name='create user pr2'),

    # Аутентификация пользователя (вход)
    path('login/', views_cbf.Auth.as_view(), name='login'),

    # Обновление токена аутентификации (обновление срока действия)
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='login_refresh'),
]
