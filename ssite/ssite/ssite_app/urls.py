from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categories/<int:pk>/', views.category, name="categories"),
    path('favourites/', views.favourites, name="favourites"),
    path('profile/', views.profile, name="profile"),
    path('login/', views.user_login, name="login"),
    path('registration/', views.user_registration, name="registration"),
    path('logout/', views.user_logout, name="logout"),
    path('detail/<int:pk>/', views.detail, name="detail"),
    path('basket_add/<int:pk>', views.basket_add, name="basket_add"),
    path('basket_quantity_p/<int:pk>', views.basket_quantity_p, name="basket_quantity_plus"),
    path('basket_quantity_m/<int:pk>', views.basket_quantity_m, name="basket_quantity_minus"),
    path('basket_remove/<int:pk>', views.basket_remove, name="basket_remove"),
    path('Favorites_add/<int:pk>', views.Favorites_add, name="Favorites_add"),
    path('Favorites_remove/<int:pk>', views.Favorites_remove, name="Favorites_remove"),
    path('search/', views.search, name='search'),
]
