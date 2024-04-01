from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import(
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework import mixins

from apps.phone.permissions import IsOwner
from apps.phone.models import Phone

from .serializers import (
    RatingSerializer,
    CommentSerializer,
    LikeSerializer,
    SavedPhoneSerializer
)
from .models import (
    PhoneComment, 
    PhoneLike,
    PhoneRating,
    SavedPhone
)


class SavedPhoneViewSet(mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = SavedPhone.objects.all()
    serializer_class = SavedPhoneSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'save' and self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'save' and self.request.method =='DELETE':
            self.permission_classes = [IsOwner]
        # if self.action == 'list':
        #     self.permission_classes = [IsOwner]
        return super().get_permissions()

    def save(self, request, pk=None):
        phone = self.get_object().get('slug')
        serializer = SavedPhoneSerializer(
            data=request.data, 
            context={
                'request':request,
                'phone':phone
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('This phone has been saved')
            if request.method == 'DELETE':
                        serializer.del_favorite()
                        return Response('This phone has been removed from savings')


class PhoneCommentView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = PhoneComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RatingView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = PhoneRating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LikeView(mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    serializer_class = LikeSerializer
    queryset = PhoneLike.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'like' and self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'like' and self.request.method =='DELETE':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def like(self, request, pk=None):
        phone = self.get_object()
        serializer = LikeSerializer(
            data=request.data, 
            context={
                'request':request,
                'phone':phone
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('unliked!')