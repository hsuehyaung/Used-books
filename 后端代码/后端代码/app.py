# import caching as caching
from flask import Flask, jsonify, request
from sqlalchemy import text

from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
import auth
# from aliyunsms.sms_send import send_sms
import json
import random
import datetime
from redis import StrictRedis

# 创建redis对象
redis_store = StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, decode_responses=True)

# 跨域
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)

# 添加配置数据库
app.config.from_object(BaseConfig)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())



# 用户登录
@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def user_login():
    print(request.json)
    userortel = request.json.get("userortel").strip()
    password = request.json.get("password").strip()
    sql = ('select * ' \
           + 'from user ' \
           + 'where telephone = "{0}" and password = "{1}"').format(userortel, password)
    data = db.session.execute(text(sql)).first()
    print(data)
    if data != None:
        user = {'id': data[0], 'username': data[1], 'password': data[2], 'telephone': data[3]}
        # 生成token
        token = auth.encode_func(user)
        print(token)
        return jsonify({"code": 200, "msg": "登录成功", "token": token, "role": data[4]})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})





# 用户注册__检测验证码和手机是否在数据库中
@app.route("/api/user/findback", methods=["POST"])
@cross_origin()
def findback():
    rq = request.json
    # 获取验证码和手机号
    password = rq.get("password")
    vercode = rq.get("vercode")
    telephone = rq.get("telephone")

    if vercode != redis_store.get('valid_code:{}'.format(telephone)):
        return jsonify({"status": "1000", "msg": "验证码错误"})


# 用户注册__检测验证码和手机是否在数据库中
@app.route("/api/user/register/test", methods=["POST"])
@cross_origin()
def register_test():
    rq = request.json
    # 获取验证码和手机号
    username = rq.get("username")
    password = rq.get("password")
    vercode = rq.get("vercode")
    telephone = rq.get("telephone")

    # 先判断验证码对错
    if vercode != redis_store.get('valid_code:{}'.format(telephone)):
        return jsonify({"status": "1000", "msg": "验证码错误"})

    data = db.session.execute(text('select * from user where telephone="%s"' % telephone)).fetchall()
    if not data:
        db.session.execute(text('insert into user(username,password,telephone,role) value("%s","%s","%s",0)' % (
            username, password, telephone)))
        db.session.commit()
        return jsonify({"status": "200", "msg": "注册成功"})
    else:
        return jsonify({"status": "1000", "msg": "该用户已存在"})


# 用户界面获取店铺信息
@app.route("/api/user/shop", methods=["GET"])
@cross_origin()
def user_get_shop():
    data = db.session.execute(text('select * from book_shop')).fetchall()

    Data = []
    for i in range(len(data)):
        dic = dict(book_name=data[i][0], price=data[i][2], sale=data[i][3])
        Data.append(dic)
    print(Data)
    # return jsonify({"status":"200", "tabledata": Data})
    return jsonify(status=200, tabledata=Data)


# 下订单
@app.route("/api/user/addorder", methods=["POST"])
@cross_origin()
def user_addorder():
    rq = request.json

    # 获取请求中的各个参数
    orderway = rq.get("order_way")
    consphone = get_token_phone(request.headers.get('token'))
    consname = rq.get("cons_name")
    consaddre = rq.get("cons_addre")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 假设书籍信息包含在请求的“books”字段里, 每本书包含isbn和quantity
    books = rq.get("books", [])  # 示例：[{"isbn": "12345", "quantity": 2}, {"isbn": "67890", "quantity": 1}]

    # 插入订单到 oorder 表
    db.session.execute(text(
        'insert into oorder( order_way, cons_phone, cons_name, cons_addre,create_time) value("%s", "%s", "%s", "%s","%s")' % (
            orderway, consphone, consname, consaddre, create_time)))
    db.session.flush()  # 刷新会话以获取生成的 ID，但不提交事务


    # 获取插入的订单的order_id
    order_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).fetchone()[0]

    # 插入每本书籍到 order_book 表
    for book in books:
        book_name = book.get('book_name')
        quantity = book.get('quantity')


        db.session.execute(text(
            'insert into order_book( order_id, book_name, quantity) value("%d", "%s", "%d")' % (
                order_id, book_name, quantity)))
    db.session.commit()
    # 提交事务


    return jsonify(status=200, msg="成功下单")




