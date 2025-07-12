from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    # このフォームモデルにUserモデルの情報を乗せる
    class Meta:
        # フォームで受け取ったデータをどのモデルで保存するのか、ユーザーに入力してもらう項目を指定
        model = User
        fields = ('username', 'password1', 'password2')  