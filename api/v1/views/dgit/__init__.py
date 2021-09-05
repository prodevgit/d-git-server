from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.v1.views.dgit.serializer import DGitPushSerializer


class DGitPushView(CreateAPIView):
    serializer_class = DGitPushSerializer

    def perform_create(self, serializer):
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        return Response(data=data)
