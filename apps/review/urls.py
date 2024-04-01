from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SavedPhoneViewSet,
    PhoneCommentView,
    RatingView,
    LikeView,
)


router = DefaultRouter()


router.register('saved-phone', SavedPhoneViewSet, 'saved phone')
router.register('phone-comment', PhoneCommentView, 'comment')
router.register('phone-rating', RatingView, 'rating')
router.register('phone-like', LikeView, 'like')


urlpatterns = [

]
urlpatterns += router.urls