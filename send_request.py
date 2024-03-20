import httpx


class Scraper:
    def __init__(self):
        self.client = httpx.Client()

    def get_html(self, url):
        resp = self.client.get(url)
        if resp.status_code == 200:
            print(f"Got html from {url}")
            return resp.text
        else:
            print(f"{resp.status_code}: Error getting html from {url}")