def get_token_phone(token):
    data = auth.decode_func(token)
    phone = data['telephone']
    return (phone)


@app.route("/api/user/unsend", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_unsend():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        print(phone)
        data = db.session.execute(text('select * from oorder where checked=0 and cons_phone="%s"' % phone)).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], orderway=data[i][1],
                       cons_name=data[i][3], cons_addre=data[i][4], create_time=data[i][6])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get("order_id")
        cons_name = rq.get("cons_name")
        cons_addre = rq.get("cons_addre")
        print(order_id)
        db.session.execute(
            text('update oorder set cons_name="%s", cons_addre="%s" where order_id="%d"' % (cons_name, cons_addre, order_id)))
        db.session.commit()
        return jsonify(status=200, msg="修改成功")
    if request.method == 'DELETE':
        order_id = request.json.get("delete_id")
        db.session.execute(text('delete from oorder where order_id="%d" ' % order_id))
        db.session.commit()
        return jsonify(status=200, msg="删除成功")


@app.route("/api/user/sending", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_sending():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))

        data = db.session.execute(text('select * from sending_order where cons_phone="%s"' % phone)).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], order_way=data[i][1],
                       cons_phone=data[i][2],
                       cons_name=data[i][3], cons_addre=data[i][4], disp_id=data[i][5], deliver_time=data[i][6],
                       disp_phone=data[i][7])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/user/sended", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_sended():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute(text('select * from sended_order where cons_phone="%s"' % phone)).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], order_way=data[i][1],
                       cons_phone=data[i][2],
                       cons_name=data[i][3], cons_addre=data[i][4], disp_id=data[i][5], deliver_time=data[i][6],
                       disp_phone=data[i][7])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/user/usermsg", methods=["POST", "GET"])
@cross_origin()
def usermsg():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute(text('select * from user_msg where phone="%s"' % phone)).fetchall()
        Data = dict(real_name=data[0][1], sex=data[0][2], age=data[0][3], mail=data[0][4], phone=data[0][5],
                   user_name=data[0][6])

        return jsonify(status=200, data=Data)


@app.route("/api/user/pwd_chg", methods=["POST"])
@cross_origin()
def user_pwd_chg():
    if request.method=='POST':
        pwd=request.json.get('new_pwd')
        old_pwd=request.json.get('old_pwd')
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute(text('select * from user where telephone="%s" and password="%s"'% (phone,old_pwd))).fetchall()
        if not data:
            return jsonify(status=1000,msg="原始密码错误")
        else:
            db.session.execute(text('update user set password="%s" where telephone="%s"'% (pwd,phone)))
            db.session.commit()
            return jsonify(status=200,msg="修改成功")


