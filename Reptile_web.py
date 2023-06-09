# 导入urlopen
import urllib.request
# 导入BeautifulSoup
from bs4 import BeautifulSoup
import re
import time
import os
from retrying import retry
import pandas as pd
import sys
import csv
from newspaper import Article as New_State
import datetime
import time


class Article:
    def __init__(self, num='', claim='', label='', tags='', response='', evidences='', description='',
                 state_image='',
                 state_time='', state_name='', verified_time='', verifier='',
                 sources='', state_url='', sources_folder=''):
        self.num = num
        self.claim = claim
        self.label = label
        self.tags = tags
        self.response = response
        self.evidences = evidences
        self.description = description
        self.state_image = state_image
        self.state_time = state_time
        self.verified_time = verified_time
        self.verifier = verifier
        self.state_name = state_name
        self.sources = sources
        self.state_url = state_url
        self.sources_folder = sources_folder

    def article_print(self):
        # tags = ",".join(self.tags)  # tag
        # evidences = "\n".join(self.evidences)
        # sources = "\n".join(self.sources)
        print(
            '序号(Num): ' + self.num + '\n' +
            '声明(Textual claim): ' + self.claim + '\n' +
            '真假程度(Label): ' + self.label + '\n' +
            '回应(Response of the verifier): ' + self.response + '\n' +
            '标签(Tags): ' + self.tags + '\n' +
            '声明者(Stated user name): ' + self.state_name + '\n' +
            '声明发生时间(Stated time): ' + self.state_time + '\n' +
            '证明者(Verifier): ' + self.verifier + '\n' +
            '证明时间(Verified time): ' + self.verified_time + '\n' +
            '证明/佐证(Evidence):' + self.evidences + '\n' +
            '详细描述(Description): ' + self.description + '\n' +
            '佐证来源(Sources): ' + self.sources + '\n' +
            '声明图片路径(Image to the claim): ' + self.state_image + '\n' +
            '每条声明链接: ' + self.state_url + '\n' +
            '来源文件夹: ' + self.sources_folder + '\n'
        )

        # 这里把返回列表
        list_data = {
            'Num': [self.num],
            'Textual claim': [self.claim],
            'Image to the claim': [self.state_image],
            'Label': [self.label],
            'Stated time': [self.state_time],
            'Stated user name': [self.state_name],
            'Tags': [self.tags],
            'Verifier': [self.verifier],
            'Verified time': [self.verified_time],
            'Response of the verifier': [self.response],
            'Facts in-short of the verifier': [self.evidences],
            'Fact descriptions of the verifier': [self.description],
            'Supporting sources of the facts': [self.sources],
            'state URL': [self.state_url],
            'Supporting sources_folder of the facts': [self.sources_folder],
        }
        headers = ['Num', 'Textual claim', 'Image to the claim', 'Label', 'Stated time', 'Stated user name',
                   'Tags', 'Verifier', 'Verified time', 'Response of the verifier', 'Facts in-short of the verifier',
                   'Fact descriptions of the verifier', 'Supporting sources of the facts', 'state URL',
                   'Supporting sources_folder of the facts']
        ret = pd.DataFrame(list_data, columns=headers)

        return ret


