from bs4 import BeautifulSoup

import httpx,re


class Scraper:
    def __init__(self):
        self.client = httpx.Client()
    
    def get_html(self,url):
        resp = self.client.get(url)
        if resp.status_code == 200:
            return resp.text
        else:
            print(f"{resp.status_code}: Error getting html from {url}")

class Parser:
    def __init__(self,html):
        self.soup = BeautifulSoup(html,"html.parser")
    
    def get_name(self):
        names = self.soup.find_all("a", "css-19v1rkv")
        name = [item.text.strip() for item in names]
        return name
    
    def extract_all(self,tag,class_):
        try:
            text = self.soup.find_all(tag,class_)
            strip_text = [item.text.strip() for item in text]
            return strip_text
        except AttributeError:
            print(f"Tag {tag} and class {class_} not found")
            return "Unknown"
    
def filter_list(ls:list):
    remove = ["Yelp","Yelp for Business","Driving (5 mi.)"]
    pattern = r'(\d+(\.\d+)?k?) reviews'
    
    ls = [item for item in ls if item not in remove]
    if any("reviews" in item for item in ls):
        reviewsCount = [re.search(pattern, item).group().replace(".","").replace("k","000").replace("reviews","") for item in ls if re.search(pattern, item)]
        return reviewsCount
    elif any("$$" in item for item in ls):
        keywords = [re.sub(r'(?<=\w)(?=[A-Z])', ', ', text) for text in ls]
        keywords = [re.sub(r'\$\$.+', '', text) for text in keywords]
        return keywords
    elif any("\xa0more" in item for item in ls):
        reviews = [item.replace("\xa0more","") for item in ls]
        return reviews
    else:
        return ls

def combine(name,rating,reviewCount,keyword,reviews):
    result = []
    for i in range(10):
        res = {"name":name[i],
               "rating":rating[i],
               "reviewCount":reviewCount[i],
               "keyword":keyword[i],
               "reviews":reviews[i]}
        result.append(res)
    return result  
        


if __name__=="__main__":
    url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY%2C+United+States&start=0"
    with open('yelp.html','r') as file:
        html_file = file.read()
    parser = Parser(html_file)
    name = parser.extract_all("a","css-19v1rkv")
    rating = parser.extract_all("span","css-gutk1c")
    reviewCount = parser.extract_all("span","css-chan6m")
    keyword = parser.extract_all("div","css-1kiyre6")
    reviews = parser.extract_all("p","css-16lklrv")
    print(combine(name,rating,reviewCount,keyword,reviews))



    

