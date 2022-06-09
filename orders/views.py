from django.shortcuts import get_object_or_404, render
from rest_framework import generics,status
from rest_framework.response import Response
from . import serializers
from .models import Order
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from  django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class HelloOrderView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="hello orders")

    def get(self, request): 
        return Response(data={"message":"hello Order "}, status=status.HTTP_200_OK)



class OrderCreateListView(generics.GenericAPIView):
    
    
    serializer_class = serializers.OrderCreationSerializer
    
    queryset = Order.objects.all()
    
    permission_classes =[IsAuthenticatedOrReadOnly]
    @swagger_auto_schema(operation_summary="list all orders")
    
    def get(self, request):
        
        orders= Order.objects.all()
        serializer= self.serializer_class(instance=orders,many=True)
        
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(operation_summary="create new order")
    def post(self, request):
      data = request.data
      
      serializer = self.serializer_class(data=data)
      
      user = request.user
      
      if serializer.is_valid():
          serializer.save(customer= user)
          
          return Response(data=serializer.data ,status= status.HTTP_201_CREATED)
      
      return Response(data=serializer.errors , status= status.HTTP_400_BAD_REQUEST)
      
    
    
class OrderDetailView(generics.GenericAPIView):
    
    permission_classes = [IsAdminUser]
    
    serializer_class = serializers.OrderDetailSerializer
    
    @swagger_auto_schema(operation_summary="retrive an order")
    
    def get(self, request, order_id):
        
        order =get_object_or_404(Order,pk=order_id)
        
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status= status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="updating an order")
    def put(self, request, order_id):
        
        data = request.data
        order =get_object_or_404(Order,pk=order_id)
        
        serializer = self.serializer_class(data=data, instance=order)
       
        if serializer.is_valid():
           serializer.save()
           
           
           return Response(data=serializer.data, status= status.HTTP_200_OK)
        return Response(data=serializer.errors , status= status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_summary="deleting/ removing an order")
    def delete(self, request, order_id):
        order =get_object_or_404(Order,pk=order_id)
        
        order.delete()
        
        return Response( status= status.HTTP_204_NO_CONTENT)
    
    
class UpdateOrderStatusView(generics.GenericAPIView):
    
    serializer_class = serializers.OrderStatusUpdateSerializer
    
    permission_classes =[IsAdminUser]
    @swagger_auto_schema(operation_summary="update an order status")
    def put (self, request,order_id):
        order =get_object_or_404(Order,pk=order_id)
        
        data = request.data
        
        serializer = self.serializer_class(data=data, instance=order)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(data=serializer.data, status= status.HTTP_200_OK)
        return Response(data=serializer.errors , status= status.HTTP_400_BAD_REQUEST)

class UserOrdersView(generics.GenericAPIView):
    
    serializer_class = serializers.OrderDetailSerializer
    
    
    
    
    @swagger_auto_schema(operation_summary="get a users allorders")
    def get(self, request,user_id):
        user = User.objects.get(pk=user_id)
        orders =Order.objects.all().filter(customer= user)
        serializer = self.serializer_class(instance=orders , many =True)
        
        return Response(data= serializer.data, status= status.HTTP_200_OK)

class UserOrderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    
    @swagger_auto_schema(operation_summary="get a users specific orders")
    def get(self, request,user_id,order_id):
        user = User.objects.get(pk=user_id)
        orders = Order.objects.all().filter(customer=user).filter(pk=order_id)
        
        serializer = self.serializer_class(instance=orders, many =True)
        
        return Response(data= serializer.data, status= status.HTTP_200_OK)
    
    