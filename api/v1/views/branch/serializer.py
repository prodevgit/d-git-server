from rest_framework.serializers import ModelSerializer

from dgit.models import DGitBranch


class DGitBranchCreateSerializer(ModelSerializer):

    class Meta:
        model = DGitBranch