from django.contrib import admin
from django.urls import path
from .views import *

app_name= 'core'

urlpatterns = [
    path('', HomeView , name = "home"),
    path('order_summary/', OrderSummaryView , name = "order_summary"),
    path('product/<int:id>/', ProductDetailView , name = "product"),
    path('checkout/', CheckoutView , name = "checkout"),

    path('update_data/', add_to_cart , name = "update_data"),
    path('add/<int:id>/', add , name = "add"),
    path('remove/<int:id>/', remove , name = "remove"),
    path('delete/<int:id>/', delete , name = "delete"),




]