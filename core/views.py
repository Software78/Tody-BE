from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .helpers import get_tokens_for_user
# from tody_app.core.helpers import get_tokens_for_user
from .serializers import LoginSerializer, SignupSerializer, TaskSerializer
from .models import Task
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.authentication import 
# Create your views here.




@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>/',
        'Delete':'/task-delete/<str:pk>/',
        'Refresh':'/api/token/refresh/',
        'Signup':'/api/user/signup/',
        'Login':'/api/user/login/',
        }
    return Response(api_urls)


@api_view(['GET'])
# @authentication_class([JWTAuthentication])
def taskList(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    res = { 'status' : status.HTTP_200_OK,'message' : 'success',   'data' : serializer.data }
    return Response(res, status = status.HTTP_200_OK)

@api_view(['GET'])
def taskDetail(request,pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    res = { 'status' : status.HTTP_200_OK,'message' : 'success', 'data' : serializer.data }
    return Response(res, status = status.HTTP_200_OK)

@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        res = { 'status' : status.HTTP_201_CREATED,'message' : 'success', 'data' : serializer.data }
    return Response(res, status = status.HTTP_201_CREATED)

@api_view(['POST'])
def taskUpdate(request,pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task,data=request.data)
    if serializer.is_valid():
        serializer.save()
        res = { 'status' : status.HTTP_200_OK,'message' : 'success', 'data' : serializer.data }
    return Response(res, status = status.HTTP_200_OK)

@api_view(['DELETE'])
def taskDelete(request,pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response("Item successfully deleted", status= 200)

class SignupAPIView(APIView):
    permission_classes = [ AllowAny]
    def post(self,request):
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            res = { 'status' : status.HTTP_201_CREATED, 'message' : 'success'}
            return Response(res, status = status.HTTP_201_CREATED)
        res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data' : serializer.errors }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    permission_classes = [ AllowAny]
    """This api will handle login and generate access and refresh token for authenticate user."""
    def post(self,request):
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                    username = serializer.validated_data["username"]
                    password = serializer.validated_data["password"]
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        res_data = get_tokens_for_user(User.objects.get(username=username))
                        response = {
                                "status": status.HTTP_200_OK,
                                "message": "success",
                                "data": res_data
                                }
                        return Response(response, status = status.HTTP_200_OK)
                    else :
                        response = {
                                "status": status.HTTP_401_UNAUTHORIZED,
                                "message": "Invalid Email or Password",
                                }
                        return Response(response, status = status.HTTP_401_UNAUTHORIZED)
            response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": serializer.errors
                    }
            return Response(response, status = status.HTTP_400_BAD_REQUEST)