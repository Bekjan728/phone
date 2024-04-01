from django.contrib import admin
from.models import (
    PhoneComment,
    PhoneRating,
    PhoneLike
)


admin.site.register([PhoneComment, PhoneRating, PhoneLike])