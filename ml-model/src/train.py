import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, average_precision_score

def train_model():
    # 1. Resolve relative directory paths
    src_dir = os.path.dirname(os.path.abspath(__file__))
    ml_root = os.path.dirname(src_dir)
    processed_dir = os.path.join(ml_root, "data", "processed")

    train_path = os.path.join(processed_dir, "train_data.csv")
    val_path = os.path.join(processed_dir, "val_data.csv")
    test_path = os.path.join(processed_dir, "test_data.csv")
    full_path = os.path.join(processed_dir, "training_data.csv")
    model_save_path = os.path.join(ml_root, "models", "model.pkl")

    # 2. Load Split Datasets (fallback to slicing full dataset if individual files do not exist)
    if os.path.exists(train_path) and os.path.exists(val_path) and os.path.exists(test_path):
        print(f"Loading split files from: {processed_dir}")
        train_df = pd.read_csv(train_path)
        val_df = pd.read_csv(val_path)
        test_df = pd.read_csv(test_path)
    elif os.path.exists(full_path):
        print(f"Splitting 70/15/15 chronologically from: {full_path}")
        df = pd.read_csv(full_path)
        df["prediction_time"] = pd.to_datetime(df["prediction_time"])
        df = df.sort_values("prediction_time").reset_index(drop=True)

        n = len(df)
        train_end = int(n * 0.70)
        val_end = int(n * 0.85)

        train_df = df.iloc[:train_end].copy()
        val_df = df.iloc[train_end:val_end].copy()
        test_df = df.iloc[val_end:].copy()
    else:
        raise FileNotFoundError(f"No processed data found in {processed_dir}. Run preprocessing first.")

    print(f"Sample Counts -> Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    feature_cols = [
        "latitude", "longitude", "crime_category", "transaction_amount",
        "recent_txn_count", "recent_withdrawal_count",
        "distance_to_recent_withdrawal_km", "historical_location_risk",
        "hour", "day_of_week"
    ]
    target_col = "withdrawal_occurred"

    # 3. Encode Categorical Features (Fit on train, align val & test)
    X_train = pd.get_dummies(train_df[feature_cols], drop_first=True)
    y_train = train_df[target_col].values

    X_val = pd.get_dummies(val_df[feature_cols], drop_first=True).reindex(columns=X_train.columns, fill_value=0)
    y_val = val_df[target_col].values

    X_test = pd.get_dummies(test_df[feature_cols], drop_first=True).reindex(columns=X_train.columns, fill_value=0)
    y_test = test_df[target_col].values

    # 4. Train Random Forest Classifier
    print("\nTraining Random Forest baseline model...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)

    # 5. Evaluate on Validation Set
    val_probs = rf_model.predict_proba(X_val)[:, 1]
    print("\n=== Validation Set Evaluation ===")
    print(f"ROC-AUC: {roc_auc_score(y_val, val_probs):.4f}")
    print(f"PR-AUC:  {average_precision_score(y_val, val_probs):.4f}")

    # 6. Evaluate on Holdout Test Set
    test_preds = rf_model.predict(X_test)
    test_probs = rf_model.predict_proba(X_test)[:, 1]

    print("\n=== Holdout Test Set Performance ===")
    print(classification_report(y_test, test_preds, digits=4))
    print(f"Test ROC-AUC: {roc_auc_score(y_test, test_probs):.4f}")
    print(f"Test PR-AUC:  {average_precision_score(y_test, test_probs):.4f}")

    # 7. Save Model Artifact
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump({
        "model": rf_model,
        "feature_names": list(X_train.columns),
        "model_version": "rf_baseline_v1"
    }, model_save_path)

    print(f"\nTrained model artifact successfully saved to: {model_save_path}")

if __name__ == "__main__":
    train_model()
    