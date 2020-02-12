import json
import time
import requests
import re
import urllib
import numpy as np
from flask import Flask, render_template, jsonify
#from googletrans import Translator

from pyecharts.charts import Map,Line,Bar,WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType

app = Flask(__name__)
#字典，受限于谷歌调用限制
cn_to_en = {'安哥拉': 'Angola', '阿富汗': 'Afghanistan', '阿尔巴尼亚': 'Albania', '阿尔及利亚': 'Algeria', '安道尔共和国': 'Andorra', '安圭拉岛': 'Anguilla', '安提瓜和巴布达': 'Antigua and Barbuda',
             '阿根廷': 'Argentina', '亚美尼亚': 'Armenia', '阿森松': 'Ascension', '澳大利亚': 'Australia', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan', '巴哈马': 'Bahamas', '巴林': 'Bahrain', 
             '孟加拉国': 'Bangladesh', '巴巴多斯': 'Barbados', '白俄罗斯': 'Belarus', '比利时': 'Belgium', '伯利兹': 'Belize', '贝宁': 'Benin', '百慕大群岛': 'Bermuda Is', '玻利维亚': 'Bolivia', 
             '博茨瓦纳': 'Botswana', '巴西': 'Brazil', '文莱': 'Brunei', '保加利亚': 'Bulgaria', '布基纳法索': 'Burkina Faso', '缅甸': 'Burma', '布隆迪': 'Burundi', '喀麦隆': 'Cameroon', 
             '加拿大': 'Canada', '开曼群岛': 'Cayman Is', '中非共和国': 'Central African Republic', '乍得': 'Chad', '智利': 'Chile', '中国': 'China', '哥伦比亚': 'Colombia', '刚果': 'Congo', 
             '库克群岛': 'Cook Is', '哥斯达黎加': 'Costa Rica', '古巴': 'Cuba', '塞浦路斯': 'Cyprus', '捷克': 'Czech Republic', '丹麦': 'Denmark', '吉布提': 'Djibouti', '多米尼加共和国': 'Dominica Rep', 
             '厄瓜多尔': 'Ecuador', '埃及': 'Egypt', '萨尔瓦多': 'EI Salvador', '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia', '斐济': 'Fiji', '芬兰': 'Finland', '法国': 'France', '法属圭亚那': 'French Guiana', 
             '法属玻利尼西亚': 'French Polynesia', '加蓬': 'Gabon', '冈比亚': 'Gambia', '格鲁吉亚': 'Georgia', '德国': 'Germany', '加纳': 'Ghana', '直布罗陀': 'Gibraltar', '希腊': 'Greece', '格林纳达': 'Grenada', 
             '关岛': 'Guam', '危地马拉': 'Guatemala', '几内亚': 'Guinea', '圭亚那': 'Guyana', '海地': 'Haiti', '洪都拉斯': 'Honduras', '香港': 'Hongkong', '匈牙利': 'Hungary', '冰岛': 'Iceland', '印度': 'India', 
             '印度尼西亚': 'Indonesia', '伊朗': 'Iran', '伊拉克': 'Iraq', '爱尔兰':'Ireland', '以色列': 'Israel', '意大利': 'Italy', '科特迪瓦': 'Ivory Coast', '牙买加': 'Jamaica', '日本': 'Japan', '约旦': 'Jordan', 
             '柬埔寨': 'Kampuchea (Cambodia )', '哈萨克斯坦': 'Kazakstan', '肯尼亚': 'Kenya', '韩国': 'Korea', '科威特': 'Kuwait', '吉尔吉斯坦': 'Kyrgyzstan', '老挝': 'Laos', '拉脱维亚': 'Latvia', '黎巴嫩': 'Lebanon', 
             '莱索托': 'Lesotho', '利比里亚': 'Liberia', '利比亚': 'Libya', '列支敦士登': 'Liechtenstein', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '澳门': 'Macao', '马达加斯加': 'Madagascar', 
             '马拉维': 'Malawi', '马来西亚': 'Malaysia', '马尔代夫': 'Maldives', '马里': 'Mali', '马耳他': 'Malta', '马里亚那群岛': 'Mariana Is', '马提尼克': 'Martinique', '毛里求斯': 'Mauritius', '墨西哥': 'Mexico', 
             '摩尔多瓦': 'Moldova', '摩纳哥': 'Monaco', '蒙古': 'Mongolia', '蒙特塞拉特岛': 'Montserrat Is', '摩洛哥': 'Morocco', '莫桑比克': 'Mozambique', '纳米比亚': 'Namibia', '瑙鲁': 'Nauru', '尼泊尔': 'Nepal', 
             '荷属安的列斯': 'Netheriands Antilles', '荷兰': 'Netherlands', '新西兰': 'New Zealand', '尼加拉瓜': 'Nicaragua', '尼日尔': 'Niger', '尼日利亚': 'Nigeria', '朝鲜': 'North Korea', '挪威': 'Norway', 
             '阿曼': 'Oman', '巴基斯坦': 'Pakistan', '巴拿马':'Panama', '巴布亚新几内亚': 'Papua New Cuinea', '巴拉圭': 'Paraguay', '秘鲁': 'Peru', '菲律宾': 'Philippines', '波兰': 'Poland', '葡萄牙': 'Portugal', 
             '波多黎各': 'Puerto Rico', '卡塔尔': 'Qatar', '留尼旺': 'Reunion', '罗马尼亚': 'Romania', '俄罗斯': 'Russia', '圣卢西亚': 'St.Lucia', '圣文森特岛': 'Saint Vincent', '东萨摩亚(美)': 'Samoa Eastern', 
             '西萨摩亚': 'Samoa Western', '圣马力诺': 'San Marino', '圣多美和普林西比': 'Sao Tome and Principe', '沙特阿拉伯': 'Saudi Arabia', '塞内加尔': 'Senegal', '塞舌尔': 'Seychelles', '塞拉利昂': 'Sierra Leone', 
             '新加坡': 'Singapore', '斯洛伐克': 'Slovakia', '斯洛文尼亚': 'Slovenia', '所罗门群岛': 'Solomon Is', '索马里': 'Somali', '南非': 'South Africa', '西班牙': 'Spain', '斯里兰卡': 'SriLanka', 
             '圣文森特': 'St.Vincent', '苏丹': 'Sudan', '苏里南': 'Suriname', '斯威士兰': 'Swaziland', '瑞典': 'Sweden', '瑞士': 'Switzerland', '叙利亚': 'Syria', '台湾省': 'Taiwan', '塔吉克斯坦': 'Tajikstan', 
             '坦桑尼亚': 'Tanzania', '泰国': 'Thailand', '多哥': 'Togo', '汤加': 'Tonga', '特立尼达和多巴哥': 'Trinidad and Tobago', '突尼斯': 'Tunisia', '土耳其': 'Turkey', '土库曼斯坦': 'Turkmenistan', 
             '乌干达': 'Uganda', '乌克兰': 'Ukraine', '阿联酋': 'United Arab Emirates', '英国': 'United Kiongdom', '美国': 'United States of America', '乌拉圭': 'Uruguay', '乌兹别克斯坦': 'Uzbekistan', 
             '委内瑞拉': 'Venezuela', '越南': 'Vietnam', '也门': 'Yemen', '南斯拉夫': 'Yugoslavia', '津巴布韦': 'Zimbabwe', '扎伊尔': 'Zaire', '赞比亚': 'Zambia'}


