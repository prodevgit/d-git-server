from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from api.v1.views.commit.serializer import CloneCommitSerializer
from dgit.models import DGitBranch, DGitCommit


class DGitBranchCreateSerializer(ModelSerializer):

    class Meta:
        model = DGitBranch
        exclude = ['owner','repository','parent']

class DGitBranchListSerializer(ModelSerializer):

    owner = SerializerMethodField()
    parent = SerializerMethodField()
    sub_branches = SerializerMethodField()

    def get_owner(self,branch):
        data={}
        data['id'] = branch.owner.id
        data['name'] = branch.owner.get_full_name()
        return data

    def get_parent(self,branch):
        if branch.parent:
            data = {}
            data['object_id'] = branch.parent.object_id
            data['name'] = branch.parent.name
            return data
        else:
            return None

    def get_sub_branches(self,branch):
        return DGitBranch.objects.filter(parent=branch).count()

    class Meta:
        model = DGitBranch
        exclude = ['repository']

class DGitBranchDetailSerializer(ModelSerializer):

    owner = SerializerMethodField()
    parent = SerializerMethodField()
    sub_branches = SerializerMethodField()

    def get_owner(self,branch):
        data={}
        data['id'] = branch.owner.id
        data['name'] = branch.owner.get_full_name()
        return data

    def get_parent(self,branch):
        if branch.parent:
            data = {}
            data['object_id'] = branch.parent.object_id
            data['name'] = branch.parent.name
            return data
        else:
            return None

    def get_sub_branches(self,branch):
        branches = DGitBranch.objects.filter(parent=branch)
        return DGitBranchListSerializer(branches,many=True).data

    class Meta:
        model = DGitBranch
        exclude = ['repository']

class CloneBranchSerializer(ModelSerializer):
    commits = SerializerMethodField()

    def get_commits(self,branch):
        data = {}
        commits = DGitCommit.objects.filter(branch=branch)
        for commit in commits:
            data[str(commit.object_id)] = CloneCommitSerializer(commit,context={'request':self.context['request']}).data
        return data

    class Meta:
        model = DGitBranch
        fields = ['name','object_id','parent','default','commits']

