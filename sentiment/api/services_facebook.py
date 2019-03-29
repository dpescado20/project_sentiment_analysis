from facebook_scraper import get_posts
import datetime


class FacebookClient:
    def get_fb_post(self, account_page):
        data = []
        for post in get_posts(account_page, pages=25):
            data.append((post['time'].strftime('%Y-%m-%d'), post['text'], post['likes']))
        return data
