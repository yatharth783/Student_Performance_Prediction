import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Realistic Synthetic Data Generation
def create_data():
    np.random.seed(42)
    n = 1000
    data = {
        'attendance': np.random.randint(60, 100, n),
        'study_hours': np.random.randint(5, 50, n),
        'prev_score': np.random.randint(40, 100, n),
        'participation': np.random.randint(20, 100, n),
        'backlogs': np.random.choice([0, 1, 2, 3], n, p=[0.7, 0.15, 0.1, 0.05])
    }
    df = pd.DataFrame(data)
    # Backend Logic: Final Score Calculation
    df['final_score'] = (df['prev_score'] * 0.4 + df['attendance'] * 0.25 + 
                         df['study_hours'] * 0.2 + df['participation'] * 0.15 - 
                         df['backlogs'] * 4 + np.random.normal(0, 2, n))
    df['final_score'] = df['final_score'].clip(0, 100)
    return df

df = create_data()
X = df.drop('final_score', axis=1)
y = df['final_score']

# Training a Robust Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model
joblib.dump(model, 'student_model.pkl')
print("Model saved as student_model.pkl")