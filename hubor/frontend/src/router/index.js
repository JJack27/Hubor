import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Test from '../views/Test.vue'
import Dashboard from '../views/Dashboard.vue';
import MonitorPage from '../views/MonitorPage.vue';
import EmergencyContactPage from '../views/EmergencyContactPage.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/test',
    name: 'test',
    component: Test
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    children:[
      {
        path: 'monitor/:id',
        name: 'monitor',
        component: MonitorPage,
      },

      {
        path: 'emergencycontact/:id',
        name: 'emergencycontact',
        component: EmergencyContactPage,
      }
    ],
  },
  
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
