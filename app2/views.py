from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . models import Car
from .serializers import CarSerializer

# Create your views here.

class CarCollectionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer


    def get(self, request):
        cars = request.user.cars.all()
        serializer = self.serializer_class(instance=cars, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class CarSingletonView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = self.serializer_class(instance=car)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=car, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


