# activities/views.py
from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer

class ActivityList(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(user=user)
