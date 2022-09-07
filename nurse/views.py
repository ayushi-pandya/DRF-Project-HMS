from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from nurse.models import NurseDuty
from nurse.serializers import AssignDutySerializer
from users.renderers import UserRenderer


class AssignDuty(generics.CreateAPIView):
    """
    API for assigned duty to staff
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = NurseDuty.objects.all()
    serializer_class = AssignDutySerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': 'Duty Assigned successfully'}, status=status.HTTP_201_CREATED)
