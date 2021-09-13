from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from DGitServer.constants import SSH_SERVER_COMMAND
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
                authorized_keys = open("/root/.ssh/authorized_keys").read()
                cmd = 'echo "' + self.request.data.get('key') + '">>/root/.ssh/authorized_keys'

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
            data['data'] = SSH_SERVER_COMMAND
        except:
            data['status'] = False
            data['message'] = "Command retrieval failed"
        return Response(data=data)