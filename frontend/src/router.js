import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import CartView from './views/CartView.vue'
import OrdersView from './views/OrdersView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/cart', component: CartView },
  { path: '/orders', component: OrdersView }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
