import uuid
from datetime import datetime
import os

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def load_training_data(path):
    return.pd.read_csv(path)

def train_model(train_data, model_path):
    y = train_data["Survived"]
    
    features = ["Pclass", "Sex", "SibSp", "Parch"]
    X = pd.get_dummies(train_data[features])
    
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    model.fit(X_train,y_train)
    if not os.path.isdir(model_path):
        os.mkdir(model_path)
    pickle.dump(model, open(f'{model_path}/model.pkl','wb'))



