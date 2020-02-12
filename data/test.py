import json
import time
import requests
import sys
import re
import urllib
from flask import Flask, render_template, jsonify
#from googletrans import Translator
import numpy as np

from pyecharts.charts import Map,Kline,Line,Bar,WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType
f = open("2020-02-05.json", encoding='utf-8')
data= json.load(f)




def province():
    f = open("2020-02-05.json", encoding='utf-8')
    data = json.load(f)
    country = []
    confirm = []
    dead = []
    heal = []
    res = {
        'country': '',
        'confirm': '',
        'dead': '',
        'heal': '',
    }
    chinaren = data['areaTree'][0]
    for i in chinaren['children']:
        country.append(i['name'])
        confirm.append(i['total']['confirm'])
        dead.append(i['total']['dead'])
        heal.append(i['total']['heal'])
    res['country'] = country
    res['confirm'] = confirm
    res['dead'] = dead
    res['heal'] = heal
    heal_line = []
    dead_line =[]
    for i in range(len(confirm)):
        fenmu = int(confirm[i])
        fenzi = int(dead[i])
        fenzi2 = int(heal[i])
        heals = fenzi2/fenmu

        Deads = fenzi/fenmu
        heal_line.append(heals)
        dead_line.append(Deads)


    arr = np.array(heal_line)
    arr1 = np.array(dead_line)

    tmp_heal = np.argsort(-arr)[0:10]  # 逆序输出

    tmp_dead = np.argsort(-arr1)[0:10]


    country_dead =[]
    deads =[]


    country_heal=[]
    heals =[]

    for i in range(10):
        itr = tmp_heal[i]
        its = tmp_dead[i]
        country_heal.append(country[itr])
        country_dead.append(country[its])
        heals.append(heal_line[itr])
        deads.append(dead_line[its])


    print(country_heal)
    print(heals)
    print(country_dead)
    print(deads)











a=province()
