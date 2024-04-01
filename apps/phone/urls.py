from rest_framework.routers import DefaultRouter

from .views import (
    BrandViewSet, 
    PhoneViewSet,
    ModelViewSet  
    )

router = DefaultRouter()
router.register('brand', BrandViewSet)
router.register('phone', PhoneViewSet)
router.register('model', ModelViewSet) 

urlpatterns = [

]

urlpatterns += router.urls

