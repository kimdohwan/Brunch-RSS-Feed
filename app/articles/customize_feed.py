from django.contrib.syndication.views import Feed, add_domain

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template import TemplateDoesNotExist, loader
from django.utils.timezone import get_default_timezone, is_naive, make_aware


# 피드 프로그램에서 글 제목을 클릭했을 때 링크되는 곳을 내 홈페이지가 아니라 브런치로 보내기위해서
# feed.add_item() 에 들어가는 link 값 할당 부분을 변경시켜주었다
class CustomFeed(Feed):
    def get_feed(self, obj, request):
        """
        Return a feedgenerator.DefaultFeed object, fully populated, for
        this feed. Raise FeedDoesNotExist for invalid parameters.
        """
        current_site = get_current_site(request)

        link = self._get_dynamic_attr('link', obj)
        link = add_domain(current_site.domain, link, request.is_secure())

        feed = self.feed_type(
            title=self._get_dynamic_attr('title', obj),
            subtitle=self._get_dynamic_attr('subtitle', obj),
            link=link,
            description=self._get_dynamic_attr('description', obj),
            language=settings.LANGUAGE_CODE,
            feed_url=add_domain(
                current_site.domain,
                self._get_dynamic_attr('feed_url', obj) or request.path,
                request.is_secure(),
            ),
            author_name=self._get_dynamic_attr('author_name', obj),
            author_link=self._get_dynamic_attr('author_link', obj),
            author_email=self._get_dynamic_attr('author_email', obj),
            categories=self._get_dynamic_attr('categories', obj),
            feed_copyright=self._get_dynamic_attr('feed_copyright', obj),
            feed_guid=self._get_dynamic_attr('feed_guid', obj),
            ttl=self._get_dynamic_attr('ttl', obj),
            **self.feed_extra_kwargs(obj)
        )

        title_tmp = None
        if self.title_template is not None:
            try:
                title_tmp = loader.get_template(self.title_template)
            except TemplateDoesNotExist:
                pass

        description_tmp = None
        if self.description_template is not None:
            try:
                description_tmp = loader.get_template(self.description_template)
            except TemplateDoesNotExist:
                pass

        for item in self._get_dynamic_attr('items', obj):
            context = self.get_context_data(item=item, site=current_site,
                                            obj=obj, request=request)
            if title_tmp is not None:
                title = title_tmp.render(context, request)
            else:
                title = self._get_dynamic_attr('item_title', item)
            if description_tmp is not None:
                description = description_tmp.render(context, request)
            else:
                description = self._get_dynamic_attr('item_description', item)

            # ---------------------------------customize part-----------------------
            # item.href 를 넣어서 동적으로 브런치 주소를 넣어준다
            link = f'https://brunch.co.kr{item.href}'
            # ----------------------------------------------------------------------

            enclosures = self._get_dynamic_attr('item_enclosures', item)
            author_name = self._get_dynamic_attr('item_author_name', item)
            if author_name is not None:
                author_email = self._get_dynamic_attr('item_author_email', item)
                author_link = self._get_dynamic_attr('item_author_link', item)
            else:
                author_email = author_link = None

            tz = get_default_timezone()

            pubdate = self._get_dynamic_attr('item_pubdate', item)
            if pubdate and is_naive(pubdate):
                pubdate = make_aware(pubdate, tz)

            updateddate = self._get_dynamic_attr('item_updateddate', item)
            if updateddate and is_naive(updateddate):
                updateddate = make_aware(updateddate, tz)

            feed.add_item(
                title=title,
                link=link,
                description=description,
                unique_id=self._get_dynamic_attr('item_guid', item, link),
                unique_id_is_permalink=self._get_dynamic_attr(
                    'item_guid_is_permalink', item),
                enclosures=enclosures,
                pubdate=pubdate,
                updateddate=updateddate,
                author_name=author_name,
                author_email=author_email,
                author_link=author_link,
                categories=self._get_dynamic_attr('item_categories', item),
                item_copyright=self._get_dynamic_attr('item_copyright', item),
                **self.item_extra_kwargs(item)
            )
        return feed
