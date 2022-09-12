from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from nurse.models import NurseDuty
from nurse.serializers import AssignDutySerializer
from users.models import Staff
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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data, 'msg': 'Duty Assigned successfully'}, status=status.HTTP_201_CREATED)


class SearchDuty(APIView):
    """
    API for give data to ajax call for search user
    """

    def get(self, request):
        room = NurseDuty.objects.all().values_list('staff__staff__username', flat=True)
        room_list = list(room)
        return Response(room_list, status=status.HTTP_200_OK)


class ViewDuty(generics.ListAPIView):
    """
    API for showing list of duty
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    serializer_class = AssignDutySerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.is_admin:
            queryset = NurseDuty.objects.all()
        else:
            staff = get_object_or_404(Staff, staff=self.request.user.id)
            queryset = NurseDuty.objects.filter(staff=staff)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

