<template>
    <div class="container">
        <!-- 图书信息表格 -->
        <div class="left-panel">
            <div class="header">
                图书信息
            </div>
            <div class="table-container">
                <el-table :data="tableData" style="width: 100%" class="table" border>
                    <el-table-column prop="book_name" label="图书名称" width="258" align="center">
                        <template slot-scope="scope">
                            <span @click="goToBookImg(scope.row.book_name)">{{ scope.row.book_name }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="price" label="产品单价" width="100" align="center">
                    </el-table-column>
                    <el-table-column prop="sale" label="月销量" width="100" align="center">
                    </el-table-column>
                    <el-table-column prop="operate" label="操作" width="108" align="center">
                        <template slot-scope="scope">
                            <el-button icon="el-icon-plus" size="small" type="success" @click="addToCart(scope.row)">
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
 
        <!-- 购物车和购买功能 -->
        <div class="right-panel">
            <div class="cart-container">
                <h3>购物车</h3>
                <el-table :data="cartData" style="width: 100%" class="cart-table" border>
                    <el-table-column prop="book_name" label="商品名称" width="200" align="center">
                    </el-table-column>
                    <el-table-column prop="price" label="单价" width="50" align="center">
                    </el-table-column>
                    <el-table-column prop="quantity" label="数量" width="205" align="center">
                        <template slot-scope="scope">
                            <el-input-number v-model="scope.row.quantity" :min="1" @change="updateCartItem(scope.$index, scope.row.quantity)"></el-input-number>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="100" align="center">
                        <template slot-scope="scope">
                            <el-button size="small" type="danger" @click="removeFromCart(scope.$index)">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div style="text-align: right; margin-top: 20px;">
                    <el-button type="primary" @click="checkout">购买
                    </el-button>
                </div>
            </div>
 
            <!-- 购买表单 -->
            <el-dialog title="购买表单" :visible.sync="purchaseDialog" class="dialog" width="80%">
                <div>
                    <el-form ref="purchaseForm" :model="purchaseForm" label-width="100px">
                        
                        <el-form-item label="客户姓名：">
                            <el-input v-model="purchaseForm.cons_name"></el-input>
                        </el-form-item>
                        <el-form-item label="客户电话：">
                            <el-input v-model="purchaseForm.cons_phone"></el-input>
                        </el-form-item>
                        <el-form-item label="配送方式：">
                            <el-select v-model="purchaseForm.order_way" placeholder="请选择配送方式">
                                <el-option label="自提" value="自提"></el-option>
                                <el-option label="配送" value="配送"></el-option>
                            </el-select>
                        </el-form-item>

                        <!-- 根据配送方式显示不同的地址输入框 -->
                        <el-form-item label="配送地址：">
                            <el-input v-model="purchaseForm.cons_addre" 
                                      :disabled="purchaseForm.order_way === '自提'" 
                                      :placeholder="purchaseForm.order_way === '自提' ? '崇文路2号二手书店' : '请输入配送地址'">
                            </el-input>
                            <span v-if="purchaseForm.order_way === '自提'" style="color: #888;"></span>
                        </el-form-item>
                    </el-form>
                    <div>  
                        <h4>选购书籍：</h4>  
                        <el-table :data="purchaseForm.cartItems" style="width: 100%">  
                            <el-table-column prop="book_name" label="书籍名称" width="200"></el-table-column>  
                            <el-table-column prop="quantity" label="数量" width="100"></el-table-column>  
                        </el-table>  
                    </div>  
                    <div style="text-align: center;">
                        <el-button type="primary" @click="submitPurchase">
                            提交
                        </el-button>
                    </div>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.getdata();
    },
    data() {
        return {
            tableData: [],
            cartData: [], // 购物车数据
            purchaseDialog: false, // 购买表单显示状态
            purchaseForm: { // 购买表单数据
                cons_name: '',
                cons_addre: '',
                cons_phone: '',
                order_way: '', // 配送方式
                cartItems: [] // 新增字段，用于存储购物车中的书籍
            }
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/user/shop").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            });
        },
        addToCart(item) {
            const cartItem = this.cartData.find(c => c.book_name === item.book_name);
            if (cartItem) {
                cartItem.quantity += 1;
            } else {
                this.cartData.push({ ...item, quantity: 1 });
            }
        },
        removeFromCart(index) {
            this.cartData.splice(index, 1);
        },
        updateCartItem(index, quantity) {
            this.cartData[index].quantity = quantity;
        },
        checkout() {
            // 将购物车中的书籍信息传递到购买表单  
            this.purchaseForm.cartItems = this.cartData.map(item => ({  
                book_name: item.book_name,  
                quantity: item.quantity  
            }));  
            this.purchaseDialog = true;
        },
        submitPurchase() {
            // 如果是自提，固定地址为崇文路2号二手书店
            if (this.purchaseForm.order_way === '自提') {
                this.purchaseForm.cons_addre = '崇文路2号二手书店';
            }

            let orderData = {
                order_way: this.purchaseForm.order_way,
                cons_name: this.purchaseForm.cons_name,
                cons_phone: this.purchaseForm.cons_phone,
                cons_addre: this.purchaseForm.cons_addre,
                books: this.purchaseForm.cartItems.map(item => ({
                    book_name: item.book_name, 
                    quantity: item.quantity
                }))
            };
            
            // 提交购买表单，这里需要处理购买逻辑
            // 假设提交成功后清空购物车并重新获取店铺数据
            this.$axios.post("/api/user/addorder", orderData).then((res) => {
                console.log(res.data);
                if (res.data.status === 200) {
                    this.$message({
                        message: "购买成功",
                        type: "success"
                    });
                    this.purchaseDialog = false;
                    this.cartData = []; // 清空购物车
                    this.getdata(); // 重新获取店铺数据
                }
            });
        },
        goToBookImg(bookName) {
    this.$router.push({ path: `/bookimg/${bookName}` });
  }
    }
}
</script>

<style scoped>
.container {
  background: url("../assets/image/11.jpg");
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-size: cover; /* 新增属性，使背景图片占满整个屏幕 */
}

.left-panel, .right-panel {
    background-color: rgba(84, 114, 80, 0.45);
    width: 48%;
    box-sizing: border-box;
}

.left-panel .header {
    width: 100%;
    height: 40px;
    text-align: center;
    line-height: 40px;
    font-size: 18px;
    font-weight: bold;
    border-bottom: 1px solid #e3e3e3;
    margin-bottom: 20px;
}

.table-container {

    max-height: 550px;
    overflow-y: auto;
}

.right-panel .cart-container {
    margin-top: 0;
}

.cart-table {
    margin-bottom: 20px;
}

.dialog {
    width: 80%;
}
/* 透明化图书信息表格 */
.table-container .el-table {
    background-color: transparent 
}

/* 透明化购物车表格 */
.cart-container .el-table {
    background-color: transparent 
}
</style>
