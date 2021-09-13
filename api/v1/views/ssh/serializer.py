from rest_framework.serializers import ModelSerializer

from ssh.models import UserSSH


class UserAddSSHKeySerializer(ModelSerializer):

    class Meta:
        model = UserSSH
        fields = ['owner']