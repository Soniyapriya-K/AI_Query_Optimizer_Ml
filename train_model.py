import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Sample training dataset
data = {
    'joins': [0, 1, 2, 3, 1, 0, 2, 4],
    'has_where': [1, 1, 0, 1, 0, 1, 1, 0],
    'has_orderby': [0, 1, 1, 1, 0, 0, 1, 1],
    'select_all': [0, 1, 1, 1, 0, 0, 1, 1],
    'like_wildcard': [0, 1, 0, 1, 0, 0, 1, 1],
    'query_length': [40, 120, 150, 300, 60, 50, 200, 400],
    'performance': [
        'Fast',
        'Moderate',
        'Slow',
        'Slow',
        'Fast',
        'Fast',
        'Moderate',
        'Slow'
    ]
}

# Convert to dataframe
df = pd.DataFrame(data)

# Features and labels
X = df.drop('performance', axis=1)
y = df['performance']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Create model folder
os.makedirs('model', exist_ok=True)

# Save trained model
joblib.dump(model, 'model/query_model.pkl')

print("Model trained successfully.")