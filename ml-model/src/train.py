import os
import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve, confusion_matrix

from features import load_feature_splits
from preprocessing import preprocess_pipeline

def train_and_evaluate_model(force_reprocess: bool = False):
    """
    Trains an optimized LightGBM Classifier on CyberSentinel features,
    tunes the decision threshold on the Validation set, evaluates on the Test set,
    and serializes the model payload.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv_path = os.path.join(base_dir, 'data', 'raw', 'bank_transactions_data_2_augmented_clean_2.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    model_dir = os.path.join(base_dir, 'models')
    model_path = os.path.join(model_dir, 'model.pkl')

    # Step 1: Preprocess raw data (force if flag is set or splits missing)
    train_csv = os.path.join(processed_dir, 'train_data.csv')
    if force_reprocess or not os.path.exists(train_csv):
        print("Preprocessing raw data into processed splits...")
        preprocess_pipeline(raw_csv_path, processed_dir)

    # Step 2: Load feature splits
    print("\n--- Step 1: Feature Extraction & Split Loading ---")
    X_train, y_train, X_val, y_val, X_test, y_test, feature_names = load_feature_splits(processed_dir)
    print(f"Loaded {len(feature_names)} features for training.")
    print(f"Train samples: {len(X_train)} | Val samples: {len(X_val)} | Test samples: {len(X_test)}")

    # Calculate class imbalance ratio dynamically from training set
    pos_count = np.sum(y_train == 1)
    neg_count = np.sum(y_train == 0)
    scale_weight = neg_count / max(1, pos_count)
    print(f"Class distribution - 0: {neg_count}, 1: {pos_count} (scale_pos_weight: {scale_weight:.2f})")

    # Step 3: Model Training with Regularization Constraints
    print("\n--- Step 2: Training LGBMClassifier ---")
    clf = LGBMClassifier(
        n_estimators=300,
        learning_rate=0.03,
        max_depth=5,
        num_leaves=15,             # Constrained to prevent over-branching and -inf gain termination
        min_child_samples=10,      # Allows capturing smaller positive clusters
        min_split_gain=0.0,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_weight,
        random_state=42,
        verbosity=-1
    )
    clf.fit(X_train, y_train)
    print("Model training complete.")

    # Step 4: Validation Evaluation & Threshold Optimization
    print("\n--- Step 3: Validation Set Performance & Threshold Tuning ---")
    val_probs = clf.predict_proba(X_val)[:, 1]
    val_auc = roc_auc_score(y_val, val_probs)
    print(f"Validation ROC-AUC Score: {val_auc:.4f}")

    # Determine optimal classification threshold via Precision-Recall curve
    precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)
    f1_scores = (2 * precisions * recalls) / (precisions + recalls + 1e-8)
    best_idx = np.argmax(f1_scores)
    
    # Handle edge case where precision_recall_curve returns len(thresholds) == len(precisions) - 1
    best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
    print(f"Optimal Decision Threshold: {best_threshold:.4f} (Max Val F1: {f1_scores[best_idx]:.4f})")

    val_preds_tuned = (val_probs >= best_threshold).astype(int)
    print("\nValidation Classification Report (Optimal Threshold):")
    print(classification_report(y_val, val_preds_tuned))

    # Step 5: Test Evaluation Using Tuned Threshold
    print("\n--- Step 4: Test Set Performance ---")
    test_probs = clf.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, test_probs)
    test_preds_tuned = (test_probs >= best_threshold).astype(int)

    print(f"Test ROC-AUC Score: {test_auc:.4f}")
    print("\nTest Classification Report (Evaluated at Optimal Threshold):")
    print(classification_report(y_test, test_preds_tuned))
    
    print("\nConfusion Matrix (Test):")
    print(confusion_matrix(y_test, test_preds_tuned))

    # Step 6: Feature Importance Analysis
    print("\n--- Step 5: Top Feature Importances ---")
    importances = pd.Series(clf.feature_importances_, index=feature_names).sort_values(ascending=False)
    print(importances.head(10))

    # Step 7: Save Model Artifact & Threshold Metadata
    os.makedirs(model_dir, exist_ok=True)
    model_payload = {
        'model': clf,
        'feature_names': feature_names,
        'optimal_threshold': float(best_threshold),
        'model_version': 'lgbm_v2_tuned'
    }
    
    joblib.dump(model_payload, model_path)
    print(f"\nModel artifact successfully saved to: {model_path}")

if __name__ == '__main__':
    # Set to True if you updated preprocessing.py or features.py to force a clean split rebuild
    train_and_evaluate_model(force_reprocess=True)