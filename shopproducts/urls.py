from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products'),
    path('productdetail/<pk>', views.productdetail, name='productdetail'),
    path('search/', views.SearchProductView.as_view(), name='search'),
    path('category/<str:pk>', views.ProductListCategory.as_view(), name='category'),
    path('categories_component/', views.categories_component, name='categories_component')
]