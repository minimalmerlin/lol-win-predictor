#!/bin/bash
# Script to remove .env from git history
# WARNING: This rewrites git history - use with caution!

echo "⚠️  WARNING: This script will rewrite git history!"
echo "This will remove .env from all commits in the repository."
echo ""
echo "Before running this script:"
echo "1. Make sure all team members have pushed their changes"
echo "2. Notify all team members that they need to re-clone after this"
echo "3. Create a backup of your repository"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "🧹 Removing .env from git history..."
echo ""

# Method 1: Using git filter-branch (works on older git versions)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Method 2 (alternative): Using BFG Repo-Cleaner (faster, but requires Java)
# Download BFG from: https://rtyley.github.io/bfg-repo-cleaner/
# bfg --delete-files .env

echo ""
echo "✅ .env removed from git history"
echo ""
echo "⚠️  IMPORTANT: Now you need to force push to GitHub:"
echo ""
echo "  git push origin --force --all"
echo ""
echo "⚠️  WARNING: This will overwrite the remote repository!"
echo "All collaborators will need to re-clone or reset their local repos."
echo ""
echo "After force pushing, you should:"
echo "1. Go to GitHub → Settings → Secrets → Revoke your old Riot API key"
echo "2. Generate a new Riot API key"
echo "3. Update your local .env file with the new key"
echo "4. Add the new key to GitHub Secrets (RIOT_API_KEY)"
