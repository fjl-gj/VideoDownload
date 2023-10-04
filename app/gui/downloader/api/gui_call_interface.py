import os
import urllib.request
from copy import deepcopy
from pip._vendor import requests
from app.gui.downloader.log.log import logger
from app.gui.downloader.utils import fomart_time
from app.gui.downloader.setting.global_var_ import globals_var
from app.gui.downloader.utils import result_proxy
from youtube_dl import YoutubeDL


def data_parems(result, proxies):
    path = os.path.join(os.path.abspath(os.getcwd()), 'static')
    logger.info(path)
    # _proxies = {"https": "http://127.0.0.1:1087", "http": "http://127.0.0.1:1087"}
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Safari/537.36',
    }
    duration = fomart_time(int(result.get('duration')))
    logger.info('Enter the parsing')
    link_message = dict()
    link_message['title'] = result.get('title')
    link_message['uploader'] = result.get('uploader')
    link_message['url_id'] = result.get('id')
    link_message['duration'] = duration
    link_message['cove'] = result['thumbnails'][0].get('url') if result['thumbnails'] else ''
    link_message['height'] = result['thumbnails'][0].get('height') if result['thumbnails'] else ''
    link_message['width'] = result['thumbnails'][0].get('width') if result['thumbnails'] else ''
    link_message['formats'] = result.get('formats')
    link_message['url_id'] = result.get('id')
    link_message['webpage_url'] = result.get('webpage_url')
    cove = deepcopy(link_message['cove'])
    if cove:
        logger.info(cove)
        cove_type = cove.split("?")[0].split(".")[-1]
        covr_path = f"{path}\\resource\\cove.{cove_type}"
        logger.info(f'{cove_type}, {covr_path}')
        resp = requests.get(cove, headers=_headers, proxies=proxies, timeout=15)
        logger.info("准备写入")
        with open(covr_path, 'wb') as f:
            f.write(resp.content)
        link_message['cove'] = covr_path
    return link_message


def run(link):
    proxies = result_proxy(globals_var.PROXY)
    logger.info(proxies)
    youtube_option = {'proxy': proxies.get("http")}
    logger.info(youtube_option)
    logger.info('Configuration loaded')
    with YoutubeDL(youtube_option) as youtube:
        logger.info('Start request')
        logger.info(link)
        # result = youtube.extract_info('https://youtu.be/fUyTKaU6zRc', download=False)
        result = youtube.extract_info(link, download=False)
        logger.info('Request completed')
        # logger.info(result)
        logger.info("开始解析")
    link_message = data_parems(result, proxies)
    return link_message


def download_api(link):
    pass


def save_download_api(resp):
    pass
