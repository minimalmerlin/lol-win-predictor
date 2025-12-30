#!/bin/bash
###############################################################################
# Automation Setup Script
###############################################################################
#
# This script sets up automated pipeline execution using cron
#
# Usage:
#   bash setup_automation.sh
#
###############################################################################

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get project directory (absolute path)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=$(which python3)
PIPELINE_SCRIPT="$PROJECT_DIR/automated_pipeline.py"
LOG_FILE="$PROJECT_DIR/pipeline.log"

echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}  Automation Setup${NC}"
echo -e "${GREEN}====================================${NC}"
echo ""
echo "Project Directory: $PROJECT_DIR"
echo "Python Binary: $PYTHON_BIN"
echo "Pipeline Script: $PIPELINE_SCRIPT"
echo ""

# Verify files exist
if [ ! -f "$PIPELINE_SCRIPT" ]; then
    echo -e "${RED}Error: Pipeline script not found at $PIPELINE_SCRIPT${NC}"
    exit 1
fi

if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Make sure environment variables are set.${NC}"
fi

# Make pipeline executable
chmod +x "$PIPELINE_SCRIPT"
echo -e "${GREEN}✓${NC} Made pipeline script executable"

# Generate cron job entry
CRON_ENTRY="0 3 * * * cd \"$PROJECT_DIR\" && \"$PYTHON_BIN\" \"$PIPELINE_SCRIPT\" >> \"$LOG_FILE\" 2>&1"

echo ""
echo -e "${YELLOW}Recommended Cron Schedule:${NC}"
echo ""
echo "  # Run daily at 3 AM"
echo "  $CRON_ENTRY"
echo ""

# Ask user if they want to install cron job
read -p "Do you want to install this cron job now? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Backup existing crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || true

    # Check if entry already exists
    if crontab -l 2>/dev/null | grep -q "automated_pipeline.py"; then
        echo -e "${YELLOW}⚠ Cron job already exists. Removing old entry...${NC}"
        crontab -l | grep -v "automated_pipeline.py" | crontab -
    fi

    # Add new cron job
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

    echo -e "${GREEN}✓${NC} Cron job installed successfully"
    echo ""
    echo "Current crontab:"
    crontab -l | grep "automated_pipeline.py"
else
    echo -e "${YELLOW}Skipped cron installation.${NC}"
    echo "You can manually add the cron job later with:"
    echo "  crontab -e"
fi

echo ""
echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}====================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Test the pipeline manually:"
echo "   python3 automated_pipeline.py --dry-run"
echo ""
echo "2. Run pipeline for real:"
echo "   python3 automated_pipeline.py --force"
echo ""
echo "3. Monitor pipeline execution:"
echo "   tail -f pipeline.log"
echo ""
echo "4. Check cron logs:"
echo "   cat pipeline.log"
echo ""
echo "5. List installed cron jobs:"
echo "   crontab -l"
echo ""
echo "6. Remove cron job:"
echo "   crontab -e  # Then delete the line"
echo ""

# Create systemd service (for Linux servers - optional)
if [ -f "/etc/systemd/system" ] && [ "$(uname)" == "Linux" ]; then
    echo -e "${YELLOW}Detected systemd. Want to create a service instead of cron? (y/N)${NC}"
    read -p "" -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        SERVICE_FILE="/etc/systemd/system/lol-pipeline.service"
        TIMER_FILE="/etc/systemd/system/lol-pipeline.timer"

        echo "Creating systemd service and timer..."

        # Service file
        sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=LoL Victory AI Pipeline
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PATH"
ExecStart=$PYTHON_BIN $PIPELINE_SCRIPT
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=multi-user.target
EOF

        # Timer file (runs daily at 3 AM)
        sudo tee "$TIMER_FILE" > /dev/null <<EOF
[Unit]
Description=Run LoL Pipeline Daily
Requires=lol-pipeline.service

[Timer]
OnCalendar=daily
OnCalendar=03:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

        # Enable and start timer
        sudo systemctl daemon-reload
        sudo systemctl enable lol-pipeline.timer
        sudo systemctl start lol-pipeline.timer

        echo -e "${GREEN}✓${NC} Systemd timer installed"
        echo "Check status with: systemctl status lol-pipeline.timer"
    fi
fi

echo -e "${GREEN}Done!${NC}"
