# test_email.py
from django.core.mail import send_mail

send_mail(
    subject="Test Email",
    message="Testing Gmail SMTP",
    from_email="RzorCut App <rzor_cut@gmail.com>",
    recipient_list=["ashraf.shiksha001@gmail.com"],
    fail_silently=False,
)
