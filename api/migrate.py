"""
Vercel Serverless Function to run database migration
Access via: https://your-domain.vercel.app/api/migrate
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.migrate_champion_data import migrate_champion_stats

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Run migration when POST request is received"""
        try:
            # Run migration
            success = migrate_champion_stats()

            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Champion data migration completed successfully"
                }).encode())
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": "Migration failed"
                }).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())

    def do_GET(self):
        """Show migration info"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "endpoint": "/api/migrate",
            "method": "POST",
            "description": "Run champion data migration from JSON to PostgreSQL",
            "note": "This will load 139 champions into the database"
        }).encode())
