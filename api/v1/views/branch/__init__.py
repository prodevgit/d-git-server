from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.v1.views.branch.serializer import DGitBranchCreateSerializer, DGitBranchListSerializer, \
    DGitBranchDetailSerializer
from api.v1.views.dgit.serializer import DGitPushSerializer
from dgit.models import DGitRepository, DGitBranch


class DGitBranchCreateView(CreateAPIView):
    serializer_class = DGitBranchCreateSerializer

    def perform_create(self, serializer):
        data = {}
        print(self.kwargs)
        try:
            repository = DGitRepository.objects.get(object_id=self.kwargs.get('object_id'))
            parent = self.request.data.get('parent')
            if parent:
                parent = DGitBranch.objects.get(object_id=parent)
            branch_exist = False
            branch = DGitBranch.objects.none()
            try:
                branch = DGitBranch.objects.get(name=self.request.data.get('name'))
                branch_exist = True
                if branch.parent != parent:
                    branch_exist = False
            except:
                pass

            if not branch_exist:
                if parent:
                    branch = serializer.save(owner=self.request.user,repository=repository,parent=parent)
                else:
                    branch = serializer.save(owner=self.request.user, repository=repository)
                data['status'] = True
                data['message'] = 'Branch created'  # Add a message giving details about branch
            else:
                data['status'] = False
                data['message'] = 'Branch already exist' #Add a message giving details about branch
        except Exception as e:
            print(e)
            data['status'] = False
            data['message'] = 'failed to create'
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        return Response(data=data)

class DGitBranchDetailView(RetrieveAPIView):
    queryset = DGitBranch.objects.order_by('id').all()
    serializer_class = DGitBranchDetailSerializer

    lookup_field = 'object_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class DGitBranchListView(ListAPIView):
    serializer_class = DGitBranchListSerializer

    def get_queryset(self):
        object_id = self.kwargs.get('object_id')
        queryset = DGitBranch.objects.filter(repository__object_id=object_id)
        return queryset