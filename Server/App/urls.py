from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('get_all_users', views.get_all_users, name='get_all_users'),
    path('process_prompt', views.process_prompt, name='process_prompt'),  
    path('submit_prompt/', views.submit_prompt, name='submit_prompt'),
    path('get_prompt_history/', views.get_prompt_history, name='get_prompt_history'),
    path('get_ranking/', views.get_ranking, name='get_ranking'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
