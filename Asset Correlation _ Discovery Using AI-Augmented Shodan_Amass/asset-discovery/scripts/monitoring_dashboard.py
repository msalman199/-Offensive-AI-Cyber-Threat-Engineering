#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

class AssetMonitoringDashboard:
    def __init__(self, results_dir="results"):
        self.results_dir = results_dir
    
    def get_recent_reports(self, days=7):
        """Get correlation reports from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        reports = []
        
        for report_file in glob.glob(f"{self.results_dir}/correlation_report*.json"):
            try:
                with open(report_file, 'r') as f:
                    report = json.load(f)
                    report_date = datetime.fromisoformat(report['timestamp'].replace('Z', '+00:00').replace('+00:00', ''))
                    
                    if report_date >= cutoff_date:
                        report['file'] = report_file
                        reports.append(report)
            except Exception as e:
                print(f"Error reading {report_file}: {e}")
        
        return sorted(reports, key=lambda x: x['timestamp'])
    
    def generate_trend_analysis(self, reports):
        """Generate trend analysis from multiple reports"""
        if not reports:
            print("No reports found for trend analysis")
            return
        
        # Extract trend data
        timestamps = [datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00').replace('+00:00', '')) for r in reports]
        total_assets = [r['total_assets'] for r in reports]
        high_risk_assets = [r['high_risk_assets'] for r in reports]
        clusters_found = [r['clusters_found'] for r in reports]
        
        # Create trend visualization
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # Total assets trend
        ax1.plot(timestamps, total_assets, marker='o', color='blue')
        ax1.set_title('Total Assets Discovered Over Time')
        ax1.set_ylabel('Number of Assets')
        ax1.grid(True, alpha=0.3)
        
        # High-risk assets trend
        ax2.plot(timestamps, high_risk_assets, marker='s', color='red')
        ax2.set_title('High-Risk Assets Over Time')
        ax2.set_ylabel('High-Risk Assets')
        ax2.grid(True, alpha=0.3)
        
        # Clusters trend
        ax3.plot(timestamps, clusters_found, marker='^', color='green')
        ax3.set_title('Asset Clusters Identified Over Time')
        ax3.set_ylabel('Number of Clusters')
        ax3.set_xlabel('Date')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.savefig(f'{self.results_dir}/trend_analysis.png', dpi=300, bbox_inches='tight')
        print(f"Trend analysis saved: {self.results_dir}/trend_analysis.png")
    
    def generate_summary_report(self, reports):
        """Generate a comprehensive summary report"""
        if not reports:
            return
        
        latest_report = reports[-1]
        
        summary = {
            "dashboard_generated": datetime.now().isoformat(),
            "analysis_period": f"Last {len(reports)} reports",
            "latest_scan": latest_report['timestamp'],
            "current_stats": {
                "total_assets": latest_report['total_assets'],
                "high_risk_assets": latest_report['high_risk_assets'],
                "clusters_found": latest_report['clusters_found']
            },
            "trends": {
                "avg_assets_per_scan": sum(r['total_assets'] for r in reports) / len(reports),
                "avg_high_risk_per_scan": sum(r['high_risk_assets'] for r in reports) / len(reports),
                "avg_clusters_per_scan": sum(r['clusters_found'] for r in reports) / len(reports)
            },
            "recommendations": self.generate_recommendations(reports)
        }
        
        with open(f'{self.results_dir}/dashboard_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("Dashboard Summary:")
        print(f"  Latest scan: {summary['latest_scan']}")
        print(f"  Current assets: {summary['current_stats']['total_assets']}")
        print(f"  High-risk assets: {summary['current_stats']['high_risk_assets']}")
        print(f"  Clusters identified: {summary['current_stats']['clusters_found']}")
        
        return summary
    
    def generate_recommendations(self, reports):
        """Generate security recommendations based on trends"""
        recommendations = []
        
        if not reports:
            return recommendations
        
        latest = reports[-1]
        
        # High-risk asset recommendations
        if latest['high_risk_assets'] > 0:
            recommendations.append({
                "priority": "HIGH",
                "category": "Risk Management",
                "description": f"Found {latest['high_risk_assets']} high-risk assets requiring immediate attention"
            })
        
        # Clustering recommendations
        if latest['clusters_found'] > 5:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Asset Management",
                "description": f"Large number of asset clusters ({latest['clusters_found']}) detected - consider consolidation"
            })
        
        # Trend-based recommendations
        if len(reports) > 1:
            asset_growth = latest['total_assets'] - reports[0]['total_assets']
            if asset_growth > 10:
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "Monitoring",
                    "description": f"Significant asset growth detected (+{asset_growth}) - increase monitoring frequency"
                })
        
        return recommendations

if __name__ == "__main__":
    dashboard = AssetMonitoringDashboard()
    
    print("Generating Asset Discovery Dashboard...")
    
    # Get recent reports
    reports = dashboard.get_recent_reports(days=30)
    
    if reports:
        # Generate trend analysis
        dashboard.generate_trend_analysis(reports)
        
        # Generate summary report
        summary = dashboard.generate_summary_report(reports)
        
        print(f"\nDashboard generated successfully!")
        print(f"Reports analyzed: {len(reports)}")
        
        if summary and summary['recommendations']:
            print("\nRecommendations:")
            for rec in summary['recommendations']:
                print(f"  [{rec['priority']}] {rec['category']}: {rec['description']}")
    else:
        print("No recent reports found. Run some discovery scans first.")
