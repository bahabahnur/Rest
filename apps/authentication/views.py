from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .send_mail import send_confirmation_email
from .serializers import RegisterAPISerializer

User = get_user_model()


class RegisterAPIView(APIView):
    """ Создание регистарции  """
    def post(self, request):
        serializer = RegisterAPISerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )


class ActivationAPIView(View):
    """Активация по email"""
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True

            user.activation_code = ''
            user.save()
            return render(request, 'accounts/index.html', {})

        except User.DoesNotExist:
            return render(request, 'accounts/exp.html', {})
