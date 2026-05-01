from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json


@csrf_exempt
def auth_page(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        # ✅ SAFE JSON PARSE
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        email = data.get("email")
        password = data.get("password")

        # ✅ VALIDATION
        if not email or not password:
            return JsonResponse({
                "error": "Email and password required"
            }, status=400)

        # ✅ AUTHENTICATION
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "message": "Login successful",
                "user_id": user.id
            })

        return JsonResponse({
            "error": "Invalid credentials"
        }, status=401)

    except Exception as e:
        print("LOGIN ERROR:", str(e))  # 🔥 logs me dikhega
        return JsonResponse({
            "error": "Server error"
        }, status=500)


def login_page(request):
    return render(request, 'login.html')