class Source:
    def __init__(self, source_num='', source_title='', source_url='', source_keywords='', source_publish_date='',
                 source_text='',
                 source_top_image='', source_summary='', source_claim_num='',source_text_appendix=''):
        self.source_num = source_num
        self.source_title = source_title
        self.source_url = source_url
        self.source_keywords = source_keywords
        self.source_publish_date = source_publish_date
        self.source_text = source_text
        self.source_top_image = source_top_image
        self.source_summary = source_summary
        self.source_claim_num = source_claim_num
        self.source_text_appendix = source_text_appendix
    def source_print(self):
        print(
            '来源序号(Source_Num): ' + self.source_num + '\n' +
            '来源标题(Source_Title): ' + self.source_title + '\n' +
            #'来源关键词(Source_KeyWords): ' + self.source_keywords + '\n' +
            '来源发布时间(Source_Publish_Date): ' + self.source_publish_date + '\n' +
            #'来源摘要(Source_Summary): ' + self.source_summary + '\n' +
            '来源内容(Source_Text): ' + self.source_text + '\n' +
            '来源附加内容(Source_Text_Appendix): ' + self.source_text_appendix + '\n' +
            '来源图片(Source_Top_Image)' + self.source_top_image + '\n' +
            '来源链接(Source_Url): ' + self.source_url + '\n' +
            '来源声明序号(Source_Claim_Num): ' + self.source_claim_num + '\n'
        )

        # 这里把返回列表
        list_data = {
            'Source_Num': [self.source_num],
            'Source_Title': [self.source_title],
            #'Source_KeyWords': [self.source_keywords],
            'Source_Publish_Date': [self.source_publish_date],
            #'Source_Summary': [self.source_summary],
            'Source_Text': [self.source_text],
            'Source_Text_Appendix':[self.source_text_appendix],
            'Source_Top_Image': [self.source_top_image],
            'Source_Url': [self.source_url],
            'Source_Claim_Num': [self.source_claim_num],
        }
        source_headers = ['Source_Num', 'Source_Title',
                          #'Source_KeyWords',
                          'Source_Publish_Date',
                          #'Source_Summary',
                          'Source_Text',
                          'Source_Text_Appendix',
                          'Source_Top_Image', 'Source_Url', 'Source_Claim_Num']
        source_ret = pd.DataFrame(list_data, columns=source_headers)
        return source_ret


# 测试进入网站是否出错
# @retry
@retry(stop_max_attempt_number=4)
def entry_net_loop(url):
    try:
        # 伪装成浏览器
        headers = {'User-Agent':
                   # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
                   }
        print("进入网页")
        req = urllib.request.Request(url=url,
                                     headers=headers)
        global response_page
        response_page = urllib.request.urlopen(req, timeout=3)
        print("代码:" + str(response_page.getcode()))
    except:
        print('超时')

    return response_page


# 测试进入来源网站是否出错
@retry(stop_max_attempt_number=2)
def entry_net_source_loop(url):
    try:
        # 伪装成浏览器
        headers = {'User-Agent':
                   # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
                   }
        print("进入来源网页")
        req = urllib.request.Request(url=url,
                                     headers=headers)
        global response_page
        response_page = urllib.request.urlopen(req, timeout=2)
        print("代码:" + str(response_page.getcode()))
    except:
        print('超时')

    return response_page


