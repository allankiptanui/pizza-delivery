from . import views
from django.urls import path



urlpatterns =[
    path('', views.OrderCreateListView.as_view(),name='orders'),
    path('<int:order_id>/', views.OrderDetailView.as_view(),name='order_detail'),
    path('update-status/<int:order_id>/', views.UpdateOrderStatusView.as_view(),name='order_status_update'),
    path('user/<int:user_id>/orders', views.UserOrdersView.as_view(),name='users_orders'),
    path('user/<int:user_id>/order/<int:order_id>/', views.UserOrderDetailView.as_view(),name='users_specific_detail'),

    
]
