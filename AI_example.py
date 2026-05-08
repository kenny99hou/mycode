# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

# Step 1: Load the data
iris = load_iris()
X = iris.data
y = iris.target

# Optional: Convert to a Pandas DataFrame for easier viewing
df = pd.DataFrame(X, columns=iris.feature_names)
df['species'] = iris.target_names[y]
print("First 5 rows of the dataset:")
print(df.head())
print("\nIris target names (species):", iris.target_names)

# Step 2: Split data into training and testing sets
# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Step 3: Choose and train the AI model (K-Nearest Neighbors classifier)
# The 'n_neighbors=3' means the model considers the 3 closest neighbors to classify a new data point
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# Step 4: Make predictions and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy on test data: {accuracy:.2f}")

# Step 5: Use the trained model to predict a new, unseen data point
# Example: a flower with sepal length 5.1cm, sepal width 3.5cm, petal length 1.4cm, petal width 0.2cm
new_flower = [[5.1, 3.5, 1.4, 0.2]] 
prediction = model.predict(new_flower)

print(f"\nPrediction for the new flower data {new_flower}: {iris.target_names[prediction[0]]}")

