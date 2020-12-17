import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'ant-design-vue/dist/antd.less';
import {Button, Form, Input, Icon, Checkbox, Card, Row, Col} from 'ant-design-vue'

createApp(App)
    .use(store)
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
    .mount('#app')
