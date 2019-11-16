import logging
import os
from requests_html import HTMLSession
from requests import post
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

dict_products = {}


def start(bot, update):
    update.effective_message.reply_text("Bienvenido al robot de la tienda Brahma!\n"
                                        "Soy util para que sepas los informacion sobre la web.\n\n"
                                        "Mis comandos disponibles son:\n"
                                        "/lista - Lista los precios de la web\n"
                                        "/foto id - Muestra la foto del id seleccionado\n"
                                        "/promedio - Muestra el precio promedio de los productos\n")


def list_products(update, context):
    session = HTMLSession()
    if len(dict_products) != 30:
        page = session.get('https://www.brahma.co/es/tienda/hombre')
        if page.status_code == 200:
            all_items = page.html.find('a.product')
            for id, item in enumerate(all_items):
                dict_products[id] = {
                    'nombre': item.find('.name', first=True).text,
                    'precio': item.find('.price', first=True).text,
                    'img_url': 'https://www.brahma.co{imagen}'.format(
                        imagen=item.find('img', first=True).attrs.get('src'))
                }
    list_response = ''
    for id, product in dict_products.items():
        list_response += '{id}. Nombre: {nombre}\n' \
                         'Precio: {precio}\n\n'.format(id=id, **product)
    context.bot.send_message(chat_id=update.effective_chat.id, text=list_response)


def echo(bot, update):
    """
    session = HTMLSession()
    page = session.get('https://www.brahma.co/es/productos/chq0035-chaqueta')
    if page.status_code == 200:
        discounted_price = page.html.find('.discounted', first=True).text
        original_price = page.html.find('.original', first=True).text
        discount = page.html.find('.price-discount-percent', first=True).text
        print(discounted_price, original_price, discount)
        if '10' in discount:
            msg = 'Todavía tiene el 10% 😢\nTe amo ❤'
        else:
            msg = 'Ya cambió el descuento. :D'
    """
    message = update.effective_message.text
    if 'AILOVIU' in str(message).upper():
        msg = 'Haz descifrado la clave:\n https://lmldt.ga/'
    else:
        msg = 'Si la carta deseas conocer el nombre clave deberás saber.'
    update.effective_message.reply_text('{msg}'.format(msg=msg))


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = "747824031:AAEON4Di-_ScFNU6D4u9rkA3JZwICkbVevE"
    NAME = "chaqueta-linda"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler('list', list_products))
    dp.add_error_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
