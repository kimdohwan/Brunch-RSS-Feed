from .myfeed import MyFeed
from ..models import Writer


class UserFeed(MyFeed):
    brunch_title = "Brunch 사용자: "
    link = "/feeds/user/"
    description = "등록한 사용자의 구독자 글을 업데이트합니다"

    def items(self, user_id):
        user = Writer.objects.get(user_id=user_id)

        query_set = Writer.objects.none()
        for writer in user.following.prefetch_related():
            query_set |= writer.articles.select_related()

        return query_set.order_by('-published_time')

    def get_object(self, request, *args, **kwargs):
        return str(kwargs['user_id'])
