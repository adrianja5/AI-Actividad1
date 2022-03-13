import argparse
import requests
import re
import json

# Constantes

## Yahoo Finance
BASE_URL = 'https://es.finance.yahoo.com/quote/'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

CURRENCIES = {'EUR': '💶',
              'USD': '💵',
              'GBP': '💷',
              'JPY': '💴'}

## Regex
reg_exp_nombre_empresa = '<title>(.*?) \('
reg_exp_divisa = 'Divisa en (.*?)<'
reg_exp_precio_actual = 'data-symbol="{empresa}".*?data-field="regularMarketPrice".*?>(.*?)<'
reg_exp_BPA = '"EPS_RATIO-value".*?>(.*?)<'
reg_exp_rent_div = '"DIVIDEND_AND_YIELD-value".*?>(.*?)<'

## Bot Telegram
BOT_BASE_URL = 'https://api.telegram.org/bot{BOT_TOKEN}/'


# Funciones

def obtener_valores(empresa):
  request = requests.get(BASE_URL + empresa, headers=HEADERS)
  content = request.content.decode('utf-8')
  
  reg_exp_precio_actual_empr = reg_exp_precio_actual.format(empresa=empresa)

  nombre_empresa = re.search(reg_exp_nombre_empresa, content, re.IGNORECASE | re.DOTALL).group(1)
  divisa = re.search(reg_exp_divisa, content, re.DOTALL).group(1)
  precio_actual = re.search(reg_exp_precio_actual_empr, content, re.IGNORECASE | re.DOTALL).group(1)
  BPA = re.search(reg_exp_BPA, content, re.IGNORECASE | re.DOTALL).group(1)
  rent_div = re.search(reg_exp_rent_div, content, re.IGNORECASE | re.DOTALL).group(1)

  return nombre_empresa, divisa, precio_actual, BPA, rent_div

def enviar_mensaje(message, chat_id):
  method = 'sendMessage'
  parameters = {'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True}
  
  requests.get(BOT_BASE_URL + method, parameters)


# Ejecución

if __name__ == '__main__':
  parser = argparse.ArgumentParser('Actividad 1')
  parser.add_argument('--fichero-empresas', type=str, required=True,
                      help='Ruta al fichero de empresas. Formato fichero: empresa1,empresa2,...')
  parser.add_argument('--fichero-ult-precio', type=str, required=True,
                      help='Ruta al fichero donde almacenar el último valor de las empresas.')
  parser.add_argument('--chat-id', type=str, required=True,
                      help='Identificador único o usuario (@channelusername) del canal.')
  parser.add_argument('--bot-token', type=str, required=True,
                      help='Token del bot.')

  opt = parser.parse_args()

  BOT_TOKEN = opt.bot_token
  BOT_BASE_URL = BOT_BASE_URL.format(BOT_TOKEN=BOT_TOKEN)
  CHAT_ID = opt.chat_id
  fichero_empresas_path = opt.fichero_empresas
  fichero_ult_precio_path = opt.fichero_ult_precio

  with open(fichero_empresas_path, 'r') as fich:
    empresas = fich.readline().rstrip().split(',')
  
  with open(fichero_ult_precio_path, 'r+') as fich:
    # Comprobar si es JSON
    try:
      valor_empresas = json.load(fich)
    except ValueError:
      valor_empresas = dict()

  # Eliminar las empresas que no estén en el fichero de empresas
  for key in list(valor_empresas):
    if key not in empresas:
      valor_empresas.pop(key)
  
  # Añadir las nuevas empresas del fichero de empresas
  valor_empresas = {empresa: 0 for empresa in empresas} | valor_empresas

  message = ''

  for empresa in empresas:
    nombre_empresa, divisa, precio_actual, BPA, rent_div = obtener_valores(empresa)

    precio_actual = precio_actual.replace('.','')
    precio_actual = float(precio_actual.replace(',','.'))

    if precio_actual > valor_empresas[empresa]:
      if message != '':
        message += '\n\n'
      valor_empresas[empresa] = precio_actual

      message += (f'<b>{nombre_empresa}</b> — <a href="{BASE_URL + empresa}"><b>{empresa}</b></a>:\n'
                  f'   <u>Divisa</u>: {divisa + (" " + CURRENCIES[divisa] if divisa in CURRENCIES else "")}\n' # Añadir emoji de divisa si está en la lista
                  f'   <u>Precio</u>: {precio_actual}\n'
                  f'   <u>BPA</u>: {BPA}\n'
                  f'   <u>Previsión de rentabilidad y dividendo</u>: {rent_div}')

  if message != '':
    enviar_mensaje(message, CHAT_ID)

  # Salvar nuevos últimos valores
  with open(fichero_ult_precio_path, 'w') as fich:
    json.dump(valor_empresas, fich, indent=4)
