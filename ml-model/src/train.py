import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from features import load_feature_splits
from preprocessing import preprocess_pipeline

def train_and_evaluate_model(force_reprocess: bool = False, contamination: float = 0.02):
    """
    Trains an unsupervised Isolation Forest on CyberSentinel features to detect 
    anomalous transactions. Evaluates the physical profile of the anomalies 
    and saves the resulting model payload.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv_path = os.path.join(base_dir, 'data', 'raw', 'bank_transactions_data_2_augmented_clean_2.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    model_dir = os.path.join(base_dir, 'models')
    model_path = os.path.join(model_dir, 'model.pkl')

    # Step 1: Preprocess raw data if forced or missing
    train_csv = os.path.join(processed_dir, 'train_data.csv')
    if force_reprocess or not os.path.exists(train_csv):
        print("Processed splits not found or force_reprocess=True. Running preprocessing...")
        preprocess_pipeline(raw_csv_path, processed_dir, train_ratio=0.80)

    # Step 2: Load feature splits (Ignore targets entirely)
    print("\n--- Step 1: Feature Extraction & Split Loading ---")
    X_train, _, X_test, _, feature_names = load_feature_splits(processed_dir)
    print(f"Loaded {len(feature_names)} features for unsupervised training.")
    print(f"Train samples (80%): {len(X_train)} | Test samples (20%): {len(X_test)}")

    # Step 3: Unsupervised Model Training (Isolation Forest)
    print("\n--- Step 2: Training Isolation Forest ---")
    print(f"Configured to flag the top {contamination*100}% most unusual transactions...")
    
    iso_forest = IsolationForest(
        n_estimators=300,
        max_samples='auto',
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )
    
    # Fit ONLY on the feature matrix
    iso_forest.fit(X_train)
    print("Model training complete.")

    # Step 4: Scoring the Test Set
    print("\n--- Step 3: Anomaly Detection on Test Set ---")
    
    # predict() returns 1 for normal, -1 for anomaly. Convert to 0 (normal) and 1 (anomaly)
    test_preds = iso_forest.predict(X_test)
    is_anomaly = (test_preds == -1).astype(int)
    
    # decision_function() returns anomaly scores. Lower/negative scores = more anomalous.
    anomaly_scores = iso_forest.decision_function(X_test)
    
    num_anomalies = is_anomaly.sum()
    print(f"Detected {num_anomalies} anomalies out of {len(X_test)} transactions ({(num_anomalies/len(X_test))*100:.2f}%).")

    # Step 5: Profiling the Anomalies (Evaluation)
    print("\n--- Step 4: Profiling Anomalies vs Normal Transactions ---")
    # Attach results to the test set for analysis
    results_df = X_test.copy()
    results_df['is_anomaly'] = is_anomaly
    results_df['anomaly_score'] = anomaly_scores
    
    # Reverse the log transformation on amount for readability in the profile
    results_df['transaction_amount_actual'] = np.expm1(results_df['log_transaction_amount'])

    # Compare averages of key features to see what the model flagged
    profile_cols = [
        'transaction_amount_actual', 
        'dist_from_last_txn_km', 
        'minutes_since_last_txn', 
        'login_attempts',
        'historical_location_risk'
    ]
    
    profile = results_df.groupby('is_anomaly')[profile_cols].mean().round(2)
    profile.index = ['Normal (0)', 'Anomaly (1)']
    
    print("\nAverage Feature Values:")
    print("-" * 50)
    print(profile.T)
    print("-" * 50)

    # Display the top 5 most extreme anomalies
    print("\n--- Step 5: Top 5 Most Extreme Anomalies in Test Set ---")
    top_5 = results_df[results_df['is_anomaly'] == 1].sort_values('anomaly_score').head(5)
    print(top_5[profile_cols + ['anomaly_score']])

    # --- Step 5.5: Export Flagged Anomalies for Review ---
    # Filter only the anomalies and save them to a CSV
    anomalies_df = results_df[results_df['is_anomaly'] == 1].copy()
    
    # Sort them by how extreme they are (most anomalous first)
    anomalies_df = anomalies_df.sort_values('anomaly_score')
    
    export_path = os.path.join(processed_dir, 'flagged_anomalies_test_set.csv')
    anomalies_df.to_csv(export_path, index=False)
    print(f"\nExported {len(anomalies_df)} flagged anomalies for review to: {export_path}")

    # Step 6: Save Model Artifact
    os.makedirs(model_dir, exist_ok=True)
    model_payload = {
        'model': iso_forest,
        'feature_names': feature_names,
        'contamination_rate': contamination,
        'model_version': 'iso_forest_v1'
    }
    
    joblib.dump(model_payload, model_path)
    print(f"\nModel artifact successfully saved to: {model_path}")

if __name__ == '__main__':
    train_and_evaluate_model(force_reprocess=True, contamination=0.02)