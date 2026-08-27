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

    # Parse prediction_time from TransactionDate
    df['prediction_time'] = pd.to_datetime(df['TransactionDate'], format='mixed')

    # STEP 1: Sort Chronologically Before Any Operation
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
    df['is_high_risk'] = df['is_withdrawal'] | (df['crime_category'] != 'routine_transaction')

    # STEP 2 & 3: Historical Location Features & Hotspot Density
    print("Calculating location rolling features (24h transactions, 30-day density, historical risk)...")
    recent_txn_counts = np.zeros(len(df), dtype=int)
    recent_withdrawal_counts = np.zeros(len(df), dtype=int)
    historical_location_risks = np.zeros(len(df), dtype=float)
    location_density_30d = np.zeros(len(df), dtype=int)

    for loc_id, group in df.groupby('location_id', sort=False):
        times = group['prediction_time'].values
        withdrawals = group['is_withdrawal'].values.astype(int)
        high_risks = group['is_high_risk'].values.astype(int)
        indices = group.index.values

        n = len(group)
        start_24h = 0
        start_30d = 0
        cum_total = 0
        cum_risk = 0

        for i in range(n):
            curr_t = times[i]
            window_24h = curr_t - np.timedelta64(24, 'h')
            window_30d = curr_t - np.timedelta64(30, 'D')

            while start_24h < i and times[start_24h] < window_24h:
                start_24h += 1
            while start_30d < i and times[start_30d] < window_30d:
                start_30d += 1

            if start_24h < i:
                recent_txn_counts[indices[i]] = i - start_24h
                recent_withdrawal_counts[indices[i]] = withdrawals[start_24h:i].sum()
            
            if start_30d < i:
                location_density_30d[indices[i]] = withdrawals[start_30d:i].sum()

            cum_total += 1
            cum_risk += high_risks[i]
            historical_location_risks[indices[i]] = round(cum_risk / cum_total, 4)

    df['recent_txn_count'] = recent_txn_counts
    df['recent_withdrawal_count'] = recent_withdrawal_counts
    df['historical_location_risk'] = historical_location_risks
    df['location_density_30d'] = location_density_30d

    # STEP 2 & 3: Account-Level Trailing Features & Distance/Velocity
    print("Calculating account trailing features (past 1h/24h withdrawals, minutes & distance since last txn)...")
    withdrawals_past_1h = np.zeros(len(df), dtype=int)
    withdrawals_past_24h = np.zeros(len(df), dtype=int)
    minutes_since_last_txn = np.full(len(df), 9999.0, dtype=float)
    dist_from_last_txn_km = np.zeros(len(df), dtype=float)
    distances_to_recent_wd = np.zeros(len(df), dtype=float)

    for acc_id, group in df.groupby('AccountID', sort=False):
        times = group['prediction_time'].values
        withdrawals = group['is_withdrawal'].values.astype(int)
        lats = group['latitude'].values
        lngs = group['longitude'].values
        indices = group.index.values
        n = len(group)

        start_1h = 0
        start_24h = 0
        last_wd_lat = None
        last_wd_lng = None

        for i in range(n):
            curr_t = times[i]
            t_1h = curr_t - np.timedelta64(1, 'h')
            t_24h = curr_t - np.timedelta64(24, 'h')

            while start_1h < i and times[start_1h] < t_1h:
                start_1h += 1
            while start_24h < i and times[start_24h] < t_24h:
                start_24h += 1

            if start_1h < i:
                withdrawals_past_1h[indices[i]] = withdrawals[start_1h:i].sum()
            if start_24h < i:
                withdrawals_past_24h[indices[i]] = withdrawals[start_24h:i].sum()

            if i > 0:
                diff_sec = (curr_t - times[i-1]) / np.timedelta64(1, 's')
                minutes_since_last_txn[indices[i]] = round(diff_sec / 60.0, 2)
                dist_from_last_txn_km[indices[i]] = round(haversine_distance(lats[i], lngs[i], lats[i-1], lngs[i-1]), 2)

            if last_wd_lat is not None:
                distances_to_recent_wd[indices[i]] = round(haversine_distance(lats[i], lngs[i], last_wd_lat, last_wd_lng), 2)

            if withdrawals[i] == 1:
                last_wd_lat = lats[i]
                last_wd_lng = lngs[i]

    df['withdrawals_past_1h'] = withdrawals_past_1h
    df['withdrawals_past_24h'] = withdrawals_past_24h
    df['minutes_since_last_txn'] = minutes_since_last_txn
    df['dist_from_last_txn_km'] = dist_from_last_txn_km
    df['distance_to_recent_withdrawal_km'] = distances_to_recent_wd

    # STEP 4: Target Variable (Forward Lookahead Window T -> T + 3h)
    print("Calculating forward lookahead target variable (withdrawal_occurred)...")
    withdrawal_targets = np.zeros(len(df), dtype=int)

    for loc_id, group in df.groupby('location_id', sort=False):
        times = group['prediction_time'].values
        withdrawals = group['is_withdrawal'].values.astype(int)
        indices = group.index.values
        n = len(group)

        end_idx = 0
        for i in range(n):
            curr_t = times[i]
            window_end = curr_t + np.timedelta64(future_window_hours, 'h')

            while end_idx < n and times[end_idx] <= window_end:
                end_idx += 1

            if i + 1 < end_idx:
                future_wds = withdrawals[i + 1:end_idx].sum()
                if future_wds > 0:
                    withdrawal_targets[indices[i]] = 1

    df['withdrawal_occurred'] = withdrawal_targets

    # Additional raw fields to preserve
    df['login_attempts'] = df['LoginAttempts'].astype(int)
    df['transaction_duration'] = df['TransactionDuration'].astype(float)
    df['customer_age'] = df['CustomerAge'].astype(int)
    df['account_balance'] = df['AccountBalance'].astype(float)

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
        'dist_from_last_txn_km',
        'minutes_since_last_txn',
        'withdrawals_past_1h',
        'withdrawals_past_24h',
        'location_density_30d',
        'historical_location_risk',
        'login_attempts',
        'transaction_duration',
        'customer_age',
        'account_balance',
        'hour',
        'day_of_week',
        'withdrawal_occurred'
    ]

    processed_df = df[final_columns].copy()
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
