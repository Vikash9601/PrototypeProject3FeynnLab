from flask import Flask, render_template,request
import joblib,pickle
import numpy as np
from sklearn.preprocessing import PolynomialFeatures

app = Flask(__name__,template_folder="templates")

def featureEng(age,tenure):
    age=int(age)
    tenure=int(tenure)
    ageclass=""
    seniority=""
    if age<=35:
        ageclass='young'
    elif (age> 35) & (age < 55):
        ageclass='middle_aged'
    else:
        ageclass='senior'

    if(tenure<=2):
        seniority='new'
    elif tenure>2 and tenure<=6:
        seniority='intermediate'
    else:
        seniority='long-standing'

    return [ageclass,seniority]

                                              
    
                           
                      


def modelpipeline(crdscore,age,tenure,balance,prods,crcdis,IAM,sal,gender):
    tenurebyage=int(tenure)/int(age)
    credscgivenage=int(crdscore)/int(age)
    gender_male=0
    gender_female=0
    age_class_young=0
    age_class_middle_aged=0
    age_class_senior=0
    seniority_intermediate=0
    seniority_new=0
    seniority_long_standing=0

    lst=featureEng(age,tenure)
    if crcdis==0:
        crcdis=-1
    if IAM==0:
        IAM=-1
    if gender=='Male':
        gender_male=1
        gender_female=-1
    else:
        gender_male=-1
        gender_female=1

    if lst[0]=='young':
        age_class_young=1
        age_class_middle_aged=-1
        age_class_senior=-1
    elif lst[0]=='middle_aged':
        age_class_young=-1
        age_class_middle_aged=1
        age_class_senior=-1
    else:
        age_class_young=-1
        age_class_middle_aged=-1
        age_class_senior=1

    if lst[1]=='new':
        seniority_new=1
        seniority_intermediate=-1
        seniority_long_standing=-1
    elif lst[1]=='intermediate':
        seniority_new=-1
        seniority_intermediate=1
        seniority_long_standing=-1
    else:
        seniority_new=-1
        seniority_intermediate=-1
        seniority_long_standing=1

    lst=featureEng(age,tenure)

    val=np.array([crdscore,age,tenure,balance,prods,sal,tenurebyage,credscgivenage]).reshape(-1,8)
    scaler = joblib.load('your_scaler.pkl')
    scaledvalue=scaler.transform(val)
    dummy_vars=[crcdis,IAM,gender_male,gender_female,age_class_middle_aged,age_class_young,age_class_senior,seniority_intermediate,seniority_new,seniority_long_standing]
    npArray=np.array(dummy_vars)
    x_test=np.hstack([scaledvalue,npArray.reshape(1,-1)])
    # newans=[scaledvalue.shape,npArray.shape]

    model=joblib.load('SVM_rbf.pkl')

    ans=model.predict_proba(x_test)
    ans=(model.predict_proba(x_test)[:, 1] >= 0.30).astype(int)
    return ans  


@app.route("/")
def index():
    return render_template('demo.html')




@app.route("/submit", methods=["POST"])

def submit():
    if request.method == "POST":
        crdscore = request.form["credit_score"]
        age = request.form["age"]
        gender = request.form["gender"]
        tenure = request.form["tenure"]
        balance = request.form["balance"]
        prods = request.form["prods"]
        crcdis = request.form.get("crcdisyesno")
        IAM = request.form.get("activeyesno")
        sal = request.form["sal"]

        ans=modelpipeline(crdscore,age,tenure,balance,prods,crcdis,IAM,sal,gender)
        return render_template('demo.html', predictions=ans)



if __name__ == "__main__":
    app.run(debug=True)
