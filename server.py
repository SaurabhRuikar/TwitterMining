from flask import Flask,render_template,request
from control_transfer import Transfer
import mysql_backend_connector
import pandas as pd
app=Flask(__name__,static_url_path="/static")
handle=Transfer()
connector=mysql_backend_connector.MysqlBackendConnector("cybersec","root","1497")
report_df=""
def color_cat(data):
    is_in=data.isin(("Offensive","Cyber Bullying"))
    return ["background-color:red" if d else '' for d in is_in]
def color_cat1(data):
    is_in=data.isin(["Normal"])
    return ["background-color:brown" if d else '' for d in is_in]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/insert")
def insert_tweets():
    global report_df
    tweets_pair=[]
    for data in zip(report_df.iloc[:,0],report_df.iloc[:,1]):
        tweets_pair.append(data)
    connector.insert_tweets(tweets_pair)
    #return "<body bgcolor='brown'><h1 align='center'>Successfully inserted</h1></body>"
    return render_template("inserted.html")

@app.route("/index_html")
def inserted():
    return render_template("index_.html")

@app.route("/delete")
def delete():
    connector.reset_table()
    #return "<body bgcolor='brown'><h1 align='center'>Successfully cleared</h1></body>"
    return render_template("cleared.html")
    
@app.route("/analyze",methods=['GET','POST'])
def classify():
    global report_df
    data=request.form
    mode=data['mode']
    user_data=data['data']
    if mode=='query':
        user_data=user_data.split(',')
    handle.set_mode(mode)
    show_data=handle.fetch_predict(user_data)
    pd.set_option('display.max_colwidth',-1)
    report_df=show_data[show_data['Prediction'].isin(['Offensive','Cyber Bullying'])]
    return render_template("show.html",data=show_data.style.apply(color_cat,subset=['Prediction']).apply(color_cat1,subset=['Prediction']).render())

@app.route("/log")
def show_logs():
    dataframe=connector.retrieve_tweets()
    return render_template("reported.html",data=dataframe.style.apply(color_cat,subset=['Categories']).apply(color_cat1,subset=['Categories']).render())
@app.route("/report")
def report():
    global report_df
    return render_template("report.html",data=report_df.style.apply(color_cat,subset=['Prediction']).apply(color_cat1,subset=['Prediction']).render())

@app.route("/signup_page")
def signup_page():
    return render_template("signup.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    if connector.login(request.form['username'],request.form['password']):
        return render_template("index_.html")
    else:
        #return "<h1>Error</h1>"
        return render_template("login.html",error=True)

@app.route("/signup",methods=["GET","POST"])
def signup():
    data=request.form
    connector.signup(data['username'],data['password'],data['email'],data['contact'])
    return render_template("login.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")




if __name__=='__main__':
    app.run(debug=True)