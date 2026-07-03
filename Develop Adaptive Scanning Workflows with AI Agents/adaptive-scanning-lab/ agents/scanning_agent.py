import nmap
import json
import random
from base_agent import BaseAgent

class AdaptiveScanningAgent(BaseAgent):
    def __init__(self, name="ScanAgent"):
        super().__init__(name)
        self.nm = nmap.PortScanner()
        self.scan_techniques = [
            '-sS',  # SYN scan
            '-sT',  # TCP connect scan
            '-sU',  # UDP scan
            '-sA',  # ACK scan
        ]
        self.port_ranges = ['1-1000', '1-65535', '80,443,22,21,25']
        
    def analyze(self, target_data):
        """Analyze previous scan results to determine next action"""
        if not target_data.get('previous_scans'):
            return {'recommendation': 'initial_scan', 'confidence': 1.0}
        
        # Simple AI logic - analyze open ports and services
        open_ports = target_data.get('open_ports', [])
        services = target_data.get('services', [])
        
        # Determine scan intensity based on findings
        if len(open_ports) > 10:
            return {'recommendation': 'deep_scan', 'confidence': 0.8}
        elif any('http' in service for service in services):
            return {'recommendation': 'web_scan', 'confidence': 0.9}
        else:
            return {'recommendation': 'standard_scan', 'confidence': 0.6}
    
    def decide(self, analysis_result):
        """Make scanning decisions based on analysis"""
        recommendation = analysis_result['recommendation']
        
        if recommendation == 'initial_scan':
            return {
                'technique': '-sS',
                'ports': '1-1000',
                'timing': '-T3'
            }
        elif recommendation == 'deep_scan':
            return {
                'technique': '-sS -sV',
                'ports': '1-65535',
                'timing': '-T2'
            }
        elif recommendation == 'web_scan':
            return {
                'technique': '-sS -sV --script=http-*',
                'ports': '80,443,8080,8443',
                'timing': '-T4'
            }
        else:
            return {
                'technique': '-sS',
                'ports': '1-1000',
                'timing': '-T3'
            }
    
    def execute_scan(self, target, scan_params):
        """Execute the actual scan"""
        try:
            command = f"nmap {scan_params['technique']} {scan_params['timing']} -p {scan_params['ports']} {target}"
            self.nm.scan(target, scan_params['ports'], scan_params['technique'])
            
            results = {
                'target': target,
                'scan_params': scan_params,
                'results': dict(self.nm[target]) if target in self.nm.all_hosts() else {},
                'timestamp': time.time()
            }
            
            self.log_action('scan_executed', results)
            return results
            
        except Exception as e:
            error_result = {'error': str(e), 'target': target}
            self.log_action('scan_failed', error_result)
            return error_result
