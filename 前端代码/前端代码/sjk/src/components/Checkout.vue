<template>
  <div class="checkout-container">
    <div class="checkout-header">结算页面</div>
    <!-- 购物车中的商品列表 -->
    <div v-for="(item, index) in shoppingCart" :key="index" class="item-container">
      <div class="item-name">{{ item.book_name }}</div>
      <el-input-number v-model.number="item.quantity" :min="1" label="数量" class="item-quantity" />
    </div>
    <!-- 收件方式选择 -->
    <div class="receive-type-container">
      <el-radio-group v-model="receiveType">
        <el-radio label="自提">自提</el-radio>
        <el-radio label="配送">配送</el-radio>
      </el-radio-group>
    </div>
    <!-- 地址信息显示 -->
    <div v-if="receiveType === '自提'" class="address-container">
      收件地址：崇文路2号二手书店
    </div>
    <div v-else class="address-container">
      <el-input placeholder="请输入收件地址" v-model="receiveAddress" />
    </div>
    <!-- 结算总额 -->
    <div class="total-price-container">
      结算总额：{{ totalPrice }}
    </div>
    <!-- 确认结算按钮 -->
    <el-button type="primary" @click="confirmCheckout" class="confirm-button">确认结算</el-button>
  </div>
</template>

<script>
export default {
  name: 'Checkout',
  data() {
    return {
      shoppingCart: [],
      receiveType: '自提',
      receiveAddress: '',
      totalPrice: 0
    };
  },
  created() {
    // 从路由参数中获取购物车数据
    const cartData = this.$route.query.cartData;
    if (cartData) {
      this.shoppingCart = JSON.parse(cartData);
      this.calculateTotalPrice();
    }
  },
  methods: {
    // 计算结算总额
    calculateTotalPrice() {
      let total = 0;
      for (const item of this.shoppingCart) {
        total += item.price * item.quantity;
      }
      this.totalPrice = total;
    },
    // 确认结算
    confirmCheckout() {
      // 检查收件地址是否为空（当选择配送时）
      if (this.receiveType === '配送' && this.receiveAddress === '') {
        this.$message({
          message: '请输入收件地址',
          type: 'warning'
        });
        return;
      }
      // 假设向服务器发送结算请求
      this.$axios.post('/api/checkout', {
        cartData: this.shoppingCart,
        receiveType: this.receiveType,
        receiveAddress: this.receiveAddress
      }).then(response => {
        if (response.data.status === 200) {
          this.$message({
            message: '结算成功',
            type: 'success'
          });
          // 结算成功后的跳转或其他操作
        } else {
          this.$message({
            message: '结算失败',
            type: 'error'
          });
        }
      }).catch(error => {
        console.error('结算请求失败', error);
        this.$message({
          message: '结算请求失败，请稍后重试',
          type: 'error'
        });
      });
    }
  }
};
</script>

<style scoped>
.checkout-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.checkout-header {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}
.item-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px;
}
.item-name {
  font-size: 18px;
  margin-bottom: 5px;
}
.item-quantity {
  width: 100px;
}
.receive-type-container {
  margin-bottom: 20px;
}
.address-container {
  margin-bottom: 20px;
}
.total-price-container {
  font-size: 20px;
  margin-bottom: 20px;
}
.confirm-button {
  width: 200px;
}
</style>