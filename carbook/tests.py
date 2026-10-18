from django.test import TestCase, Client
from django.urls import reverse
from io import BytesIO
from PIL import Image

class ImageConvertViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('image_convert')

    def create_test_image(self):
        img = Image.new('RGB', (100, 100), color = 'red')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io

    def test_get_image_convert(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image_convert.html')

    def test_post_valid_image_and_format(self):
        img_io = self.create_test_image()
        response = self.client.post(self.url, {'format': 'PNG'}, 
                                    format='multipart', 
                                    data={'image': img_io})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertIn('attachment; filename="converted.png"', response['Content-Disposition'])

    def test_post_invalid_format(self):
        img_io = self.create_test_image()
        response = self.client.post(self.url, {'format': 'INVALID'}, 
                                    format='multipart', 
                                    data={'image': img_io})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid format selected.'})

    def test_post_invalid_image(self):
        invalid_file = BytesIO(b'notanimage')
        invalid_file.name = 'test.txt'
        response = self.client.post(self.url, {'format': 'JPEG'}, 
                                    format='multipart', 
                                    data={'image': invalid_file})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

class OtherViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('carbook:index'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('carbook:about'))
        self.assertEqual(response.status_code, 200)

    def test_services_view(self):
        response = self.client.get(reverse('carbook:services'))
        self.assertEqual(response.status_code, 200)

    def test_blog_view(self):
        response = self.client.get(reverse('carbook:blog'))
        self.assertEqual(response.status_code, 200)
