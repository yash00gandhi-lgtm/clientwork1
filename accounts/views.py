from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def auth_page(request):
    if request.method == "POST":
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "message": "Login successful",
                "user_id": user.id
            })
        else:
            return JsonResponse({
                "error": "Invalid credentials"
            }, status=401)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

def login_page(request):
    return render(request, 'login.html')