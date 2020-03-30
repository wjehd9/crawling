from bs4 import BeautifulSoup

def getProducInfo(li):
    img_area = li.find("div", {"class": "img_area"})
    img = img_area.find("img")
    imgData = img['data-original']

    info = li.find("div", {"class": "info"})
    tit = info.find("div", {"class": "tit"})
    link = tit.find("a", {"class": "link"})
    title = link['title']
    href = link['href']

    price = info.find("span", {"class": "price"})
    em = price.find("em")
    if em is None:
        return {"name": title, "price": price.text, "priceDate": price.text, "img": imgData, "link": href}
    number = em.find("span", {"class": "num"})
    priceDate = number['data-reload-date']

    return {"name": title, "price": number.text.replace(",", ""), "priceDate": priceDate, "img": imgData, "link": href}

def parseObject(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    ul = bsObj.find("ul", {"class": "goods_list"})
    lis = ul.findAll("li", {"class": "_itemSection"})

    global relation
    relation = []

    co_relation = bsObj.find("div", {"class": "co_relation"})
    if co_relation is not None:
        co_relation_srh = co_relation.find("div", {"class": "co_relation_srh"})
        co_ul = co_relation_srh.find("ul")
        co_li = co_ul.findAll("li")

        findRelation(co_li)

    products = []
    for li in lis:
        product = getProducInfo(li)
        print(product)
        products.append(product)

    return products

def findRelation(arr):
    for li in arr:
        a_rel = li.find("a")
        save_rel = a_rel.text.replace("\n","")
        save_rel = save_rel.replace("\t", "")
        relation.append(save_rel)