from django.shortcuts import render, redirect
from .models import DiabetesPrediction
import pandas as pd
import pickle

cols = ["HighBP","HighChol","CholCheck","BMI","Smoker","Stroke","HeartDiseaseorAttack","PhysActivity","Fruits","Veggies","HvyAlcoholConsump","GenHlth","MentHlth","PhysHlth","DiffWalk","Sex","Age"]
inputCols = ["High Blood Pressure? (1 or 0)", "High Cholesterol? (1 or 0)", "Have you had a Cholesterol Check in the past 5 years? (1 or 0)", "BMI", "Have you smoked at least 100 cigarettes in your entire life? (1 or 0)", "Have you ever had a stroke? (1 or 0)", "Do you have coronary heart disease (CHD) or myocardial infarction (MI)? (1 or 0)", "Have you had any physical activity in the past 30 days? (1 or 0)", "Do you consume Fruit 1 or more times per day? (1 or 0)", "Do you consume Vegetables 1 or more times per day? (1 or 0)", "Are you a heavy drinker? (adult men: >14 drinks per week, adult women: >7 drinks per week) (1 or 0)", "Rate your general health (1-5)", "How many days in the previous month have you struggled with your mental health (0-30)", "How many days in the previous month have you struggled with your physical health (0-30)", "Do you have serious difficulty walking or climbing stairs? (1 or 0)", "Sex (female: 0, male: 1)", "Age (18-24: 1, 25-29: 2, 30-34: 3, 35-39: 4, 40-44: 5, 45-49: 6, 50-54: 7, 55-59: 8, 60-64: 9, 65-69: 10, 70-74: 11, 75-79: 12, 80+: 13)"]
random_forest_model = pickle.load(open('random_forest_model.pkl', 'rb'))

def predict_diabetes(request):
    if request.method == 'POST':
        user_input = request.POST.getlist('user_input[]')  # Assuming you're sending data as form POST
        user_input = [float(i) for i in user_input]
        user_data = pd.DataFrame([user_input], columns=cols)
        probability = random_forest_model.predict_proba(user_data)[:, 1][0]

        prediction = DiabetesPrediction.objects.create(user_input=user_input, probability=probability)
        prediction.save()

        return redirect('result', probability=str(probability))

    return render(request, 'diabetes_app/predict.html', {"cols": inputCols})

def result(request, probability):
    return render(request, 'diabetes_app/result.html', {'probability': float(probability)})