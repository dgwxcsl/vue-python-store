<template>
  <div class="orders-page">
    <h2>我的订单</h2>
    <div v-if="orders.length === 0" class="empty">暂无历史订单</div>
    <div v-else>
      <div class="order-card" v-for="order in orders" :key="order.id">
        <div class="order-header">
          <span>订单 #{{ order.id }}</span>
          <span>{{ order.created_at }}</span>
        </div>
        <div class="order-body">
          <div>总价：<strong>¥{{ order.total }}</strong></div>
          <div>商品：{{ order.items }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const orders = ref([])

    const loadOrders = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        return
      }
      const res = await fetch('/api/orders', {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) {
        return
      }
      orders.value = await res.json()
    }

    onMounted(loadOrders)
    return { orders }
  }
}
</script>

<style>
.orders-page { max-width: 760px; margin: 0 auto; background: #fff; padding: 24px; border-radius: 20px; box-shadow: 0 18px 40px rgba(0,0,0,.06); }
.order-card { margin-bottom: 18px; padding: 18px; border: 1px solid #eef2f7; border-radius: 16px; }
.order-header { display: flex; justify-content: space-between; margin-bottom: 12px; font-weight: 600; }
.order-body { color: #555; line-height: 1.6; }
.empty { padding: 40px 0; text-align: center; color: #777; }
</style>
