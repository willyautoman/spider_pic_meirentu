from time import sleep

import httpx
from lxml import etree

proxy={
    'http://': 'http://127.0.0.1:7890'
}

for num in range(1, 31):
    res = httpx.get("https://meirentu.cc/group/xiaoyu-" + str(num) + ".html")
    # print(res.status_code)
    etree_doc = etree.HTML(res.text)

    pic_list = etree_doc.xpath("/html/body/div[2]/div[2]/div/ul/li//a/@href")
    with open("huayu.txt", "a") as f:
        for i in range(0, len(pic_list) - 1):
            pic_list[i] = "https://meirentu.cc" + pic_list[i]
            f.write(pic_list[i] + "\n")
        f.close()
    sleep(4)