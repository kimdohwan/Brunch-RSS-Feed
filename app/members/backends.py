from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


# 프로제트에 사용될 관리자 계정 자동으로 생성
class SettingsBackend:
    def authenticate(self, request, username=None, password=None):
        login_valid = settings.ADMIN_LOGIN == username
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)

        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # User 인스턴스 생성할 때 password 가 없는 이유?
                # 우리 DB 에는 admin 유져의 password 를 공란으로 남겨진다
                # 내가 작성한 authenticate 에서 유일하게 비밀번호를 검사한다
                # 만약 admin 계정의 비밀번호 수정 시 DB 접근없이 settings.AUTH_PASSWORD 만 바꿔주면 잘 동작한다.
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
