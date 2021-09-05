import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.admin import sensitive_post_parameters_m
from rest_auth.app_settings import TokenSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import login as django_login
from api.v1.views.auth.functions import create_token
from api.v1.views.auth.serializer import LoginSerializer

class UserCreateView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = User.objects.create_user('dev', 'admin@dgit.dev', 'admin')
        user.first_name = 'Dev'
        user.last_name = 'Admin'
        user.save()
        return Response(data=user.first_name)


class LoginView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        self.token = create_token(self.token_model, self.user,
                                  self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

    def post(self, request, *args, **kwargs):

        context = {}
        response = None
        self.request = request
        email = self.request.data.get('email', [])

        if email:
            if isinstance(email, list):
                email = email[0]
        else:
            context['msg'] = "There was an error with your E-Mail/Password combination. Please try again"
            response = Response(context, status=status.HTTP_404_NOT_FOUND)
            return response


        try:
            self.serializer = self.get_serializer(data=self.request.data,
                                                  context={'request': request})
            self.serializer.is_valid(raise_exception=True)
            self.login()

            user = authenticate(
                username=email, password=self.request.data['password'])

            max_age = 365 * 24 * 60 * 60  # one year

            expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                                 "%a, %d-%b-%Y %H:%M:%S GMT")
            request.session.set_expiry(float(max_age))

            response = self.get_response()

            response.set_cookie("auth", response.data.get("key"), max_age=max_age, expires=expires,
                                domain=settings.SESSION_COOKIE_DOMAIN,
                                secure=settings.SESSION_COOKIE_SECURE or None, samesite='Lax')

        except Exception as error:
            print("Exception while trying to connect with workspace. Error: {}".format(error))

            context['msg'] = "There was an error with your E-Mail/Password combination. Please try again"
            response = Response(context, status=status.HTTP_404_NOT_FOUND)

        return response
