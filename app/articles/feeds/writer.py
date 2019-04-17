from .myfeed import MyFeed
from ..models import Writer


# 커스터마이징한 MyFeed 를 상속
class WriterFeed(MyFeed):
    brunch_title = "Brunch 작가: "
    link = "/feeds/writer/"
    description = "등록한 작가의 최신글들을 업데이트합니다"

    def items(self, user_id):  # Writer 에 연결된(Foreign key) Article
        return Writer.objects.get(user_id=user_id).articles.all().order_by('-published_time')

    def get_object(self, request, *args, **kwargs):
        return str(kwargs['writer_id'])  # 검색된 작가id 전달
