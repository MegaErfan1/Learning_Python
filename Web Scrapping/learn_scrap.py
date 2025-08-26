import requests
from bs4 import BeautifulSoup


def scrape_book_info(url, target_class):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    page_title = soup.title.get_text(strip=True) if soup.title else None
    elements = soup.find_all(class_=target_class)
    texts = [el.get_text(strip=True) for el in elements]
    img_tag = soup.select_one("div#product_gallery img")
    img_src = img_tag["src"] if img_tag else None
    if img_src and img_src.startswith("../"):
        img_src = requests.compat.urljoin(url, img_src)
    return page_title, texts, img_src


if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    target_class = "product_main"
    title, items, img_link = scrape_book_info(url, target_class)

    print("page title: ", title)
    print("\ntexts from class ", target_class, ":", items)
    print("\nImgage URL :", img_link)
