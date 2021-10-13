"""
-------------------------------------------------
   File Name：     CrackVerifyCode.py
   Description :   处理验证码
   Author :        Cyrus_Ren
   date：          2018/12/8
-------------------------------------------------
   Change Activity:
                   
-------------------------------------------------
"""
__author__ = 'Cyrus_Ren'

from PIL import Image
import pytesseract
import re
from get_config import config
from urllib.parse import quote_plus, urlencode
from bs4 import BeautifulSoup

CRACK_CODE_URL = 'https://kns.cnki.net/KNS8/Brief/CheckCode'
CRACK_CODE_PATH = 'data/crack_code.jpeg'


class CrackCode(object):
    def get_image(self, current_url, session, page_source):
        '''
        获取验证码图片
        '''
        self.header = config.crawl_common_headers
        self.session = session
        self.re_current_url = re.search(r'.net(.*)', current_url).group(1)

        # 获得验证码图片地址
        soup = BeautifulSoup(page_source.text, 'lxml')
        img_url = soup.find('img')['src']

        # 下载图片
        img_url = 'https://kns.cnki.net' + img_url
        image_res = self.session.get(img_url, headers=self.header)
        with open(CRACK_CODE_PATH, 'wb') as file:
            file.write(image_res.content)
        # 是否自动识别
        if config.crawl_is_crack_code == '1':
            return self.crack_code()
        else:
            return self.handle_code()

    def crack_code(self):
        '''
        自动识别验证码
        '''
        image = Image.open(CRACK_CODE_PATH)
        # 转为灰度图像
        image = image.convert('L')
        # 设定二值化阈值
        threshold = 127
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')
        code = pytesseract.image_to_text(image)
        print('验证码识别：' + code)
        return self.send_code(code)

    def handle_code(self):
        '''
        手动识别验证码
        '''
        image = Image.open(CRACK_CODE_PATH)
        image.show()
        code = input('出现验证码，请手动输入：')
        return self.send_code(code)

    def send_code(self, code):
        '''
        发送验证码
        '''
        # 对发送链接进行处理
        re_url = quote_plus(self.re_current_url)
        re_url = re.sub(r'%2F', '%2f', re_url)
        re_url = re.sub(r'%3F', '%3f', re_url)
        re_url = re.sub(r'%3D', '%3d', re_url)

        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'kns.cnki.net',
            'Origin': 'https://kns.cnki.net',
            'Referer': 'https://kns.cnki.net/KNS8/AdvSearch?dbcode=CDMD',
            'X-Requested-With': 'XMLHttpRequest',
        }

        headers = {**headers, **config.crawl_common_headers}

        post_data = {
            'vericode': code,
        }

        res = self.session.post(
            CRACK_CODE_URL, data=post_data, headers=headers)
        return res


crack = CrackCode()
