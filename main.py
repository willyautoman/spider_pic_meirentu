import time

from loguru import logger

import httpx
from lxml import etree
import os


@logger.catch
def get_pic():
    # ----------预处理-------------#
    with open("xiuren.txt", "r") as f:
        url_list = f.readlines()
    for i in range(0, len(url_list) - 1):
        url_list[i] = url_list[i].replace("\n", "")

    # ----------获取图片------------#
    logger.add("log.log")
    for url in url_list:
        try:
            res = httpx.get(url)
        except :
            with open("error_root_url.txt","a")as f:
                f.write(url + "\n")
                f.close()
            continue
        else:
            web_text = etree.HTML(res.text)
            page_list = web_text.xpath("/html/body/div[2]/div/div/div[4]/div/div//a/@href")
            num = 1
            for i in range(0, len(page_list) - 1):
                page_list[i] = "https://meirentu.cc" + page_list[i]
                try:
                    res1 = httpx.get(page_list[i])
                except:
                    with open("error_2nd_url.txt", "a") as f:
                        f.write(page_list[i] + "\n")
                        f.close()
                    continue
                else:
                    pic_text = etree.HTML(res1.text)
                    pic_title = pic_text.xpath("/html/body/div[2]/div/div/div[1]/h1/text()")[0]
                    pic_list = pic_text.xpath("/html/body/div[2]/div/div/div[3]/div//div/img/@src")

                    if not os.path.exists("pic/xiuren/" + pic_title):
                        os.mkdir("pic/xiuren/" + pic_title)
                    headers = {"referer": url}
                    for pic_url in pic_list:
                        try:
                            pic_content = httpx.get(pic_url, headers=headers)
                        except:
                            with open("error_pic_url.txt", "a") as f:
                                f.write(pic_url + "\n")
                                f.close()
                            continue
                        else:
                            pic_name = pic_title + "_" + str(num) + ".jpg"
                            with open("pic/xiuren/" + pic_title + "/" + pic_name, "wb") as f:
                                f.write(pic_content.content)
                                f.close()
                                logger.info(pic_name)
                            num = num + 1
                            time.sleep(4)


get_pic()