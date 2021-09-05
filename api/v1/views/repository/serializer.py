from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from dgit.models import DGitRepository


class RepositoryCreateSerializer(ModelSerializer):

    class Meta:
        model = DGitRepository
        exclude = ['members','policy','owner']


class RepositoryDetailSerializer(ModelSerializer):

    owner = SerializerMethodField()
    members = SerializerMethodField()
    policy = SerializerMethodField()

    def get_owner(self, repository):
        owner = {}
        owner['id'] = repository.owner.id
        owner['name'] = repository.owner.get_full_name()
        return owner

    def get_members(self, repository):
        members = []
        for member in repository.members.all():
            member_data = {}
            member_data['id'] = member.id
            member_data['name'] = member.get_full_name()
            members.append(member_data)
        return members

    def get_policy(self,repository):
        policy = {}
        policy['id'] = repository.policy.id
        policy_members = []
        for permission in repository.policy.permissions.all():
            member = {}
            member['member_id'] = permission.user.id
            member['member_name'] = permission.user.get_full_name()
            member['role'] = permission.role.name
            policy_members.append(member)
        policy['members'] = policy_members
        return policy

    class Meta:
        model = DGitRepository
        exclude = ['id']

class RepositoryListSerializer(ModelSerializer):

    owner = SerializerMethodField()

    def get_owner(self, repository):
        owner = {}
        owner['id'] = repository.owner.id
        owner['name'] = repository.owner.get_full_name()
        return owner

    class Meta:
        model = DGitRepository
        exclude = ['id','members','policy']