import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def scrape_ponisha_python_projects():
    # مسیر پوشه data (اگر وجود نداشت بساز)
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, "ponisha_python_projects.xlsx")

    # تنظیمات مرورگر (headless یعنی بدون باز کردن پنجره)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # مسیر chromedriver (باید نصب باشه و توی همین مسیر باشه یا توی PATH)
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # آدرس جستجوی پروژه‌های Python
    url = "https://ponisha.ir/search/projects?q=python"
    driver.get(url)
    time.sleep(3)

    # اسکرول برای لود شدن پروژه‌های بیشتر
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # گرفتن HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # پیدا کردن کارت‌های پروژه
    projects = soup.find_all("div", class_="project-card")  # 👈 ممکنه نیاز باشه آپدیت بشه

    data = []
    for i, project in enumerate(projects, 1):
        try:
            name = project.find("h2").get_text(strip=True)
        except:
            name = ""

        try:
            description = project.find("div", class_="description").get_text(strip=True)
        except:
            description = ""

        try:
            price = project.find("div", class_="budget").get_text(strip=True)
        except:
            price = ""

        try:
            time_left = project.find("div", class_="time-left").get_text(strip=True)
        except:
            time_left = ""

        try:
            skills = ", ".join([s.get_text(strip=True) for s in project.find_all("a", class_="skill")])
        except:
            skills = ""

        data.append({
            "شماره": i,
            "نام پروژه": name,
            "توضیحات پروژه": description,
            "قیمت (تومان)": price,
            "زمان باقی‌مانده": time_left,
            "مهارت‌های مورد نیاز": skills
        })

    # ذخیره در اکسل
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"✅ {len(data)} پروژه ذخیره شد → {output_file}")


if __name__ == "__main__":
    scrape_ponisha_python_projects()
