import json

import google.generativeai as generativeai
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import AppUserForm, UserForm
from .models import AppUser, PromptModel
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#4 Business logic (handling requests and responses)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_form = UserForm(data)
            if user_form.is_valid():
                user = user_form.save(commit=False)  # Save user without committing to the DB yet
                user.set_password(user_form.cleaned_data['password'])  # Set the password properly
                user.save()  # Save user instance
                
                # Now create AppUser instance
                app_user_form = AppUserForm(data)
                if app_user_form.is_valid():
                    app_user = app_user_form.save(commit=False)
                    app_user.user = user  # Link AppUser to User
                    app_user.save()  # Save AppUser instance
                    return JsonResponse({'message': 'Sign up successful!'}, status=201)
                else:
                    return JsonResponse({'errors': app_user_form.errors}, status=400)
            else:
                return JsonResponse({'errors': user_form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'message': 'This endpoint only accepts POST requests.'}, status=405)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=200)
            return JsonResponse({'error': 'Invalid email or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'message': 'This endpoint only accepts POST requests.'}, status=405)


# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             email = data.get('email')
#             password = data.get('password')
#             biometric = data.get('biometric')  # Assume biometric authentication data is sent here
#             authenticator_code = data.get('authenticator_code')  # Authenticator code
#             # First, try to authenticate using password
#             if password:
#                 user = authenticate(request, username=email, password=password)
#                 if user is not None:
#                     return JsonResponse({'message': 'Login successful'}, status=200)
#                 return JsonResponse({'error': 'Invalid email or password'}, status=400)
#             # Now, check for biometric data (add your biometric verification logic)
#             if biometric:
#                 # This is placeholder logic for verifying biometric data
#                 # You'll need to integrate with a biometric provider here.
#                 if verify_biometric(biometric):
#                     return JsonResponse({'message': 'Login successful'}, status=200)
#                 return JsonResponse({'error': 'Biometric verification failed'}, status=400)
#             # Finally, check if an authenticator code was provided (Google/MS Authenticator)
#             if authenticator_code:
#                 if verify_authenticator_code(authenticator_code):  # Add authenticator logic
#                     return JsonResponse({'message': 'Login successful'}, status=200)
#                 return JsonResponse({'error': 'Invalid authenticator code'}, status=400)
#             return JsonResponse({'error': 'No valid login method provided'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#     return JsonResponse({'message': 'This endpoint only accepts POST requests.'}, status=405)


@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        try:
            users = AppUser.objects.all()  # Fetch all users from AppUser model
            result = [{
                'email': user.user.email,
                'nickname': user.nickname,
                'sector': user.sector,
                'region': user.region,
                'total_score': user.total_score
            } for user in users]
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
def calculate_peetore(yes_count, no_count):
    return yes_count - no_count



# @csrf_exempt
# def process_prompt(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             prompt = data.get('prompt')
#             if prompt:
#                 # Call Google Gemini API here
#                 # Replace with your API key and URL for Google Gemini
#                 response = requests.post(
#                     'https://api.example.com/gemini',  # Replace with actual URL
#                     headers={'Authorization': 'Bearer YOUR_API_KEY'},
#                     json={'prompt': prompt}
#                 )

#                 if response.status_code == 200:
#                     response_data = response.json()
#                     # Process the response as needed
#                     return JsonResponse({'response': response_data}, status=200)
#                 else:
#                     return JsonResponse({'error': 'Error calling Google Gemini API'}, status=response.status_code)
#             else:
#                 return JsonResponse({'error': 'No prompt provided'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#     else:
#         return JsonResponse({'message': 'This endpoint only accepts POST requests.'}, status=405)
# GEMINI_API_URL = "https://api.google.com/gemini/v1/prompt"

@csrf_exempt
gemini_ai.configure(api_key="YOUR_API_KEY")

def send_prompt_to_gemini(prompt_text):
    try:
        # Send the prompt to Google Gemini
        response = gemini_ai.generate_text(
            prompt=prompt_text
        )
        return response['text'] if response else None
    except Exception as e:
        return str(e)
# def send_prompt_to_gemini(prompt_text):
#     # Send the prompt to Google Gemini API
#     try:
#         headers = {'Authorization': 'Bearer <YOUR_ACCESS_TOKEN>'} #key or secret?
#         response = requests.post(GEMINI_API_URL, json={'prompt': prompt_text}, headers=headers)
        
#         if response.status_code == 200:
#             return response.json().get('response')
#         return None
#     except Exception as e:
#         return None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def submit_prompt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt_text = data.get('prompt')
            user_id = data.get('user_id')  # Fetch user ID from the request
            user = User.objects.get(id=user_id)  # Fetch the user object from Django's User model
            
            # Send prompt to Google Gemini
            #incorrect, need to use the sdk
            gemini_response = send_prompt_to_gemini(prompt_text)
            if gemini_response:
                # Store the prompt and response in the database
                prompt = PromptModel.objects.create(
                    user=user,  # Correct model and user
                    prompt_text=prompt_text,
                    gemini_response=gemini_response,
                    response=gemini_response,
                    yes_count=0,
                    no_count=0,
                    score=0
                )
                return JsonResponse({
                    'status': 'success',
                    'gemini_response': gemini_response
                })
            return JsonResponse({'status': 'error', 'message': 'Gemini API error'}, status=500)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def process_prompt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt_text = data.get('prompt')
            user_id = data.get('user_id')  # Fetch user ID from the request
            user = User.objects.get(id=user_id)  # Fetch the user object
            if not prompt_text:
                return JsonResponse({'error': 'No prompt provided.'}, status=400)
            
            # Call Google Gemini API
            gemini_response = send_prompt_to_gemini(prompt_text)
            if gemini_response:
                yes_count = gemini_response.count('Yes')  # Example Yes/No logic
                no_count = gemini_response.count('No')
                
                return JsonResponse({
                    'status': 'success',
                    'gemini_response': gemini_response,
                    'yes_count': yes_count,
                    'no_count': no_count
                }, status=200)
            return JsonResponse({'error': 'Failed to get response from Gemini API.'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def get_prompt_history(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')  # Get user_id from the request
            user = User.objects.get(id=user_id)
            prompts = PromptModel.objects.filter(user=user).values('prompt_text', 'response')
            return JsonResponse(list(prompts), safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_ranking(request):
    if request.method == 'GET':
        try:
            # Ranking logic: sort users by total prompt scores
            users = AppUser.objects.all().order_by('-total_score')[:10]  # Top 10 users
            ranking_data = [{
                'nickname': user.nickname,
                'prompt_score': user.total_score,
                'sector': user.sector,
                'region': user.region
            } for user in users]
            return JsonResponse(ranking_data, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)