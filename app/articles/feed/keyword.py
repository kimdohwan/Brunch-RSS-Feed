from .myfeed import MyFeed
from ..models import Keyword


# 커스터마이징한 MyFeed 상속
class KeywordFeed(MyFeed):
    brunch_title = "Brunch 키워드: "  # 피드의 이름에 들어갈 문자열
    link = "/feeds/keyword/"
    description = "등록한 검색어의 최신글들을 업데이트합니다"

    def items(self, keyword):  # Keyword 에 연결된(ManyToMany) Article
        return Keyword.objects.get(keyword=keyword).articles.all().order_by('-published_time')

    def get_object(self, request, *args, **kwargs):
        return str(kwargs['keyword'])  # 검색된 키워드 전달
