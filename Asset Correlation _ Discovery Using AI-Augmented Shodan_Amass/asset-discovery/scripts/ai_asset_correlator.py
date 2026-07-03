#!/usr/bin/env python3
import json
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import requests
import subprocess
import sys
from datetime import datetime

class AIAssetCorrelator:
    def __init__(self):
        self.assets_df = pd.DataFrame()
        self.correlation_graph = nx.Graph()
        
    def load_shodan_data(self, query, limit=100):
        """Load asset data from Shodan"""
        try:
            cmd = f"shodan search --fields ip_str,port,org,hostnames,product,version '{query}' --limit {limit}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            assets = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('\t')
                    if len(parts) >= 6:
                        assets.append({
                            'ip': parts[0],
                            'port': parts[1],
                            'org': parts[2],
                            'hostnames': parts[3],
                            'product': parts[4],
                            'version': parts[5],
                            'source': 'shodan'
                        })
            return assets
        except Exception as e:
            print(f"Error loading Shodan data: {e}")
            return []
    
    def load_amass_data(self, domain):
        """Load subdomain data from Amass"""
        try:
            cmd = f"amass enum -passive -d {domain} -json"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            assets = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)
                        assets.append({
                            'domain': data.get('name', ''),
                            'ip': ','.join(data.get('addresses', [])),
                            'source': 'amass',
                            'type': data.get('type', ''),
                            'tag': data.get('tag', '')
                        })
                    except json.JSONDecodeError:
                        continue
            return assets
        except Exception as e:
            print(f"Error loading Amass data: {e}")
            return []
    
    def correlate_assets(self, shodan_assets, amass_assets):
        """Use AI to correlate assets from different sources"""
        # Combine datasets
        all_assets = []
        
        # Process Shodan assets
        for asset in shodan_assets:
            all_assets.append({
                'identifier': asset['ip'],
                'secondary_id': asset.get('hostnames', ''),
                'org': asset.get('org', ''),
                'product': asset.get('product', ''),
                'port': asset.get('port', ''),
                'source': 'shodan',
                'risk_score': self.calculate_risk_score(asset)
            })
        
        # Process Amass assets
        for asset in amass_assets:
            all_assets.append({
                'identifier': asset['domain'],
                'secondary_id': asset.get('ip', ''),
                'org': '',
                'product': '',
                'port': '',
                'source': 'amass',
                'risk_score': self.calculate_risk_score(asset)
            })
        
        self.assets_df = pd.DataFrame(all_assets)
        
        # Perform clustering for correlation
        self.perform_clustering()
        
        # Build correlation graph
        self.build_correlation_graph()
        
        return self.assets_df
    
    def calculate_risk_score(self, asset):
        """Calculate risk score based on asset characteristics"""
        score = 0
        
        # High-risk ports
        high_risk_ports = ['22', '23', '80', '443', '3389', '5900']
        if asset.get('port') in high_risk_ports:
            score += 3
        
        # Known vulnerable products
        vulnerable_products = ['apache', 'nginx', 'iis', 'ssh']
        product = asset.get('product', '').lower()
        if any(vp in product for vp in vulnerable_products):
            score += 2
        
        # External facing (has public IP)
        if asset.get('ip') and not asset['ip'].startswith(('10.', '192.168.', '172.')):
            score += 1
        
        return min(score, 10)  # Cap at 10
    
    def perform_clustering(self):
        """Use DBSCAN clustering to group related assets"""
        if self.assets_df.empty:
            return
        
        # Create feature vectors for clustering
        features = []
        for _, row in self.assets_df.iterrows():
            feature_text = f"{row['org']} {row['product']} {row['secondary_id']}"
            features.append(feature_text)
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        feature_matrix = vectorizer.fit_transform(features)
        
        # DBSCAN clustering
        clustering = DBSCAN(eps=0.3, min_samples=2)
        clusters = clustering.fit_predict(feature_matrix.toarray())
        
        self.assets_df['cluster'] = clusters
    
    def build_correlation_graph(self):
        """Build a network graph showing asset relationships"""
        for _, asset in self.assets_df.iterrows():
            self.correlation_graph.add_node(
                asset['identifier'],
                source=asset['source'],
                risk_score=asset['risk_score'],
                cluster=asset['cluster']
            )
        
        # Add edges between assets in the same cluster
        clusters = self.assets_df.groupby('cluster')
        for cluster_id, group in clusters:
            if cluster_id != -1:  # Ignore noise points
                assets_in_cluster = group['identifier'].tolist()
                for i, asset1 in enumerate(assets_in_cluster):
                    for asset2 in assets_in_cluster[i+1:]:
                        self.correlation_graph.add_edge(asset1, asset2, weight=0.8)
    
    def generate_report(self, output_file):
        """Generate comprehensive correlation report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_assets': len(self.assets_df),
            'sources': self.assets_df['source'].value_counts().to_dict(),
            'clusters_found': len(self.assets_df['cluster'].unique()) - (1 if -1 in self.assets_df['cluster'].values else 0),
            'high_risk_assets': len(self.assets_df[self.assets_df['risk_score'] >= 7]),
            'correlation_summary': self.get_correlation_summary()
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report generated: {output_file}")
        return report
    
    def get_correlation_summary(self):
        """Get summary of correlations found"""
        summary = {}
        clusters = self.assets_df.groupby('cluster')
        
        for cluster_id, group in clusters:
            if cluster_id != -1:
                summary[f'cluster_{cluster_id}'] = {
                    'asset_count': len(group),
                    'sources': group['source'].unique().tolist(),
                    'avg_risk_score': group['risk_score'].mean(),
                    'assets': group['identifier'].tolist()
                }
        
        return summary

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 ai_asset_correlator.py <shodan_query> <target_domain>")
        sys.exit(1)
    
    correlator = AIAssetCorrelator()
    
    # Load data from both sources
    print("Loading Shodan data...")
    shodan_assets = correlator.load_shodan_data(sys.argv[1])
    
    print("Loading Amass data...")
    amass_assets = correlator.load_amass_data(sys.argv[2])
    
    # Correlate assets
    print("Correlating assets using AI...")
    correlated_df = correlator.correlate_assets(shodan_assets, amass_assets)
    
    # Generate report
    report = correlator.generate_report('results/correlation_report.json')
    
    print(f"\nCorrelation Summary:")
    print(f"Total assets discovered: {report['total_assets']}")
    print(f"Clusters identified: {report['clusters_found']}")
    print(f"High-risk assets: {report['high_risk_assets']}")
