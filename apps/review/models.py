from django.db import models
from django.contrib.auth import get_user_model
# from django.urls import reverse


from apps.phone.models import Phone


User = get_user_model ()


class PhoneComment (models.Model):
    user = models. ForeignKey (
        to=User,
        on_delete=models. CASCADE,
        related_name='comments'
    )
    phone = models. ForeignKey(
        to=Phone,
        on_delete=models.CASCADE,
        related_name= 'phones_comments'
    )
    comment_text = models. TextField ()
    created_at = models. DateTimeField (auto_now_add=True)
    
    def str(self) :
        return f'Comment from {self.user.username} to {self.phone.title}'
    

class PhoneRating (models.Model) :
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE =5
    RATING_CHOICES = (
        (ONE,'1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR,'4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    phone = models. ForeignKey (
        to=Phone, 
        on_delete=models.CASCADE, 
        related_name= 'phones_ratings'
    )

    def _str_ (self) -> str:
        return f'{self.rating} points to {self.phone.title}'
    
    class Meta:
        unique_together = ['user', 'phone', 'rating']

    
class PhoneLike(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name= 'likes'
    )
    phone = models.ForeignKey(
    to=Phone, 
    on_delete=models.CASCADE, 
    related_name= 'phone_likes'
    )

    def _str__(self) :
        return f'Liked by {self.user. username}'
    

class SavedPhone(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
    )
    phone = models. ForeignKey (
    to=Phone, 
    on_delete=models. CASCADE,
    )