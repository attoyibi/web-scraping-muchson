import os
import requests
from bs4 import BeautifulSoup
import openai

# URL yang ingin di-scrape
url = "http://olympus.realpython.org/profiles/aphrodite"
# url = "https://www.kompas.com/"

# Simulasi User-Agent agar tidak terblokir
headers = {"User-Agent": "Mozilla/5.0"}

# Ambil halaman
response = requests.get(url, headers=headers)

print(f"HTTP Status Code: {response.status_code}")

if response.status_code == 200:
    # Cetak HTML mentah dari halaman
    print(response.text)
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Cari semua elemen yang diinginkan, misalnya nama dan fakta
    name = soup.find("h2").get_text(strip=True)
    facts = [fact.get_text(strip=True) for fact in soup.find_all("li")]
    center = soup.find("center").get_text(strip=True)
    print(f"Name: {name}")
    print(f"Name: {center}")
    print("Facts:")
    for fact in facts:
        print(f"- {fact}")

    # Gabungkan nama dan fakta menjadi satu string
    data = f"Name: {name}\nFacts:\n" + "\n".join(f"- {fact}" for fact in facts)

    # Gunakan variabel lingkungan untuk API Key
    api_key = ""  # Pastikan key diset dalam environment

    if not api_key:
        print("Error: API Key tidak ditemukan! Pastikan variabel lingkungan OPENAI_API_KEY sudah diatur.")
    else:
        # Inisialisasi OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # Gunakan OpenAI API dengan model terbaru
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"berikan aku kesimpulan berita kompat terkait apa ? :\n{response.text}"}],
            max_tokens=1000
        )

        print("Processed Data:")
        print(response.choices[0].message.content.strip())
else:
    print("Gagal mengambil halaman. Coba lagi nanti.")
