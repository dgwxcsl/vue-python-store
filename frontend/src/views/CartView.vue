<template>
  <div class="cart-page">
    <h2>购物车</h2>
    <div v-if="cart.length === 0" class="empty">购物车为空</div>
    <div v-else>
      <div class="cart-item" v-for="(item, index) in cart" :key="index">
        <img :src="item.image" :alt="item.name" />
        <div>
          <h3>{{ item.name }}</h3>
          <p>¥{{ item.price }} x {{ item.quantity }}</p>
          <p>练习生：{{ item.member }}</p>
        </div>
      </div>
      <div class="summary">
        <div>总价：<strong>¥{{ total }}</strong></div>
        <button @click="checkout">提交订单</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  setup() {
    const cart = ref([])
    const total = computed(() => cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0))

    const loadCart = () => {
      cart.value = JSON.parse(localStorage.getItem('cart') || '[]').map(item => ({ ...item, quantity: item.quantity || 1 }))
    }

    const checkout = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        alert('请先登录再下单')
        return
      }
      const res = await fetch('/api/cart/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ items: cart.value, total: total.value })
      })
      const data = await res.json()
      if (!res.ok) {
        alert(data.error || '提交失败')
        return
      }
      localStorage.removeItem('cart')
      cart.value = []
      alert('订单提交成功')
    }

    onMounted(loadCart)
    return { cart, total, checkout }
  }
}
</script>

<style>
.cart-page { max-width: 800px; margin: 0 auto; background: #fff; padding: 24px; border-radius: 20px; box-shadow: 0 18px 40px rgba(0,0,0,.06); }
.cart-item { display: flex; gap: 18px; align-items: center; margin-bottom: 18px; }
.cart-item img { width: 120px; border-radius: 16px; }
.summary { display: flex; justify-content: space-between; align-items: center; margin-top: 24px; padding-top: 18px; border-top: 1px solid #eef2f7; }
button { padding: 12px 18px; border: none; border-radius: 999px; background: #5a65ff; color: #fff; cursor: pointer; }
.empty { padding: 40px 0; text-align: center; color: #777; }
</style>
