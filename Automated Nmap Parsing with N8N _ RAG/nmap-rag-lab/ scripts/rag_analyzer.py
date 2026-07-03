#!/usr/bin/env python3
import json
import re
from datetime import datetime

class RAGVulnerabilityAnalyzer:
    def __init__(self, kb_file):
        with open(kb_file, 'r') as f:
            self.knowledge_base = json.load(f)
    
    def analyze_scan_results(self, scan_file):
        """Analyze scan results using RAG approach"""
        with open(scan_file, 'r') as f:
            scan_data = json.load(f)
        
        enhanced_results = {
            'analysis_time': datetime.now().isoformat(),
            'total_hosts': len(scan_data['hosts']),
            'enhanced_vulnerabilities': [],
            'recommendations': []
        }
        
        for host in scan_data['hosts']:
            host_vulns = self._analyze_host(host)
            enhanced_results['enhanced_vulnerabilities'].extend(host_vulns)
        
        # Generate recommendations
        enhanced_results['recommendations'] = self._generate_recommendations(
            enhanced_results['enhanced_vulnerabilities']
        )
        
        return enhanced_results
    
    def _analyze_host(self, host):
        """Analyze individual host for vulnerabilities"""
        vulnerabilities = []
        
        # Check open ports against known vulnerabilities
        for port in host['ports']:
            if port['state'] == 'open':
                port_vulns = self._check_port_vulnerabilities(
                    host['ip'], port, host.get('os', '')
                )
                vulnerabilities.extend(port_vulns)
        
        # Enhance existing vulnerability detections
        for vuln in host.get('vulnerabilities', []):
            enhanced_vuln = self._enhance_vulnerability(host['ip'], vuln)
            vulnerabilities.append(enhanced_vuln)
        
        return vulnerabilities
    
    def _check_port_vulnerabilities(self, ip, port, os_info):
        """Check port against vulnerability knowledge base"""
        vulnerabilities = []
        
        for kb_vuln in self.knowledge_base['vulnerabilities']:
            if port['port'] in kb_vuln['ports']:
                # Check for service indicators
                service_match = any(
                    indicator.lower() in port.get('service', '').lower() or
                    indicator.lower() in os_info.lower()
                    for indicator in kb_vuln['indicators']
                )
                
                if service_match:
                    vulnerabilities.append({
                        'ip': ip,
                        'port': port['port'],
                        'cve': kb_vuln['cve'],
                        'name': kb_vuln['name'],
                        'severity': kb_vuln['severity'],
                        'description': kb_vuln['description'],
                        'remediation': kb_vuln['remediation'],
                        'confidence': 'HIGH' if service_match else 'MEDIUM'
                    })
        
        return vulnerabilities
    
    def _enhance_vulnerability(self, ip, vuln):
        """Enhance detected vulnerability with KB information"""
        enhanced = {
            'ip': ip,
            'script': vuln['script'],
            'output': vuln['output'],
            'severity': 'UNKNOWN',
            'cve': 'N/A',
            'remediation': 'Manual investigation required'
        }
        
        # Try to match against knowledge base
        for kb_vuln in self.knowledge_base['vulnerabilities']:
            if any(indicator.lower() in vuln['output'].lower() 
                   for indicator in kb_vuln['indicators']):
                enhanced.update({
                    'cve': kb_vuln['cve'],
                    'name': kb_vuln['name'],
                    'severity': kb_vuln['severity'],
                    'remediation': kb_vuln['remediation']
                })
                break
        
        return enhanced
    
    def _generate_recommendations(self, vulnerabilities):
        """Generate prioritized recommendations"""
        recommendations = []
        
        # Group by severity
        critical = [v for v in vulnerabilities if v.get('severity') == 'CRITICAL']
        high = [v for v in vulnerabilities if v.get('severity') == 'HIGH']
        
        if critical:
            recommendations.append({
                'priority': 'IMMEDIATE',
                'action': f'Address {len(critical)} critical vulnerabilities immediately',
                'details': [v.get('remediation', 'Unknown') for v in critical[:3]]
            })
        
        if high:
            recommendations.append({
                'priority': 'HIGH',
                'action': f'Address {len(high)} high-severity vulnerabilities',
                'details': [v.get('remediation', 'Unknown') for v in high[:3]]
            })
        
        return recommendations

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 rag_analyzer.py <scan_json_file>")
        sys.exit(1)
    
    analyzer = RAGVulnerabilityAnalyzer('data/vulnerability_kb.json')
    results = analyzer.analyze_scan_results(sys.argv[1])
    
    output_file = f"data/rag_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"RAG analysis completed. Results saved to {output_file}")
    print(f"Found {len(results['enhanced_vulnerabilities'])} enhanced vulnerabilities")
    print(f"Generated {len(results['recommendations'])} recommendations")
