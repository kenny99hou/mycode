import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Load your parsed log data (e.g., Query Duration)
df = pd.read_csv('db2_query_logs.csv')

# 2. Use Isolation Forest (Unsupervised Anomaly Detection)
# It isolates observations by randomly selecting a feature and split value.
model = IsolationForest(contamination=0.01) # Look for top 1% outliers
df['anomaly'] = model.fit_predict(df[['duration_seconds']])

# 3. Print only the anomalies
print(df[df['anomaly'] == -1])
