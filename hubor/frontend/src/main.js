import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'ant-design-vue/dist/antd.less';
import 'font-awesome/css/font-awesome.min.css';

import {message, Badge, Tabs, Button, Form, Input, Icon, Checkbox, 
    Card, Row, Col, Layout, Menu, Avatar, Table, Modal, DatePicker, 
    Select, List, Descriptions
} from 'ant-design-vue'
import Axios from 'axios';
import { DescriptionsItem } from 'ant-design-vue/lib/descriptions';


const app = createApp(App);
const baseURL = "";

//app.config.globalProperties.$baseURL = "http://192.168.1.64:8000/";

app.config.globalProperties.$getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

app.config.globalProperties.$setCookie = function (name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

app.config.globalProperties.$post = async function(url, body) {
    return Axios.post(
        baseURL + url,
        body,
        {
            headers:{
                'X-CSRFToken': this.$getCookie('csrftoken'),
                'withCredentials': true
            }
        }
    )
}

app.config.globalProperties.$put = async function(url, body) {
    return Axios.put(
        baseURL + url,
        body,
        {
            headers:{
                'X-CSRFToken': this.$getCookie('csrftoken'),
                'withCredentials': true
            }
        }
    )
}

app.config.globalProperties.$get = async function(url) {
    return Axios.get(
        baseURL + url,
        {
            headers:{
                'X-CSRFToken': this.$getCookie('csrftoken'),
                'withCredentials': true
            }
        }
    )
}

app.config.globalProperties.$delete = async function(url) {
    return Axios.delete(
        baseURL + url,
        {
            headers:{
                'X-CSRFToken': this.$getCookie('csrftoken'),
                'withCredentials': true
            }
        }
    )
}

app.config.globalProperties.$message = message;

app.use(store)
    .use(Avatar)
    .use(Badge)
    .use(Button)
    .use(Card)
    .use(Checkbox)
    .use(Col)
    .use(DatePicker)
    .use(Descriptions)
    .use(Descriptions.Item)
    .use(Form)
    .use(Form.Item)
    .use(Icon)
    .use(Input)
    .use(Layout)
    .use(Layout.Footer)
    .use(Layout.Sider)
    .use(Layout.Header)
    .use(List)
    .use(List.Item)
    .use(Modal)
    .use(Menu)
    .use(message)
    .use(router)
    .use(Row)
    .use(Select)
    .use(Tabs)
    .use(Tabs.TabPane)
    .use(Table)
    .mount('#app');
