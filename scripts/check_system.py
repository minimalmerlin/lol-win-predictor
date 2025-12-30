#!/usr/bin/env python3
"""
System Health Check Script
===========================
Validates database, models, API imports, and environment variables.

Usage:
    python scripts/check_system.py

Exit Codes:
    0 - All checks passed
    1 - One or more checks failed

Author: Merlin Mechler
Reference: Session 6 (MLOps Pipeline)
"""

import sys
import os
from pathlib import Path
import time

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")

def print_check(name, status, details=""):
    """Print check result"""
    symbol = "✓" if status else "✗"
    color = Colors.GREEN if status else Colors.RED
    print(f"{color}{symbol} {name}{Colors.RESET}", end="")
    if details:
        print(f" - {details}")
    else:
        print()

def check_database():
    """Check PostgreSQL (Supabase) connection"""
    print_header("1. DATABASE CHECK")

    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
    except ImportError:
        print_check("psycopg2 import", False, "psycopg2 not installed")
        return False

    # Check SUPABASE_URL environment variable
    supabase_url = os.getenv("SUPABASE_URL") or os.getenv("POSTGRES_URL")
    if not supabase_url:
        print_check("SUPABASE_URL env var", False, "Not set")
        print(f"{Colors.YELLOW}  Hint: export SUPABASE_URL='postgresql://...'{Colors.RESET}")
        return False

    print_check("SUPABASE_URL env var", True, "Set")

    # Test database connection (5s timeout)
    try:
        start_time = time.time()
        conn = psycopg2.connect(
            supabase_url,
            cursor_factory=RealDictCursor,
            connect_timeout=5
        )
        elapsed = time.time() - start_time
        print_check("Database connection", True, f"{elapsed:.2f}s")

        # Test query: count matches
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM matches")
        result = cur.fetchone()
        match_count = result['count']
        print_check("Query: SELECT COUNT(*) FROM matches", True, f"{match_count} matches")

        # Test other tables
        cur.execute("SELECT COUNT(*) as count FROM match_champions")
        champ_count = cur.fetchone()['count']
        print_check("Query: SELECT COUNT(*) FROM match_champions", True, f"{champ_count} rows")

        cur.execute("SELECT COUNT(*) as count FROM match_snapshots")
        snapshot_count = cur.fetchone()['count']
        print_check("Query: SELECT COUNT(*) FROM match_snapshots", True, f"{snapshot_count} rows")

        cur.close()
        conn.close()

        return True

    except psycopg2.OperationalError as e:
        print_check("Database connection", False, f"Connection failed: {str(e)[:50]}")
        return False
    except psycopg2.Error as e:
        print_check("Database query", False, f"Query failed: {str(e)[:50]}")
        return False
    except Exception as e:
        print_check("Database check", False, f"Unexpected error: {str(e)[:50]}")
        return False


def check_models():
    """Check if ML models exist and are loadable"""
    print_header("2. MODEL CHECK")

    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    models_dir = project_root / "models"

    if not models_dir.exists():
        print_check("models/ directory", False, "Not found")
        return False

    print_check("models/ directory", True, str(models_dir))

    # Expected model files
    expected_models = [
        "champion_predictor.pkl",
        "game_state_predictor.pkl",
    ]

    # Optional models (won't fail if missing)
    optional_models = [
        "win_predictor_rf.pkl",
        "win_predictor_lr.pkl",
    ]

    all_passed = True

    # Check expected models
    for model_name in expected_models:
        model_path = models_dir / model_name

        if not model_path.exists():
            print_check(f"Model: {model_name}", False, "Not found")
            all_passed = False
            continue

        # Try to load with joblib
        try:
            import joblib
            start_time = time.time()
            data = joblib.load(model_path)
            elapsed = time.time() - start_time

            # Check if loaded data is valid
            if isinstance(data, dict):
                size_mb = model_path.stat().st_size / (1024 * 1024)
                print_check(f"Model: {model_name}", True, f"{size_mb:.1f}MB, loaded in {elapsed:.2f}s")
            else:
                size_mb = model_path.stat().st_size / (1024 * 1024)
                print_check(f"Model: {model_name}", True, f"{size_mb:.1f}MB (raw model)")

        except Exception as e:
            print_check(f"Model: {model_name}", False, f"Load failed: {str(e)[:40]}")
            all_passed = False

    # Check optional models (just existence, no loading)
    for model_name in optional_models:
        model_path = models_dir / model_name
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print_check(f"Optional: {model_name}", True, f"{size_mb:.1f}MB")
        else:
            print(f"{Colors.YELLOW}  ⊘ Optional: {model_name} - Not found{Colors.RESET}")

    return all_passed


