from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


class Brand(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(max_length=50)
    about = models.TextField()
    image = models.ImageField(upload_to='brand_images')
    slug = models.SlugField(primary_key=True, blank=True, max_length=120)        


    def save(self, *args, **kwargs):
 
        if not self.slug:
            self.slug = slugify(self.title)  # slugify(self.name) + '_' + slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title  # f'{self.name} {self.name}' 
    
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Phone(models.Model):
    STATUS_CHOICES = (             
        ('archive', 'Archived'),
        ('avail', 'Available')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(max_length=70)
    brand = models.ForeignKey(
        to=Brand,
        related_name='phone_brands',
        on_delete=models.CASCADE
    )
    desc = models.CharField(max_length=200)
    image = models.ImageField(upload_to='phone_images')
    year_publ = models.CharField(max_length=4)
    slug = models.SlugField(primary_key=True, blank=True, max_length=80)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9)       
    # phone = models.FileField(upload_to='phone_files')    
    # model = models.ManyToManyField(
    #     to='Model',
    #     related_name='phone_model'
    # )                   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)   
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'


class Model(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    model = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=25)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.model)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.model
    
    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"