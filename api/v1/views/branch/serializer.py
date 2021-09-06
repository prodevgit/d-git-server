from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from dgit.models import DGitBranch


class DGitBranchCreateSerializer(ModelSerializer):

    class Meta:
        model = DGitBranch
        exclude = ['owner','repository']

class DGitBranchSerializer(ModelSerializer):

    repository = SerializerMethodField()
    owner = SerializerMethodField()
    parent = SerializerMethodField()
    sub_branches = SerializerMethodField()

    class Meta:
        model = DGitBranch
        exclude = []