def gettext(str):
    pa = '.*?>(.*?)<.*?'
    txt = re.findall(pa, str, re.S)
    text =''
    for i in range(len(txt)):
        text=text+txt[i]
    return text
def update_news():
    search_title = '新型冠状病毒'
    search = urllib.parse.quote_plus(search_title)
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        ,
        "Cookies": "_T_WM=72947584203; SUB=_2A25zN_7nDeRhGeBO7lIU-C_JzD-IHXVQ24KvrDV6PUJbkdAKLWPlkW1NRePjmjAFGvwCGWME-H-D98R0Bcz8AMRy; SUHB=0U1ZWxWLcHC2Ez; SCF=At9-6f-j4PYNHn-XChtrim8D4eL3HYJ3fHnllUb94PLKI5i7xZCqyN84hTg7u_uPSINjMMh9QIbss-TTamWBjiA.; WEIBOCN_FROM=1110006030; XSRF-TOKEN=419251; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%259E%258B%25E5%2586%25A0%25E7%258A%25B6%25E7%2597%2585%25E6%25AF%2592%26fid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%259E%258B%25E5%2586%25A0%25E7%258A%25B6%25E7%2597%2585%25E6%25AF%2592%26uicode%3D10000011"
    }
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D{search}%26t%3D0&page_type=searchall'
    URL = url.format(search=search)
    r = json.loads(requests.get(URL,headers=headers).text)
    data = r['data']
    cards = data['cards']
    text = []
    link = []
    source = []
    cretae_time = []
    news_data = []
    flag=[]
    for item in cards:
        mblog = item['mblog']
        text.append(mblog['text'])
        link.append(item['scheme'])
        cretae_time.append(mblog['created_at'])
        source.append(item['mblog']['user']['screen_name'])
    for i in range(len(text)):
        tmp = gettext(text[i])
        flag.append(tmp)

    for j in range(5):
        news_data.append({
                'title': flag[j][0:35]+'...',
                'sourceUrl': link[j],
                'infoSource': cretae_time[j] + '    ' + source[j]
            })

    """
    url = 'https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&dspName=iphone&from_sf=1&dsp=iphone&resource_id=28565&alr=1&query=%E8%82%BA%E7%82%8E'
    r = json.loads(requests.get(url).text)
    top10 = r['Result'][0]['items_v2'][0]['aladdin_res']['DisplayData']['result']['items'][:5]     #list
    
    news_data = []
    for r in top10:
        news_data.append({
            'title': r['eventDescription'],
            'sourceUrl': r['eventUrl'],
            'infoSource': time.strftime('%m-%d %H:%M:%S', time.localtime(int(r['eventTime']))) + '    ' + r['siteName']   #时间属性 + 消息来源
        })  #构建新的列表
    print(news_data)
    """
    return news_data

