import hashlib
import json
import os
import re
import requests
from requests.utils import cookiejar_from_dict
from retrying import retry
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

# 更新后的API地址
WEREAD_URL = "https://weread.qq.com/"
WEREAD_NOTEBOOKS_URL = "https://weread.qq.com/api/user/notebook"  # 修改
WEREAD_BOOKMARKLIST_URL = "https://weread.qq.com/web/book/bookmarklist"  # 修改
WEREAD_READ_INFO_URL = "https://weread.qq.com/web/book/getProgress"  # 新增
WEREAD_REVIEW_LIST_URL = "https://weread.qq.com/web/review/list"  # 修改
WEREAD_BOOK_INFO = "https://weread.qq.com/api/book/info"  # 修改
WEREAD_SHELF_URL = "https://weread.qq.com/web/shelf/sync"  # 新增
WEREAD_BEST_REVIEW_URL = "https://weread.qq.com/web/review/list/best"  # 新增

class WeReadApi:
    def __init__(self):
        self.cookie = self.get_cookie()
        self.session = requests.Session()
        self.session.cookies = self.parse_cookie_string()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Referer": WEREAD_URL
        })

    # Cookie相关方法保持不变
    def try_get_cloud_cookie(self, url, id, password):
        # ... [原有代码保持不变] ...

    def get_cookie(self):
        # ... [原有代码保持不变] ...

    def parse_cookie_string(self):
        # ... [原有代码保持不变] ...

    # 更新后的API方法
    def get_bookshelf(self):
        """获取书架上所有书籍"""
        r = self.session.get(WEREAD_SHELF_URL)
        if r.ok:
            return r.json()
        else:
            self.handle_error(r)
            raise Exception(f"获取书架失败: {r.text}")

    def get_notebooklist(self):
        """获取所有划线书籍"""
        r = self.session.get(WEREAD_NOTEBOOKS_URL)
        if r.ok:
            data = r.json()
            return data.get("books", [])
        else:
            self.handle_error(r)
            raise Exception(f"获取笔记本失败: {r.text}")

    def get_bookinfo(self, bookId):
        """获取书籍信息"""
        params = {"bookId": bookId}
        r = self.session.get(WEREAD_BOOK_INFO, params=params)
        if r.ok:
            return r.json()
        else:
            self.handle_error(r)
            raise Exception(f"获取书籍信息失败: {r.text}")

    def get_bookmark_list(self, bookId):
        """获取书籍划线"""
        params = {"bookId": bookId}
        r = self.session.get(WEREAD_BOOKMARKLIST_URL, params=params)
        if r.ok:
            return r.json().get("updated", [])
        else:
            self.handle_error(r)
            raise Exception(f"获取划线失败: {r.text}")

    def get_read_info(self, bookId):
        """获取阅读进度"""
        params = {"bookId": bookId}
        r = self.session.get(WEREAD_READ_INFO_URL, params=params)
        if r.ok:
            return r.json()
        else:
            self.handle_error(r)
            raise Exception(f"获取阅读进度失败: {r.text}")

    def get_review_list(self, bookId, listType=4, maxIdx=0, count=3):
        """获取用户评论"""
        params = {
            "bookId": bookId,
            "listType": listType,
            "maxIdx": maxIdx,
            "count": count,
            "listMode": 2,
            "synckey": 0
        }
        r = self.session.get(WEREAD_REVIEW_LIST_URL, params=params)
        if r.ok:
            return r.json().get("reviews", [])
        else:
            self.handle_error(r)
            raise Exception(f"获取评论失败: {r.text}")

    def get_best_review(self, bookId, maxIdx=0, count=3):
        """获取置顶评论"""
        params = {
            "bookId": bookId,
            "synckey": 0,
            "maxIdx": maxIdx,
            "count": count
        }
        r = self.session.get(WEREAD_BEST_REVIEW_URL, params=params)
        if r.ok:
            return r.json()
        else:
            self.handle_error(r)
            raise Exception(f"获取置顶评论失败: {r.text}")

    def handle_error(self, response):
        """统一错误处理"""
        try:
            errcode = response.json().get("errcode", 0)
            if errcode in [-2010, -2012]:
                print("::error::Cookie已失效，请更新！参考：https://mp.weixin.qq.com/s/B_mqLUZv7M1rmXRsMlBf7A")
        except:
            print(f"请求失败，状态码：{response.status_code}")

    # 移除不再需要的旧API方法
    # ... [删除get_chapter_info、transform_id、calculate_book_str_id等方法] ...

# 使用示例
if __name__ == "__main__":
    weread = WeReadApi()
    
    # 测试获取书架
    shelf = weread.get_bookshelf()
    print(f"书架书籍数量：{len(shelf.get('books', []))}")
    
    # 测试获取书籍信息
    book_id = "41949197"  # 替换为实际bookId
    book_info = weread.get_bookinfo(book_id)
    print(f"书籍标题：{book_info.get('title')}")
    
    # 测试获取划线
    bookmarks = weread.get_bookmark_list(book_id)
    print(f"划线数量：{len(bookmarks)}")
