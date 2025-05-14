# %%
import requests
import pandas as pd
import datetime
import json
import os

# %%
def get_response(**kwargs):
  url = 'https://www.tabnews.com.br/api/v1/contents/'
  # rafael/como-eram-as-ides-com-interface-baseada-em-texto-de-1970-aos-dias-atuais
  resp = requests.get(url, params=kwargs)
  return resp

def save_data(data, option='json'):
  now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
  if option == 'json':
    path = 'datas/contents/json'
    os.makedirs(path, exist_ok=True)
    with open(f'../datas/contents/json/{now}.json', 'w') as open_file:
      json.dump(data, open_file, indent=4)
  elif option == 'dataframe':
    df = pd.DataFRame(data)
    path = 'datas/contents/parquet'
    os.makedirs(path, exist_ok=True)
    df.to_parquet(f'../datas/contents/parquet/{now}.parquet', index=False)

# %%
resp = get_response(page=1, per_page=100, strategy='new')
if resp.status_code == 200:
  print("Sucesso!")
  data = resp.json()
  save_data(data)
else:
  print('Deu ruim!')
# %%
