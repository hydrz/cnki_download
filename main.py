"""
-------------------------------------------------
   File Name：     main.py
   Description :   爬虫主程序
   Author :        Cyrus_Ren
   date：          2018/12/8
-------------------------------------------------
   Change Activity:

-------------------------------------------------
"""

import os
import re
import shutil
import time
from urllib import parse
# 引入字节编码
from urllib.parse import quote

import requests
# 引入beautifulsoup
from bs4 import BeautifulSoup

from crack_verify_code import crack
from get_config import config

HEADER = config.crawl_common_headers

BASIC_URL = 'https://kns.cnki.net/KNS8/AdvSearch?dbcode=CDMD'
SEARCH_HANDLE_URL = 'https://ishufang.cnki.net/KRS/KRSWriteHandler.ashx'
GET_PAGE_URL = 'https://kns.cnki.net/KNS8/Brief/GetGridTableHtml'
DOWNLOAD_URL = 'https://kns.cnki.net/'

PAGE_SIZE = 50
REFERENCE_FILE = 'data/ReferenceList.csv'


class SearchTools(object):
    '''
    构建搜索类
    实现搜索方法
    '''

    def __init__(self):
        self.session = requests.Session()
        self.cur_page_num = 1

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Host': 'kns.cnki.net',
            'Referer': 'https://kns.cnki.net/kns8?dbcode=CDMD',
        }
        self.session.get(BASIC_URL, headers={
                         **headers, **config.crawl_common_headers})

    # 第一次发送post请求
    def search_first(self):
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ishufang.cnki.net',
            'Origin': 'https://kns.cnki.net',
            'Referer': 'https://kns.cnki.net/KNS8/AdvSearch?dbcode=CDMD',
        }

        headers = {**headers, **config.crawl_common_headers}

        post_data = {
            'keyWord': '学科教学',
            'dbcode': 'CDMD',
            'cnkiUserKey': 'df281c79-287b-3599-8ecf-6a9a32c908b6',
            'action': 'keyWord',
            'userName': '',
        }

        return self.session.post(
            SEARCH_HANDLE_URL, data=post_data, headers=headers)

        # 再一次发送get请求,get请求中需要传入第一个检索条件的值

    # 第一次发送post请求
    def search_reference(self, page=1):
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Host': 'kns.cnki.net',
            'Origin': 'https: // kns.cnki.net',
            'Pragma': 'no-cache',
            'Referer': 'https://kns.cnki.net/KNS8/AdvSearch?dbcode=CDMD',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        headers = {**headers, **config.crawl_common_headers}

        post_data = {
            'IsSearch': 'false',
            'QueryJson': '{"Platform":"","DBCode":"CDMD","KuaKuCode":"","QNode":{"QGroup":[{"Key":"Subject","Title":"","Logic":4,"Items":[],"ChildItems":[{"Key":"input[data-tipid=gradetxt-1]","Title":"学科专业名称","Logic":0,"Items":[{"Key":"","Title":"学科教学","Logic":1,"Name":"XF","Operate":"=","Value":"学科教学","ExtendType":1,"ExtendValue":"中英文对照","Value2":""}],"ChildItems":[]},{"Key":"input[data-tipid=gradetxt-2]","Title":"学科专业名称","Logic":1,"Items":[{"Key":"","Title":"数学","Logic":1,"Name":"XF","Operate":"=","Value":"数学","ExtendType":1,"ExtendValue":"中英文对照","Value2":""}],"ChildItems":[]}]},{"Key":"ControlGroup","Title":"","Logic":1,"Items":[],"ChildItems":[]}]}}',
            'SearchSql': '2827E4B6502D87109B360C96D644AF296EF5FC54D0AA7F4F40F2BA012D1535D265CE1C64437F32308F51247A3BA2B0901DCACB8977091DFB02731EA28E86078B9826BA8C49DE58F9FA13473B06C04C16EF60099A760E135CFDBC2A0A53F26D864DE8B97B973087029069C00A5340F8AB0A4A1CFCB3F4ADAC9A349AEDD29BEFC8432FF5A1B0AA4FC93AD9A174B9D5A76D07E8B276D682F9D62069B356081A6E18577273A52F8A91CEECBD03453B44E70243C89588E364BFCBEE92C66BBE8270525D28B2A97AE5C33B5D0C10F6E8BC6D7D12AB0D00378C60A4A11C0CA08E6F24E7118C40D7A189787833D5A8D0A610927E7B693E16C772213FB593CF7DD25FD93EA8069A615417BFF76BB753904FD2CE1E66BA29B900A636A26799295652788EB545669357BF93C2F5BEB718C58282B8C125FD669B3A8E5AAAD69672F06EDF30DCE59BAB25D3BC8AF4C7850F92F96E68DEB1909893B5FEF7C0DC7A02D02D418E019819DE12710F6C11BE721821F994FA13E3AA6648262648BD72D67D3E7B9089994A5FBCE42382710E5FEAB76E641697E1B59A7272820D7B865FD00D6A39C347D53B37AE65A33253B60E6BD0015D6BD88DA9B64984E63C70B9D9432B7E0895CDA4F9A6D46485CE777336D9141EBAFE42FB84ABDABF4958CDA88BD67CD174FA003EAF7B4BA56773DD915D1142199B2A74851F2EBE0F1213DB539A0847190F6FFB783F9F3DBE320BEEE283EB7873E8041BDAB9F0864CD1E1ABD6278FFC4C4A28EA6BF1BE9E9C5C99E2F1BA35D951CAB3153FDC97CC45AD126F2E2752167F04F07318579A042BBE51495AF19784F5886B3A4AE49125C9499B2864E9CEA1A4EDFA94A9F8A69EF1B3D607ABDC916B6D8A12AED9D5B5D8430A84663D477007BDE49237D75C417D03683E3498B4CB87DB7954207001685A1E32B4533E674037221C27D0CB6041CB59B3A31ADF98F103C10E1392D8001755877AFABF5E7C3091128C7B8B157E4A42A99D3274CE5499A777D92E556578E323B5571A3B73',
            'PageName': 'AdvSearch',
            'HandlerId': '16',
            'DBCode': 'CDMD',
            'KuaKuCodes': '',
            'CurPage': page,
            'RecordsCntPerPage': str(PAGE_SIZE),
            'CurDisplayMode': 'listmode',
            'CurrSortField': '%e5%87%ba%e7%89%88%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27DATE%27)',
            'CurrSortFieldType': 'desc',
            'IsSortSearch': 'false',
            'IsSentenceSearch': 'false',
            'Subject': '',
        }

        # 检索结果的第一个页面
        res = self.session.post(
            GET_PAGE_URL, data=post_data,  headers=headers)

        soup = BeautifulSoup(res.text, 'lxml')
        verifycode = soup.find('div', attrs={'class': 'verifycode'})
        if verifycode != None:
            crack.get_image(GET_PAGE_URL, self.session, res)
            return self.search_reference(page)

        return res

    def pre_parse_page(self, page_source):
        soup = BeautifulSoup(page_source, "html.parser", from_encoding="utf-8")

        reference_num = soup.select_one('.pagerTitleCell > em').get_text()
        print('检索到' + reference_num + '条结果')

        reference_num_int = int(reference_num.replace(',', ''))

        page, i = divmod(reference_num_int, PAGE_SIZE)

        if i != 0:
            page += 1

        print('检索到' + str(page) + '页结果，大约需要' + s2h(page * 5) + '。')

        return page

    def parse_page(self, page_source):
        '''
        保存页面信息
        解析每一页的下载地址
        '''
        soup = BeautifulSoup(page_source, 'lxml')
        # 定位到内容表区域
        tr_table = soup.find(name='table', attrs={
                             "class": "result-table-list"})

        # 表头
        cur = soup.find(name='span', attrs={"class": "cur"})

        if cur.string == '1':
            th_text = ''
            thead = soup.select_one('.result-table-list > thead > tr')
            for index, th_info in enumerate(thead):
                th_text += self.parse_tb(th_info) + ','

            if config.crawl_is_downLoad_link == '1':
                th_text += '下载地址'

            with open(REFERENCE_FILE, 'a', encoding='utf-8') as file:
                file.write(th_text + '\n')

        # 数据列
        for index, tr_info in enumerate(tr_table.find_all(name='tr')):
            tr_text = ''
            download_url = ''
            # 遍历每一列
            for idx, td_info in enumerate(tr_info.find_all(name='td')):
                tr_text += self.parse_tb(td_info) + ','
                # 寻找下载链接
                dl_url = td_info.find('a', attrs={'class': 'downloadlink'})
                if dl_url:
                    download_url = dl_url.attrs['href']
            # 将每一篇文献的信息分组
            single_refence_list = tr_text.split(',')
            # print(single_refence_list)

            if config.crawl_is_download == '1':
                self.download_refence(download_url, single_refence_list)

            if config.crawl_is_downLoad_link == '1':
                download_url = DOWNLOAD_URL + download_url
                if tr_text != '':
                    tr_text += download_url

            with open(REFERENCE_FILE, 'a', encoding='utf-8') as file:
                file.write(tr_text + '\n')

    def download_refence(self, url, single_refence_list):
        """
        拼接下载地址
        进行文献下载
        """
        print('正在下载: ' + single_refence_list[1] + '.caj')
        name = single_refence_list[1] + '_' + single_refence_list[2]
        # 检查文件命名，防止网站资源有特殊字符本地无法保存
        file_pattern_compile = re.compile(r'[\\/:\*\?"<>\|]')
        name = re.sub(file_pattern_compile, '', name)
        # 拼接下载地址
        self.download_url = DOWNLOAD_URL + url
        # 保存下载链接
        with open('data/Links.txt', 'a', encoding='utf-8') as file:
            file.write(self.download_url + '\n')
        # 检查是否开启下载模式
        if config.crawl_is_download == '1':
            if not os.path.isdir('data/CAJs'):
                os.mkdir(r'data/CAJs')
            refence_file = requests.get(self.download_url, headers=HEADER)
            with open('data/CAJs\\' + name + '.caj', 'wb') as file:
                file.write(refence_file.content)
            time.sleep(config.crawl_step_wait_time)

    # 拼接表格行
    def parse_tb(self, td_info):
        text = ''
        for string in td_info.stripped_strings:
            if ' ' in string:
                string = string.split(' ')[0]
            text += string
        return text


def s2h(seconds):
    '''
    将秒数转为小时数
    '''
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return ("%02d小时%02d分钟%02d秒" % (h, m, s))


def main():
    time.perf_counter()

    # 递归删除文件
    if os.path.isdir('data'):
        shutil.rmtree('data')

    # 创建一个空的
    os.mkdir('data')

    search = SearchTools()
    search.search_first()

    page = 1

    res = search.search_reference(page)

    total_page = search.pre_parse_page(res.text)

    is_all_download = input('是否要开始下载（y/n）?')

    if is_all_download != 'y':
        return

    search.parse_page(res.text)
    total_page -= 1

    while(total_page > 0):
        print('.')
        page += 1
        res = search.search_reference(page)
        search.parse_page(res.text)
        total_page -= 1
        time.sleep(config.crawl_step_wait_time)

    print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
    print('爬取完毕，共运行：' + s2h(time.perf_counter()))


if __name__ == '__main__':
    main()
