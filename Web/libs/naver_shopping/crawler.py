import requests
from urllib import parse

def crawl(keyword, pageNo, condition):
    url = urlDefine(keyword, pageNo, condition)
    data = requests.get(url)
    print(data.status_code, url)
    return data.content

def urlDefine(keyword, pageNo, condition):
    if condition == 1:
        address = "https://search.shopping.naver.com/search/all.nhn?query={}&pagingIndex={}&frm=NVSHATC&sort=rel".format(parse.quote(keyword), pageNo)
        return address
    elif condition == 2:
        address = "https://search.shopping.naver.com/search/all.nhn?query={}&pagingIndex={}&frm=NVSHATC&sort=price_asc".format(parse.quote(keyword), pageNo)
        return address
    elif condition == 3:
        address = "https://search.shopping.naver.com/search/all.nhn?query={}&pagingIndex={}&frm=NVSHATC&sort=date".format(parse.quote(keyword), pageNo)
        return address
    else:
        address = "https://search.shopping.naver.com/search/all.nhn?query={}&pagingIndex={}&frm=NVSHATC&sort=review".format(parse.quote(keyword), pageNo)
        return address