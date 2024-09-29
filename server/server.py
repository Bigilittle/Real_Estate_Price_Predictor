from flask import Flask, request, jsonify
import pandas as pd
import json
import joblib  
import dill


app = Flask(__name__)


pipeline = dill.load('../model/pipeline.pkl') 
model = dill.load('../model/model.pkl')  

@app.route('/add', methods=['POST'])
def add():
    features = json.loads(request.json)
    
    try:
        df = pd.DataFrame([features])
    except ValueError as e:
        return f"Error converting to DataFrame: {str(e)}", 400

    if df.empty:
        return 'DataFrame is empty or invalid', 400

    try:
        processed_df = pipeline.transform(df)
    except Exception as e:
        return f"Error applying pipeline: {str(e)}", 500

    try:
        prediction = model.predict(processed_df)
    except Exception as e:
        return f"Error predicting with model: {str(e)}", 500

    result = prediction[0]
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run('localhost', 8080)