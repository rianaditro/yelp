import pandas

from send_request import Scraper
from parse_html import Parser


def main():
    result = []
    url="https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY%2C+United+States&start="
    scraper = Scraper()
    i = 90
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
    df = pandas.DataFrame(result)
    df.to_excel("yelp.xlsx",index=False)