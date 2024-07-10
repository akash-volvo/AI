import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from scipy.optimize import minimize
from authenticate import *

# Fetch all documents and extract unique tags from 'old' elements
unique_tags = set()
documents = results_collection.find({}, {'old.tag': 1})

for doc in documents:
    if 'old' in doc and doc['old'] is not None:
        tag = doc['old'].get('tag')
        if tag:
            unique_tags.add(tag)

# Convert the set to a sorted list
unique_tags = sorted(unique_tags)

for tag in unique_tags:
    # Fetch documents and extract weights and success labels
    weights_list = []
    success_list = []

    # Query to filter documents where 'old.tag' is the specific tag
    query = {
        'old.tag': tag,
    }

    # Projection to only fetch necessary fields
    projection = {
        'correct_prediction': 1,
        'weights': 1
    }

    # Fetch documents from the results_collection
    documents = results_collection.find(query, projection)

    # Extract weights and success labels from documents
    for doc in documents:
        if 'weights' in doc and 'correct_prediction' in doc:
            weights = doc['weights']
            correct_prediction = doc['correct_prediction']
            
            # Add weights and corresponding success label to lists
            weights_list.append(weights)
            success_list.append(1 if correct_prediction == 'y' else 0)

    # Create DataFrame for X (weights) and Series for y (success labels)
    X = pd.DataFrame(weights_list)
    y = pd.Series(success_list, name='success')

    # Check for NaN values in X and handle them with SimpleImputer
    if X.isnull().any().any():
        print(f"NaN values detected in data for tag '{tag}'. Applying imputation...")
        imputer = SimpleImputer(strategy='mean')
        X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

    # Train a logistic regression model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    
    # Check if there are samples of both classes (y and n) in the training set
    if len(set(y_train)) == 1:
        print(f"Not enough class variability for tag '{tag}'. Skipping...")
        continue

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
    initial_weights = np.random.dirichlet(np.ones(X.shape[1]), size=1)[0]  # Use Dirichlet distribution for initial guess

    # Bounds for the weights (e.g., between 0 and 1)
    bounds = [(0, 1)] * X.shape[1]

    # Constraints dictionary
    constraints = {'type': 'eq', 'fun': constraint}

    # Optimize the weights to maximize the success probability
    result = minimize(objective, initial_weights, bounds=bounds, constraints=constraints, method='SLSQP')

    # Get the best weights
    best_weights = result.x
    best_success_probability = -result.fun + 0.1 * np.sum(np.square(best_weights - 1 / len(best_weights)))

    # Prepare the document to be inserted into the new results_collection
    weights_document = {
        'tag': tag,
        'weights': {X.columns[i]: best_weights[i] for i in range(len(X.columns))}
    }

    # Update the document in the results_collection, or insert if it does not exist
    weights_collection.update_one(
        {'tag': tag}, 
        {'$set': weights_document}, 
        upsert=True
    )
    print(f"New weights for tag '{tag}':")
    for key, value in weights_document['weights'].items():
        print(f"{key}: {value:.6f}")

    print('--------------------------------------')

# Close the MongoDB client when done
client.close()
