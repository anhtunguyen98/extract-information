from __future__ import print_function
from flask import Flask, render_template,request,json,redirect
from infer import ModelInfer
app = Flask(__name__)
model = ModelInfer()
@app.route('/',methods=['GET','POST'] )
def welcome():


    return render_template('Demo.html')


@app.route('/gen',methods=['POST'])
def vote():
    print("vote")
    text = request.get_json()["text"]
    st1,st2=model.res_sentence(text)
    text=""

    p='<p align="center" class="tag_{}">{} <br> {}</p>'

    for i in range(len(st2)):
        label=st2[i]
        word=st1[i]
        if label=="O":
            text += p.format(label, word, "")
        else:
            text+=p.format(label,word,label)


    text={'text':text}
    return json.dumps({'success': True, 'text_tagged': text}), 200, {'Content-Type': 'application/json; charset=UTF-8'}




if __name__=='__main__':
    test_sentence = "xe máy đi với tốc độ hơn 80 km/h bị phạt bao nhiều tiền"
    # test_sentence
    app.run(host='0.0.0.0',debug=False,port=5000)





