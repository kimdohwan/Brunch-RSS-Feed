from .myfeed import MyFeed
from ..models import Keyword


# 커스터마이징한 MyFeed 상속
class KeywordFeed(MyFeed):
    brunch_title = "Brunch 키워드: "  # 피드의 이름에 들어갈 문자열
    link = "/feeds/keyword/"
    description = "등록한 검색어의 최신글들을 업데이트합니다"

    def items(self, keyword):  # Keyword 에 연결된(ManyToMany) Article

        try:
            query_set = Keyword.objects.get(keyword=keyword).articles.all().order_by('-published_time')

        # 크롤링 작업을 모두 마치지 못한 상태에서 피드를 호출할 경우
        # 빈 리스트를 리턴 한 후, 피드 생성 중이라는 메시지를 Feed 의 title 에 셋팅(Myfeed)
        except Keyword.DoesNotExist:
            query_set = []

        return query_set
        # return Keyword.objects.get(keyword=keyword).articles.all().order_by('-published_time')

    def get_object(self, request, *args, **kwargs):
        return str(kwargs['keyword'])  # 검색된 키워드 전달
