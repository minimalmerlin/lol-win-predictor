"""
Model Training Script with Clean Data
======================================
Trains win prediction models on clean data without data leakage.

Features:
- Uses configurable data paths from config.py
- Automatically grows with the dataset
- No data leakage (only champion IDs as features)
- Proper train/test split
- Model performance tracking
- Automatic backup of old models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
import joblib
import json
from datetime import datetime
from pathlib import Path
import shutil

from config import (
    get_training_data_path,
    get_data_info,
    CHAMPION_PREDICTOR_PATH,
    WIN_PREDICTOR_RF_PATH,
    WIN_PREDICTOR_LR_PATH,
    MODEL_PERFORMANCE_PATH,
    MODEL_BACKUP_DIR,
    TRAINING_CONFIG
)


def load_and_prepare_data():
    """
    Load training data and prepare features.
    Only uses champion IDs to avoid data leakage.
    """
    print("=" * 60)
    print("LOADING TRAINING DATA")
    print("=" * 60)

    # Get the appropriate data file (with intelligent fallback)
    try:
        data_path = get_training_data_path()
        print(f"\nUsing data file: {data_path}")
    except FileNotFoundError as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("\n💡 TROUBLESHOOTING:")
        print("  1. Check if pipeline Step 1 (Data Fetching) completed successfully")
        print("  2. Verify merge step created clean_training_data_massive.csv")
        print("  3. Ensure at least one CSV file exists in data/ directory")
        raise

    # Load data with error handling
    try:
        df = pd.read_csv(data_path)
        print(f"✓ Loaded {len(df)} matches")
    except Exception as e:
        print(f"\n❌ ERROR: Failed to read CSV file: {e}")
        print(f"   File: {data_path}")
        raise

    # Show data info
    print("\nDataset Info:")
    data_info = get_data_info()
    for name, info in data_info.items():
        if info['exists']:
            print(f"  {name}: {info['matches']} matches")

    # Features: Only champion IDs (10 features)
    feature_cols = [
        'blue_champ_1', 'blue_champ_2', 'blue_champ_3', 'blue_champ_4', 'blue_champ_5',
        'red_champ_1', 'red_champ_2', 'red_champ_3', 'red_champ_4', 'red_champ_5'
    ]

    # Target
    target_col = 'blue_win'

    # Check for missing columns
    missing_cols = set(feature_cols + [target_col]) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in data: {missing_cols}")

    # Prepare X and y
    X = df[feature_cols]
    y = df[target_col]

    print(f"\nFeatures shape: {X.shape}")
    print(f"Target distribution:")
    print(f"  Blue wins: {(y == 1).sum()} ({(y == 1).sum() / len(y) * 100:.1f}%)")
    print(f"  Red wins: {(y == 0).sum()} ({(y == 0).sum() / len(y) * 100:.1f}%)")

    # Check for data leakage indicators
    if (y == 1).sum() / len(y) > 0.7 or (y == 1).sum() / len(y) < 0.3:
        print("\n⚠️  WARNING: Unbalanced dataset detected!")
        print("   This might indicate data quality issues.")

    return X, y, len(df)


def train_random_forest(X_train, y_train, X_test, y_test):
    """Train Random Forest model"""
    print("\n" + "=" * 60)
    print("TRAINING RANDOM FOREST")
    print("=" * 60)

    rf_params = TRAINING_CONFIG['rf_params']
    print(f"\nParameters: {rf_params}")

    model = RandomForestClassifier(**rf_params)

    print("\nTraining...")
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print(f"\n✓ Training complete!")
    print(f"  Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"  ROC-AUC: {roc_auc:.4f}")

    # Detailed metrics
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Red Win', 'Blue Win']))

    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Feature importance
    print(f"\nTop 5 Most Important Features:")
    feature_names = X_train.columns
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:5]

    for i, idx in enumerate(indices, 1):
        print(f"  {i}. {feature_names[idx]}: {importances[idx]:.4f}")

    return model, accuracy, roc_auc


def train_logistic_regression(X_train, y_train, X_test, y_test):
    """Train Logistic Regression model (fast baseline)"""
    print("\n" + "=" * 60)
    print("TRAINING LOGISTIC REGRESSION (Baseline)")
    print("=" * 60)

    lr_params = TRAINING_CONFIG['lr_params']
    print(f"\nParameters: {lr_params}")

    model = LogisticRegression(**lr_params)

    print("\nTraining...")
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print(f"\n✓ Training complete!")
    print(f"  Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"  ROC-AUC: {roc_auc:.4f}")

    return model, accuracy, roc_auc


def backup_old_models():
    """Backup existing models before overwriting"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for model_path in [WIN_PREDICTOR_RF_PATH, WIN_PREDICTOR_LR_PATH]:
        if model_path.exists():
            backup_path = MODEL_BACKUP_DIR / f"{model_path.stem}_{timestamp}.pkl"
            shutil.copy(model_path, backup_path)
            print(f"  Backed up: {model_path.name} -> {backup_path.name}")


