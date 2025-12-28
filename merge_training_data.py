#!/usr/bin/env python3
"""
Training Data Merger
====================

Merges multiple training data CSV files into a single consolidated dataset.
- Removes duplicates based on match_id
- Handles both simple (champion-only) and extended (with items) formats
- Normalizes column order for consistency
- Creates backup of existing massive dataset

Usage:
    python merge_training_data.py
"""

import pandas as pd
import os
import shutil
from pathlib import Path
from datetime import datetime


class DataMerger:
    """Handles merging of multiple training data files"""

    def __init__(self, output_file='data/clean_training_data_massive.csv'):
        self.output_file = Path(output_file)
        self.data_dir = Path('data')

        # Files to merge (in priority order)
        self.source_files = [
            self.data_dir / 'clean_training_data_items.csv',    # 5,000 matches with items
            self.data_dir / 'clean_training_data_massive.csv',  # 8,024 matches
            self.data_dir / 'clean_training_data.csv'           # 100 matches (test data)
        ]

    def backup_existing_file(self):
        """Create timestamped backup of existing output file"""
        if not self.output_file.exists():
            print("ℹ️  No existing file to backup")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.output_file.parent / f"{self.output_file.stem}_backup_{timestamp}.csv"

        shutil.copy2(self.output_file, backup_file)
        print(f"✅ Backup created: {backup_file.name}")

    def normalize_dataframe(self, df):
        """
        Normalize dataframe to have consistent columns.
        Removes item columns if present (train_model.py doesn't use them yet).
        Keeps only champion IDs and match_id, blue_win.
        """
        # Required columns for training
        required_cols = ['match_id', 'blue_win']
        champion_cols = [
            'blue_champ_1', 'blue_champ_2', 'blue_champ_3', 'blue_champ_4', 'blue_champ_5',
            'red_champ_1', 'red_champ_2', 'red_champ_3', 'red_champ_4', 'red_champ_5'
        ]

        all_required = required_cols + champion_cols

        # Check if all required columns exist
        missing = set(all_required) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Select only required columns (drops item columns if present)
        df_normalized = df[all_required].copy()

        return df_normalized

    def load_source_files(self):
        """Load all source files and combine them"""
        print("\n" + "=" * 80)
        print("LOADING SOURCE FILES")
        print("=" * 80)

        all_dfs = []

        for source_file in self.source_files:
            if not source_file.exists():
                print(f"⏭️  Skipping {source_file.name} (not found)")
                continue

            try:
                df = pd.read_csv(source_file)
                original_count = len(df)

                # Normalize columns
                df = self.normalize_dataframe(df)

                all_dfs.append(df)
                print(f"✅ Loaded {source_file.name}: {original_count:,} matches")

            except Exception as e:
                print(f"❌ Error loading {source_file.name}: {str(e)}")
                continue

        if not all_dfs:
            raise ValueError("No source files could be loaded!")

        return all_dfs

    def merge_and_deduplicate(self, dfs):
        """Merge dataframes and remove duplicates"""
        print("\n" + "=" * 80)
        print("MERGING & DEDUPLICATING")
        print("=" * 80)

        # Concatenate all dataframes
        combined = pd.concat(dfs, ignore_index=True)
        print(f"📊 Combined total: {len(combined):,} matches")

        # Remove duplicates based on match_id
        before_dedup = len(combined)
        combined = combined.drop_duplicates(subset='match_id', keep='first')
        after_dedup = len(combined)

        duplicates_removed = before_dedup - after_dedup
        print(f"🗑️  Removed {duplicates_removed:,} duplicates")
        print(f"✅ Final dataset: {after_dedup:,} unique matches")

        return combined

    def validate_data(self, df):
        """Validate the merged dataset"""
        print("\n" + "=" * 80)
        print("VALIDATING MERGED DATA")
        print("=" * 80)

        # Check for missing values
        missing = df.isnull().sum()
        if missing.any():
            print("⚠️  Warning: Missing values detected:")
            print(missing[missing > 0])
        else:
            print("✅ No missing values")

        # Check target distribution
        blue_wins = (df['blue_win'] == 1).sum()
        red_wins = (df['blue_win'] == 0).sum()
        total = len(df)

        blue_pct = blue_wins / total * 100
        red_pct = red_wins / total * 100

        print(f"\n📊 Target Distribution:")
        print(f"   Blue wins: {blue_wins:,} ({blue_pct:.1f}%)")
        print(f"   Red wins:  {red_wins:,} ({red_pct:.1f}%)")

        # Check if balanced (should be roughly 50/50)
        if abs(blue_pct - 50) > 10:
            print(f"⚠️  Warning: Unbalanced dataset! Expected ~50%, got {blue_pct:.1f}%")
        else:
            print(f"✅ Dataset is balanced")

        # Check champion ID ranges (should be positive integers)
        champion_cols = [col for col in df.columns if 'champ' in col]
        for col in champion_cols:
            if (df[col] <= 0).any():
                print(f"⚠️  Warning: Invalid champion IDs in {col}")

        print("✅ Validation complete")

    def save_merged_data(self, df):
        """Save the merged dataset"""
        print("\n" + "=" * 80)
        print("SAVING MERGED DATASET")
        print("=" * 80)

        # Ensure output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save to CSV
        df.to_csv(self.output_file, index=False)

        # Get file size
        file_size = self.output_file.stat().st_size / 1024 / 1024  # MB

        print(f"✅ Saved to: {self.output_file}")
        print(f"📦 File size: {file_size:.2f} MB")
        print(f"📊 Total matches: {len(df):,}")

    def run(self):
        """Execute the complete merge process"""
        print("=" * 80)
        print("🔀 TRAINING DATA MERGER")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # Backup existing file
            self.backup_existing_file()

            # Load source files
            dfs = self.load_source_files()

            # Merge and deduplicate
            merged_df = self.merge_and_deduplicate(dfs)

            # Validate
            self.validate_data(merged_df)

            # Save
            self.save_merged_data(merged_df)

            print("\n" + "=" * 80)
            print("✅ MERGE COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print(f"\n📈 Summary:")
            print(f"   Input files:  {len([f for f in self.source_files if f.exists()])}")
            print(f"   Output file:  {self.output_file}")
            print(f"   Total matches: {len(merged_df):,}")
            print(f"   Ready for training: ✅")
            print("\n" + "=" * 80 + "\n")

            return True

        except Exception as e:
            print("\n" + "=" * 80)
            print("❌ MERGE FAILED!")
            print("=" * 80)
            print(f"Error: {str(e)}")
            print("\n" + "=" * 80 + "\n")
            return False


def main():
    """Main entry point"""
    merger = DataMerger()
    success = merger.run()

    # Exit with appropriate code
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
