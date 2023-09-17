from django.urls import path, include

from product.views import LatestProductsList, ProductDetail, CategoryDetail, UserProducts, search, CategorySelect, CreateDestroyProduct

urlpatterns = [
    path('latest-products/', LatestProductsList.as_view()),
    path('categories-all/', CategorySelect.as_view()),
    path('products/search/', search),
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetail.as_view()),
    path('products/<slug:category_slug>/', CategoryDetail.as_view()),
    path('user-products/', UserProducts.as_view()),
    path('product/create/', CreateDestroyProduct.as_view()),
    path('product/destroy/<int:id>/', CreateDestroyProduct.as_view()),
]
