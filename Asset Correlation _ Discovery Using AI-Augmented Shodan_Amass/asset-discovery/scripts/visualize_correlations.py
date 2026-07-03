#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.patches import Patch

def visualize_asset_correlations(report_file):
    """Create visualizations of asset correlations"""
    
    with open(report_file, 'r') as f:
        report = json.load(f)
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Source distribution pie chart
    sources = report['sources']
    ax1.pie(sources.values(), labels=sources.keys(), autopct='%1.1f%%')
    ax1.set_title('Asset Sources Distribution')
    
    # 2. Risk score distribution
    if 'correlation_summary' in report:
        clusters = report['correlation_summary']
        risk_scores = [cluster['avg_risk_score'] for cluster in clusters.values()]
        ax2.hist(risk_scores, bins=10, alpha=0.7, color='red')
        ax2.set_title('Risk Score Distribution by Cluster')
        ax2.set_xlabel('Average Risk Score')
        ax2.set_ylabel('Number of Clusters')
    
    # 3. Cluster size distribution
    if 'correlation_summary' in report:
        cluster_sizes = [cluster['asset_count'] for cluster in clusters.values()]
        ax3.bar(range(len(cluster_sizes)), cluster_sizes, color='blue', alpha=0.7)
        ax3.set_title('Assets per Cluster')
        ax3.set_xlabel('Cluster ID')
        ax3.set_ylabel('Number of Assets')
    
    # 4. Summary statistics
    ax4.axis('off')
    stats_text = f"""
    Asset Discovery Summary
    
    Total Assets: {report['total_assets']}
    Clusters Found: {report['clusters_found']}
    High-Risk Assets: {report['high_risk_assets']}
    
    Discovery Sources:
    """
    for source, count in sources.items():
        stats_text += f"  • {source}: {count}\n"
    
    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, 
             fontsize=12, verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig('results/correlation_visualization.png', dpi=300, bbox_inches='tight')
    print("Visualization saved: results/correlation_visualization.png")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 visualize_correlations.py <report_file>")
        sys.exit(1)
    
    visualize_asset_correlations(sys.argv[1])
