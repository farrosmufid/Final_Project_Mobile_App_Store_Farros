from flask import Flask, render_template, request
import joblib
import pickle
import pandas as pd

app = Flask(__name__)

# home page
@app.route('/')
def home():
    return render_template('index.html')

# base page
@app.route('/base', methods = ['POST', 'GET'])
def base():
    return render_template('base.html')

# predict page
@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    return render_template('predict.html')

# eda page
@app.route('/eda', methods = ['POST', 'GET'])
def eda():
    return render_template('eda.html')

# dataset page
@app.route('/dataset', methods = ['POST', 'GET'])
def dataset():
    return render_template('dataset.html')

# result page
@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        input = request.form

        isNotFree = 0

        if float(input['price']) > 0:
            isNotFree = 1

        vpp_value = 0

        if int(input['vpp']) == 1:
            vpp_value = 1

        df_predict = pd.DataFrame({
           'size_bytes_in_MB': [input['size']],
           'isNotFree':[isNotFree],
           'price': [input['price']],
           'sup_devices.num':[input['num_sup_devices']],
           'ipadSc_urls.num':[input['num_screenshots']],
           'lang.num' : [input['num_languages']],
           'vpp_lic' : [vpp_value],
           'prime_genre': [input['prime_genre']],
           'cont_rating': [input['cont_rating']]
         })

        filename = 'Mobile App Store Model.sav'

        model = pickle.load(open(filename,'rb'))

        prediction = model.predict_proba(df_predict)[0][1]

        if prediction > 0.5:
            result = "good app"
        else:
            result = "bad app"

        #return render_template('result.html', data=input, pred=result)
        return render_template('result.html', data=input, pred=result, prob=prediction)

if __name__ == "__main__":
    filename = 'Mobile App Store Model.sav'
    model = pickle.load(open(filename,'rb'))

    app.run(debug=True)

# export FLASK_APP=dash.py
# export FLASK_DEBUG=ON 