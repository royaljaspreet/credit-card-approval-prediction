from flask import*
import sqlite3
import os
import pickle
import numpy as np
import sklearn

app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('loggedin'))
    else:
        return render_template("index.html")
@app.route('/loggedin')
def loggedin():
    if 'user_id' in session:
        return render_template("user.html")
    else:
        return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.pop("user_id")
    return redirect(url_for('index'))

    
@app.route('/signin')
def signin():
    return render_template('signin.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/team')
def team():
    return render_template('team.html')    

@app.route('/predict')
def predict():
    if 'user_id' in session:
        return render_template("predict.html")
    else:
        return redirect(url_for('index'))
        
@app.route('/validateSignup',methods = ['GET','POST'])
def validateSignup():
    msg = None
    r =""
    if request.method == 'POST':
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        if len(password)>=6:
            
            conn = sqlite3.connect("detailsDB.db")
            c = conn.cursor()
            r = c.execute("SELECT * FROM userdetail WHERE email = '"+email+"'")
            em =  "notem"
            for i in r :
                em = i
            if em == "notem":
                q = c.execute("SELECT * FROM userdetail WHERE username = '"+username+"'")
                us = "notus"
                for x in q:
                    us = x
                if us == "notus":
                    c.execute("INSERT INTO userdetail VALUES('"+email+"','"+username+"','"+password+"')")
                    conn.commit()
                    conn.close()
                    msg = "Account Created"
                    return render_template("signin.html", mssg = msg)
                else:
                    msg = "User Already exist"
                    return render_template("index.html",msg = msg)
            else:
                msg = "User Already exist"
                return render_template("index.html",msg = msg)
        else:   
            msg = "password >= 6"
            return render_template("signup.html",msg= msg)


    else:
        return redirect(url_for('index'))
@app.route('/validateSignin',methods = ['GET','POST'])
def validateSignin():
    msg = "Invalid Details "
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("detailsDB.db")
        c = conn.cursor()
        c.execute("SELECT * FROM userdetail WHERE email = '"+email+"' and password = '"+password+"'")
        r = c.fetchall()
        for i in r :
            if (email == i[0] and password == i[2]):
                username = i[1]
                session["loggedin"] = True
                session["user_id"] = username
                return redirect(url_for('loggedin'))
            else:
                break
        return render_template("signin.html" ,msg = msg )



    else:
        return redirect(url_for('index'))
@app.route('/validatepredict' ,methods=['GET','POST'])
def validatepredict():
    if request.method == 'POST':
        Age = int(request.form['Age'])
        if (Age < 18):
            msg = "you are under age"
            return render_template("predict.html",msg = msg)
        else:
            Debt = int(request.form['Debt'])
            EducationLevel = int(request.form['EducationLevel'])
            if (EducationLevel >13 or EducationLevel <0):
                mssg = "Choose b/w 0-13" 
                return render_template("predict.html",mssg = mssg)
            else:
                YearsEmployed = int(request.form['YearsEmployed'])
                Gender  = request.form['Gender']
                if (Gender == 'Male'):
                    Gender = 0
                else:
                    Gender = 1
                Income= int(request.form['Income'])
                PriorDefault = request.form['PriorDefault']
                if (PriorDefault=='yes') :
                    PriorDefault = 0
                else:
                    PriorDefault = 1
                Bankcustomer = request.form['Bankcustomer']
                if (Bankcustomer =='yes'):
                    Bankcustomer = 1
                else:
                    Bankcustomer = 0
                Married = request.form['Married']
                if (Married == 'yes'):
                    Married = 1
                else:
                    Married = 0
                Employed  = request.form['Employed']
                if (Employed == 'yes'):
                    Employed = 1
                else :
                    Employed = 0                    
                Citizen = request.form['IndianCitizen']
                if (Citizen == 'yes'):
                    Citizen = 2
                else:
                    Citizen = 0
                features  = [Gender,Age,Debt,Married,Bankcustomer,EducationLevel,YearsEmployed,PriorDefault,Employed,Citizen,Income]   
                final_features = [np.array(features)]
                print(final_features)
                model=pickle.load(open('LogisticRegression.pkl','rb'))
                prediction=model.predict(final_features)
                '''output=round(prediction[0],2)'''
                output = prediction
                if output == 0:
                    return render_template('result.html',prediction_text="Congratulations ! Your Credit Card Application is Approved")
                else:
                    return render_template('result.html',prediction_text="We regret to inform you that we cannot approve your application at this time")

    else:
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug = True)




                