def update_overall():
    url = 'http://lab.isaaclin.cn/nCoV/api/overall'
    overall_data = json.loads(requests.get(url).text)   #标准的json数据格式化
    overall_data['time'] = time.strftime("%m-%d %H:%M", time.localtime(time.time()))    #当前时间
    # time.time() --> '1580232854.7124019'
    ## time.localtime(time.time()) --> 'time.struct_time(tm_year=2020, tm_mon=1, tm_mday=29, tm_hour=1, tm_min=34, tm_sec=36, tm_wday=2, tm_yday=29, tm_isdst=0)'
    ### time.strftime("%m-%d %H:%M", time.localtime(time.time())) ---> '01-29 01:37'    获得当前月、日、小时、分钟
    return overall_data
#

def update_hotnews():
    url = 'https://i-lq.snssdk.com/api/feed/hotboard_online/v1/?is_in_channel=1&count=5&fe_source=news_hot&tab_name=stream&is_web_refresh=1&client_extra_params={%22hot_board_source%22:%22news_hot%22,%22fe_version%22:%22v10%22}&extra={%22CardStyle%22:0,%22JumpToWebList%22:true}&category=hotboard_online&update_version_code=75717'
    r = requests.get(url).text   #标准的json数据格式化
    data = re.findall(r'title\\":\\"(.*?)\\',r)[:-1]
        
    # time.time() --> '1580232854.7124019'
    ## time.localtime(time.time()) --> 'time.struct_time(tm_year=2020, tm_mon=1, tm_mday=29, tm_hour=1, tm_min=34, tm_sec=36, tm_wday=2, tm_yday=29, tm_isdst=0)'
    ### time.strftime("%m-%d %H:%M", time.localtime(time.time())) ---> '01-29 01:37'    获得当前月、日、小时、分钟
    return data #list

