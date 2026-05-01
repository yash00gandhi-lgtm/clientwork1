from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@csrf_exempt
def test_email(request):
    if request.method == "POST":
        try:
            send_mail(
                subject="Test Automation Email",
                message="🔥 Automation system working perfectly!",
                from_email="your_email@gmail.com",
                recipient_list=["yash00gandhi@gmail.com"],
                fail_silently=False,
            )
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})