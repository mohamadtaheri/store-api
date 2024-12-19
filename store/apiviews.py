from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from .serializers import ProductSerializer
from .models import Product

class ProductPagination(LimitOffsetPagination):
    max_limit = 100
    default_limit = 2
    
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,)
    filterset_fields = ('id',)
    search_fields = ('name', 'description',)
    pagination_class = ProductPagination
    
    def get_queryset(self):
        
        params_dict = self.request.query_params.dict()
       
        if 'onsale' in params_dict.keys():
            onsale = params_dict['onsale']
            queryset = Product.objects.all()
            from django.utils import timezone
            now = timezone.now()
            if onsale.lower() == 'true':
                return queryset.filter(
                    sale_start__lte = now,
                    sale_end__gte = now
                )
            else:
                from django.db.models import Q
                return queryset.filter(
                    Q(sale_end__lte=now) | Q(sale_end__isnull=True)
                )
        
            
        return super().get_queryset()
        