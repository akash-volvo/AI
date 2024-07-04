import warnings
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from scipy.optimize import minimize

warnings.filterwarnings("ignore")

# Load the data
data = pd.read_csv('demo.csv')

# Preprocess the data
X = data[['weight_context', 'weight_numeric', 'weight_class', 'weight_style', 'weight_attribute']]
y = data['success']

# Train a logistic regression model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Define the objective function for optimization
def objective(weights):
    prediction = model.predict_proba(np.array(weights).reshape(1, -1))[0, 1]
    regularization = 0.1 * np.sum(np.square(weights - 1 / len(weights)))  # Increase regularization strength
    return -prediction + regularization  # Maximize prediction, minimize regularization

# Define the constraint: weights must sum to 1
def constraint(weights):
    return np.sum(weights) - 1

# Initial guess for the weights
initial_weights = np.random.dirichlet(np.ones(5), size=1)[0]  # Use Dirichlet distribution for initial guess

# Bounds for the weights (e.g., between 0 and 1)
bounds = [(0, 1)] * 5

# Constraints dictionary
constraints = {'type': 'eq', 'fun': constraint}

# Optimize the weights to maximize the success probability
result = minimize(objective, initial_weights, bounds=bounds, constraints=constraints, method='SLSQP')

# Get the best weights
best_weights = result.x
best_success_probability = -result.fun + 0.1 * np.sum(np.square(best_weights - 1 / len(best_weights)))

print("Best Weights:")
for i in range(len(X.columns)):
    print(f"{X.columns[i]}: {best_weights[i]:.6f}")
