import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime
from bs4 import BeautifulSoup
import requests
def save(url,path):
    r=requests.get(url)
    with open(path,"w") as f:
        f.write(r.text)
    f.close()
path="times.html"
url = "https://books.toscrape.com"
#call this method to save the html structure of the page you want to scrape
list=[]
with open(path,"r") as f:
    soup = BeautifulSoup(f,"html.parser")
    for h in soup.findAll('li'):
        a = h.find('a')
        try:
            if 'href' in a.attrs:
                url = a.get('href')
                list.append(url.replace("catalogue/","https://books.toscrape.com/catalogue/"))
        except:
            pass
list.remove("index.html")
#not a functioning link
client = MongoClient("mongodb+srv://username:password@cluster0.dexxeof.mongodb.net/")
#replace username and pasword with your personal credentials
db = client.scrapy
def insertToDb(page,data):
    collection=db[page]
    doc={"Date": datetime.datetime.now(tz=datetime.timezone.utc),
         "Title":data[0],
         "Rating":data[1],
         "Image Url":data[2],
         "Price":data[3],
         "Instock":data[4],}
    inserted=collection.insert_one(doc)
    return inserted.inserted_id

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    def start_requests(self):
        for url in list:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        page= response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        
        #Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        cards=response.css(".product_pod")
        for card in cards:
            bookdetail=[]
            title=card.css("h3>a::text").get()
            bookdetail.append(title)
            star=card.css(".star-rating").attrib["class"].split(" ")[-1]
            bookdetail.append(star)
            img= card.css(".image_container img")
            bookdetail.append(img.attrib["src"].replace("../../../../media","https://books.toscrape.com/media"))
            # to make the links functional
            price=card.css(".price_color::text").get()
            bookdetail.append(price)
            available=card.css(".availability")
            if len(available.css(".icon-ok"))>0:
                inStock=True
            else:
                inStock=False
            bookdetail.append(inStock)
            insertToDb(page,bookdetail)
#title,rating,image,price,Instock ~~ oreder of insertion        