from flask import Flask,render_template,request
from control_transfer import Transfer
import pandas as pd
app=Flask(__name__)
handle=Transfer()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze",methods=['GET','POST'])
def classify():
    data=request.form
    mode=data['mode']
    user_data=data['data']
    handle.set_mode(mode)
    show_data=handle.fetch_predict(user_data)
    pd.set_option('display.max_colwidth',-1)
    return render_template("show.html",data=show_data.to_html())
if __name__=='__main__':
    app.run()