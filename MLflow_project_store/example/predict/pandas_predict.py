import mlflow
logged_model = 'runs:/fd358f6f3f03496991c7c717f9a26488/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.

data = [[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1]]
import pandas as pd
result = loaded_model.predict(pd.DataFrame(data))

print(data)
print(pd.DataFrame(data).head())
print(result)