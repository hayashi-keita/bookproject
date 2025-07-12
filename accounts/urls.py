from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignupView
# アプリが増えきたとき、URLを指定する際に混乱しないようにするため
app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]