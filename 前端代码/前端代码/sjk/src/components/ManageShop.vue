<template>
    <div>
        <div class="header">
            图书管理
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 89%" class="table">
                <el-table-column prop="book_name" label="图书名称" width="200" align="center">
                </el-table-column>
                <el-table-column prop="price" label="产品单价" width="200" align="center">
                </el-table-column>
                <el-table-column prop="sale" label="库存" width="200" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="操作" width="200" align="center">
                    <template slot-scope="scope">
                        <el-button size="small" type="warning" @click="showdia_chg(scope.row)">修改
                        </el-button>

                        <el-button size="small" type="danger" @click="showdia_dlt(scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column width="120" align="center">
                    <template slot="header">
                        <el-button icon="el-icon-plus" size="small" type="success" @click="showdia_add()">添加图书
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-dialog title="添加图书" :visible.sync="dia_add" width="30%">
                <el-form ref="add_form" :model="add_form" label-width="100px" :rules="add_form_rules">
                    <el-form-item label="图书名称：" prop="book_name">
                        <el-input v-model="add_form.book_name"></el-input>
                    </el-form-item>
                    <el-form-item label="ISBN：" prop="ISBN">
                        <el-input v-model="add_form.ISBN"></el-input>
                    </el-form-item>
                    <el-form-item label="产品单价：" prop="price">
                        <el-input v-model="add_form.price"></el-input>
                    </el-form-item>
                    <el-form-item label="库存：" prop="m_sale_v">
                        <el-input v-model="add_form.m_sale_v"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="addshop()">
                        添加
                    </el-button>
                </div>
            </el-dialog>

            <el-dialog title="修改图书" :visible.sync="dia_chg" width="30%">
                <el-form ref="form" :model="chg_form" label-width="100px">
                    <el-form-item label="图书名称：">
                        <span>{{ chg_form.book_name }}</span>
                    </el-form-item>
                    <el-form-item label="ISBN：">
                        <span>{{ chg_form.ISBN }}</span>
                    </el-form-item>
                    <el-form-item label="产品单价：">
                        <el-input v-model="chg_form.price"></el-input>
                    </el-form-item>
                    <el-form-item label="库存：">
                        <el-input v-model="chg_form.m_sale_v"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="changeshop()">
                        修改
                    </el-button>
                </div>
            </el-dialog>
            <el-dialog title="删除图书" :visible.sync="dia_dlt" width="30%">
                <div>
                    确定删除此图书吗？
                </div>
                <div style="text-align: center;">
                    <el-button type="primary" @click="deleteshop()">
                        确定
                    </el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.getdata()
    },
    data() {
        return {
            tableData: [],
            dia_add: false,
            dia_chg: false,
            dia_dlt: false,
            add_form: {
                book_name: '',
                ISBN: '',
                price: '',
                m_sale_v: '',
                action: "add",
            },
            chg_form: {
                book_name: '',
                ISBN: '',
                price: '',
                m_sale_v: '',
                action: "change",
            },
            want_delete: '',
            add_form_rules: {
                book_name: [{ required: true, message: '必填项', trigger: 'blur' }],
                ISBN: [{ required: true, message: '必填项', trigger: 'blur' }],
                price: [{ required: true, message: '必填项', trigger: 'blur' }],
                m_sale_v: [{ required: true, message: '必填项', trigger: 'blur' }]

            }
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/shop").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            })
        },
        showdia_add() {
            this.dia_add = true;
        },
        addshop() {
            this.$refs.add_form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    this.$axios.post("/api/manager/shop", this.add_form).then((res) => {
                        console.log(res.data);
                        if (res.data.status == 200) {
                            this.$message({
                                message: "添加成功",
                                type: "success"
                            })
                            this.dia_add = false;
                            this.getdata();
                        } else {
                            this.$message({
                                message: res.data.msg,
                                type: "error"
                            })
                        }
                    })
            })


        },
        showdia_chg(row) {
            this.chg_form.book_name = row.book_name;
            this.chg_form.ISBN = row.ISBN;
            this.chg_form.price = row.price;
            this.chg_form.m_sale_v = row.sale;
            this.dia_chg = true;
        },
        changeshop() {
            this.$axios.post("/api/manager/shop", this.chg_form).then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.$message({
                        message: "修改成功",
                        type: "success"
                    })
                    this.dia_chg = false;
                    this.getdata();
                }
            })
        },
        showdia_dlt(row) {
            this.want_delete = row.book_name;
            this.dia_dlt = true;
        },
        deleteshop() {
            this.$axios.delete("/api/manager/shop", { data: { want_delete: this.want_delete } }).then((res) => {
                if (res.data.status == 200) {
                    this.$message({
                        message: res.data.msg,
                        type: "success"
                    })
                    this.getdata()
                    this.dia_dlt = false;
                }
            })
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

    width: 80%;
    margin: auto;
    margin-top: 30px;
}
</style>