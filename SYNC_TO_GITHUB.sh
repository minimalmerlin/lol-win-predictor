#!/bin/bash

echo "🔄 Syncing with GitHub & Railway..."
echo ""

# 1. Check remote
echo "📡 Checking remote repository..."
git remote -v

echo ""
echo "🌿 Current branch:"
git branch -a

echo ""
echo "📊 Current status:"
git status --short | head -20

echo ""
echo "═══════════════════════════════════════════"
echo "Next steps (run manually):"
echo "═══════════════════════════════════════════"
echo ""
echo "1️⃣  Stage all changes:"
echo "    git add ."
echo ""
echo "2️⃣  Commit changes:"
echo "    git commit -m \"Major cleanup & AI Build Generator - Production ready\""
echo ""
echo "3️⃣  Pull and merge remote changes:"
echo "    git pull origin main --allow-unrelated-histories"
echo ""
echo "4️⃣  Push to GitHub:"
echo "    git push origin main"
echo ""
echo "5️⃣  Railway will auto-deploy! 🚀"
echo ""