def word_cloud() -> WordCloud:
    url = 'https://i-lq.snssdk.com/api/feed/hotboard_online/v1/?is_in_channel=1&count=10&fe_source=news_hot&tab_name=stream&is_web_refresh=1&client_extra_params={%22hot_board_source%22:%22news_hot%22,%22fe_version%22:%22v10%22}&extra={%22CardStyle%22:0,%22JumpToWebList%22:true}&category=hotboard_online&update_version_code=75717'
    r = requests.get(url).text   #标准的json数据格式化
    data = re.findall(r'title\\":\\"(.*?)\\',r)[:-1]
    datanum = [8,7,6,5,5,4,4,2,1,1]
       
    words = [w for w in zip(data,datanum)]


    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-shape-diamond"))
    )
    return c     

def update_china_data(unit=3600 * 2):

    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)
    data = json.loads(r_data['data'])    #初始化json数据，为dict ['chinaTotal']
    p_data = {}
    #print(data['areaTree'][0]['children'][0])
    for i in data['areaTree'][0]['children']:   #各个省份
        p_data[i['name']] = i['total']['confirm']
    # 先对字典进行排序,按照value从大到小
    p_data= sorted(p_data.items(), key=lambda x: x[1], reverse=True)
    #print(p_data)
    
    return p_data

def china_map(data)-> Map:
    opt= [
        {"min":1001,"color":'#731919'},
        {"min":500,"max":1000,"color":'red'},
        {"min":100,"max":499,"color":'#e26061'},
        {"min":10,"max":99,"color":'#f08f7f'},
        {"min":1,"max":9,"color":'#ffb86a'},
        {"value":0,"color":'#ffffff'}
    ]
    c = (
            Map()
            .add(
                "确诊人数", data, "china", is_map_symbol_show=False,
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True,font_size=8))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=1000,is_piecewise=True,pieces=opt),
                legend_opts=opts.LegendOpts(is_show=False),
                #title_opts=opts.TitleOpts(title="全国疫情(2019-nCov)")
            )
        )
    return c
# 获取世界数据    
def update_world_data(unit=3600 * 2):
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)
    data = json.loads(r_data['data'])    #初始化json数据，为dict ['chinaTotal']
    #print(data['areaTree'][0]['children'][0])
    countryEN = []
    total_confirm = []
    for i in data['areaTree']:
        countryEN.append(cn_to_en[i['name']])
        total_confirm.append(i['total']['confirm'])
    data = [list(z) for z in zip(countryEN, total_confirm)]
    return data

def world_map(data)-> Map:
    opt= [
        {"min":1001,"color":'#731919'},
        {"min":51,"max":1000,"color":'red'},
        {"min":11,"max":50,"color":'#e26061'},
        {"min":6,"max":10,"color":'#f08f7f'},
        {"min":1,"max":5,"color":'#ffb86a'},
        {"value":0,"color":'#ffffff'}
    ]
    c = (
            Map()
            .add("确诊人数", data, "world",is_map_symbol_show=False)
            #.add("商家A", [list(z) for z in zip(countryEN, total_confirm)], "world")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False,font_size=8),)
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=1000,is_piecewise=True,pieces=opt),
                legend_opts=opts.LegendOpts(is_show=False),
                #title_opts=opts.TitleOpts(title="全球疫情(2019-nCov)")
            )
        )
    return c

