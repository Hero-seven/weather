var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        username: sessionStorage.username || localStorage.username,
        is_show_edit: false,
        provinces: [],
        cities: [],
        districts: [],
        addresses: [],
        limit: '',
        default_address_id: '',
        form_address: {
            province_id: '',
            city_id: '',
            district_id: '',
        },
    },
    mounted: function(){
        axios.get(this.host + 'index/areas/', {
                responseType: 'json'
            })
            .then(response => {
                this.provinces = response.data;
            })
            .catch(error => {
                alert(error.response.data);
            });
    },
    watch: {
        'form_address.province_id': function(){
            if (this.form_address.province_id) {
                axios.get(this.host + 'index/areas/'+ this.form_address.province_id + '/', {
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
        'form_address.city_id': function(){
            if (this.form_address.city_id){
                axios.get(this.host + 'index/areas/'+ this.form_address.city_id + '/', {
                        responseType: 'json'
                    })
                    .then(response => {
                        this.districts = response.data.subs;
                    })
                    .catch(error => {
                        console.log(error.response.data);
                        this.districts = [];
                    });
            }
        }
    },
    methods: {
        // 展示新增地址界面
        show_add: function(){
            this.clear_all_errors();
            this.editing_address_index = '';
            this.form_address.receiver = '';
            this.form_address.province_id = '';
            this.form_address.city_id = '';
            this.form_address.district_id = '';
            this.form_address.place = '';
            this.form_address.mobile = '';
            this.form_address.tel = '';
            this.form_address.email = '';
            this.is_show_edit = true;
        },
        // 展示编辑地址界面
        show_edit: function(index){
            this.clear_all_errors();
            this.editing_address_index = index;
            // 只获取数据，防止修改form_address影响到addresses数据
            this.form_address = JSON.parse(JSON.stringify(this.addresses[index]));
            this.is_show_edit = true;
        },

        // 保存地址
        save_address: function(){
            if (this.error_receiver || this.error_place || this.error_mobile || this.error_email || !this.form_address.province_id || !this.form_address.city_id || !this.form_address.district_id ) {
                alert('信息填写有误！');
            } else {
                this.form_address.title = this.form_address.receiver;
                if (this.editing_address_index === '') {
                    // 新增地址
                    axios.post(this.host + '/addresses/', this.form_address, {
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json'
                    })
                    .then(response => {
                        // 将新地址添加大数组头部
                        this.addresses.splice(0, 0, response.data);
                        this.is_show_edit = false;
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
                } else {

                    // 修改地址
                    axios.put(this.host + '/addresses/' + this.addresses[this.editing_address_index].id + '/', this.form_address, {
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json'
                    })
                    .then(response => {
                        this.addresses[this.editing_address_index] = response.data;
                        this.is_show_edit = false;
                    })
                    .catch(error => {
                        alert(error.response.data.detail || error.response.data.message);
                    })
                }
            }
        },
    }
});