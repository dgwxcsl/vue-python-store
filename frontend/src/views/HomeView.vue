<template>
  <div class="home">
    <section class="hero">
      <h1>四代练习生周边</h1>
      <p>为每一位练习生准备专属周边，快速浏览、加入购物车、下单支付。</p>
    </section>

    <section class="products">
      <div class="product-card" v-for="product in products" :key="product.id">
        <img :src="product.image" :alt="product.name" />
        <div class="card-info">
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <div class="bottom-row">
            <strong>¥{{ product.price }}</strong>
            <button @click="addToCart(product)">加入购物车</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const products = ref([])

    const loadProducts = async () => {
      const res = await fetch('/api/products')
      products.value = await res.json()
    }

    const addToCart = (product) => {
      const current = JSON.parse(localStorage.getItem('cart') || '[]')
      current.push({ ...product, quantity: 1 })
      localStorage.setItem('cart', JSON.stringify(current))
      alert(`${product.name} 已加入购物车`)
    }

    onMounted(loadProducts)
    return { products, addToCart }
  }
}
</script>

<style>
.home .hero { margin-bottom: 24px; padding: 24px; background: #fff; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,.05); }
.home .hero h1 { margin: 0 0 8px; font-size: 2rem; }
.home .hero p { margin: 0; color: #555; }
.products { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
.product-card { background: #fff; border-radius: 18px; padding: 16px; box-shadow: 0 10px 30px rgba(0,0,0,.08); display: flex; flex-direction: column; }
.product-card img { width: 100%; border-radius: 14px; object-fit: cover; height: 180px; }
.card-info { display: flex; flex-direction: column; gap: 12px; margin-top: 12px; }
.bottom-row { display: flex; justify-content: space-between; align-items: center; }
button { border: none; padding: 10px 14px; border-radius: 999px; background: #5a65ff; color: #fff; cursor: pointer; }
button:hover { opacity: .95; }
</style>