def line_connect_null() -> Line:
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)

    data = json.loads(r_data['data'])    #初始化json数据，为dict ['chinaTotal']    
    #每日确诊增加数
    Dailyincrease = []
    a = [x['confirm'] for x in data['chinaDayList']]
    for i in range(len(a)):
        if i == 0:
            Dailyincrease.append(0)
        else:
            Dailyincrease.append(int(a[i]) - int(a[i-1]))  
    #每日疑似增加数
    Dailysuspect = []
    a = [x['suspect'] for x in data['chinaDayList']]
    for i in range(len(a)):
        if i == 0:
            Dailysuspect.append(0)
        else:
            Dailysuspect.append(int(a[i]) - int(a[i-1]))        
    c = (
        Line()
        .add_xaxis([x['date'] for x in data['chinaDayList']])   #直接列表
        .add_yaxis('确诊',[x['confirm'] for x in data['chinaDayList']])    #‘列表名，[]’
        .add_yaxis('疑似',[x['suspect'] for x in data['chinaDayList']])

        .add_yaxis('每日确诊增加数',Dailyincrease,areastyle_opts=opts.AreaStyleOpts(opacity=0.5))   #areastyle_opts=opts.AreaStyleOpts(opacity=0.5) 投射面积
        .add_yaxis('每日疑似增加数',Dailysuspect,is_smooth=True)    #is_smooth=True 代表平滑曲线
        .set_global_opts(
            #title_opts=opts.TitleOpts(title="2019-nCov"),
            datazoom_opts=opts.DataZoomOpts(range_end=100),
        )
    )
    return c

def line_heal() -> Line:
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)
    data = json.loads(r_data['data'])    #初始化json数据，为dict ['chinaTotal']    
    #每日确诊增加数
    Dailyincrease = []
    a = [x['confirm'] for x in data['chinaDayList']]
    for i in range(len(a)):
        if i == 0:
            Dailyincrease.append(0)
        else:
            Dailyincrease.append(int(a[i]) - int(a[i-1]))  
    #每日疑似增加数
    Dailysuspect = []
    a = [x['suspect'] for x in data['chinaDayList']]
    for i in range(len(a)):
        if i == 0:
            Dailysuspect.append(0)
        else:
            Dailysuspect.append(int(a[i]) - int(a[i-1]))        
    c = (
        Line()
        .add_xaxis([x['date'] for x in data['chinaDayList']])   #直接列表
        .add_yaxis('治愈',[x['heal'] for x in data['chinaDayList']])
        .add_yaxis('死亡',[x['dead'] for x in data['chinaDayList']])
        .set_global_opts(
            #title_opts=opts.TitleOpts(title="2019-nCov"),
            datazoom_opts=opts.DataZoomOpts(range_end=100),
        )
    )
    return c

def province():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)
    data = json.loads(r_data['data'])  # 初始化json数据，为dict ['chinaTotal']

    country = []
    confirm = []
    dead = []
    heal = []
    res = {
        'country': '',
        'confirm': '',
        'dead': '',
        'heal': '',
        'heals':'',
        'deads':'',
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
    dead_line = []
    for i in range(len(confirm)):
        fenmu = int(confirm[i])
        fenzi = int(dead[i])
        fenzi2 = int(heal[i])
        heals = fenzi2 / fenmu
        deads = fenzi / fenmu
        heal_line.append(heals)
        dead_line.append(deads)
    res['heals'] = heal_line
    res['deads'] = dead_line

    return jsonify(res)
def city():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)
    data = json.loads(r_data['data'])  # 初始化json数据，为dict ['chinaTotal']
    city = []
    city_tmp = []
    dead = []
    dead_tmp = []
    heal = []
    heal_tmp = []
    confirm = []
    confirm_tmp = []
    chinaren = data['areaTree'][0]['children']
    for province in chinaren:
        City = province['children']
        for item in City:
            city.append(item['name'])
            confirm.append(item['total']['confirm'])
            dead.append(item['total']['dead'])
            heal.append(item['total']['heal'])
    arr = np.array(confirm)

    tmp = np.argsort(-arr)[0:20]  # 逆序输出
    for j in tmp:
        city_tmp.append(city[j])
        confirm_tmp.append(confirm[j])
        dead_tmp.append(dead[j])
        heal_tmp.append(heal[j])
    res = {
        'country': '',
        'confirm': '',
        'dead': '',
        'heal': '',
        'heals':'',
        'deads':'',
    }
    res['country'] = city_tmp
    res['confirm'] = confirm_tmp
    res['dead'] = dead_tmp
    res['heal'] = heal_tmp

    return jsonify(res)

