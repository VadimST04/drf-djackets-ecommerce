from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, generics, status
from rest_framework.authentication import TokenAuthentication

from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer, CategorySelectSerializer, CreateProductSerializer


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response({'products': []})


class UserProducts(generics.ListAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        token = self.request.auth
        return Product.objects.filter(user=token.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class CategorySelect(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySelectSerializer


class CreateDestroyProduct(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        # Debugging info
        print(self.request.user)
        print(self.request.auth)
        if not self.request.user.is_authenticated:
            raise PermissionDenied('Authentication credentials were not provided.')

        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(id=self.kwargs["id"])
        return obj
