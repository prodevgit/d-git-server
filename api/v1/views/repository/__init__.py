import os
import traceback
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from DGitServer.constants import DGIT_DATA_PATH
from DGitServer.settings import BASE_DIR
from access_control.models import Policy, RepositoryPermission, Role, RepositoryInvite, CloneToken
from api.v1.views.branch.serializer import CloneBranchSerializer
from api.v1.views.repository.serializer import RepositoryCreateSerializer, RepositoryListSerializer, \
    RepositoryDetailSerializer
from dgit.constants import ROLE_OWNER, ROLE_DEVELOPER
from dgit.models import DGitRepository, DGitRepositoryFile, RepoFileTracker, DGitBranch, DGitFile, DGitCommit

from utils.decorators import repo_auth
from utils.functions import send_email
from utils.messages import MESSAGE

DEFAULT_BRANCHES = ({'name':'master','default':False},{'name':'develop','default':True})
DEFAULT_FILES = ('.dgitignore','readme.md','auth/','testing/','api/v1/testbranch/views.py')
class RepositoryCreateView(CreateAPIView):
    serializer_class = RepositoryCreateSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            repository_name = self.request.data.get('name')
            repository_name=repository_name.replace(' ','-').lower()
            repository_count = DGitRepository.objects.filter(name=repository_name,owner=self.request.user).count()
            if repository_count:
                data['status'] = False
                data['message'] = MESSAGE.get('err_create_repo')
                return data
            repository = serializer.save(name=repository_name,owner=self.request.user)
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
            for branch in DEFAULT_BRANCHES:
                branch = DGitBranch.objects.create(name=branch['name'],repository=repository,owner=self.request.user,is_root=True,default=branch['default'])
                commit = DGitCommit.objects.create(
                            message='Initial Commit',
                            owner=self.request.user,
                            branch=branch
                        )
                REPO_PARENT_DIRECTORY = f'{BASE_DIR.parent}/{DGIT_DATA_PATH}/repositories/{self.request.user.username}/{repository.object_id}/{branch.name}'
                if not os.path.isdir(REPO_PARENT_DIRECTORY):
                    os.makedirs(REPO_PARENT_DIRECTORY)
                for file in DEFAULT_FILES:
                    if '/' in file:
                        print(file)
                        print(os.path.isdir(f'{REPO_PARENT_DIRECTORY}/{file}'))
                        if not os.path.isdir(f'{REPO_PARENT_DIRECTORY}/{file}'):
                            dir = file.rsplit('/',1)[0]
                            print(f'{REPO_PARENT_DIRECTORY}/{dir}')
                            os.makedirs(f'{REPO_PARENT_DIRECTORY}/{dir}')
                    try:
                        with open(f'{REPO_PARENT_DIRECTORY}/{file}','wb+') as f:
                            f.write(b'')
                            dgit_file = DGitFile.objects.create(
                                            name=file,
                                            owner=self.request.user,
                                            path=f'repositories/{self.request.user.username}/{repository.object_id}/{file}',
                                            commit=commit
                                        )
                    except IsADirectoryError as e:
                        print(e)
                    # except FileExistsError as e:
                    #     print(e)
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

class RepositoryCloneView(APIView):
    authentication_classes = []
    permission_classes = []

    @method_decorator(repo_auth)
    def dispatch(self, *args, **kwargs):
        return super(RepositoryCloneView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            clone_token = request.META['HTTP_AUTHORIZATION']
            clone_token = CloneToken.objects.get(token=clone_token)
            repository = clone_token.repository
            branches = DGitBranch.objects.filter(repository=repository)
            default_branch = branches.filter(default=True).first()
            clone_data = {}
            clone_data['repository'] = repository.object_id
            clone_data['name']= repository.name
            clone_data['objects_count'] = DGitFile.objects.filter(commit__branch__repository=repository).count()
            clone_data['default'] = {'name':default_branch.name,'object_id':default_branch.object_id}
            clone_data['data'] = CloneBranchSerializer(branches,many=True,context={'request':self.request}).data
            data['status'] = True
            data['data'] = clone_data
        except Exception as e:
            print(e)
            data['status'] = False
            data['message'] = "You're not authorized to clone this repository"
        return Response(data=data)


class RepositoryPushView(APIView):
    authentication_classes = []
    permission_classes = []

    @method_decorator(repo_auth)
    def dispatch(self, *args, **kwargs):
        return super(RepositoryPushView, self).dispatch(*args, **kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            # start_time =
            request_for = request.GET.get('request_for')
            print(request_for)
            if request_for == 'tracker':
                fdata = request.data.get('fdata')
                session = uuid.uuid4()
                for file in fdata:
                    repofiletracker = RepoFileTracker.objects.create(name=file['name'],path=file['path'],identifier=file['identifier'],session=session)
                data['status'] = True
                data['message']= 'Files added to tracker'
                data['data']=session

            elif request_for == 'pusher':
                object_id = request.data.get('repository')
                branch = request.data.get('branch')
                commit = request.data.get('commit')
                session = request.GET.get('session').replace('-','')
                repository = DGitRepository.objects.filter(object_id=object_id).first()
                repofiletracker = RepoFileTracker.objects.filter(session=session)
                file_desc={}
                for filetracker in repofiletracker:
                    identifier = str(filetracker.identifier)
                    file_desc[identifier] = {}
                    file_desc[identifier]['name'] = filetracker.name
                    file_desc[identifier]['path'] = filetracker.path
                repository_dir = f'{settings.REPOSITORY_DIR}/{object_id}'
                if not os.path.isdir(repository_dir):
                    os.mkdir(repository_dir)

                for identifier,file in request.FILES.items():
                    _name = file_desc[identifier]['name']
                    _path = file_desc[identifier]['path'].rsplit('/',1)[0]
                    file_path = f'{settings.REPOSITORY_DIR}/{object_id}/branch/{branch}/commit/{commit}{_path}'
                    if not os.path.isdir(file_path):
                        os.makedirs(file_path)
                    with open(f'{file_path}/{_name}', 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                for filetracker in repofiletracker:
                    filetracker.delete()
                data['status'] = True
                data['message'] = 'Push success'
        except Exception as e:
            print(e)
            data['status'] = False
            data['message'] = MESSAGE.get('something_wrong')
        return Response(data=data)

class RepositoryUnauthorizedCloneView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data={}
        data['status'] = False
        data['message'] = "You don't have access to this repository"
        return Response(data=data)

    def get(self, request, *args, **kwargs):
        data={}
        data['status'] = False
        data['message'] = "You don't have access to this repository"
        return Response(data=data)

class RepositoryObjectDownloadView(APIView):
    authentication_classes = []
    permission_classes = []

    @method_decorator(repo_auth)
    def dispatch(self, *args, **kwargs):
        return super(RepositoryObjectDownloadView, self).dispatch(*args, **kwargs)

    def get(self,request):
        object = DGitFile.objects.filter(object_id=request.GET.get('ref')).first()
        filename = object.name
        import mimetypes
        filepath = f'{BASE_DIR.parent}/{DGIT_DATA_PATH}/{object.path}'
        print(filepath)
        fl = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

