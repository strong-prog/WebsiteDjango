from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.items, name='index'),
    path('item/', views.items, name='items'),
    path('item/<item_id>', views.item, name='item'),
    path('order/', views.add_to_basket, name='add_to_basket'),
    path('buy/<item_id>', views.buy_one, name='buy'),
    path('buy/', views.buy_many, name='buy_many'),
    path('redirect-to-pay-form/', views.redirect_to_pay_form, name='redirect_to_pay_form')
]