def save_models_and_performance(rf_model, lr_model, rf_accuracy, rf_roc_auc, matches_count):
    """Save trained models and performance metrics"""
    print("\n" + "=" * 60)
    print("SAVING MODELS")
    print("=" * 60)

    # Backup old models
    print("\nBacking up old models...")
    backup_old_models()

    # Save new models
    print("\nSaving new models...")
    joblib.dump(rf_model, WIN_PREDICTOR_RF_PATH)
    print(f"  ✓ Saved: {WIN_PREDICTOR_RF_PATH}")

    joblib.dump(lr_model, WIN_PREDICTOR_LR_PATH)
    print(f"  ✓ Saved: {WIN_PREDICTOR_LR_PATH}")

    # Save performance metrics
    performance = {
        "accuracy": float(rf_accuracy),
        "roc_auc": float(rf_roc_auc),
        "timestamp": datetime.now().isoformat(),
        "matches_count": int(matches_count),
        "training_config": TRAINING_CONFIG
    }

    with open(MODEL_PERFORMANCE_PATH, 'w') as f:
        json.dump(performance, f, indent=2)

    print(f"  ✓ Saved: {MODEL_PERFORMANCE_PATH}")


def main():
    """Main training pipeline"""
    print("\n" + "=" * 60)
    print("LoL WIN PREDICTION MODEL TRAINING")
    print("CLEAN DATA - NO LEAKAGE")
    print("=" * 60)

    # Load data
    X, y, total_matches = load_and_prepare_data()

    # Train/Test split
    print("\n" + "=" * 60)
    print("SPLITTING DATA")
    print("=" * 60)

    test_size = TRAINING_CONFIG['test_size']
    random_state = TRAINING_CONFIG['random_state']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # Ensure balanced split
    )

    print(f"\nTrain/Test Split ({int((1-test_size)*100)}/{int(test_size*100)}):")
    print(f"  Training set: {len(X_train)} matches")
    print(f"  Test set: {len(X_test)} matches")

    # Train models
    rf_model, rf_accuracy, rf_roc_auc = train_random_forest(X_train, y_train, X_test, y_test)
    lr_model, lr_accuracy, lr_roc_auc = train_logistic_regression(X_train, y_train, X_test, y_test)

    # Save everything
    save_models_and_performance(rf_model, lr_model, rf_accuracy, rf_roc_auc, total_matches)

    # Final summary
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"\nRandom Forest Model:")
    print(f"  Accuracy: {rf_accuracy * 100:.2f}%")
    print(f"  ROC-AUC: {rf_roc_auc:.4f}")
    print(f"\nLogistic Regression Model:")
    print(f"  Accuracy: {lr_accuracy * 100:.2f}%")
    print(f"  ROC-AUC: {lr_roc_auc:.4f}")
    print(f"\nTrained on {total_matches} matches")
    print(f"Models saved to: {WIN_PREDICTOR_RF_PATH.parent}")

    # Sanity check
    if rf_accuracy > 0.85:
        print("\n⚠️  WARNING: Accuracy > 85% might indicate data leakage!")
        print("   Please verify that only champion IDs are used as features.")
    else:
        print("\n✓ Accuracy looks reasonable (< 85%)")
        print("  No obvious signs of data leakage.")


if __name__ == "__main__":
    main()
