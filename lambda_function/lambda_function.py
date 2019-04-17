from crawler import Crawler


def lambda_handler(event, context):
    keyword = event.get('keyword')
    writer = event.get('writer')
    crawler = Crawler(
        keyword=keyword,
        writer=writer
    )
    crawler.crawl()
    return {
        'status': '204 created',
        'crawl':  keyword or writer
    }
