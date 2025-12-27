"""
Download large model files for Railway deployment.
This script downloads the large model file from an external source
since GitHub doesn't allow files >100MB.
"""

import os
import sys

def check_model_exists():
    """Check if models exist locally"""
    model_path = "models/win_predictor_rf.pkl"
    
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"✅ Model found: {model_path} ({size_mb:.1f}MB)")
        return True
    else:
        print(f"⚠️  Model not found: {model_path}")
        print("Railway will use the smaller linear regression model as fallback")
        return False

if __name__ == "__main__":
    check_model_exists()
