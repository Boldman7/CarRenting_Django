from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from .models import User
from .models import Question, Choice
from .models import Tech
from .models import ParseUser

from .serializers import UserSerializer
from .serializers import TechSerializer
from .serializers import SignUpSerializer
from .serializers import SignVerifySerializer
from .serializers import RequestVerifySerializer

import requests
import json

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'car-rentals/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'car-rentals/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'car-rentals/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'car-rentals/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('car-rentals:results', args = (question.id,)))

class AllTech(ListAPIView):

    queryset = Tech.objects.all()
    serializer_class = TechSerializer

    def post(self, request, format=None):
        serializer = TechSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TechView(APIView):

    def get(self, request, pk, format=None):
        try:
            tech = Tech.objects.get(pk=pk)
            serializer = TechSerializer(tech)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        tech = Tech.objects.get(pk=pk)
        tech.delete()
        return Response(status=status.HTTP_200_OK)

##########################################################################   Login APIs   #######################################################################

# SignIn & SignUp #
class SignUpView(APIView):

    def post(self, request):
        signup_serializer = SignUpSerializer(data=request.data)
        if (signup_serializer.is_valid()):

            # Receive mobile, name from app
            mobile = signup_serializer.data.get("mobile")
            email = signup_serializer.data.get("email")
            name = signup_serializer.data.get("name")

            if mobile == None:
                message = "required_mobile"
                response_data = {"success": "false", "data": {"message": message}}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Send request signin to the SDK server
            request_data = signup_serializer.data
            # Global Constants -> this url. ??
            response = requests.post('https://api.platform.integrations.muzzley.com/v3/applications/6eb9d03d-33da-4bcc-9722-611bb9c9fec2/user-sms-entry', data = request_data)
            jsonResponse = json.loads(response.content)

            # Check if jsonResponse has success value.
            if response.status_code == 400:
                if jsonResponse.get("code") == 21211:
                    message = "invalid_mobile"
                    response_data = {"success": "false", "data": {"message": message}}
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Check if there's the mobile number alreday in DB.
            existed_user = User.objects.filter(mobile = mobile).first()

            if existed_user != None:
                existed_user.user_id = jsonResponse.get("id")
                existed_user.name = jsonResponse.get("name")
                existed_user.mobile = jsonResponse.get("mobile")
                existed_user.namespace = jsonResponse.get("namespace")
                existed_user.confirmation_hash = jsonResponse.get("confirmation_hash")
                existed_user.target_id = jsonResponse.get("target_id")
                existed_user.href = jsonResponse.get("href")
                existed_user.type = jsonResponse.get("type")
                existed_user.created_at = jsonResponse.get("created")
                existed_user.updated_at = jsonResponse.get("updated")
                existed_user.save()
                response_data = {"success": "true", "data": {"message": "Login request succeeded."}}
                return Response(response_data, status = status.HTTP_201_CREATED)
            else:
                user_serializer = UserSerializer(data = jsonResponse)

                if user_serializer.is_valid():
                    user_serializer.create(jsonResponse)
                    response_data = {"success": "true", "data": {"message": "Login request succeeded."}}
                    return Response(response_data, status=status.HTTP_201_CREATED)
                else:
                    response_data = {"success": "false", "data": {"message": "There's a problem with saving your information."}}
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {"success": "false", "data":{"message": "There's a problem with receiving your information."}}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

## Sign Verify #
class SignVerifyView(APIView):

    def post(self, request):
        signverify_serializer = SignVerifySerializer(data = request.data)
        if (signverify_serializer.is_valid()):
            mobile = signverify_serializer.data.get("mobile")
            code = signverify_serializer.data.get("code")

            if mobile == None:
                message = "required_mobile"
                response_data = {"success": "false", "data": {"message": message}}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if code == None:
                message = "required_code"
                response_data = {"success": "false", "data": {"message": message}}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Check if there's the mobile number alreday in DB.
            existed_user = User.objects.filter(mobile = mobile).first()

            if existed_user != None:
                user_id = existed_user.user_id
                confirmation_hash = existed_user.confirmation_hash
                request_data = {"confirmation_hash": confirmation_hash, "code": code}
                # headers = {'Content-type': 'application/json'}
                # request_verify_serializer = RequestVerifySerializer()
                # request_verify_serializer.confirmation_hash = confirmation_hash
                # request_verify_serializer.code = code

                response = requests.post(
                    'https://api.platform.integrations.muzzley.com/v3/users/' + user_id + '/sms-verify',
                    data=request_data)
                jsonResponse = json.loads(response.content)

                if response.status_code == 401:
                    response_data = {"success": "false", "data": {"message": "Sms verification failed."}}
                    return Response(response_data, status = status.HTTP_400_BAD_REQUEST)
                else:
                    response_data = {"success": "true", "data": {"message": "Sms verification succeeded."}}
                    return Response(jsonResponse, status = status.HTTP_201_CREATED)
            else:
                response_data = {"success": "false", "data": {"message": "Your phone number hasn't registered."}}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
