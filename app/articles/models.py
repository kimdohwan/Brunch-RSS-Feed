from django.db import models


class BrunchUser(models.Model):
    """
    BrunchUser 를 추상 모델로 사용한 이유:
        user_id  브런치 유져의 id 를 나타내지만, BrunchUser 를 상속받은 각각의 모델에서 다른 기능을 위해 사용된다.
          Writer : user_id 는 Article 의 글쓴이를 의미하며, 앱 사용자의 입력(작가검색) or 크롤링 작업을 통해 입력된다.
          Subscriber : user_id 는 현재 앱의 사용자가 입력하는 데이터이며, 입력된 user_id 가 브런치에서 구독하고있는
          작가들을 구독 리스트로 갖는다.
    """
    user_id = models.CharField(verbose_name='아이디', null=False, max_length=200, unique=True)

    class Meta:
        abstract = True


class Writer(BrunchUser):
    media_name = models.CharField(verbose_name='작가명', null=True, max_length=200)
    num_subscription = models.IntegerField(verbose_name='구독자 수', null=True)


class Subscriber(BrunchUser):
    writer_list = models.ForeignKey(
        Writer,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subscribers',
        verbose_name='구독중인 작가'
    )


class Keyword(models.Model):
    keyword = models.CharField(verbose_name='검색 단어', null=True, max_length=200)


class Article(models.Model):
    title = models.CharField(verbose_name='제목', null=False, max_length=200)
    content = models.TextField(verbose_name='본문', null=False)
    article_txid = models.CharField(verbose_name='작가id_글번호', null=False, unique=True, max_length=200)
    published_time = models.DateTimeField()
    text_id = models.IntegerField(verbose_name='글 번호', null=False)
    writer = models.ForeignKey(
        Writer,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    keyword = models.ManyToManyField(
        Keyword,
        related_name='articles',
    )
