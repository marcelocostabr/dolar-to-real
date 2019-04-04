import json
import requests
from datetime import date
from datetime import datetime, timedelta

# Dado um número de versão MAJOR.MINOR.PATCH, incremente a:
# 1. versão Maior(MAJOR): uma realmente nova versão,
# 2. versão Menor(MINOR): quando adicionar funcionalidades mantendo compatibilidade, e
# 3. versão de Correção(PATCH): quando corrigir falhas mantendo compatibilidade.

version = '1.0.1'
dolar   = eval(input('Digite o total em $USD: '))
today = date.today()

# Recupera a cotação do último *dia útil* antes da consulta
# Assumindo que segunda é 1 e domingo é 7
# Se 1 reduz 3 dias | Se de 2 a 6 reduz 1 | Se 7 reduz 2

weekday = today.isoweekday()

if (weekday == 1):
    now = datetime.now()
    workday = now - timedelta(days=3)
    day = workday.strftime('%m-%d-%Y')

if (weekday > 1) and (weekday < 7):
    now = datetime.now()
    workday = now - timedelta(days=1)
    day = workday.strftime('%m-%d-%Y')

if (weekday == 7):
    now = datetime.now()
    workday = now - timedelta(days=2)
    day = workday.strftime('%m-%d-%Y')

# Cria a consulta a API do Banco Central
url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='" + day + "'&$top=1&$format=json&$select=cotacaoVenda"
r = requests.get(url)

if r.status_code == 200:
    exchange_rate = json.loads(r.content)
    reais = exchange_rate['value'][0]['cotacaoVenda']
    reais_rounded = round(reais, 2)
    reais_srt = str(reais_rounded)

# conversão direta
exchange = (dolar * reais)

# Taxa padrão de Spread aplicada pelo Nubank e pelo Banco Neon
spread = (exchange * 0.04)

# Taxa do IOF - data base 04-04-2019
iof = ((exchange + spread) * 0.0638)

# Valor Total com IOF e Spread
total = exchange + spread + iof
total_rounded = round(total, 2)
amount = str(total_rounded)

print('')
print('V ' + version)
print('=========================')
print('Cotação do dólar R$: ' + reais_srt)
print('=========================')
print('Data contábil: ' + day)
print('=========================')
print('Total R$ ' + amount)
print('=========================')
