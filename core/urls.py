from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('api/task-list/', views.taskList, name="task-list"),
    path('api/task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
    path('api/task-create/', views.taskCreate, name="task-create"),
    path('api/task-update/<str:pk>/', views.taskUpdate, name="task-update"),
    path('api/task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("api/user/signup/", views.SignupAPIView.as_view(), name="user-signup"),
    path("api/user/login/", views.LoginAPIView.as_view(), name="user-login"),
]