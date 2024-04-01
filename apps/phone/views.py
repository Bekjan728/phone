from rest_framework.viewsets import ModelViewSet, GenericViewSet   
from rest_framework.permissions import AllowAny
from rest_framework import mixins   

from .models import (
    Brand,
    Phone,
    Model     
)

from .serializers import (
    BrandCreateSerializer, 
    BrandListSerializer, 
    BrandRetrieveSerializer,
    
    PhoneCreateSerializer, 
    PhoneListSerializer, 
    PhoneUpdateSerializer,
    PhoneRetrieveSerializer,

    ModelCreateSerializer,   
    ModelListSerializer,     
    ModelRetrieveSerializer  
)

class BrandViewSet(ModelViewSet):      
    queryset = Brand.objects.all()
    serializer_class = BrandCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return BrandCreateSerializer
        elif self.action == 'list':
            return BrandListSerializer
        elif self.action == 'retrieve':
            return BrandRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    

class PhoneViewSet(ModelViewSet):      # CRUD - Create, Retrieve, Update, Delete, List 
    queryset = Phone.objects.all()
    serializer_class = PhoneCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return PhoneCreateSerializer
        elif self.action == 'list':
            return PhoneListSerializer
        elif self.action == 'retrieve':
            return PhoneRetrieveSerializer
        elif self.action in ['update', 'partial_update']:
            return PhoneUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ModelViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ModelCreateSerializer
        elif self.action == 'list':
            return ModelListSerializer
        elif self.action == 'retrieve':
            return ModelRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()