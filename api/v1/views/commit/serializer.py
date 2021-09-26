from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from api.v1.views.dgit.serializer import DGitFileSerializer
from dgit.models import DGitCommit, DGitFile


class CloneCommitSerializer(ModelSerializer):
    objects = SerializerMethodField()
    prev_commit = SerializerMethodField()

    def get_objects(self, commit):
        data = {}
        files = DGitFile.objects.filter(commit=commit)
        for file in files:
            data[str(file.object_id)] = DGitFileSerializer(file,context={'request':self.context['request']}).data
        return data

    def get_prev_commit(self,commit):
        return commit.prev_commit.object_id if commit.prev_commit else None

    class Meta:
        model = DGitCommit
        fields = ['object_id','owner','branch','prev_commit','objects']