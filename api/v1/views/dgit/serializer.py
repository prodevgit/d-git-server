from rest_framework.serializers import ModelSerializer

from dgit.models import DGitFile, DGitPush


class DGitPushSerializer(ModelSerializer):

    class Meta:
        model = DGitPush