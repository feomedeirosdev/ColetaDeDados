# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# %%

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.residentevildatabase.com/personagens/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}

def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_infos(soup):
    div_page = soup.find("div", class_="td-page-content")
    paragrafo = div_page.find_all('p')[1]
    ems = paragrafo.find_all('em')

    data = {}
    for i in ems:
        # print(i)
        chave, valor, *_ = i.text.split(':')
        data[chave.strip()] = valor.strip()

    return data

def get_aparicoes(soup):
    lis = (soup.find('div', class_='td-page-content')
            .find('h4')
            .find_next()
            .find_all('li'))

    lis = list(lis)
    aparicoes = [i.text for i in lis]
    return aparicoes

def get_personagem(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Não foi possível obter os dados")
        return {}
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data['Aparicoes'] = get_aparicoes(soup)
        return data

def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)

    ancoras = list((soup_personagens.find('div', class_='td-page-content')
                        .find_all('a')))

    links = [i['href'] for i in ancoras]
    return links

# %%
links = get_links()
data = []
for i in tqdm(links):
    # print(i)
    d = get_personagem(i)
    d['link'] = i
    nome = i.strip('/').split('/')[-1].replace('-',' ').title()
    d['Nome'] = nome
    data.append(d)

# %%
# len(data)
df = pd.DataFrame(data) 
df

# %%
df.to_csv('dados_re.csv', index=False, sep=';')

# %%
df.to_parquet('dados_re.parquet', index=False)
df.to_pickle('dados_re.pkl')

# %%
df_new = pd.read_parquet('dados_re.parquet')
df_new

# %%
df_new2 = pd.read_pickle('dados_re.pkl')
df_new2











# cookies = {
#     '_gid': 'GA1.2.645954048.1747134587',
#     '__gads': 'ID=c2debecf20b7435e:T=1747134585:RT=1747137712:S=ALNI_MYUVldVYvpMMVWgbRWcrmrqKqH7Mg',
#     '__gpi': 'UID=0000101f5545df6c:T=1747134585:RT=1747137712:S=ALNI_MajqLgpg2dj6swgswWw4SSHjWppJw',
#     '__eoi': 'ID=d615dc8438eeaf85:T=1747134585:RT=1747137712:S=AA-AfjYzTdv23sb3_d98ED9fiqJB',
#     '_ga_DJLCSW50SC': 'GS2.1.s1747137711$o2$g1$t1747137724$j47$l0$h0',
#     '_ga_D6NF5QC4QT': 'GS2.1.s1747137712$o2$g1$t1747137725$j47$l0$h0',
#     '_ga': 'GA1.2.2027959073.1747134581',
#     'FCNEC': '%5B%5B%22AKsRol9qB_CC2IAmDCq-753ao9Y9GRcb_KwdrbgsFlaKkAAjAXH1UVXPUABj3mxmKPFqonc6CZVMvkboX0lKrBiyCrd0stOSnl7lSYixoQT4cfLGkcwpfFT7mkWFf3_J8tjs7WOASy32pyMqWvZbKVjlgf1AmQoj1Q%3D%3D%22%5D%5D',
# }
# 'cookie': '_gid=GA1.2.645954048.1747134587; __gads=ID=c2debecf20b7435e:T=1747134585:RT=1747137712:S=ALNI_MYUVldVYvpMMVWgbRWcrmrqKqH7Mg; __gpi=UID=0000101f5545df6c:T=1747134585:RT=1747137712:S=ALNI_MajqLgpg2dj6swgswWw4SSHjWppJw; __eoi=ID=d615dc8438eeaf85:T=1747134585:RT=1747137712:S=AA-AfjYzTdv23sb3_d98ED9fiqJB; _ga_DJLCSW50SC=GS2.1.s1747137711$o2$g1$t1747137724$j47$l0$h0; _ga_D6NF5QC4QT=GS2.1.s1747137712$o2$g1$t1747137725$j47$l0$h0; _ga=GA1.2.2027959073.1747134581; FCNEC=%5B%5B%22AKsRol9qB_CC2IAmDCq-753ao9Y9GRcb_KwdrbgsFlaKkAAjAXH1UVXPUABj3mxmKPFqonc6CZVMvkboX0lKrBiyCrd0stOSnl7lSYixoQT4cfLGkcwpfFT7mkWFf3_J8tjs7WOASy32pyMqWvZbKVjlgf1AmQoj1Q%3D%3D%22%5D%5D',
# %%
