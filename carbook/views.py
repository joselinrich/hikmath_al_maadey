import logging
import io
from PIL import Image

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import ContactMessage
from .forms import ContactForm

logger = logging.getLogger(__name__)


def home_view(request):
    return HttpResponse("<h1>Welcome to the Homepage</h1>")


def x2(request):
    return render(request, 'index.html')


def image_convert(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        output_format = request.POST.get('format', 'JPEG').upper()
        valid_formats = ['JPEG', 'PNG', 'BMP']
        if output_format not in valid_formats:
            return JsonResponse({'error': 'Invalid format selected.'}, status=400)
        try:
            img = Image.open(uploaded_image)
            converted_image_io = io.BytesIO()
            img.convert('RGB').save(converted_image_io, format=output_format)
            converted_image_io.seek(0)
            response = HttpResponse(converted_image_io, content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename="converted.{output_format.lower()}"'
            return response
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return JsonResponse({'error': f'Error processing image: {e}'}, status=400)
    return render(request, 'image_convert.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def blog(request):
    return render(request, 'blog.html')


def pricing(request):
    return render(request, 'pricing.html')


def car(request):
    return render(request, 'car.html')


# --- CONTACT PAGE VIEW ---
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            full_email_message = f"""
New Inquiry Received from Contact Page:

Name: {name}
Email: {email}
Subject: {subject}

Message / Details:
{message}
            """

            try:
                send_mail(
                    subject=f"Website Inquiry: {subject}",
                    message=full_email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['joselinrichs@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                logger.error(f"Email sending failed: {e}")
                messages.error(request, f'Email sending failed. Error: {e}')

            return redirect('carbook:contact')
        else:
            messages.error(request, 'Please correct the errors in the form below.')
            return render(request, 'contact.html', {'form': form})
    
    return render(request, 'contact.html', {'form': ContactForm()})


# --- HOMEPAGE FREE INSPECTION FORM VIEW (NEWLY ADDED) ---
def free_inspection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        location = request.POST.get('location')

        # Database-இல் சேமிக்க
        ContactMessage.objects.create(
            name=name,
            email="Not Provided (Inspection Form)",
            subject=f"Inspection Request: {service}",
            message=f"Phone/WhatsApp: {phone}\nService Required: {service}\nBuilding Location: {location}"
        )

        # Email மெசேஜ் தயாரித்தல்
        full_email_message = f"""
New Free Inspection Request Received:

Name: {name}
Phone/WhatsApp: {phone}
Service Required: {service}
Building Location: {location}
        """

        try:
            send_mail(
                subject=f"Free Inspection Request - {name}",
                message=full_email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['joselinrichs@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your inspection request has been submitted successfully!')
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            messages.error(request, f'Failed to send request: {e}')

        # ஃபார்ம் சப்மிட் ஆனதும் அதே Homepage-லேயே நிற்கவைக்கும்
        return redirect(request.META.get('HTTP_REFERER', 'carbook:index'))
    
    return redirect('carbook:index')


def car_single(request):
    return render(request, 'car-single.html')


def blog_single(request):
    return render(request, 'blog-single.html')


def pricing_connected(request):
    return render(request, 'pricing_connected.html')


def car_connected(request):
    return render(request, 'car_connected.html')