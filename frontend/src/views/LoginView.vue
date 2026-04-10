<template>
  <div class="form-page">
    <h2>登录</h2>
    <form @submit.prevent="submitLogin">
      <label>
        用户名
        <input v-model="username" required />
      </label>
      <label>
        密码
        <input type="password" v-model="password" required />
      </label>
      <button type="submit">登录</button>
      <p class="hint">没有账号？<router-link to="/register">注册一个</router-link></p>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  emits: ['login-success'],
  setup(_, { emit }) {
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const submitLogin = async () => {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.value, password: password.value })
      })
      const data = await res.json()
      if (!res.ok) {
        alert(data.error || '登录失败')
        return
      }
      localStorage.setItem('token', data.token)
      localStorage.setItem('username', data.username)
      emit('login-success', data.username)
      router.push('/')
    }

    return { username, password, submitLogin }
  }
}
</script>

<style>
.form-page { max-width: 420px; margin: 0 auto; background: #fff; padding: 28px; border-radius: 20px; box-shadow: 0 18px 40px rgba(0,0,0,.08); }
h2 { margin-top: 0; }
label { display: block; margin-bottom: 18px; font-weight: 600; }
input { width: 100%; padding: 12px 14px; border: 1px solid #d6d6d6; border-radius: 12px; margin-top: 8px; }
button { width: 100%; padding: 12px; margin-top: 12px; border: none; border-radius: 999px; background: #5a65ff; color: #fff; font-weight: 700; cursor: pointer; }
.hint { margin-top: 16px; color: #666; }
a { color: #5a65ff; }
</style>
