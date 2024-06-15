from bs4 import BeautifulSoup
from time import sleep
import requests
import csv

vinyls_csv = open("Vinyls.csv", "w", encoding="utf-8_sig", newline="\n")
write_obj = csv.writer(vinyls_csv)
write_obj.writerow(["Tile/Artist", "Price", "Is_On_Sale", "Vinyl_Cover"])
headers = {
    "User-Agent": "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'"
}
page = 1

while page <= 5:
    url = f"https://vinyl.ge/product-category/vinyl-records/page/{page}"
    response = requests.get(url, headers=headers).text

    soup = BeautifulSoup(response, 'html.parser')
    section = soup.find("ul", class_="products columns-4")
    vinyls = section.find_all("li")

    for vinyl in vinyls:
        vinyl_info = vinyl.find("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
        vinyl_cover = vinyl_info.img["src"]
        vinyl_title = vinyl_info.h2.text
        vinyl_prices = vinyl_info.find("span", class_="price")

        try:
            vinyl_price = vinyl_prices.ins.span.bdi.text
        except AttributeError:
            vinyl_price = vinyl_prices.span.bdi.text

        try:
            s = vinyl_info.find("span", class_="onsale").text
            on_sale = "Yes"
        except AttributeError:
            on_sale = "No"

        write_obj.writerow([vinyl_title, vinyl_price, on_sale, vinyl_cover])

        print(vinyl_title)
        print(vinyl_price)
        print(on_sale)
        print(vinyl_cover)
        print()

    page += 1
    sleep(15)

