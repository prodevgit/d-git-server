from django.urls import reverse
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from DGitServer.settings import PROTOCOL
from dgit.models import DGitFile, DGitPush


class DGitPushSerializer(ModelSerializer):

    class Meta:
        model = DGitPush

class DGitFileSerializer(ModelSerializer):
    url = SerializerMethodField()
    path = SerializerMethodField()

    def get_url(self,file):
        return f"{PROTOCOL}://{self.context['request'].get_host()}{reverse('v1:repository-object-download-api')}?ref={file.object_id}"

    def get_path(self,file):
        return file.path.split(f'{str(file.commit.branch.repository.object_id)}/')[1]

    class Meta:
        model = DGitFile
        fields = '__all__'