@app.route("/api/manager/shop", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_shop():
    # 获取店铺信息
    if request.method == 'GET':
        data = db.session.execute(text('select * from book_shop')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(book_name=data[i][0], ISBN=data[i][1], price=data[i][2], sale=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST' and request.json.get('action') == "add":
        rq = request.json
        book_name = rq.get('book_name')
        ISBN = rq.get('ISBN')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        exist = db.session.execute(text('select * from book_shop where book_name="%s"' % book_name)).fetchall()
        if not exist:
            db.session.execute(text('insert book_shop(book_name,ISBN,price,m_sale_v) value("%s","%s",%d,%d)' % (
                book_name, ISBN, int(price), int(m_sale_v))))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该店铺已存在")

    if request.method == 'POST' and request.json.get('action') == "change":
        rq = request.json
        book_name = rq.get('book_name')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        db.session.execute(text('update book_shop set price="%d", m_sale_v="%d" where book_name="%s" ' % (
            int(price), int(m_sale_v), book_name)))
        db.session.commit()
        return jsonify(status=200, msg="修改成功")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute(text('delete from book_shop where book_name="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="删除成功")





@app.route("/api/manager/dispatcher", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_dispatcher():
    if request.method == 'GET':
        data = db.session.execute(text('select * from dispatcher')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(dispatcher_id=data[i][0], dispatcher_name=data[i][1], dispatcher_phone=data[i][2])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST':
        rq = request.json
        dispatcher_id = rq.get('dispatcher_id')
        dispatcher_name = rq.get('dispatcher_name')
        dispatcher_phone = rq.get('dispatcher_phone')
        exist = db.session.execute(text('select * from dispatcher where dispatcher_id="%s"' % dispatcher_id)).fetchall()
        if not exist:
            db.session.execute(
                text('insert dispatcher(dispatcher_id,dispatcher_name,dispatcher_phone) value("%s","%s","%s")' % (
                    dispatcher_id, dispatcher_name, dispatcher_phone)))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该编号已存在")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute(text('delete from dispatcher where dispatcher_id="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="解雇成功")


@app.route("/api/manager/wuliu", methods=["GET"])
@cross_origin()
def manager_wuliu():
    ended = request.args.get('id')
    if ended == '0':
        data = db.session.execute(text('select * from wuliu where ended=0')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    else:
        data = db.session.execute(text('select * from wuliu where ended=1')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/manager/unsend", methods=["GET", "POST"])
@cross_origin()
def manager_unsend():
    if request.method == 'GET':
        data = db.session.execute(text('select * from oorder where checked=0')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], orderway=data[i][1],
                       cons_phone=data[i][2],
                       cons_name=data[i][3], cons_addre=data[i][4], create_time=data[i][6])
            Data.append(dic)

        disp_range = db.session.execute(text('select * from dispatcher')).fetchall()  # 获取所有的送货员就id，供选择
        Disp_range = []
        for i in range(len(disp_range)):
            dic = dict(disp_id=disp_range[i][0])
            Disp_range.append(dic)
        return jsonify(status=200, tabledata=Data, disp_range=Disp_range)
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get('order_id')
        disp_id = rq.get('dispatcher_id')
        deliver_time = rq.get('deliver_time')

        cons_phone = db.session.execute(text('select cons_phone from oorder where order_id="%d"' % int(order_id))).first()

        db.session.execute(text('insert wuliu( order_id, cons_phone,disp_id,deliver_time) value(%d,"%s","%s","%s")' % (
        int(order_id), cons_phone[0], disp_id, deliver_time)))
        db.session.execute(
            text('UPDATE oorder SET checked = 1  WHERE order_id = :order_id'),
            {'order_id': order_id}
        )
        db.session.commit()
        return jsonify(status=200, msg="成功派发")

@app.route("/api/manager/sending", methods=["GET", "POST"])
@cross_origin()
def manager_sending():
    if request.method == 'GET':
        data = db.session.execute(text('select * from sending_order')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], order_way=data[i][1],
                       cons_phone=data[i][2],
                       cons_name=data[i][3], cons_addre=data[i][4], disp_id=data[i][5], deliver_time=data[i][6])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST':
        # 获取要结束的订单id，这里假设前端传递过来的数据中包含order_id字段来指定要结束的订单
        rq = request.json
        order_id = rq.get('order_id')

        # 执行数据库更新操作，将oorder表中对应订单的checked字段更新为2，表示结束订单
        db.session.execute(
            text('UPDATE oorder SET checked = 2 WHERE order_id = :order_id'),
            {'order_id': order_id}
        )
        db.session.execute(
            text('UPDATE wuliu SET ended = 1 WHERE order_id = :order_id'),
            {'order_id': order_id}
        )
        db.session.commit()

        return jsonify(status=200, msg="订单已成功结束")


@app.route("/api/manager/sended", methods=["GET"])
@cross_origin()
def manager_sended():
    if request.method == 'GET':
        data = db.session.execute(text('select * from sended_order')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], order_way=data[i][1],
                       cons_phone=data[i][2],
                       cons_name=data[i][3], cons_addre=data[i][4], disp_id=data[i][5], deliver_time=data[i][6])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
@app.route("/api/user/book/<string:book_name>", methods=["GET"])
def get_book_info(book_name):
    query = text("SELECT * FROM book_shop WHERE book_name = :book_name")
    data = db.session.execute(query, {'book_name': book_name}).fetchall()
    if data:
        book_info = {
            "book_name": data[0][0],
            "ISBN": data[0][1],
            "price": data[0][2],
            "m_sale_v": data[0][3],
            "book_img": data[0][4]
        }
        return jsonify(book_info)
    else:
        return jsonify({"message": "Book not found"}), 404
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
    # 开启了debug模式
