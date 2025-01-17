import ...

def load_test_data(path):
    return pd.read_csv(path)

def load_model(model_path):
    return pickle.load(open(model_path, 'rb'))

def predict(model, test_data, output_path):
    feateres = ["Pclass", "Sex", "SibSp","Parch"]
    data = pd.get_dummies(test_data[feateres])
    predictons = model.predict(data)

    output = pd.DataFrames({'PassengerId': test_data.PassengerId, 'Survived': predictons})
    output.to_csv(f'{output_path}/predictions.csv', index=False)







