#!/usr/bin/env python3
"""
Victory AI Daily Loop - ML Pipeline Orchestrator
================================================

Automated end-to-end ML pipeline for League of Legends Win Prediction System.

Pipeline Stages:
1. Data Fetching - Collect new match data from Riot API
2. Data Processing - Generate item builds and frontend stats
3. Model Training - Train and evaluate ML models

Usage:
    python pipeline.py [--matches N] [--skip-fetch] [--skip-processing] [--skip-training]

Examples:
    python pipeline.py                    # Default: 100 matches
    python pipeline.py --matches 1000     # Fetch 1000 matches
    python pipeline.py --skip-fetch       # Skip fetching, only process & train
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional


class PipelineConfig:
    """Pipeline configuration and paths"""
    ROOT_DIR = Path(__file__).parent
    FETCH_SCRIPT = ROOT_DIR / "fetch_matches_with_items.py"
    MERGE_SCRIPT = ROOT_DIR / "merge_training_data.py"
    PROCESS_SCRIPT = ROOT_DIR / "generate_item_builds.py"
    TRAIN_SCRIPT = ROOT_DIR / "train_model.py"

    # Validate scripts exist
    REQUIRED_SCRIPTS = [FETCH_SCRIPT, MERGE_SCRIPT, PROCESS_SCRIPT, TRAIN_SCRIPT]


class PipelineLogger:
    """Formatted console logging for pipeline execution"""

    @staticmethod
    def header(message: str):
        """Print section header"""
        print("\n" + "=" * 80)
        print(f"  {message}")
        print("=" * 80)

    @staticmethod
    def step(step_num: int, total: int, message: str):
        """Print step header"""
        print(f"\n[STEP {step_num}/{total}] {message}")
        print("-" * 80)

    @staticmethod
    def info(message: str):
        """Print info message"""
        print(f"ℹ️  {message}")

    @staticmethod
    def success(message: str):
        """Print success message"""
        print(f"✅ {message}")

    @staticmethod
    def error(message: str):
        """Print error message"""
        print(f"❌ ERROR: {message}", file=sys.stderr)

    @staticmethod
    def duration(seconds: float):
        """Print formatted duration"""
        if seconds < 60:
            print(f"⏱️  Duration: {seconds:.2f} seconds")
        else:
            minutes = int(seconds // 60)
            secs = seconds % 60
            print(f"⏱️  Duration: {minutes}m {secs:.2f}s")


class PipelineStep:
    """Represents a single pipeline step"""

    def __init__(self, name: str, script_path: Path, args: list = None):
        self.name = name
        self.script_path = script_path
        self.args = args or []
        self.duration = 0.0
        self.success = False

    def execute(self) -> bool:
        """
        Execute the pipeline step

        Returns:
            True if successful, False otherwise
        """
        if not self.script_path.exists():
            PipelineLogger.error(f"Script not found: {self.script_path}")
            return False

        PipelineLogger.info(f"Executing: python {self.script_path.name}")

        # Build command
        cmd = [sys.executable, str(self.script_path)] + self.args

        # Execute with timing
        start_time = time.time()

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=False,  # Show output in real-time
                text=True,
                cwd=str(self.script_path.parent)
            )

            self.duration = time.time() - start_time
            self.success = True

            PipelineLogger.success(f"{self.name} completed successfully")
            PipelineLogger.duration(self.duration)

            return True

        except subprocess.CalledProcessError as e:
            self.duration = time.time() - start_time
            self.success = False

            PipelineLogger.error(f"{self.name} failed with exit code {e.returncode}")
            PipelineLogger.duration(self.duration)

            return False

        except KeyboardInterrupt:
            self.duration = time.time() - start_time
            PipelineLogger.error(f"{self.name} interrupted by user")
            return False

        except Exception as e:
            self.duration = time.time() - start_time
            self.success = False

            PipelineLogger.error(f"{self.name} failed with unexpected error: {str(e)}")
            PipelineLogger.duration(self.duration)

            return False


class MLPipeline:
    """Main ML Pipeline orchestrator"""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.steps = []
        self.total_duration = 0.0
        self.start_time = None

    def add_step(self, step: PipelineStep):
        """Add a step to the pipeline"""
        self.steps.append(step)

    def validate_environment(self) -> bool:
        """Validate that all required scripts exist"""
        PipelineLogger.info("Validating pipeline environment...")

        missing_scripts = []
        for script in self.config.REQUIRED_SCRIPTS:
            if not script.exists():
                missing_scripts.append(script.name)

        if missing_scripts:
            PipelineLogger.error(f"Missing required scripts: {', '.join(missing_scripts)}")
            return False

        PipelineLogger.success("Environment validation passed")
        return True

    def run(self) -> bool:
        """
        Execute the complete pipeline

        Returns:
            True if all steps succeeded, False otherwise
        """
        self.start_time = time.time()

        PipelineLogger.header("🚀 VICTORY AI DAILY LOOP - ML PIPELINE")
        PipelineLogger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        PipelineLogger.info(f"Total steps: {len(self.steps)}")

        # Validate environment
        if not self.validate_environment():
            return False

        # Execute each step
        for idx, step in enumerate(self.steps, 1):
            PipelineLogger.step(idx, len(self.steps), step.name)

            success = step.execute()

            if not success:
                PipelineLogger.error(f"Pipeline failed at step {idx}: {step.name}")
                self._print_summary(failed_step=idx)
                return False

        # All steps succeeded
        self._print_summary()
        return True

    def _print_summary(self, failed_step: Optional[int] = None):
        """Print pipeline execution summary"""
        self.total_duration = time.time() - self.start_time

        PipelineLogger.header("📊 PIPELINE EXECUTION SUMMARY")

        # Step-by-step breakdown
        for idx, step in enumerate(self.steps, 1):
            status = "✅ SUCCESS" if step.success else "❌ FAILED"
            if step.duration > 0:
                print(f"  {idx}. {step.name:30} {status:15} ({step.duration:.2f}s)")
            else:
                print(f"  {idx}. {step.name:30} ⏭️  SKIPPED")

        print("\n" + "-" * 80)

        # Total duration
        PipelineLogger.duration(self.total_duration)

        # Final status
        print()
        if failed_step is None:
            PipelineLogger.success("Pipeline completed successfully! 🎉")
            print("\n✨ Model is ready for deployment!")
        else:
            PipelineLogger.error(f"Pipeline failed at step {failed_step}/{len(self.steps)}")
            print("\n⚠️  Fix the error and re-run the pipeline.")

        print("=" * 80 + "\n")


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Victory AI ML Pipeline - Automated training loop",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py                    # Run full pipeline (100 matches)
  python pipeline.py --matches 1000     # Fetch 1000 matches
  python pipeline.py --skip-fetch       # Skip data fetching
  python pipeline.py --skip-merge       # Skip data merging
  python pipeline.py --skip-processing  # Skip data processing
  python pipeline.py --skip-training    # Skip model training
        """
    )

    parser.add_argument(
        "--matches",
        type=int,
        default=100,
        help="Number of matches to fetch (default: 100, use 10000 for production)"
    )

    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Skip data fetching step"
    )

    parser.add_argument(
        "--skip-merge",
        action="store_true",
        help="Skip data merging step"
    )

    parser.add_argument(
        "--skip-processing",
        action="store_true",
        help="Skip data processing step"
    )

    parser.add_argument(
        "--skip-training",
        action="store_true",
        help="Skip model training step"
    )

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    config = PipelineConfig()

    # Initialize pipeline
    pipeline = MLPipeline(config)

    # Add steps based on arguments
    if not args.skip_fetch:
        # Note: fetch_matches_with_items.py uses TARGET_MATCHES from config
        # For now, we'll use the default. To make it configurable, the fetch script
        # would need to accept command-line arguments
        fetch_step = PipelineStep(
            name="Data Fetching (Riot API)",
            script_path=config.FETCH_SCRIPT,
            args=[]  # Could add ["--matches", str(args.matches)] if script supports it
        )
        pipeline.add_step(fetch_step)

    if not args.skip_merge:
        merge_step = PipelineStep(
            name="Data Merging (Consolidate Datasets)",
            script_path=config.MERGE_SCRIPT,
            args=[]
        )
        pipeline.add_step(merge_step)

    if not args.skip_processing:
        process_step = PipelineStep(
            name="Data Processing (Item Builds)",
            script_path=config.PROCESS_SCRIPT,
            args=[]
        )
        pipeline.add_step(process_step)

    if not args.skip_training:
        train_step = PipelineStep(
            name="Model Training & Evaluation",
            script_path=config.TRAIN_SCRIPT,
            args=[]
        )
        pipeline.add_step(train_step)

    # Validate we have at least one step
    if len(pipeline.steps) == 0:
        PipelineLogger.error("No steps to execute (all steps skipped)")
        sys.exit(1)

    # Execute pipeline
    success = pipeline.run()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
