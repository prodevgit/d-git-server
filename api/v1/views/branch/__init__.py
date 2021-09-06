from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.v1.views.branch.serializer import DGitBranchCreateSerializer
from api.v1.views.dgit.serializer import DGitPushSerializer
from dgit.models import DGitRepository, DGitBranch


class DGitBranchCreateView(CreateAPIView):
    serializer_class = DGitBranchCreateSerializer

    def perform_create(self, serializer):
        data = {}
        print(self.kwargs)
        try:
            repository = DGitRepository.objects.get(object_id=self.kwargs.get('object_id'))
            parent = self.kwargs.get('parent')
            if parent:
                parent = DGitBranch.objects.get(object_id=parent)
                branch = serializer.save(owner=self.request.user,repository=repository,parent=parent)
            else:
                branch = serializer.save(owner=self.request.user, repository=repository)
            data['status'] = True
            data['message'] = 'Branch created' #Add a message giving details about branch
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
