# -*- coding:utf-8 -*-
"""
    image search
    https://developers.google.com/image-search/v1/jsondevguide
"""
from os import mkdir
from os.path import exists, join
from time import sleep
from urllib import FancyURLopener
from urllib2 import Request, urlopen

try:
    from simplejson import load
except ImportError:
    from json import load

user_agent = None
class MyOpener(FancyURLopener):
    """
        Start FancyURLopener with defined version
    """
    version = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; '
               'it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')


def search_image(term="butterfly", image_path='image', count=3):
    """
    根据关键字搜索图片， 返回下载的图片路径列表
    :param term:        关键词
    :param image_path:  保存路径
    :param count:       存储个数
    :return:            status, [image_path, ]
    """
    # Replace spaces ' ' in search term for '%20' in order to comply with request
    term = term.replace(' ', '%20')
    urls = get_images_urls_from_google_api(term, count)
    images = download_images(urls[:count], join(image_path, term))
    return bool(len(images)), images


def download_images(urls, image_path):
    """
    下载图片
    :param urls:        连接地址列表
    :param image_path:  图片保存目录
    :return:            图片的文件目录列表
    """
    global user_agent
    if not user_agent:
        user_agent = MyOpener()

    # create image path
    if not exists(image_path):
        mkdir(image_path)

    images = []
    # Iterate for each result and get unescaped url
    for no, myUrl in enumerate(urls, 1):
        filename = join(image_path, str(no) + '.jpg')
        images.append(filename)
        if exists(filename):
            continue
        user_agent.retrieve(myUrl, filename)
    return images


def get_images_urls_from_google_api(term, count):
    """
    根据关键字搜索图片， 返回下载的图片路径列表
    :param term:     关键词
    :param count:    存储个数
    :return:         图片链接列表
    """
    image_urls = []
    # Notice that the start changes for each iteration
    # in order to request a new set of images for each loop
    url = ('https://ajax.googleapis.com/ajax/services/search/images?'
           '&start={start}&userip=MyIP&v=1.0&q={term}')
    for i in xrange(count):
        request = Request(url.format(term=term, start=i * 4),
                          None, {'Referer': 'testing'})
        response = urlopen(request)

        # Get results using JSON
        results = load(response)
        if results['responseStatus'] != 200:
            return False, U'google api 返回状态码[%d]' % results['responseStatus']

        for myUrl in results['responseData']['results']:
            print myUrl['title'], myUrl['tbWidth'], myUrl['tbHeight']
            if myUrl['tbUrl'].startswith('http://'):
                image_urls.append(myUrl['tbUrl'])

        if len(image_urls) >= count:
            break

        # 防止google api 拒绝服务
        sleep(0.5)
    return image_urls


from unittest import TestCase


class TestSearch_image(TestCase):
    def test_search_image(self):
        status, images = search_image()

        self.assertTrue(status)
        for image in images:
            exists(image)

