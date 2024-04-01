from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import Brand


class BrandCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_brand(self):
        data = {
            'name': 'Apple',
            'about': 'A famous brand'
        }

        image_path = 'media/brand_images/3_XEQvXoj.jpeg'  # Update the path as needed
        image_file = SimpleUploadedFile("3_XEQvXoj.jpeg", open(image_path, 'rb').read(), content_type="image/jpeg")
        data['image'] = image_file

        response = self.client.post('/phones/brand/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Brand.objects.filter(name='Doe John').exists())

    def test_read_brand(self):
        brand = Brand.objects.create(
            name='Samsung',
            about='Another brand',
            image='media/brands/3.jpeg'
        )
        response = self.client.get(f'/phones/brand/{brand.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Apple')
        self.assertEqual(response.data['last_name'], 'Samsung')

    def test_update_brand(self):
        brand = Brand.objects.create(
            name='Lenovo',
            about='An old brand',
            image='media/brand_images/3.jpeg'
        )
        
        data = {
            'name': 'New',
            'about': 'An updated brand'
        }

        updated_image_path = 'media/brand_images/3_XEQvXoj.jpeg' 
        updated_image_file = SimpleUploadedFile("new_image.jpeg", open(updated_image_path, 'rb').read(), content_type="image/jpeg")
        data['image'] = updated_image_file

        response = self.client.put(f'/phones/brand/{brand.slug}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        brand.refresh_from_db()
        self.assertEqual(brand.name, 'New')
        self.assertEqual(brand.about, 'An updated brand')

    def test_delete_brand(self):
        brand = Brand.objects.create(
            name='To',
            about='An brand to be deleted',
            image='media/brands/3_XEQvXoj.jpeg'
        )
        response = self.client.delete(f'/phones/brand/{brand.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Brand.objects.filter(slug=brand.slug).exists())
