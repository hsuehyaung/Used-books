<template>
    <div>
        <div class="header">
            已发货订单
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table" border>
                <el-table-column prop="order_id" label="订单编号" width="80" align="center">
                </el-table-column>
                <el-table-column prop="order_way" label="订购方式" width="100" align="center">
                </el-table-column>
                <el-table-column prop="cons_phone" label="收件人电话" width="150" align="center">
                </el-table-column>
                <el-table-column prop="cons_name" label="收件人姓名" width="100" align="center">
                </el-table-column>
                <el-table-column prop="cons_addre" label="收件地址" width="150" align="center">
                </el-table-column>
                <el-table-column prop="disp_id" label="送货员编号" width="120" align="center">
                </el-table-column>
                <el-table-column prop="deliver_time" label="预计送达时间" width="110" align="center">
                </el-table-column>
                <!-- 新增操作列，用于结束订单 -->
                <el-table-column label="操作" width="100" align="center">
                    <template slot-scope="scope">
                        <el-button type="danger" size="small" @click="finishOrder(scope.row.order_id)">结束订单</el-button>
                    </template>
                </el-table-column>
            </el-table>
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
        };
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/sending").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            });
        },
        // 新增方法，用于向后端发送请求结束订单
        finishOrder(orderId) {
            this.$axios.post("/api/manager/sending", { order_id: orderId }).then((res) => {
                console.log(res.data);
                if (res.data.status === 200) {
                    this.$message({
                        message: "订单已成功结束",
                        type: "success"
                    });
                    // 刷新数据列表，重新获取已发货订单数据
                    this.getdata();
                } else {
                    this.$message({
                        message: "结束订单失败，请稍后再试",
                        type: "error"
                    });
                }
            }).catch((error) => {
                console.error("结束订单请求出错:", error);
                this.$message({
                    message: "网络异常，结束订单操作出现问题，请检查网络或联系管理员",
                    type: "error"
                });
            });
        }
    }
}
</script>

<style scoped>
.header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
}

.body {
    width: 76%;
    margin: auto;
    margin-top: 30px;
}
</style>