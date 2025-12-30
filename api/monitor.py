"""
Vercel Serverless Function - Performance Monitoring
====================================================
Provides real-time performance metrics and model health checks.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path
base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir))
sys.path.insert(0, str(base_dir / 'api'))

try:
    from utils.db import get_database_stats, test_connection
except ImportError as e:
    print(f"Import error: {e}")
    get_database_stats = None
    test_connection = None

app = Flask(__name__)
CORS(app)


def load_performance_history():
    """Load performance history from log file"""
    try:
        log_file = base_dir / 'logs' / 'performance_history.json'
        if log_file.exists():
            with open(log_file, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading performance history: {e}")
        return []


def save_performance_snapshot(snapshot):
    """Save a performance snapshot to history"""
    try:
        log_file = base_dir / 'logs' / 'performance_history.json'
        log_file.parent.mkdir(exist_ok=True)

        history = load_performance_history()
        history.append(snapshot)

        # Keep only last 30 days
        cutoff = datetime.now() - timedelta(days=30)
        history = [h for h in history if datetime.fromisoformat(h['timestamp']) > cutoff]

        with open(log_file, 'w') as f:
            json.dump(history, f, indent=2)

    except Exception as e:
        print(f"Error saving performance snapshot: {e}")


@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def handler(path=''):
    """
    Get performance monitoring metrics.

    Returns:
        {
            "health": "healthy" | "warning" | "critical",
            "models": {
                "game_state": {
                    "accuracy": 0.7928,
                    "roc_auc": 0.8780,
                    "status": "healthy",
                    "last_trained": "2025-12-30T13:03:57"
                }
            },
            "database": {
                "status": "healthy",
                "matches": 10000,
                "connection_time_ms": 45
            },
            "alerts": [],
            "timestamp": "2025-12-30T15:00:00"
        }
    """
    try:
        health_status = "healthy"
        alerts = []

        # Load model performance
        game_state_perf = {}
        try:
            perf_path = base_dir / 'models' / 'game_state_performance.json'
            if perf_path.exists():
                with open(perf_path, 'r') as f:
                    game_state_perf = json.load(f)
        except Exception as e:
            alerts.append(f"Could not load game state performance: {str(e)}")
            health_status = "warning"

        # Check model health
        model_status = "healthy"
        accuracy = game_state_perf.get('accuracy', 0)

        if accuracy < 0.70:
            model_status = "critical"
            health_status = "critical"
            alerts.append(f"Game State accuracy critically low: {accuracy:.4f}")
        elif accuracy < 0.75:
            model_status = "warning"
            if health_status == "healthy":
                health_status = "warning"
            alerts.append(f"Game State accuracy below target: {accuracy:.4f}")

        # Check database health
        db_status = "healthy"
        db_connection_time = 0
        db_stats = {}

        if test_connection and get_database_stats:
            start_time = datetime.now()
            db_healthy = test_connection()
            db_connection_time = (datetime.now() - start_time).total_seconds() * 1000

            if db_healthy:
                db_stats = get_database_stats()
            else:
                db_status = "critical"
                health_status = "critical"
                alerts.append("Database connection failed")

            # Check connection time
            if db_connection_time > 1000:  # 1 second
                db_status = "warning"
                if health_status == "healthy":
                    health_status = "warning"
                alerts.append(f"Database connection slow: {db_connection_time:.0f}ms")

        # Build response
        response = {
            "health": health_status,
            "models": {
                "game_state": {
                    "accuracy": accuracy,
                    "roc_auc": game_state_perf.get('roc_auc', 0),
                    "status": model_status,
                    "last_trained": game_state_perf.get('timestamp', 'unknown'),
                    "trained_on": game_state_perf.get('matches_count', 0)
                }
            },
            "database": {
                "status": db_status,
                "matches": db_stats.get('matches', 0),
                "connection_time_ms": round(db_connection_time, 2),
                "size": db_stats.get('database_size', 'unknown')
            },
            "alerts": alerts,
            "timestamp": datetime.now().isoformat()
        }

        # Save snapshot
        save_performance_snapshot(response)

        return jsonify(response)

    except Exception as e:
        print(f"Monitor error: {e}")
        import traceback
        traceback.print_exc()

        return jsonify({
            "health": "critical",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/history', methods=['GET'])
def history():
    """
    Get performance history.

    Query params:
        - days: Number of days to retrieve (default: 7, max: 30)

    Returns:
        {
            "history": [
                {
                    "timestamp": "2025-12-30T00:00:00",
                    "accuracy": 0.7928,
                    "alerts": []
                },
                ...
            ],
            "summary": {
                "avg_accuracy": 0.7928,
                "total_alerts": 2
            }
        }
    """
    try:
        days = min(int(request.args.get('days', 7)), 30)

        history = load_performance_history()

        # Filter by date
        cutoff = datetime.now() - timedelta(days=days)
        filtered = [h for h in history if datetime.fromisoformat(h['timestamp']) > cutoff]

        # Calculate summary
        if filtered:
            accuracies = [h['models']['game_state']['accuracy'] for h in filtered]
            avg_accuracy = sum(accuracies) / len(accuracies)
            total_alerts = sum(len(h.get('alerts', [])) for h in filtered)
        else:
            avg_accuracy = 0
            total_alerts = 0

        return jsonify({
            "history": filtered,
            "summary": {
                "days": days,
                "snapshots": len(filtered),
                "avg_accuracy": round(avg_accuracy, 4),
                "total_alerts": total_alerts
            }
        })

    except Exception as e:
        print(f"History error: {e}")
        return jsonify({
            "error": str(e)
        }), 500
