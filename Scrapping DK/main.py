import requests
import pandas as pd
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
}


def fetch_products():
    urls = [
        "https://api.digikala.com/v1/incredible-offers/",
        "https://api.digikala.com/v1/incredible-offers/products/?page=1&q="
    ]

    all_products = []

    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"❌ خطا در دریافت {url}: {e}")
            continue

        product_lists = []

        running_out_products = data.get("data", {}).get(
            "running_out_incredible_products", {}).get("products", [])
        if running_out_products:
            product_lists.append(running_out_products)

        products_data = data.get("data", {}).get("products", [])
        if products_data:
            product_lists.append(products_data)

        for plist in product_lists:
            for p in plist:
                try:
                    name = p.get("test_title_fa") or p.get(
                        "title_fa")

                    uri = p.get("url", {}).get("uri") or p.get(
                        "default_variant", {}).get("url", {}).get("uri")
                    link = f"https://www.digikala.com{uri}" if uri else "لینک ندارد"

                    price_info = p.get("default_variant", {}).get("price", {})
                    price = price_info.get("selling_price", 0)
                    discount = price_info.get("discount_percent", 0)

                    all_products.append({
                        "نام محصول": name,
                        "قیمت": price,
                        "تخفیف (%)": discount,
                        "لینک": link
                    })
                except:
                    continue

    return all_products


if __name__ == "__main__":
    products = fetch_products()

    if products:
        df = pd.DataFrame(products).drop_duplicates(subset=["لینک"])

        df = df.sort_values(by="تخفیف (%)", ascending=False)

        today = datetime.today().strftime("%Y-%m-%d")
        filename = f"digikala_final_{today}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')

        print(f"✅ تعداد محصول پیدا شده: {len(df)}")
    else:
        print("⚠️ هیچ محصولی پیدا نشد")
