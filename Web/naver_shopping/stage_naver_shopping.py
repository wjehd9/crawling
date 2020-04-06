import json  # json 파일을 만들기 위함
from libs.naver_shopping.crawler import crawl
from libs.naver_shopping.parser import parseObject
import pandas as pd
import requests
from datetime import datetime
from libs.naver_shopping.create import createFolder

def doing(keyword, condition, position):
    totalProducts = []
    for pageNo in range(1, 6):
        try:
            pageString = crawl(keyword, pageNo, condition)
            products = parseObject(pageString)
            totalProducts += products

        except:
            print("--Error--")

    file = open(position + "/#products.json", "w+")
    file.write(json.dumps(totalProducts))
    file.close()

    df = pd.read_json(position + "/#products.json")

    now = datetime.now()

    global directory
    global name

    if condition == 1:
        name = "기본"
    if condition == 2:
        name = "낮은 가격순"
    if condition == 3:
        name = "등록일순"
    if condition == 4:
        name = "리뷰 많은순"

    for index, info in enumerate(totalProducts):
        r = requests.get(info['img'])
        directory = position + "/" + keyword + "/{}-{}-{}-{}-{}-{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second) + "/" + name
        createFolder(directory)
        file = open(directory + "/{}# ".format(index) + info['price'] + "원 - " + info['name'].replace("/", ",") + ".png", "wb+")
        file.write(r.content)
        file.close()

    writer = pd.ExcelWriter(directory + "/#" + keyword + "#상품 명단.xlsx")
    df.to_excel(writer, "sheet1")
    writer.save()
