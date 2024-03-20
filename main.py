import pandas

from send_request import Scraper
from parse_html import Parser


def main():
    result = []
    url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY%2C+United+States&start="
    scraper = Scraper()
    i = 0
    while True:
        html = scraper.get_html(url+str(i))
        parser = Parser(html)
        if not parser.validate_page():
            break
        parser.extract_html()
        parser.filter_result()
        result.extend(parser.result())
        i += 10

    return result


if __name__ == "__main__":
    result = main()
    df = pandas.DataFrame(result)
    df.to_csv("yelp.csv", index=False)
