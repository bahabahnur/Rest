from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from apps.authentication.serializers import (
    RegisterAPISerializer, LoginSerializer, ChangePasswordSerializer)
from apps.authentication.tasks import send_notification_task


User = get_user_model()


class RegisterAPIView(APIView):
    """ Создание регистарции  """
    def post(self, request):
        serializer = RegisterAPISerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_notification_task.delay(user=user.id, seconds=10)
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


class LoginAPIView(TokenObtainPairView):
    """Логинь"""
    serializer_class = LoginSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    Конечная точка для смены пароля.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Logout(APIView):
#        queryset = User.objects.all()
#
#        def get(self, request, format=None):
#            # simply delete the token to force a login
#            request.user.auth_token.delete()
#            return Response(status=status.HTTP_200_OK)
