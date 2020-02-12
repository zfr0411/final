import json
import os
import requests,datetime

def get_data():
    today = datetime.date.today()
    data_json=str(today)+'.json'
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r = json.loads(requests.get(url).text)
    with open(os.path.join('data',data_json),'w',encoding='utf-8') as f:
        f.write(r['data'])

if __name__ == "__main__":
    get_data()