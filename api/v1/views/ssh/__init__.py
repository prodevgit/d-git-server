import os

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from DGitServer.constants import SSH_SERVER_COMMAND, SSH_AUTHORIZED_KEYS
from api.v1.views.ssh.functions import validate_ssh
from api.v1.views.ssh.serializer import UserAddSSHKeySerializer
from utils.messages import MESSAGE

class UserAddSSHKeyView(CreateAPIView):
    serializer_class = UserAddSSHKeySerializer

    def perform_create(self, serializer):
        data = {}
        try:
            is_key = validate_ssh(self.request.data.get('key'))
            if is_key:
                user_ssh = serializer.save(owner=self.request.user)
                with open(SSH_AUTHORIZED_KEYS,'ab') as authorized_keys:
                    authorized_keys.write(bytes('\n\n','utf-8'))
                    authorized_keys.write(bytes(self.request.data.get('key'),'utf-8'))

                data['status'] = True
                data['message'] = MESSAGE.get('created')
            else:
                data['status'] = False
                data['message'] = "Ssh create failed"

        except Exception as e:
            print(e)
            data['status'] = False
            data['message'] = MESSAGE.get('err_create_repo')

        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        return Response(data=data)

class SSHServerCommandView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            data['status'] = True
            print(SSH_SERVER_COMMAND)
            # data['data'] = '/home/dgit/dgit_env/bin/python /home/dgit/d-git-server/generate_ssh_token.py'
            data['data'] = '/home/dgit/d-git-server/generate_ssh_token.py'
        except:
            data['status'] = False
            data['message'] = "Command retrieval failed"
        return Response(data=data)