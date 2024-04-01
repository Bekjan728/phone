from rest_framework import serializers


from .models import (
    Brand,
    Phone,
    Model
    )
from apps.review.serializers import CommentSerializer

class BrandCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 1

    class Meta:
        model = Brand
        exclude = ('slug',)

    def validate(self, attrs):
        brand = attrs.get('title')
        if Brand.objects.filter(title=brand).exists():
            raise serializers.ValidationError(
                'This brand already exists'
            )
        user = self.context['request'].user                   # 1
        attrs['user'] = user
        return attrs
    

class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand 
        fields = ['title', 'slug', 'user']  # 2


class BrandRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 3

    class Meta:
        model = Brand
        fields = '__all__'

    def validate(self, attrs):                               
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class PhoneCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Phone
        exclude = ('slug',)

    def validate(self, attrs: dict):
        phone = attrs.get('title')
        if Phone.objects.filter(title=phone).exists():
            raise serializers.ValidationError(
                'This phone already exists'
            )
        user = self.context['request'].user                 
        attrs['user'] = user
        return attrs
    

class PhoneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone 
        fields = ['title', 'brand', 'slug', 'user']      


class PhoneUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Phone                                       
        fields = ['title', 'brand', 'desc', 'image', 'year_publ', 'slug', 'status',  'user']  # 'phone', 'model',
    
    def validate(self, attrs):                                 
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class PhoneRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   # 7

    class Meta:
        model = Phone
        fields = '__all__'

    def validate(self, attrs):                                 # 7
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['comments'] = CommentSerializer(
        instance.phones_comments.all(), many=True
        ).data

    #     rating = instance.books_ratings.aggregate(Avg('rating'))['rating__avg']   
    #     if rating:
    #         rep['rating'] = round(rating, 1) 
    #     else:
    #         rep['rating'] = 0.0
        
    #     rep['likes'] = instance.books_likes.all().count()
    #     rep['liked_by'] = LikeSerializer(
    #         instance.books_likes.all().only('user'), many=True).data 

        return rep


class ModelCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   # 8

    class Meta:
        model = Model
        fields = ['model', 'user']                             # 8

    def validate(self, attrs):
        model = attrs.get('model')
        if Model.objects.filter(model=model).exists():
            raise serializers.ValidationError(
                'Such model already exists'
            )
        user = self.context['request'].user                    # 8
        attrs['user'] = user
        return attrs


class ModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class ModelRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    # 9
    phones = PhoneListSerializer(read_only=True, many=True)

    class Meta: 
        model = Model 
        fields = ['user', 'model', 'phones']                     # 9

    def to_representation(self, instance: Model):
        phones = instance.phone_model.all()
        rep = super().to_representation(instance)
        rep['phone'] = PhoneListSerializer(
            instance=phones, many=True).data
        return rep
    
    def validate(self, attrs):                                   # 9
        user = self.context['request'].user
        attrs['user'] = user
        return attrs