from django.urls import path

from . import views

app_name = "enquiries"

urlpatterns = [
    path("request-quote/", views.request_quote, name="request-quote"),
    path("contact/", views.contact, name="contact"),
]
