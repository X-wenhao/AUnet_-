from flask import Flask,jsonify,request

app=Flask(__name__)

@app.route('/test',methods=['POST'])
def test():
    data=request.get_json()
    print(data[0])
    return 'hello'

@app.route('/test',methods=['GET'])
def test1():

    data=[{
        '协ji':[{'name':'213'}]
    }]

    return jsonify(data)


if __name__=="__main__":
    app.run(debug=True)