from .serializers import ResourcesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Resource
from drf_yasg.utils import swagger_auto_schema
from .permissions import Accountant, Worker
from rest_framework.permissions import IsAuthenticated

class GetDataView(APIView):
    permission_classes = [IsAuthenticated, Accountant]

    def get(self, request, *args, **kwargs):
        queryset = Resource.objects.all()
        serializer = ResourcesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateView(APIView):
    permission_classes = [IsAuthenticated, Worker]

    @swagger_auto_schema(request_body=ResourcesSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ResourcesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, Worker]

    def delete(self, request, pk, *args, **kwargs):
        try:
            user_data = Resource.objects.get(pk=pk)
        except Resource.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        user_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=ResourcesSerializer)
    def put(self, request, pk, format=None):
        user_data = Resource.objects.get(pk=pk)
        serializer = ResourcesSerializer(user_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)