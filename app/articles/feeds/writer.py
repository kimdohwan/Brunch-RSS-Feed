from .myfeed import MyFeed
from ..models import Writer


# 커스터마이징한 MyFeed 를 상속
class WriterFeed(MyFeed):
    brunch_title = "Brunch 작가: "
    link = "/feeds/writer/"
    description = "등록한 작가의 최신글들을 업데이트합니다"

    def items(self, user_id):  # Writer 에 연결된(Foreign key) Article

        try:
            query_set = Writer.objects.get(user_id=user_id).articles.all().order_by('-published_time')

        # 크롤링 작업을 모두 마치지 못한 상태에서 피드를 호출할 경우
        # 빈 리스트를 리턴 한 후, 피드 생성 중이라는 메시지를 Feed 의 title 에 셋팅(Myfeed)
        except Writer.DoesNotExist:
            query_set = []

        return query_set

    def get_object(self, request, *args, **kwargs):
        return str(kwargs['user_id'])  # 검색된 작가id 전달
