from . import fd,db
from .models import Fd_data,Fc_data,Book
from flask import request,jsonify,abort
from .views import auth

'''
所有操作均在login状态下执行，假设用户传递正确的参数
api相关信息见api文档
'''

def get_url_args():
    '''
    获取url查询参数
    :return: []
    '''
    args_dict={}
    args_dict['organization']=request.args.get("organization")
    args_dict['type']=request.args.get("type")
    args_dict['time']=request.args.get('time')

    return args_dict

def data_to_data_dict(data):
    '''
    将data参数转化为参数字典
    无name参数
    :param data: Fc_data or Fd_data
    :return: []
    '''
    data_dict = {}
    data_dict['time'] = data.time
    data_dict['details'] = data.details
    data_dict['income'] = data.income
    data_dict['outcome']=data.outcome
    data_dict['balance']=data.balance
    data_dict['other']=data.other
    return data_dict

@fd.route('/api/v1/financial-disclosure/datas',methods=['GET'])
@auth.login_required
def datas_get():
    args_dict=get_url_args()
    query_table=None

    #确定查询对象
    if args_dict['organization']=='financial-department':
        query_table=Fd_data
    elif args_dict['organization']=='financial-commision':
        query_table=Fc_data
    else:
        return abort(404)

    #查询并按照拼音排序
    data_list=query_table.query.filter_by(time=args_dict['time'])\
        .order_by(query_table.name_pinyin).all()

    resp={}
    for data in data_list:
        data_dict=data_to_data_dict(data)
        if resp.get(data.name):
            resp[data.name].append(data_dict)
        else:
            resp[data.name]=[]

    res=[]
    res.append(resp)
    return jsonify(res)

@fd.route('/api/v1/financial-disclosure/datas',methods=['POST'])
@auth.login_required
def datas_post():
    args_dict = get_url_args()
    query_table = None
    if args_dict['organization'] == 'financial-department':
        query_table = Fd_data
    elif args_dict['organization'] == 'financial-commision':
        query_table = Fc_data
    else:
        pass

    #api设计为传递[{}],为了和GET相同，未设计为{}
    data=request.get_json()[0]
    print(data)
    data_name=list(data.keys())[0]
    print(data_name)
    for data_dict in data[data_name]:
        print(data_dict)
        data_commit=query_table(name=data_name,
                                details=data_dict['details'],
                                time=data_dict['time'],
                                income=data_dict['income'],
                                outcome=data_dict['outcome'],
                                balance=data_dict['balance'],
                                other=data_dict['other'])
        if data_commit.is_existance():
            abort(400)
        else:
            db.session.add(data_commit)
    db.session.commit()
    return ('',200)


@fd.route('/api/v1/financial-disclosure/books',methods=['GET'])
@auth.login_required
def books_get():
    args_dict={}
    args_dict['organization'] = request.args.get('organization')

    data_list=Book.query.filter_by(organization=args_dict["organization"]).all()

    if not data_list:
        abort(404)

    resp={}
    i=1
    for data in data_list:
       index=str(i)
       resp[index]=data.time

    return jsonify(resp)

@fd.route('/api/v1/financial-disclosure/books',methods=['POST'])
@auth.login_required
def books_post():
    args_dict=get_url_args()

    #POST/DELETE/UPGRADE均并入POST，判断method
    method=request.headers.get("request-method")

    if method=='POST':
        book=Book(organization=args_dict['organization'],time=args_dict['time'])
        if book.is_existance():
            db.session.add(book)
            db.session.commit()
        else:
            abort(400)

    elif method=='DELETE':
        book=Book(organization=args_dict['organization'],time=args_dict['time'])
        if book.is_existance():
            db.session.remove(book)
            db.session.commit()
        else:
            abort(404)

    return ('',200)