#海外国家趋势
def world_line() -> Bar:
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)
    data = json.loads(r_data['data'])  # 初始化json数据，为dict ['chinaTotal']
    city = []
    city_tmp=[]
    dead = []
    dead_tmp =[]
    heal = []
    heal_tmp=[]
    confirm = []
    confirm_tmp=[]
    chinaren = data['areaTree'][0]['children']
    for province in chinaren:
        City=province['children']
        for item in City:
            city.append(item['name'])
            confirm.append(item['total']['confirm'])
            dead.append(item['total']['dead'])
            heal.append(item['total']['heal'])
    arr = np.array(confirm)

    tmp = np.argsort(-arr)[0:20]  # 逆序输出
    for j in tmp:
        city_tmp.append(city[j])
        confirm_tmp.append(confirm[j])
        dead_tmp.append(dead[j])
        heal_tmp.append(heal[j])

    chart = Bar()
    chart.add_xaxis(city_tmp)
    chart.add_yaxis("确诊", confirm_tmp, stack=True)
    chart.add_yaxis("死亡", dead_tmp, stack=True)
    chart.add_yaxis("治愈", heal_tmp, stack=True)

    chart.set_global_opts(yaxis_opts=opts.AxisOpts(is_show=True, max_=3000))
    return chart

def china_online():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r_data = json.loads(requests.get(url).text)
    data = json.loads(r_data['data'])    #初始化json数据，为dict ['chinaTotal']    
    #每日确诊增加数
    # chinaTotal = data['chinaTotal']     #结果为列表
    # chinaAdd = data['chinaAdd']
    # lastUpdateTime = data['lastUpdateTime']
    return data

@app.route("/")
def index():
    return render_template("index.html")

# 全国地图数据
@app.route("/map")
def get_map():
    data = update_china_data()
    return china_map(data).dump_options_with_quotes()   #其中dump_options_with_quotes()是必备，任意图形。# 全国地图数据
#世界地图
@app.route("/maps")
def get_maps():
    #countryEN,total_confirm = update_world_data()
    data = update_world_data()
    return world_map(data).dump_options_with_quotes()   #其中dump_options_with_quotes()是必备，任意图形。
#疫情播报
@app.route("/news")
def get_news():
    news = update_news()
    return jsonify(news)

#全国统计数量
@app.route("/online")
def get_online():
    onlines = china_online()
    return jsonify(onlines)
#实时热榜    
@app.route("/hotnews")
def get_hotnews():
    hotnews = update_hotnews()
    return jsonify(hotnews)

@app.route("/wordcloud")
def get_word_cloud():
    word = word_cloud()
    return word.dump_options_with_quotes()
@app.route("/province")
def get_province():
    Province = province()
    return Province
@app.route("/city")
def get_city():
    City = city()
    return City

# K线

@app.route("/line")
def get_line():
    c = line_connect_null()
    return c.dump_options_with_quotes()   #其中dump_options_with_quotes()是必备，任意图形。# 全国地图数据




@app.route("/heal")
def get_heal():
    c = line_heal()
    return c.dump_options_with_quotes()   #其中dump_options_with_quotes()是必备，任意图形。# 全国地图数据        
# @app.route("/overall")
# def get_overall():
#     overall = update_overall()
#     return jsonify(overall)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0",port=5050,debug=True)