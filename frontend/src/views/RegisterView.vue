<template>
  <div class="form-page">
    <h2>注册</h2>
    <form @submit.prevent="submitRegister">
      <label>
        用户名
        <input v-model="username" required />
      </label>
      <label>
        密码
        <input type="password" v-model="password" required />
      </label>
      <button type="submit">注册</button>
      <p class="hint">已有账号？<router-link to="/login">去登录</router-link></p>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const submitRegister = async () => {
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.value, password: password.value })
      })
      const data = await res.json()
      if (!res.ok) {
        alert(data.error || '注册失败')
        return
      }
      alert('注册成功，请登录')
      router.push('/login')
    }

    return { username, password, submitRegister }
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
