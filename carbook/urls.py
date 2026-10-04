from django.urls import path
from . import views

app_name = 'carbook'

urlpatterns = [
    path('', views.x2, name='index'),
    path('free-inspection/', views.free_inspection, name='free_inspection'),  # <-- இந்த வரியைப் புதிதாகச் சேர்க்கவும்
    path('image-convert/', views.image_convert, name='image_convert'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('pricing/', views.pricing, name='pricing'),
    path('car/', views.car, name='car'),
    path('contact/', views.contact, name='contact'),
    path('car-single/', views.car_single, name='car-single'),
    path('blog-single/', views.blog_single, name='blog-single'),
    path('pricing-connected/', views.pricing_connected, name='pricing-connected'),
    path('car-connected/', views.car_connected, name='car-connected'),
]