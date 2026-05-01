from django.core.mail import send_mail
from django.conf import settings


# 🔥 LEAD AUTOMATION
def send_lead_notification(lead):
    try:
        # ========================
        # 📩 ADMIN NOTIFICATION
        # ========================
        admin_message = (
            f"New Lead Alert 🚀\n\n"
            f"Name: {getattr(lead, 'name', 'N/A')}\n"
            f"Phone: {getattr(lead, 'phone', 'N/A')}\n"
            f"Email: {getattr(lead, 'email', 'N/A') or 'N/A'}\n"
            f"Program: {getattr(lead, 'program', 'N/A') or 'N/A'}\n\n"
            f"⚡ Action Required: Contact this lead ASAP!"
        )

        send_mail(
            subject="🔥 New Gym Lead Received",
            message=admin_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # ========================
        # 💪 USER WELCOME MAIL
        # ========================
        if getattr(lead, 'email', None):
            user_message = (
                f"Hey {getattr(lead, 'name', 'there')},\n\n"
                f"Thanks for showing interest in our gym! 🔥\n\n"
                f"Our team will contact you shortly.\n\n"
                f"🏋️ Visit us anytime or reply to this email.\n\n"
                f"⚡ Limited Offer:\n"
                f"Join within 24 hours & get exclusive benefits.\n\n"
                f"Stay strong 💪\n"
                f"Fitness Place Team"
            )

            send_mail(
                subject="Welcome to Fitness Place 💪",
                message=user_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[lead.email],
                fail_silently=True,
            )

    except Exception as e:
        print("❌ LEAD AUTOMATION ERROR:", str(e))


# 🔥 BOOKING AUTOMATION
def send_booking_confirmation(booking):
    try:
        if getattr(booking, 'email', None):
            booking_message = (
                f"Hey {getattr(booking, 'name', 'there')},\n\n"
                f"Your booking is successfully confirmed 🎯\n\n"
                f"📅 Date: {getattr(booking, 'date', 'N/A')}\n"
                f"⏰ Time: {getattr(booking, 'time', 'N/A')}\n"
                f"🏋️ Program: {getattr(booking, 'program', 'N/A')}\n\n"
                f"👉 Please arrive 10 minutes early.\n\n"
                f"Let’s get you in shape 💪\n"
                f"Fitness Place Team"
            )

            send_mail(
                subject="✅ Your Gym Booking is Confirmed",
                message=booking_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[booking.email],
                fail_silently=True,
            )

    except Exception as e:
        print("❌ BOOKING AUTOMATION ERROR:", str(e))