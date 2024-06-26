import re

from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.names = None
        self.ratings = None
        self.reviewCounts = None
        self.keywords = None

    def validate_page(self):
        if self.soup.find("h3", "css-lp6ju1"):
            print("Page not found. Scraping finished")
            return False
        else:
            return True

    def find_tag(self, tag, class_):
        text = self.soup.find_all(tag, class_)
        strip_text = [item.text.strip() for item in text]
        if strip_text == []:
            print(f"No tag '{tag}' found")
        return strip_text

    def extract_html(self):
        self.names = self.find_tag("a", "css-19v1rkv")
        self.ratings = self.find_tag("span", "css-gutk1c")
        self.reviewCounts = self.find_tag("span", "css-chan6m")
        self.keywords = self.find_tag("div", "css-1kiyre6")

    def filter_result(self):
        # remove unwanted text from names and ratings
        remove = ["Yelp", "Yelp for Business", "Driving (5 mi.)", "Bird's-eye View"]
        self.names = [item for item in self.names if item not in remove]
        self.ratings = [float(item) for item in self.ratings if item not in remove]

        # remove unwanted text from reviewCounts
        def clean_data(ls: list):
            pattern = r'\d+(\.\d+)?k?'
            new_ls = []
            for item in ls:
                if re.search(pattern, item):
                    item = re.search(pattern, item).group()
                    if "k" in item:
                        item = item.replace(".", "").replace("k", "00")
                    new_ls.append(float(item))
            return new_ls
        self.reviewCounts = clean_data(self.reviewCounts)

        # remove unwanted text from keywords
        self.keywords = [item.split('$')[0].replace("DUMBO", "") for item in self.keywords]
        # separate each keyword by comma
        self.keywords = [re.sub(r'(?<=\w)(?=[A-Z])', ',', text) for text in self.keywords]

    def result(self):
        result = []
        for i in range(len(self.names)):
            res = {"name": self.names[i],
                   "rating": self.ratings[i],
                   "reviewCount": self.reviewCounts[i],
                   "keyword": self.keywords[i]}
            result.append(res)
        return result


if __name__ == "__main__":
    with open("yelp.html", "r") as f:
        html = f.read()
    parser = Parser(html)
    parser.extract_html()
    parser.filter_result()
    print(parser.result())
