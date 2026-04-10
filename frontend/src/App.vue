<template>
  <div class="app">
    <header class="topbar">
      <div class="brand">练习生周边商城</div>
      <nav>
        <router-link to="/">首页</router-link>
        <router-link to="/cart">购物车</router-link>
        <router-link to="/orders">我的订单</router-link>
        <router-link v-if="!username" to="/login">登录</router-link>
        <span v-else class="user-name">欢迎，{{ username }}</span>
      </nav>
    </header>
    <main>
      <router-view @login-success="handleLoginSuccess"></router-view>
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const username = ref(localStorage.getItem('username') || '')

    const handleLoginSuccess = (name) => {
      username.value = name
    }

    return { username, handleLoginSuccess }
  }
}
</script>

<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: Arial, sans-serif; background: #f0f4f8; }
.app { min-height: 100vh; }
.topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; background: linear-gradient(90deg, #ff9a9e, #fad0c4); }
.brand { font-size: 1.25rem; font-weight: bold; color: #fff; }
nav { display: flex; gap: 16px; align-items: center; }
nav a { color: #fff; text-decoration: none; font-weight: 500; }
.user-name { color: #fff; font-weight: 600; }
main { padding: 24px; }
</style>
