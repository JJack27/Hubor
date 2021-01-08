import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'ant-design-vue/dist/antd.less';

import {Button, Form, Input, Icon, Checkbox, Card, Row, Col, message, Layout, Menu} from 'ant-design-vue'
import Axios from 'axios';


const app = createApp(App);

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
        url,
        body,
        {
            headers:{
                'X-CSRFToken': this.$getCookie('csrftoken'),
            }
        }
    )
}

app.config.globalProperties.$get = async function(url) {
    return Axios.get(
        url,
        {
            headers:{
                'X-CSRFToken': this.$getCookie('csrftoken'),
            }
        }
    )
}

app.config.globalProperties.$message = message;

app.use(store)
    .use(router)
    .use(Button)
    .use(Form)
    .use(Icon)
    .use(Input)
    .use(Form.Item)
    .use(Checkbox)
    .use(Card)
    .use(Row)
    .use(Col)
    .use(Layout)
    .use(Layout.Footer)
    .use(Layout.Sider)
    .use(Layout.Header)
    .use(Menu)
    .mount('#app');
