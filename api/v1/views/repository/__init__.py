from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from access_control.models import Policy, RepositoryPermission, Role, RepositoryInvite
from api.v1.views.repository.serializer import RepositoryCreateSerializer, RepositoryListSerializer, \
    RepositoryDetailSerializer
from dgit.constants import ROLE_OWNER, ROLE_DEVELOPER
from dgit.models import DGitRepository
from utils.functions import send_email
from utils.messages import MESSAGE


class RepositoryCreateView(CreateAPIView):
    serializer_class = RepositoryCreateSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            repository = serializer.save(owner=self.request.user)
            repository.members.add(self.request.user)
            owner_role = Role.objects.get(role=ROLE_OWNER)
            repo_permission = RepositoryPermission.objects.create(
                role=owner_role,
                user=self.request.user,
                is_read = True,
                is_write = True,
                is_merge = True,
                is_delete = True
            )
            policy = Policy.objects.create()
            policy.permissions.add(repo_permission)
            policy.save()
            repository.policy = policy
            repository.save()
            data['status'] = True
            data['message'] = MESSAGE.get('created')

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

class RepositoryDetailView(RetrieveAPIView):
    queryset = DGitRepository.objects.order_by('id').all()
    serializer_class = RepositoryDetailSerializer

    lookup_field = 'object_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class RepositoryListView(ListAPIView):
    queryset = DGitRepository.objects.all()
    serializer_class = RepositoryListSerializer

class RepositoryAddMemberView(APIView):

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            object_id = kwargs.get('object_id')
            member_id = request.data.get('member')
            member = User.objects.get(id=member_id)
            try:
                member_token = Token.objects.get(user=member)
            except:
                member_token = Token.objects.create(user=member)

            body_vars = {
               'user': member,
               'repo': object_id,
               'domain': get_current_site(request),
               'token': member_token.key,
               'settings': settings
            }
            header = {
               'subject': 'DGit - Project Access',
               'to': [member.email],
               'template_name': 'repo_invite'
            }
            repository_invite = RepositoryInvite.objects.filter(user=member,repository=object_id).first()
            if repository_invite and not repository_invite.expired:
                data['status'] = False
                if repository_invite.accepted:
                    data['message'] = MESSAGE.get('repo_member_already').format(user=member.get_full_name())
                else:
                    data['message'] = MESSAGE.get('repo_invite_already')
            else:
                send_email(header, body_vars)
                repository_invite = RepositoryInvite.objects.create(user=member,repository=object_id)
                data['status'] = True
                data['message'] = MESSAGE.get('repo_invite')
        except Exception as e:
            print(e)
            data['status'] = False
            data['message'] = MESSAGE.get('something_wrong')
        return Response(data=data)

class RepositoryAcceptInviteView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = {}
        token = Token.objects.filter(key=kwargs.get('token')).first()
        if token:
            member = token.user
            repository_object_id = kwargs.get('object_id')
            repository_invite = RepositoryInvite.objects.filter(user=member,repository=repository_object_id,expired=False).first()
            if repository_invite and not repository_invite.expired:
                operation = kwargs.get('operation')
                if operation == 'accept':
                    repository_invite.accepted = True
                    repository_invite.expired = True
                    repository_invite.save()
                    dev_role = Role.objects.get(role=ROLE_DEVELOPER)
                    repository_permission = RepositoryPermission.objects.create(
                        role=dev_role,
                        user=member,
                        is_read=True,
                        is_write=True,
                        is_merge=False,
                        is_delete=False
                    )
                    repository = DGitRepository.objects.get(object_id=repository_object_id)
                    repository.policy.permissions.add(repository_permission)
                    repository.members.add(member)
                    repository.save()
                    data['status'] = True
                    data['message'] = MESSAGE.get('repo_invite_accept')
                elif operation == 'reject':
                    repository_invite.rejected = True
                    repository_invite.expired = True
                    repository_invite.save()
                    data['status'] = True
                    data['message'] = MESSAGE.get('repo_invite_reject')
                else:
                    data['status'] = False
                    data['message'] = MESSAGE.get('repo_invite_operation_invalid')
            else:
                data['status'] = False
                data['message'] = MESSAGE.get('repo_invite_expired')

        return Response(data=data)
