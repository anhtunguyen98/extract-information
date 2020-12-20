from __future__ import print_function
from flask import Flask, render_template,request,json,redirect
from infer import ModelInfer
import numpy as np
app = Flask(__name__)
model = ModelInfer()
@app.route('/',methods=['GET','POST'] )
def welcome():
    return render_template('test2.html')



definitions = {
    "A": "Hihihi",
    "AC": "Haha",
    "TV": "Nung cho ha m"
}

@app.route('/gen',methods=['POST'])
def vote():
    print("vote")
    text = request.get_json()["text"]
    st1,st2=model.res_sentence(text)
    print(st1)
    print(st2)
    text=""

    p='<mark data-entity="{}" d-entity="{}" class="radius_option" data-toggle="popover" title="{}" data-trigger="hover" data-content="{}">{}</mark>'

    for i in range(len(st2)):
        label=st2[i]
        word=st1[i]
        if label=="O":
            text += ' ' + word
        else:
            text+=p.format(label,label,label, definitions.get(label) if label in definitions.keys() else "kimochi",word)

    

    text={'text':text}

    if 'O' in st2:
        st2.remove('O')
    unique, counts = np.unique(st2, return_counts=True)
    c = [str(x) for x in counts] 
    t = dict(zip(unique, c))
    print(text)
    print(t)
    return json.dumps({'success': True, 'text_tagged': text, 'tags':t}), 200, {'Content-Type': 'application/json; charset=UTF-8'}




if __name__=='__main__':
    test_sentence = "xe máy đi với tốc độ hơn 80 km/h bị phạt bao nhiều tiền"
    # test_sentence
    app.run(host='localhost',debug=False,port=8080)





