from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    PhoneComment,
    PhoneRating,
    PhoneLike,
    SavedPhone,
)


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = PhoneComment
        exclude = ['id']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = PhoneLike
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        phone = self.context.get('phone')
        like = PhoneLike.objects.filter(user=user, phone=phone).first()
        if like:
            raise serializers.ValidationError('already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        phone = self.context.get('phone')
        like = PhoneLike.objects.filter(user=user, phone=phone).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('not liked yet')


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PhoneRating
        fields = ('rating', 'user', 'phone')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating') 
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError('Incorrect value. The rating should be between 1 and 5.')
        # if rating:
        #     raise serializers.ValidationError('already exists')
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class SavedPhoneSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SavedPhone
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        phone = request.get('phone')
        favorite = SavedPhone.objects.filter(user=user, phone=phone).first()
        if not favorite:
            return super().create(validated_data)
        raise serializers.ValidationError('This phone has been saved')

    def del_favorite(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        phone = request.get('phone').slug
        favorite = SavedPhone.objects.filter(user=user, phone=phone).first()
        if favorite:
            favorite.delete()
        else:
            raise serializers.ValidationError('This phone has not been saved')