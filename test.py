from requests_html import HTMLSession

session = HTMLSession()
page = session.get('https://www.brahma.co/es/tienda/hombre')
# page.html.render()
dict_products = {}
if page.status_code == 200:
    all_items = page.html.find('a.product')
    for id, item in enumerate(all_items):
        dict_products[id] = {
            'nombre': item.find('.name', first=True).text,
            'precio': item.find('.price', first=True).text,
            'img_url': 'https://www.brahma.co{imagen}'.format(imagen=item.find('img', first=True).attrs.get('src'))
        }

list_response = ''
for id, product in dict_products.items():
    list_response += '{id}. Nombre: {nombre}\n' \
                     'Precio: {precio}\n\n'.format(id=id, **product)
print(list_response)
# html.ng-scope body#ProductsList div.content.lang-es main.products-controller.index div.products div.col a.product.ng-isolate-scope
