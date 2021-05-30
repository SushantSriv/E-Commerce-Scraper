# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pickle
from itertools import cycle
import time


proxies = {
       'http://162.144.220.192:80',
       'http://167.215.240.121:5137',
       'http://159.203.91.6:8080',
       'http://157.230.232.130:80',
       
       
        }
proxy_pool = cycle(proxies)
class BookDetails():
    
    def _init_(self):
        self.title = ""
        self.link = ""


def get_url_list():

    list =[]
    for page_number in range(1, 10):		
        page_url = 'https://www.flipkart.com/search?q=top+books+in+2018&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&sort=relevance&page={0}'.format(page_number)
       
        list.append(page_url)
        

    return list
    
pages_list = get_url_list()
    
def GetBooks(pages_list):
    count = 0
    books = []


    for url in pages_list:
        for i in range(1,11):
            
            proxy = next(proxy_pool)
            print("Request #%d"%i)
            try:
                    count = count + 1
                    
                   
                    
                    headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
                    getPage = requests.get(url,proxies={"http": proxy, "https": proxy}, headers=headers)
                    BestBoooksPage = BeautifulSoup(getPage.text, 'html.parser')
                    BooksList = BestBoooksPage.find_all("a",class_="_2cLu-l")
                    
                   
                    for bookList in BooksList:
                        obj  = BookDetails()
                        obj.title = bookList['title']
                        obj.link = "https://www.flipkart.com"+bookList['href']
                        
                        books.append(obj)
                    time.sleep(1)
            except:
                        print("Skipping. Connnection error")

        
    return books
        

book_details = GetBooks(pages_list)
print(len(book_details))


def details(book_details):
    books_details = {
        "data": []
    }
    count = 0
    for book in book_details:
        time.sleep(1)
        print("\n")
        count = count + 1
        print("Book Number "+str(count))

        headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        url = book.link
        page = requests.get(url, headers=headers)
        Page = BeautifulSoup(page.text, 'html.parser')
        try:
            author_name = Page.find("a",class_="_3la3Fn _1zZOAc oZoRPi").text
        except:
                pass
        try:
            Highlights = Page.find("div",class_="g2dDAR")
            list = Highlights.find_all("li",class_="_2-riNZ")
            highlights_list = []
            for item in list:
                highlights_list.append(item.text)
                
        except:
            pass
        try:
            rating = Page.find("div",class_="_1i0wk8").text
        except:
            pass
        try:  
            reviews_data = Page.find_all("div",class_="qwjRop")
            book_reviews=[]
            for review in reviews_data:
                r = review.find("div",class_="").text
                r_edited = r.split("READ MORE")[0]
                book_reviews.append(r_edited)
            print("Book Review")
        except:
            pass
        details = {
                    "author" : author_name,
                    "highlights" : highlights_list,
                    "rating" : rating,
                    "reviews" : book_reviews,    
                }
        books_details['data'].append(details)
        print(books_details)
        
        print("\n")
    
    print(books_details)
    time.sleep(1)
    with open('book_details_pickle.pkl', 'wb') as f:
        pickle.dump(books_details,f,protocol=pickle.HIGHEST_PROTOCOL)  
details(book_details)
