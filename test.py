from requests_html import HTMLSession

session = HTMLSession()
page = session.get('https://www.brahma.co/es/tienda/hombre')
# page.html.render()
if page.status_code == 200:
    all_items = page.html.find('.item-info')
    for item in all_items:
        print(item.find('.name', first=True).text)
        print(item.find('.price', first=True).text)

    print(all_items)
    price_founded = page.html.find('.price', first=True).text
    # discount = page.html.find('.price-discount-percent', first=True).text
    print(price_founded)
