#!/bin/bash
###############################################################################
# Pipeline Wrapper Script
# This script is called by cron to run the automated pipeline
###############################################################################

# Change to project directory
cd "/Users/merlinmechler/Library/Mobile Documents/com~apple~CloudDocs/Data Analysis/Win_Predicition_System_WR" || exit 1

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the pipeline
/usr/local/bin/python3 automated_pipeline.py "$@"

# Exit with pipeline's exit code
exit $?
