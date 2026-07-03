#!/usr/bin/env python3
import subprocess
import json
import xml.etree.ElementTree as ET
import sys
from datetime import datetime

def run_nmap_scan(target, output_file):
    """Execute Nmap scan and save results"""
    cmd = [
        'nmap', '-sS', '-sV', '-O', '--script=vuln',
        '-oX', output_file, target
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"Scan completed for {target}")
            return True
        else:
            print(f"Scan failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Scan timed out")
        return False

def parse_nmap_xml(xml_file):
    """Parse Nmap XML output to JSON"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        results = {
            'scan_time': datetime.now().isoformat(),
            'hosts': []
        }
        
        for host in root.findall('host'):
            host_data = {
                'ip': '',
                'status': '',
                'ports': [],
                'os': '',
                'vulnerabilities': []
            }
            
            # Get IP address
            address = host.find('address')
            if address is not None:
                host_data['ip'] = address.get('addr')
            
            # Get host status
            status = host.find('status')
            if status is not None:
                host_data['status'] = status.get('state')
            
            # Get open ports
            ports = host.find('ports')
            if ports is not None:
                for port in ports.findall('port'):
                    port_data = {
                        'port': port.get('portid'),
                        'protocol': port.get('protocol'),
                        'state': '',
                        'service': ''
                    }
                    
                    state = port.find('state')
                    if state is not None:
                        port_data['state'] = state.get('state')
                    
                    service = port.find('service')
                    if service is not None:
                        port_data['service'] = service.get('name', '')
                    
                    host_data['ports'].append(port_data)
            
            # Get OS information
            os_elem = host.find('os')
            if os_elem is not None:
                osmatch = os_elem.find('osmatch')
                if osmatch is not None:
                    host_data['os'] = osmatch.get('name', '')
            
            # Get vulnerability script results
            hostscript = host.find('hostscript')
            if hostscript is not None:
                for script in hostscript.findall('script'):
                    if 'vuln' in script.get('id', ''):
                        host_data['vulnerabilities'].append({
                            'script': script.get('id'),
                            'output': script.get('output', '')
                        })
            
            results['hosts'].append(host_data)
        
        return results
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 nmap_scanner.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    xml_output = f"scans/scan_{target.replace('/', '_').replace('.', '_')}.xml"
    json_output = f"data/scan_{target.replace('/', '_').replace('.', '_')}.json"
    
    # Run Nmap scan
    if run_nmap_scan(target, xml_output):
        # Parse results
        parsed_data = parse_nmap_xml(xml_output)
        if parsed_data:
            with open(json_output, 'w') as f:
                json.dump(parsed_data, f, indent=2)
            print(f"Results saved to {json_output}")
        else:
            print("Failed to parse scan results")
    else:
        print("Scan failed")
