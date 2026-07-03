#!/usr/bin/env python3
import sqlite3
import json
import sys
import os

class SpiderFootExtractor:
    def __init__(self, db_path="/opt/spiderfoot/spiderfoot.db"):
        self.db_path = db_path
    
    def extract_scan_data(self, scan_id=None):
        if not os.path.exists(self.db_path):
            return {"error": "SpiderFoot database not found"}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if scan_id:
            query = "SELECT * FROM tbl_scan_results WHERE scan_instance_id = ?"
            cursor.execute(query, (scan_id,))
        else:
            query = "SELECT * FROM tbl_scan_results ORDER BY generated DESC LIMIT 50"
            cursor.execute(query)
        
        results = cursor.fetchall()
        conn.close()
        
        formatted_results = []
        for row in results:
            formatted_results.append({
                "module": row[1],
                "type": row[2],
                "data": row[3],
                "source": row[4]
            })
        
        return formatted_results
    
    def get_latest_scan_summary(self):
        data = self.extract_scan_data()
        if isinstance(data, dict) and "error" in data:
            return data
        
        summary = {
            "total_findings": len(data),
            "domains": [],
            "ips": [],
            "emails": []
        }
        
        for item in data:
            if "DOMAIN" in item["type"]:
                summary["domains"].append(item["data"])
            elif "IP" in item["type"]:
                summary["ips"].append(item["data"])
            elif "EMAIL" in item["type"]:
                summary["emails"].append(item["data"])
        
        return summary

if __name__ == "__main__":
    extractor = SpiderFootExtractor()
    summary = extractor.get_latest_scan_summary()
    print(json.dumps(summary, indent=2))