def reptile_page(page_num, state_num, csv_path):
    # ------------------设置参数-------------------------------------
    # 设置反扒时间
    time_sleep = 1
    # 伪装成浏览器
    # headers = {'User-Agent':
    #            # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
    #                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    #            }
    # 这里设置爬的页数
    page_num = page_num
    i = state_num
    csv_path = csv_path

    # 错误的页就直接丢掉
    # --------------------程序主体-------------------------------

    # try:
    while page_num > 0:
        # 读取网页内容
        url_page_list = "https://www.politifact.com/factchecks/list/?page=" + str(page_num)

        # 这里用于跳出本次循环
        try:
            html_resp = entry_net_loop(url_page_list)
            html = html_resp.read()
            # 用BeautifulSoup解析html
            obj = BeautifulSoup(html, 'html.parser')
        except:
            print("第" + str(page_num) + "页," + "抓取失败的:" + str(state_num))
            continue

        if (page_num > 700):
            if len(obj.find_all("div", class_="pfhead")) != 0:
                print("已经抓取到最后一页了")
                break
        # 打印声明

        for target in obj.find_all(href=re.compile("/factchecks/20")):
            url_page = "https://www.politifact.com" + target['href']

            try:
                html_resp_page = entry_net_loop(url_page)
                if html_resp_page.getcode() == 404:
                    continue
                html = html_resp_page.read()
                soup_href = BeautifulSoup(html, 'html.parser')
            except:
                print("第" + str(page_num) + "页," + "抓取失败的:" + str(state_num))
                continue

            tags_article_block = soup_href.find_all("div", class_='o-stage__inner')
            article = Article(str(i), state_url=url_page)
            if len(tags_article_block) != 0:
                # 获取真假
                tags_label_soup = BeautifulSoup(str(tags_article_block[0]), 'html.parser')
                href_label = tags_label_soup.find_all("img", height="196", width="219", class_="c-image__original")[0][
                    'alt']
                article.label = href_label

                # 获取声明时间
                href_state_time_temp = tags_label_soup.find_all("div", class_="m-statement__desc")[0].text.strip()
                m = re.search(
                    "(January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{1,},\s[0-9]{4}",
                    href_state_time_temp)
                # str = re.search("\n{2,}","\n",str)
                href_state_time = m.group(0)
                article.state_time = href_state_time

                # 获取声明
                href_claim = tags_label_soup.find_all("div", class_="m-statement__quote")[0]
                # 获取声明者名字
                href_state_name = tags_label_soup.find_all("a", class_="m-statement__name")[0].text.strip()

                article.state_name = href_state_name

                article.claim = href_claim.text.strip()

            # 这里判断一下如果连声明都没抓取到，这里就直接放弃该条声明
            if len(article.claim) == 0:
                continue

            # 获取证明时间
            href_verifiers_time = soup_href.find_all("span", class_='m-author__date')
            if len(href_verifiers_time) != 0:
                for href_verified_time in href_verifiers_time:
                    article.verified_time = href_verified_time.text.strip()

            # 获取证明作者名字
            tags_verifiers_block = soup_href.find_all("div", class_='m-author__content copy-xs u-color--chateau')
            if len(tags_verifiers_block) != 0:
                str_article_verifier = []
                for tags_verifier_block in tags_verifiers_block:
                    str_article_verifier.append(tags_verifier_block.a.text.strip())
                article.verifier = ",".join(str_article_verifier)
            # 获取回应
            tags_response_block = soup_href.find_all("h2", class_="c-title c-title--subline")
            if len(tags_response_block) != 0:
                article.response = tags_response_block[0].text.strip()

            # 获取标签tag
            tags_tags_block = soup_href.find_all("a", class_="c-tag")
            if len(tags_tags_block) != 0:
                tags_str = []
                for tags_tag_block in tags_tags_block:
                    tags_str.append(tags_tag_block.span.text)
                article.tags = ",".join(tags_str)

            # 获取证明(短证明)
            tags_evidences_block = soup_href.find_all("div", class_="short-on-time")
            if len(tags_evidences_block) != 0:
                evidence_str = ''
                for tags_evidence_block in tags_evidences_block:
                    for child in tags_evidence_block.children:
                        evidence_str += child.text.replace('\n', '') + '\n'
                article.evidences = evidence_str.strip()

            # 获取来源
            tags_sources_block = soup_href.find_all("article", class_="m-superbox__content")
            if len(tags_sources_block) != 0:
                for tags_source_block in tags_sources_block:
                    tags_ps_block = tags_source_block.find_all("p")
                    source_str = ''
                    href_str = ''
                    source_num = 1
                    for tags_p_block in tags_ps_block:
                        source = Source()
                        source_str += tags_p_block.text.replace('\n', '') + '\n'
                        if tags_p_block.a != None:
                            if 'href' in tags_p_block.a.attrs:
                                sources_path = csv_path + '/source_{}.csv'.format(i // 3000)
                                try:
                                    # print("来源：" + tags_p_block.a['href'])
                                    if '.pdf' in tags_p_block.a['href']:
                                        continue
                                    source_news = New_State(tags_p_block.a['href'])
                                    source_news.download()
                                    source_news.parse()
                                    # print(source_news.text)
                                    if(i==169 and source_num ==2):
                                        print("进入了啊------------------------------")
                                    # 载入来源数据
                                    source.source_title = source_news.title
                                    if len(source_news.text) == 0:
                                        continue
                                    source.source_text = source_news.text.replace('\n\n', '\n')[:32000]
                                    source.source_text_appendix = source_news.text.replace('\n\n', '\n')[32000:64000]
                                    source.source_summary = source_news.summary

                                    for source_news_keyword in source_news.keywords:
                                        source.source_keywords = ",".join(source_news_keyword)
                                    source.source_url = tags_p_block.a['href']
                                    source.source_publish_date = source_news.publish_date.strftime('%Y-%m-%d')
                                    source.source_claim_num = str(i)
                                    source.source_top_image = ''

                                    name_img_num = '{}'.format(i).zfill(5)
                                    name_source_num = '{}'.format(source_num).zfill(3)
                                    name_source = name_img_num + '_' + name_source_num + '.jpg'
                                    source_img_path = csv_path + '/source_image/' + name_source
                                    source.source_num = name_img_num + '_' + name_source_num
                                    try:
                                        print("来源图片：" + source_news.top_img)
                                        html_source_img = entry_net_source_loop(source_news.top_img)
                                        img_source = html_source_img.read()
                                        with open(source_img_path, 'wb') as fd:
                                            fd.write(img_source)
                                        source.source_top_image = source_img_path
                                    except:
                                        print("来源图片抓取失败")
                                        print(e)
                                        print(sys.exc_info())
                                        continue

                                    pd_source_ret = source.source_print()
                                    if len(source.source_text) != 0:
                                        if not os.path.exists(sources_path):
                                            pd_source_ret.to_csv(sources_path, mode='a', index=False,
                                                                 encoding='utf-8')
                                        else:
                                            pd_source_ret.to_csv(sources_path, mode='a', header=False,
                                                                 index=False, encoding='utf-8')
                                        print("第" + str(i) + "个声明," + "第" + str(source_num) + "条来源")
                                        #print("模拟休息1S")
                                        #time.sleep(time_sleep)
                                    else:
                                        continue
                                        print("抓取到空来源")

                                    source_num += 1
                                    # print(source_news.top_img)
                                except Exception as e:
                                    # print(e)
                                    # print(sys.exc_info())
                                    print("-----抓取来源错误，跳到下一个来源----")

                                href_str += tags_p_block.a['href'] + '\n'
                article.sources = source_str.strip()
                article.sources_folder = href_str.strip()

            # 获取详细描述
            tags_descriptions_block = soup_href.find_all("article", class_="m-textblock")

            if len(tags_descriptions_block) != 0:
                tags_descriptions_bloc_soup = BeautifulSoup(str(tags_descriptions_block[0]), 'html.parser')
                info = [s.extract() for s in tags_descriptions_bloc_soup('section')]
                tags_descriptions_block_clear = tags_descriptions_bloc_soup.find_all("article", class_="m-textblock")
                if len(tags_descriptions_block_clear) != 0:
                    for tags_description_block_clear in tags_descriptions_block_clear:
                        article.description = tags_description_block_clear.text.strip()
            # 创建图片存储文件夹，不管有没有图片都要创建
            # 这里使用绝对路径
            img_path = csv_path + '/image'
            if not os.path.exists(img_path):
                os.mkdir(img_path)
            # 抓取图片
            tags_imgs_block = soup_href.find_all("img", class_='c-image__original lozad')
            if len(tags_imgs_block) != 0:
                error_img = ''
                for tags_img_block in tags_imgs_block:
                    picture_href = tags_img_block['data-src']

                    try:
                        html_resp_img = entry_net_loop(picture_href)
                        img_res = html_resp_img.read()
                    except:
                        print("第" + str(page_num) + "页," + "抓取失败的:" + str(state_num) + "的图片抓取失败")
                        error_img = '/error_'
                        continue

                    name_img_num = '{}'.format(i).zfill(5)
                    name_img = '/' + name_img_num
                    with open(img_path + error_img + name_img + '.jpg', 'wb') as fp:
                        fp.write(img_res)
                article.state_image = img_path + name_img + '.jpg'
            else:
                article.state_image = ''

            # article.state_image = img_path + '/claim_{}.jpg'.format(i)

            pd_ret = article.article_print()
            csv_path_join = csv_path + '/claim_information_{}.csv'.format(i // 3000)

            if not os.path.exists(csv_path_join):
                pd_ret.to_csv(csv_path_join, mode='a', index=False,
                              encoding='utf-8')
            else:
                pd_ret.to_csv(csv_path_join, mode='a', header=False,
                              index=False, encoding='utf-8')
            print("第" + str(page_num) + "页," + "总共遍历了" + str(i) + "个声明")
            #print("模拟休息1S")
            i += 1
            #time.sleep(time_sleep)

        # 爬完一页休息5S，反爬
        time.sleep(1)
        print("休息2秒再找下一页")
        page_num += 1
    print("这里开始全删:" + str((i // 30) * 30))


def main():
    page_num = 643  # 页数
    state_num = 18450
    # 声明条数
    csv_path = 'D:/dataset/fact4_dataset'  # 存储路径
    reptile_page(page_num, state_num, csv_path)


# except Exception as e:
#     print("第" + str(page_num) + "页," + "抓取失败的:" + str(i))
#     print(e)  # 输出：division by zero
#     print(sys.exc_info())
#     print('something wrong!')

if __name__ == '__main__':
    main()

# 已经丢掉的页面 139
