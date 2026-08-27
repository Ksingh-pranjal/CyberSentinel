import os
import numpy as np
import pandas as pd

# Define fixed crime categories for consistent encoding across train/val/test
CRIME_CATEGORIES = [
    'routine_transaction',
    'suspicious_cash_withdrawal',
    'unusual_online_activity',
    'high_value_transfer'
]

def extract_features(df):
    """
    Transforms processed dataframe into engineered ML features.
    
    Parameters:
        df (pd.DataFrame): Processed dataframe from preprocessing.py
        
    Returns:
        X (pd.DataFrame): Feature matrix
        y (pd.Series or None): Target vector ('withdrawal_occurred')
    """
    data = df.copy()

    # 1. Cyclical Time Features (Hour & Day of Week)
    data['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24.0)
    data['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24.0)
    
    data['day_sin'] = np.sin(2 * np.pi * data['day_of_week'] / 7.0)
    data['day_cos'] = np.cos(2 * np.pi * data['day_of_week'] / 7.0)
    
    data['is_weekend'] = (data['day_of_week'] >= 5).astype(int)

    # 2. Transaction Activity Ratios & Scaled Features
    data['withdrawal_ratio'] = data['recent_withdrawal_count'] / (data['recent_txn_count'] + 1.0)
    data['log_transaction_amount'] = np.log1p(np.maximum(0, data['transaction_amount']))
    data['log_account_balance'] = np.log1p(np.maximum(0, data['account_balance']))

    # 3. Categorical Encoding for crime_category
    for cat in CRIME_CATEGORIES:
        data[f'crime_cat_{cat}'] = (data['crime_category'] == cat).astype(int)

    # 4. Location Numeric Encoding (LOC_001 -> 1)
    if 'location_id' in data.columns:
        data['location_numeric_id'] = data['location_id'].str.replace('LOC_', '').astype(int)

    # Fill any NaNs safely
    fill_defaults = {
        'withdrawals_past_1h': 0,
        'withdrawals_past_24h': 0,
        'minutes_since_last_txn': 9999.0,
        'dist_from_last_txn_km': 0.0,
        'location_density_30d': 0,
        'login_attempts': 1,
        'transaction_duration': 0,
        'customer_age': 30
    }
    for col, default_val in fill_defaults.items():
        if col in data.columns:
            data[col] = data[col].fillna(default_val)

    # Select final numerical feature columns for model training
    feature_cols = [
        'latitude',
        'longitude',
        'log_transaction_amount',
        'log_account_balance',
        'recent_txn_count',
        'recent_withdrawal_count',
        'withdrawal_ratio',
        'distance_to_recent_withdrawal_km',
        'dist_from_last_txn_km',
        'minutes_since_last_txn',
        'withdrawals_past_1h',
        'withdrawals_past_24h',
        'location_density_30d',
        'historical_location_risk',
        'login_attempts',
        'transaction_duration',
        'customer_age',
        'hour_sin',
        'hour_cos',
        'day_sin',
        'day_cos',
        'is_weekend',
        'location_numeric_id',
        'crime_cat_routine_transaction',
        'crime_cat_suspicious_cash_withdrawal',
        'crime_cat_unusual_online_activity',
        'crime_cat_high_value_transfer'
    ]

    X = data[feature_cols].copy()
    y = data['withdrawal_occurred'].copy() if 'withdrawal_occurred' in data.columns else None

    return X, y

def load_feature_splits(processed_dir):
    """
    Loads train_data.csv and test_data.csv and applies feature extraction.
    
    Returns:
        X_train, y_train, X_test, y_test, feature_names
    """
    train_path = os.path.join(processed_dir, 'train_data.csv')
    test_path = os.path.join(processed_dir, 'test_data.csv')

    print(f"Loading split files from {processed_dir}...")
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    X_train, y_train = extract_features(df_train)
    X_test, y_test = extract_features(df_test)

    feature_names = list(X_train.columns)

    return X_train, y_train, X_test, y_test, feature_names

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    
    X_train, y_train, X_test, y_test, feature_names = load_feature_splits(processed_dir)
    
    print("\n--- Features Pipeline Execution Successful ---")
    print(f"Features Count: {len(feature_names)}")
    print(f"\nTrain Feature Matrix Shape: {X_train.shape}")
    print(f"Test Feature Matrix Shape:  {X_test.shape}")

