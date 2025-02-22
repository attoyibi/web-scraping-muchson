from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

# Konfigurasi Chrome headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inisialisasi WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL Tribunnews
url = "https://www.tribunnews.com/"
driver.get(url)

# Tunggu agar halaman termuat sepenuhnya
time.sleep(5)

# Parsing halaman dengan BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Mengambil artikel utama
articles = soup.find_all("li", class_="p1520 art-list pos_rel")
article_list = []

for article in articles:
    title_tag = article.find("a", class_="f20 ln24 fbo txt-oev-2")
    img_tag = article.find("img")
    
    if title_tag:
        title = title_tag.get_text(strip=True)
        link = title_tag["href"]
        full_link = f"https://www.tribunnews.com{link}" if link.startswith("/") else link
        image = img_tag["src"] if img_tag else "No Image"
        
        article_list.append({
            "title": title,
            "link": full_link,
            "image": image
        })

# Mengambil highlight
highlights = soup.find_all("div", class_="highlite")
highlight_list = []

for highlight in highlights:
    hl_contents = highlight.find_all("div", class_="hl_contents")
    for hl in hl_contents:
        link_tag = hl.find("a")
        img_tag = hl.find("img")
        title_tag = hl.find("div", class_="hltitle")
        topic_tag = hl.find("div", class_="hltopic")
        
        if link_tag and title_tag:
            title = title_tag.get_text(strip=True)
            link = link_tag["href"]
            image = img_tag["src"] if img_tag else "No Image"
            topic = topic_tag.get_text(strip=True) if topic_tag else "No Topic"
            
            highlight_list.append({
                "title": title,
                "topic": topic,
                "link": link,
                "image": image
            })

# Menyimpan hasil ke CSV
csv_filename = "tribunnews_scraped_data.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Topic", "Link", "Image"])
    
    for news in highlight_list:
        writer.writerow([news["title"], news["topic"], news["link"], news["image"]])
    
    for news in article_list:
        writer.writerow([news["title"], "", news["link"], news["image"]])

print(f"Data telah disimpan dalam {csv_filename}")

# Tutup browser
driver.quit()
