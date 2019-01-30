var vm = new Vue({
    el: '#app',
    data: {
        provinces: [],
        cities: [],
        districts: [],
        district_name: '',
        form_address: {
            province_id: '',
            city_id: '',
            district_id: '',
        },
        temperature_data: [1.8, 5, 11.6, 20.3, 26, 30.2, 30.9, 29.7, 25.8, 19.1, 10.1, 3.7],
        precipitation_data: [2.7, 4.4, 9.9, 24.7, 37.3, 71.9, 160.1, 138.2, 48.5, 22.8, 9.5, 2]
    },


    mounted: function () {
        axios.get("http://127.0.0.1:8000/" + 'areas/', {
            responseType: 'json'
        }).then(response => {
            this.provinces = response.data;
        }).catch(error => {
            alert(error.response.data);
        });

        axios.get("http://127.0.0.1:8000/" + 'index/' + '110100' + '/', {
            responseType: 'json'
        })
            .then(response => {
                this.temperature_data = response.data.temperature_data;
                this.precipitation_data = response.data.precipitation_data;
                this.district_name = response.data.district_name
                myChart1.setOption(option1)
                myChart2.setOption(option2)

            })
            .catch(error => {
                console.log(error);

            });

    },
    watch: {
        'form_address.province_id': function () {
            if (this.form_address.province_id) {
                axios.get("http://127.0.0.1:8000/" + 'areas/' + this.form_address.province_id + '/', {
                    responseType: 'json'
                })
                    .then(response => {
                        this.cities = response.data.subs;
                    })
                    .catch(error => {
                        console.log(error.response.data);
                        this.cities = [];
                    });
            }
        },
        'form_address.city_id': function () {
            if (this.form_address.city_id) {
                axios.get("http://127.0.0.1:8000/" + 'areas/' + this.form_address.city_id + '/', {
                    responseType: 'json'
                })
                    .then(response => {
                        this.districts = response.data.subs;

                    })
                    .catch(error => {
                        cconsole.log(error.response.data);
                        this.districts = [];
                    });
            }
        },

        'form_address.district_id': function (newvalue, oldvalue) {
            axios.get("http://127.0.0.1:8000/" + 'index/' + this.form_address.district_id + '/', {
                // axios.get("http://127.0.0.1:8000/" + 'index/' + '360102' + '/', {
                //     responseType: 'json'
            })
                .then(response => {
                    this.temperature_data = response.data.temperature_data;
                    this.precipitation_data = response.data.precipitation_data;
                    this.district_name = response.data.district_name
                    myChart1.setOption({
    title: {
        text: '气温(℃)',
    },
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        show: true,
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series:
        {
            name: '气温',
            type: 'line',
            data: vm.temperature_data,
            // data: vm.temperature_data,
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        }
})
                    myChart2.setOption({
    title: {
        text: '降水量(mm)',
        align: 'center'
    },
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        show: true,
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: [

        {
            name: '降水量',
            type: 'bar',
            data: vm.precipitation_data,
            markPoint: {
                data: [
                    {name: '年最高', value: 182.2, xAxis: 7, yAxis: 183},
                    {name: '年最低', value: 2.3, xAxis: 11, yAxis: 3}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        }
    ]
})
                })
                .catch(error => {
                    console.log(error);

                });

        }
    },

});

// 基于准备好的dom，初始化echarts实例
var myChart1 = echarts.init(document.getElementById('temperature'), 'dark');

// 气温图表
// 指定图表的配置项和数据
option1 = {
    title: {
        text: '气温(℃)',
    },
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        show: true,
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series:
        {
            name: '气温',
            type: 'line',
            data: vm.temperature_data,
            // data: vm.temperature_data,
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        }
};
// 使用刚指定的配置项和数据显示图表。
myChart1.setOption(option1);

// 降水量图表
// 基于准备好的dom，初始化echarts实例
var myChart2 = echarts.init(document.getElementById('precipitation'), 'dark');

// 指定图表的配置项和数据
option2 = {
    title: {
        text: '降水量(mm)',
        align: 'center'
    },
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        show: true,
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: [

        {
            name: '降水量',
            type: 'bar',
            data: vm.precipitation_data,
            markPoint: {
                data: [
                    {name: '年最高', value: 182.2, xAxis: 7, yAxis: 183},
                    {name: '年最低', value: 2.3, xAxis: 11, yAxis: 3}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        }
    ]
};

// 使用刚指定的配置项和数据显示图表。
myChart2.setOption(option2);