def check_api_imports():
    """Check if API code can be imported (no syntax errors)"""
    print_header("3. API IMPORT CHECK")

    # Change to project root for imports
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    sys.path.insert(0, str(project_root))

    all_passed = True

    # Test critical imports
    critical_imports = [
        ("api.core.config", "Settings and configuration"),
        ("api.core.logging", "Logging setup"),
        ("api.core.database", "Database layer"),
        ("api.services.ml_engine", "ML Engine singleton"),
        ("api.routers.predictions", "Predictions router"),
        ("api.routers.champions", "Champions router"),
        ("api.routers.stats", "Stats router"),
    ]

    for module_path, description in critical_imports:
        try:
            __import__(module_path)
            print_check(f"Import: {module_path}", True, description)
        except ImportError as e:
            print_check(f"Import: {module_path}", False, f"ImportError: {str(e)[:40]}")
            all_passed = False
        except Exception as e:
            print_check(f"Import: {module_path}", False, f"Error: {str(e)[:40]}")
            all_passed = False

    # Try to import main FastAPI app
    try:
        from api.index import app
        print_check("Import: api.index.app", True, "FastAPI app")

        # Check if app has routes
        route_count = len(app.routes)
        print_check("API routes registered", True, f"{route_count} routes")

    except ImportError as e:
        print_check("Import: api.index.app", False, f"ImportError: {str(e)[:40]}")
        all_passed = False
    except Exception as e:
        print_check("Import: api.index.app", False, f"Error: {str(e)[:40]}")
        all_passed = False

    return all_passed


def check_environment():
    """Check critical environment variables"""
    print_header("4. ENVIRONMENT CHECK")

    all_passed = True

    # Critical environment variables
    critical_vars = [
        ("SUPABASE_URL", "PostgreSQL connection string", True),
    ]

    # Optional but recommended
    optional_vars = [
        ("RIOT_API_KEY", "Riot Games API key", False),
        ("VERCEL_ENV", "Vercel environment (production/preview)", False),
    ]

    # Check critical vars
    for var_name, description, required in critical_vars:
        value = os.getenv(var_name)
        if value:
            # Mask sensitive values
            if "postgresql://" in value.lower() or "api_key" in var_name.lower():
                masked = value[:20] + "..." + value[-10:] if len(value) > 30 else "***"
                print_check(f"ENV: {var_name}", True, f"{description} (set)")
            else:
                print_check(f"ENV: {var_name}", True, f"{description} = {value}")
        else:
            if required:
                print_check(f"ENV: {var_name}", False, f"{description} - NOT SET")
                all_passed = False
            else:
                print(f"{Colors.YELLOW}  ⊘ ENV: {var_name} - Not set (optional){Colors.RESET}")

    # Check optional vars
    for var_name, description, _ in optional_vars:
        value = os.getenv(var_name)
        if value:
            if "api_key" in var_name.lower():
                masked = value[:10] + "..." if len(value) > 10 else "***"
                print_check(f"ENV: {var_name}", True, f"{description} (set)")
            else:
                print_check(f"ENV: {var_name}", True, f"{description} = {value}")
        else:
            print(f"{Colors.YELLOW}  ⊘ ENV: {var_name} - Not set (optional){Colors.RESET}")

    return all_passed


def main():
    """Run all health checks"""
    print(f"\n{Colors.BOLD}🏥 SYSTEM HEALTH CHECK{Colors.RESET}")
    print(f"{Colors.BOLD}Session 8: PostgreSQL Migration Validation{Colors.RESET}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Run all checks
    results = {
        "Database": check_database(),
        "Models": check_models(),
        "API Imports": check_api_imports(),
        "Environment": check_environment(),
    }

    # Summary
    print_header("SUMMARY")

    passed = sum(results.values())
    total = len(results)

    for check_name, status in results.items():
        print_check(check_name, status)

    print(f"\n{Colors.BOLD}Result: {passed}/{total} checks passed{Colors.RESET}")

    if all(results.values()):
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL CHECKS PASSED - SYSTEM HEALTHY{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME CHECKS FAILED - SYSTEM UNHEALTHY{Colors.RESET}\n")
        print(f"{Colors.YELLOW}Hint: Check the failed items above and fix the issues.{Colors.RESET}")
        print(f"{Colors.YELLOW}For database issues, ensure SUPABASE_URL is set correctly.{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
