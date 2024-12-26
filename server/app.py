from flask import Flask, request, render_template
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np

app = Flask(__name__)

# Load the scaler and models


with open('scaled_all.pkl', 'rb') as f:
    scaled_all = pickle.load(f)

with open('scaled_batsmen.pkl', 'rb') as f:
    scaled_batsmen = pickle.load(f)

with open('scaled_bowl.pkl', 'rb') as f:
    scaled_bowl= pickle.load(f)

with open('allrounder.pkl', 'rb') as f:
    allroundermodel = pickle.load(f)

with open('batsmen.pkl', 'rb') as f:
   batsmenmodel = pickle.load(f)

with open('bowler.pkl', 'rb') as f:
    bowlermodel = pickle.load(f)
#x_batsmen = df_batsmen[["RUNS","MAT","INNS","4S","50"]]
#x_all = df_allrounder1[[" Wicket"," RUNS"," MAT"," INNS"]]
#x_bowl = df_bowler1[[" Wicket"," MAT"," INNS"," NO"]]
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/batsman', methods=['POST'])
def batsmen():
    try:

        return render_template('batsman.html' )

    except Exception as e:
        return f"Error: {str(e.with_traceback())}"
@app.route('/bowler', methods=['POST'])
def bowler():
    try:

        return render_template('bowler.html' )

    except Exception as e:
        return f"Error: {str(e.with_traceback())}"
@app.route('/allrounder', methods=['POST'])
def allrounder():
    try:

        return render_template('allrounder.html', )

    except Exception as e:
        return f"Error: {str(e.with_traceback())}"


@app.route('/batsman_predict', methods=['POST'])
def batsmen_prediction():
    try:
        user_input=[]
        if request.form['runs'].isdigit() and request.form['matches'].isdigit() and request.form['innings'].isdigit() and request.form['s4'] and request.form['s50'].isdigit():
            runs = float(request.form['runs'])
            match = float(request.form['matches'])
            innings = float(request.form['innings'])
            s4 = float(request.form['s4'])
            s50 = float(request.form['s50'])
            scaled_batsmen_input = scaled_batsmen.transform([[runs,match,innings,s4,s50]])
            prediction1 = batsmenmodel.predict(scaled_batsmen_input)[0]
            return render_template('result.html', predictions=int(prediction1[0]))
        else:
            return render_template('error_input.html', error_message="Please Enter valid input")
    except Exception as e:
        return f"Error: {str(e.with_traceback())}"
@app.route('/bowler_predict', methods=['POST'])
def bowler_prediction():
    try:

        if request.form['no'].isdigit() and request.form['matches'].isdigit() and request.form['innings'].isdigit() and request.form['wickets'].isdigit():
            no = float(request.form['no'])
            match = float(request.form['matches'])
            innings = float(request.form['innings'])
            wickets = float(request.form['wickets'])

            scaled_bowler_input = scaled_bowl.transform([[wickets,match,innings,no]])
            prediction2 = bowlermodel.predict(scaled_bowler_input)[0]
            return render_template('result.html', predictions=int(prediction2))
        else:
            return render_template('error_input.html', error_message="Please Enter valid input")
    except Exception as e:
        return f"Error: {str(e.with_traceback())}"

@app.route('/allrounder_predict', methods=['POST'])
def allrounder_prediction():
    try:
        user_input=[]
        if request.form['runs'].isdigit() and request.form['matches'].isdigit() and request.form['innings'].isdigit() and request.form['wickets'].isdigit():
            runs = float(request.form['runs'])
            match = float(request.form['matches'])
            innings = float(request.form['innings'])
            wickets = float(request.form['wickets'])

            scaled_all_input = scaled_all.transform([[ wickets, runs, match, innings]])
            prediction3 = allroundermodel.predict(scaled_all_input)[0]
            return render_template('result.html', predictions=int(prediction3))
        else:
            return render_template('error_input.html', error_message="Please Enter valid input")
    except Exception as e:
        return f"Error: {str(e.with_traceback())}"
if __name__ == '__main__':
    app.run(debug=True)

