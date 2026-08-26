import os
import numpy as np
import pandas as pd

# City-to-Coordinate Mapping for the 43 US Cities in the dataset
CITY_COORDINATES = {
    'Albuquerque': (35.0844, -106.6504),
    'Atlanta': (33.7490, -84.3880),
    'Austin': (30.2672, -97.7431),
    'Baltimore': (39.2904, -76.6122),
    'Boston': (42.3601, -71.0589),
    'Charlotte': (35.2271, -80.8431),
    'Chicago': (41.8781, -87.6298),
    'Colorado Springs': (38.8339, -104.8214),
    'Columbus': (39.9612, -82.9988),
    'Dallas': (32.7767, -96.7970),
    'Denver': (39.7392, -104.9903),
    'Detroit': (42.3314, -83.0458),
    'El Paso': (31.7619, -106.4850),
    'Fort Worth': (32.7555, -97.3308),
    'Fresno': (36.7468, -119.7726),
    'Houston': (29.7604, -95.3698),
    'Indianapolis': (39.7684, -86.1581),
    'Jacksonville': (30.3322, -81.6557),
    'Kansas City': (39.0997, -94.5786),
    'Las Vegas': (36.1699, -115.1398),
    'Los Angeles': (34.0522, -118.2437),
    'Louisville': (38.2527, -85.7585),
    'Memphis': (35.1495, -90.0490),
    'Mesa': (33.4152, -111.8315),
    'Miami': (25.7617, -80.1918),
    'Milwaukee': (43.0389, -87.9065),
    'Nashville': (36.1627, -86.7816),
    'New York': (40.7128, -74.0060),
    'Oklahoma City': (35.4676, -97.5164),
    'Omaha': (41.2565, -95.9345),
    'Philadelphia': (39.9526, -75.1652),
    'Phoenix': (33.4484, -112.0740),
    'Portland': (45.5152, -122.6784),
    'Raleigh': (35.7796, -78.6382),
    'Sacramento': (38.5816, -121.4944),
    'San Antonio': (29.4241, -98.4936),
    'San Diego': (32.7157, -117.1611),
    'San Francisco': (37.7749, -122.4194),
    'San Jose': (37.3382, -121.8863),
    'Seattle': (47.6062, -122.3321),
    'Tucson': (32.2226, -110.9747),
    'Virginia Beach': (36.8529, -75.9780),
    'Washington': (38.9072, -77.0369)
}

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the Great Circle (Haversine) distance between two points in km."""
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def assign_crime_category(row):
    """Categorize transaction profile based on channel, type, login attempts, duration, and amount."""
    is_atm = (row['Channel'] == 'ATM')
    is_debit = (row['TransactionType'] == 'Debit')
    amount = row['TransactionAmount']
    login_attempts = row['LoginAttempts']
    duration = row['TransactionDuration']
    channel = row['Channel']
    
    if is_atm and is_debit and (amount > 250 or login_attempts > 1):
        return 'suspicious_cash_withdrawal'
    elif channel == 'Online' and (login_attempts > 1 or duration > 150):
        return 'unusual_online_activity'
    elif amount > 400:
        return 'high_value_transfer'
    else:
        return 'routine_transaction'

def preprocess_pipeline(raw_csv_path, output_dir, future_window_hours=3, train_ratio=0.70, val_ratio=0.15):
    print(f"Reading raw dataset from: {raw_csv_path}")
    df = pd.read_csv(raw_csv_path)

    # Clean BOM or unexpected column names
    df.columns = [c.replace('\ufeff', '').strip() for c in df.columns]

    # Parse prediction_time from TransactionDate (handles both date-only and date-time strings)
    df['prediction_time'] = pd.to_datetime(df['TransactionDate'], format='mixed')

    # Sort chronologically
    df = df.sort_values('prediction_time').reset_index(drop=True)

    # 1. Location ID Mapping
    unique_cities = sorted(df['Location'].unique())
    city_to_loc_id = {city: f"LOC_{i+1:03d}" for i, city in enumerate(unique_cities)}
    df['location_id'] = df['Location'].map(city_to_loc_id)

    # 2. Coordinates Mapping (latitude, longitude)
    df['latitude'] = df['Location'].map(lambda loc: CITY_COORDINATES.get(loc, (0.0, 0.0))[0])
    df['longitude'] = df['Location'].map(lambda loc: CITY_COORDINATES.get(loc, (0.0, 0.0))[1])

    # 3. Time Features
    df['hour'] = df['prediction_time'].dt.hour
    df['day_of_week'] = df['prediction_time'].dt.dayofweek

    # 4. Crime Category & Amount
    df['crime_category'] = df.apply(assign_crime_category, axis=1)
    df['transaction_amount'] = df['TransactionAmount'].astype(float)

    # 5. ATM Debit withdrawal flag
    df['is_withdrawal'] = (df['Channel'] == 'ATM') & (df['TransactionType'] == 'Debit')

    # High-risk / suspicious indicator for risk scoring
    df['is_high_risk'] = df['is_withdrawal'] | (df['crime_category'] != 'routine_transaction')

    print("Calculating historical location features...")

    # 6. Historical Location Features (rolling 24h & cumulative risk)
    # Group by location_id and calculate rolling counts
    recent_txn_counts = np.zeros(len(df), dtype=int)
    recent_withdrawal_counts = np.zeros(len(df), dtype=int)
    historical_location_risks = np.zeros(len(df), dtype=float)

    for loc_id, group in df.groupby('location_id', sort=False):
        times = group['prediction_time'].values
        withdrawals = group['is_withdrawal'].values.astype(int)
        high_risks = group['is_high_risk'].values.astype(int)
        indices = group.index.values

        n = len(group)
        loc_recent_txn = np.zeros(n, dtype=int)
        loc_recent_wd = np.zeros(n, dtype=int)
        loc_risk = np.zeros(n, dtype=float)

        cum_total = 0
        cum_risk = 0

        # Efficient sliding window pointers over sorted timestamps
        start_idx = 0
        for i in range(n):
            curr_t = times[i]
            # Trailing 24 hours
            window_start = curr_t - np.timedelta64(24, 'h')

            while start_idx < i and times[start_idx] < window_start:
                start_idx += 1

            # Count in [window_start, curr_t]
            loc_recent_txn[i] = i - start_idx + 1
            loc_recent_wd[i] = withdrawals[start_idx:i+1].sum()

            cum_total += 1
            cum_risk += high_risks[i]
            loc_risk[i] = round(cum_risk / cum_total, 4)

        recent_txn_counts[indices] = loc_recent_txn
        recent_withdrawal_counts[indices] = loc_recent_wd
        historical_location_risks[indices] = loc_risk

    df['recent_txn_count'] = recent_txn_counts
    df['recent_withdrawal_count'] = recent_withdrawal_counts
    df['historical_location_risk'] = historical_location_risks

    print("Calculating distance to recent withdrawal per account...")

    # 7. Distance to Recent Withdrawal per Account
    distances = np.zeros(len(df), dtype=float)
    last_withdrawal_loc = {}  # account_id -> (lat, lng)

    account_ids = df['AccountID'].values
    lats = df['latitude'].values
    lngs = df['longitude'].values
    withdrawals_flag = df['is_withdrawal'].values

    for i in range(len(df)):
        acc_id = account_ids[i]
        curr_lat = lats[i]
        curr_lng = lngs[i]

        if acc_id in last_withdrawal_loc:
            prev_lat, prev_lng = last_withdrawal_loc[acc_id]
            distances[i] = round(haversine_distance(curr_lat, curr_lng, prev_lat, prev_lng), 2)
        else:
            distances[i] = 0.0

        if withdrawals_flag[i]:
            last_withdrawal_loc[acc_id] = (curr_lat, curr_lng)

    df['distance_to_recent_withdrawal_km'] = distances

    print("Calculating future-window target variable (withdrawal_occurred)...")

    # 8. Future Target Variable: withdrawal_occurred
    # 1 if an ATM + Debit event occurs at candidate location within future_window_hours (e.g., 3h)
    withdrawal_targets = np.zeros(len(df), dtype=int)

    for loc_id, group in df.groupby('location_id', sort=False):
        times = group['prediction_time'].values
        withdrawals = group['is_withdrawal'].values.astype(int)
        indices = group.index.values
        n = len(group)

        # Sliding window for future lookahead: (curr_t, curr_t + window]
        end_idx = 0
        for i in range(n):
            curr_t = times[i]
            window_end = curr_t + np.timedelta64(future_window_hours, 'h')

            while end_idx < n and times[end_idx] <= window_end:
                end_idx += 1

            # Future window elements after current index i up to end_idx
            if i + 1 < end_idx:
                future_wds = withdrawals[i + 1:end_idx].sum()
                if future_wds > 0:
                    withdrawal_targets[indices[i]] = 1

    df['withdrawal_occurred'] = withdrawal_targets

    # Select final requested columns in exact order
    final_columns = [
        'location_id',
        'latitude',
        'longitude',
        'prediction_time',
        'crime_category',
        'transaction_amount',
        'recent_txn_count',
        'recent_withdrawal_count',
        'distance_to_recent_withdrawal_km',
        'historical_location_risk',
        'hour',
        'day_of_week',
        'withdrawal_occurred'
    ]

    processed_df = df[final_columns].copy()

    # Format timestamp to string YYYY-MM-DD HH:MM:SS
    processed_df['prediction_time'] = processed_df['prediction_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Chronological Train (70%), Validation (15%), Test (15%) Split
    n_total = len(processed_df)
    train_end = int(n_total * train_ratio)
    val_end = int(n_total * (train_ratio + val_ratio))

    train_df = processed_df.iloc[:train_end].copy()
    val_df = processed_df.iloc[train_end:val_end].copy()
    test_df = processed_df.iloc[val_end:].copy()

    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, 'training_data.csv')
    train_path = os.path.join(output_dir, 'train_data.csv')
    val_path = os.path.join(output_dir, 'val_data.csv')
    test_path = os.path.join(output_dir, 'test_data.csv')

    processed_df.to_csv(full_path, index=False)
    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"\n--- Preprocessing & Data Splitting Complete ---")
    print(f"Full Dataset: {len(processed_df)} records -> {full_path}")
    print(f"Train Split:  {len(train_df)} records ({train_df['prediction_time'].min()} to {train_df['prediction_time'].max()}) -> {train_path}")
    print(f"Val Split:    {len(val_df)} records ({val_df['prediction_time'].min()} to {val_df['prediction_time'].max()}) -> {val_path}")
    print(f"Test Split:   {len(test_df)} records ({test_df['prediction_time'].min()} to {test_df['prediction_time'].max()}) -> {test_path}")

    print("\n--- Target Breakdown across Splits (withdrawal_occurred) ---")
    print("Train Target %:")
    print(train_df['withdrawal_occurred'].value_counts(normalize=True))
    print("Val Target %:")
    print(val_df['withdrawal_occurred'].value_counts(normalize=True))
    print("Test Target %:")
    print(test_df['withdrawal_occurred'].value_counts(normalize=True))

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'raw', 'bank_transactions_data_2_augmented_clean_2.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    preprocess_pipeline(raw_path, processed_dir)

