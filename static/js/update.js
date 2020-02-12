var myChart = echarts.init(document.getElementById('ncov-gender'));
option = {
    title: {
        text: '患者年龄分布',
        subtext: '部分数据有所缺失'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['男性', '女性']
    },

    yAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    xAxis: {
        type: 'category',
        data: ['0-10岁', '10-20岁', '20-30岁', '30-40岁', '40-50岁', '50-60岁','60-70岁','70岁以上']
    },
    series: [
        {
            name: '男性',
            type: 'bar',
            data: [1.87, 5.22, 14.55, 24.99, 25.37 ,12.31,8.96,6.73],
        },
        {
            name: '女性',
            type: 'bar',
            data: [3.18, 4.09, 11.36, 20.91, 21.36,16.82,15.91,6.37],
        }
    ]
};
myChart.setOption(option)

var myChart1 = echarts.init(document.getElementById('ncov-distribute'));
option = {
    title: {
        text: '各年龄段感染概率'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['男性', '女性', '男性_修正','女性_修正' ]
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['0-10岁', '10-20岁', '20-30岁', '30-40岁', '40-50岁', '50-60岁','60-70岁','70岁以上']
     },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '男性',
            type: 'line',
            stack: '总量',
            data: [15.56,45.65,107.25,155.42,173.25,80.40,88.91,108.52],
           // [1.87, 5.22, 14.55, 24.99, 25.37 ,12.31,8.96,6.73],
           //[6.2, 5.9,     7.0,   8.3,  7.8,   7.9,  5.2,  3.2]
        //[15.56,45.65,107.25,155.42,173.25,80.40,88.91,108.52]
        },
        {
            name: '女性',
            type: 'line',
            stack: '总量',
            data:[29.04   ,38.81,    88.68,129.74, 139.70,105.72,145.29,108.45]
            //[3.18, 4.09, 11.36, 20.91, 21.36,16.82,15.91,6.37],
            //[5.3,      5.1,    6.2,   7.8 ,7.4,  7.7,   5.3,3.6  ]
        //[29.04   ,38.81,    88.68,129.74, 139.70,105.72,145.29,108.45]


        },


    ]
};
myChart1.setOption(option)



function getHost() {
    return document.location.protocol + "//" +window.location.host;}

    var PP_ops = {
    init:function () {
        this.drawprovince();
        this.drawcity();
        this.drawdis();

    },
        drawprovince:function () {
    $.ajax({
        type: "GET",
        url: getHost() + "/province",
        dataType: 'json',
        success: function (result) {

            var myChart = echarts.init(document.getElementById('ncov-worldbar'));
            option = {

    title: {

    },
   tooltip: {
        trigger: 'axis',

    },
    legend: {
        data:['确诊','死亡','治愈']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        data: result['country'],

    },
    yAxis: {max:2500},
    series: [{
        name: '确诊',
        stack:"人数",
        type: 'bar',
        data: result['confirm']
    },
    {
        name: '死亡',
        stack:"人数",
        type: 'bar',
        data: result['dead']
    },
        {
        name: '治愈',
        stack:"人数",
        type: 'bar',
        data: result['heal']
    },


    ],

};
            myChart.setOption(option)


        }
    })},
        drawcity:function () {

    $.ajax({
        type: "GET",
        url: getHost() + "/city",
        dataType: 'json',
        success: function (result) {
            console.log(result)

            var myChart = echarts.init(document.getElementById('ncov-worldline'));
            option = {

    title: {

    },
   tooltip: {
        trigger: 'axis',

    },
    legend: {
        data:['确诊','死亡','治愈']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        data: result['country'],
         axisLabel: {

             interval: 0,
        textStyle: {

          fontSize : 8     //更改坐标轴文字大小
        }
     },
    },
    yAxis: {max:3000},
    series: [{
        name: '确诊',
        stack:"人数",
        type: 'bar',
        data: result['confirm']
    },
    {
        name: '死亡',
        stack:"人数",
        type: 'bar',
        data: result['dead']
    },
        {
        name: '治愈',
        stack:"人数",
        type: 'bar',
        data: result['heal']
    },


    ],

};
            myChart.setOption(option);

            var province = echarts.init(document.getElementById('ncov-gender'));
            option = {
    title: {
        text: '患者年龄分布',
        subtext: '部分数据有所缺失'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['男性', '女性']
    },

    yAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    xAxis: {
        type: 'category',
        data: ['0-10岁', '10-20岁', '20-30岁', '30-40岁', '40-50岁', '50-60岁','60-70岁','70岁以上']
    },
    series: [
        {
            name: '男性',
            type: 'bar',
            data: [1.87, 5.22, 14.55, 24.99, 25.37 ,12.31,8.96,6.73],
        },
        {
            name: '女性',
            type: 'bar',
            data: [3.18, 4.09, 11.36, 20.91, 21.36,16.82,15.91,6.37],
        }
    ]
};
            province.setOption(option);

            var city = echarts.init(document.getElementById('ncov-distribute'));
            option = {
    title: {
        text: '各年龄段感染概率'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['男性', '女性', '男性_修正','女性_修正' ]
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['0-10岁', '10-20岁', '20-30岁', '30-40岁', '40-50岁', '50-60岁','60-70岁','70岁以上']
     },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '男性',
            type: 'line',
            stack: '总量',
            data: [15.56,45.65,107.25,155.42,173.25,80.40,88.91,108.52],
           // [1.87, 5.22, 14.55, 24.99, 25.37 ,12.31,8.96,6.73],
           //[6.2, 5.9,     7.0,   8.3,  7.8,   7.9,  5.2,  3.2]
        //[15.56,45.65,107.25,155.42,173.25,80.40,88.91,108.52]
        },
        {
            name: '女性',
            type: 'line',
            stack: '总量',
            data:[29.04   ,38.81,    88.68,129.74, 139.70,105.72,145.29,108.45]
            //[3.18, 4.09, 11.36, 20.91, 21.36,16.82,15.91,6.37],
            //[5.3,      5.1,    6.2,   7.8 ,7.4,  7.7,   5.3,3.6  ]
        //[29.04   ,38.81,    88.68,129.74, 139.70,105.72,145.29,108.45]


        },


    ]
};
            city.setOption(option)

        }
    })},

        drawdis:function () {
    $.ajax({
        type: "GET",
        url: getHost() + "/province",
        dataType: 'json',
        success: function (result) {

            var heal_dead = echarts.init(document.getElementById('ncov-gender'));
            option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'line'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data: ['死亡率', '治愈率']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'value'

        }
    ],
    yAxis: [
        {
            type: 'category',
            axisTick: {
                show: true
            },

            data: res['country']

        }
    ],
    series: [
        {
            name: '死亡率',
            type: 'bar',
             stack: '总量',

            data: res['deads']
        },

        {
            name: '治愈率',
            type: 'bar',
            stack: '总量',
            data: res['heals']
        }
    ]
};

            heal_dead.setOption(option)


        }
    })},




}
$(document).ready(function () {
    PP_ops.init()

});
var chinamap = echarts.init(document.getElementById('ncov-map'), 'white', {renderer: 'canvas'});
var worldmap = echarts.init(document.getElementById('ncov-maps'), 'white', {renderer: 'canvas'});

