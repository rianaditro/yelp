from bs4 import BeautifulSoup

import httpx,re,pandas


class Scraper:
    def __init__(self):
        self.client = httpx.Client()
    
    def get_html(self,url):
        resp = self.client.get(url)
        if resp.status_code == 200:
            print(f"Got html from {url}")
            return resp.text
        else:
            print(f"{resp.status_code}: Error getting html from {url}")

class Parser:
    def __init__(self,html):
        self.soup = BeautifulSoup(html,"html.parser")
        self.names = None
        self.ratings = None
        self.reviewCounts = None
        self.keywords = None
    
    def validate_page(self):
        if self.soup.find("h3","css-lp6ju1"):
            print("Page not found. Scraping finished")
            return False
        else:
            return True

    def find_tag(self,tag,class_):
        text = self.soup.find_all(tag,class_)
        strip_text = [item.text.strip() for item in text]
        if strip_text == []:
            print(f"No tag '{tag}' found")
        return strip_text
        
    def extract_html(self):
        self.names = self.find_tag("a","css-19v1rkv")
        self.ratings = self.find_tag("span","css-gutk1c")
        self.reviewCounts = self.find_tag("span","css-chan6m")
        self.keywords = self.find_tag("div","css-1kiyre6")

        self.soup = None

    def filter_result(self):
        # remove unwanted text from names and ratings
        remove = ["Yelp","Yelp for Business","Driving (5 mi.)","Bird's-eye View"]
        self.names = [item for item in self.names if item not in remove]
        self.ratings = [float(item) for item in self.ratings if item not in remove]

        # remove unwanted text from reviewCounts
        pattern = r'(\d+(\.\d+)?k?) reviews'
        self.reviewCounts = [re.search(pattern, item).group().replace(".","").replace("k","000").replace("reviews","") for item in self.reviewCounts if re.search(pattern, item)]
        self.reviewCounts = [int(item) for item in self.reviewCounts]

        # remove unwanted text from keywords
        self.keywords = [item.split('$')[0].replace("DUMBO","") for item in self.keywords]
        # separate each keyword by comma
        self.keywords = [re.sub(r'(?<=\w)(?=[A-Z])', ', ', text) for text in self.keywords]

    def result(self):
        result = []
        for i in range(len(self.names)):
            res = {"name":self.names[i],
                   "rating":self.ratings[i],
                   "reviewCount":self.reviewCounts[i],
                   "keyword":self.keywords[i]}
            result.append(res)
            print(res)
        return result    

def main():
    result = []
    url="https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY%2C+United+States&start="
    scraper = Scraper()
    i = 230
    while True:
        html = scraper.get_html(url+str(i))
        parser = Parser(html)
        if parser.validate_page() == False:
            break
        parser.extract_html()
        parser.filter_result()
        result.extend(parser.result())
        i = i+10
            
    return result

if __name__=="__main__":
    result = main()
    print(result)
    # df = pandas.DataFrame(result)
    # df.to_excel("yelp.xlsx",index=False)

