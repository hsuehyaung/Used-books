<template>
  <div>
    <h2>购物车</h2>
    <el-table :data="cartItems" style="width: 100%" class="table">
      <el-table-column prop="book_name" label="商品名称" width="200"></el-table-column>
      <el-table-column prop="price" label="价格" width="200"></el-table-column>
      <el-table-column label="操作" width="150">
        <template slot-scope="scope">
          <el-button @click="removeFromCart(scope.row)" type="danger" size="small">移除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-button type="primary" @click="checkout">去结算</el-button>
  </div>
</template>

<script>
export default {
  computed: {
    cartItems() {
      return this.$store.state.cart;
    }
  },
  methods: {
    removeFromCart(item) {
      this.$store.dispatch('removeFromCart', item);
    },
    checkout() {
      this.$router.push('/checkout');
    }
  }
};
</script>