var nline = echarts.init(document.getElementById('ncov-line'), 'white', {renderer: 'canvas'});
//var worldbar = echarts.init(document.getElementById('ncov-worldbar'), 'white', {renderer: 'canvas'});

//var worldline = echarts.init(document.getElementById('ncov-worldline'), 'white', {renderer: 'canvas'});
var heal = echarts.init(document.getElementById('ncov-heal'), 'white', {renderer: 'canvas'});

$(
    function () {
        //updateOverall();
        updateNews();
        updateOnline(); //实时统计数据
        updateHotNews();    //热点更新
        fetchData(chinamap);
        fetchData2(worldmap);
        //kline(nkline);
        line(nline);
        //getworldbar(worldbar);
        //getworldline(worldline);
        getheal(heal);
        setInterval(updateNews, 30 * 60 * 1000);    //半小时获取一次
        //setInterval(updateOverall, 60 * 1000);
        setInterval(fetchData, 30 * 60 * 1000);
        setInterval(fetchData2, 30 * 60 * 1000);
        setInterval(updateHotNews, 10 * 60 * 1000);
    }
);

function getHost() {
    return document.location.protocol + "//" +window.location.host;
}


function updateOnline(){
    $.ajax({
        type: "GET",
        url: getHost() + "/online",
        dataType: 'json',
        success: function (result) {
            online_html = '<li class="text-muted"><i class="fa fa-smile-o pr-2"></i>  更新时间：' + result['lastUpdateTime'] +'</li><li class="badge badge-primary"><i class="fa fa-bug pr-2"></i>全国确诊：' + result['chinaTotal']['confirm'] + '</li><br><li class="badge badge-success"><i class="fa fa-heartbeat pr-2"></i>治愈：' + result['chinaTotal']['heal'] + '</li><br><li class="badge badge-secondary"><i class="fa fa-hospital-o pr-2"></i>死亡：' + result['chinaTotal']['dead'] + '</li>'
            $('#online').html(online_html)
        }
    });
}

function updateHotNews(){
    $.ajax({
        type: "GET",
        url: getHost() + "/hotnews",
        dataType: 'json',
        success: function (result) {
            hotnews_html = ""
            for(var i = 0, len = result.length; i < len; i++){
                hotnews_html += "<li><div class='base-timeline-info'>" + result[i] + "</div></li>"
            }
            $('#hotnews').html(hotnews_html)
        }
    });
}

function updateNews(){
    $.ajax({
        type: "GET",
        url: getHost() + "/news",
        dataType: 'json',
        success: function (result) {
            news_html = ""
            for(var i = 0, len = result.length; i < len; i++){
                news_html += "<li><div class='base-timeline-info'><a href=" + result[i]['sourceUrl'] + ">" + result[i]['title'] + "</a></div><small class='text-muted'>" + result[i]['infoSource'] + '</small></li>'
            }
            $('#newslist').html(news_html)
        }
    });
}


//中国地图
function fetchData(chinamap) {
    $.ajax({
        type: "GET",
        url: getHost() + "/map",
        dataType: 'json',
        success: function (result) {
            chinamap.setOption(result);
        }
    });
}
//世界地图

function fetchData2(worldmap) {
    $.ajax({
        type: "GET",
        url: getHost() + "/maps",
        dataType: 'json',
        success: function (result) {
            worldmap.setOption(result);


        }
    });
}


//kline

//line
function line(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/line",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}
/*
function getworldbar(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/worldbar",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);


        }
    });
}

function getworldline(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/worldline",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}
*/
function getheal(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/heal",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}

function getworldcloud(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/wordcloud",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}
