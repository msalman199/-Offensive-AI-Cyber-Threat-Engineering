<div align="center">

# 🕸️ Automated Nmap Parsing with N8N + RAG

### 🧠 Red Team Operations | Al Nafi Cybersecurity Training Platform

![Nmap](https://img.shields.io/badge/Nmap-Network%20Scanning-4682B4?style=for-the-badge&logo=nmap&logoColor=white)
![N8N](https://img.shields.io/badge/N8N-Workflow%20Automation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Vulnerability%20Analysis-000000?style=for-the-badge&logo=databricks&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)

![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=flat-square)
![Duration](https://img.shields.io/badge/Duration-2--3%20Hours-blue?style=flat-square)
![Category](https://img.shields.io/badge/Category-Network%20Security%20Assessment-orange?style=flat-square)
![Certification](https://img.shields.io/badge/Maps%20to-Red%20Team%20Operator%20Adversary%20Emulation-critical?style=flat-square)

</div>

---

## 📚 Table of Contents

- [🎯 Learning Objectives](#-learning-objectives)
- [✅ Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [🚀 Task 1: Environment Setup and Tool Installation](#-task-1-environment-setup-and-tool-installation)
- [🔎 Task 2: Configure Nmap Scanning](#-task-2-configure-nmap-scanning)
- [🔗 Task 3: Parse Nmap Results using N8N](#-task-3-parse-nmap-results-using-n8n)
- [🧠 Task 4: Implement RAG for Enhanced Vulnerability Discovery](#-task-4-implement-rag-for-enhanced-vulnerability-discovery)
- [⚙️ Task 5: Create Integrated Automation Pipeline](#️-task-5-create-integrated-automation-pipeline)
- [🔬 Task 6: Verification and Testing](#-task-6-verification-and-testing)
- [🗺️ MITRE ATT&CK Mapping](#️-mitre-attck-mapping)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📝 Key Takeaways](#-key-takeaways)
- [⚠️ Legal & Ethical Disclaimer](#️-legal--ethical-disclaimer)

---

## 🎯 Learning Objectives

| # | Objective |
|---|-----------|
| 1 | 📡 Configure and execute automated Nmap network scanning |
| 2 | 🔗 Parse Nmap XML output using N8N workflow automation |
| 3 | 🧠 Implement RAG (Retrieval-Augmented Generation) for enhanced vulnerability analysis |
| 4 | ⚙️ Create an automated pipeline for network security assessment |

## ✅ Prerequisites

| Requirement | Details |
|---|---|
| 💻 Linux CLI | Basic command-line knowledge |
| 📡 Network Scanning | Understanding of scanning concepts |
| 🧩 Data Structures | Familiarity with JSON/XML |
| 🐍 Python | Basic scripting experience |

---

## 🖥️ Lab Environment

> Al Nafi provides a **Linux-based cloud machine** for this lab. Click **Start Lab** to access your dedicated environment. The machine is provisioned bare metal with no pre-installed tools — you will install every component during the lab.

---

## 🚀 Task 1: Environment Setup and Tool Installation

![Step](https://img.shields.io/badge/Step-1.1-blue?style=flat-square) **Install Required Dependencies**

```bash
# 📦 Update system packages
sudo apt update && sudo apt upgrade -y

# 🧰 Install essential packages
sudo apt install -y curl wget git python3 python3-pip nodejs npm nmap

# 🐳 Install Docker for N8N
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# 📥 Install Python dependencies
pip3 install requests beautifulsoup4 lxml pandas numpy
```

![Step](https://img.shields.io/badge/Step-1.2-blue?style=flat-square) **Install N8N Automation Platform**

```bash
# 🌐 Launch N8N via Docker
docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

Open a new terminal and verify N8N is running:

```bash
# ✅ Confirm the service responds
curl -s http://localhost:5678 | grep -q "n8n" && echo "N8N is running" || echo "N8N failed to start"
```

![Step](https://img.shields.io/badge/Step-1.3-blue?style=flat-square) **Create Working Directory Structure**

```bash
# 📂 Create project directory structure
mkdir -p ~/nmap-rag-lab/{scans,scripts,data,workflows}
cd ~/nmap-rag-lab

# 🎯 TODO: Replace with your assigned lab target range
echo "127.0.0.1
10.0.0.1/24" > targets.txt
```

---

## 🔎 Task 2: Configure Nmap Scanning

![Step](https://img.shields.io/badge/Step-2.1-purple?style=flat-square) **Create Automated Nmap Scanner Script**

```python
cat > scripts/nmap_scanner.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import json
import xml.etree.ElementTree as ET
import sys
from datetime import datetime

def run_nmap_scan(target, output_file):
    """Execute Nmap scan and save results"""
    # 🎯 TODO: Adjust scan flags (-sS, -sV, -O, --script=vuln) to match your assignment scope
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

    if run_nmap_scan(target, xml_output):
        parsed_data = parse_nmap_xml(xml_output)
        if parsed_data:
            with open(json_output, 'w') as f:
                json.dump(parsed_data, f, indent=2)
            print(f"Results saved to {json_output}")
        else:
            print("Failed to parse scan results")
    else:
        print("Scan failed")
EOF

chmod +x scripts/nmap_scanner.py
```

![Step](https://img.shields.io/badge/Step-2.2-purple?style=flat-square) **Execute Test Scan**

```bash
# 🧪 Run test scan on localhost
python3 scripts/nmap_scanner.py 127.0.0.1

# 📄 Verify output files
ls -la scans/ data/
```

---

## 🔗 Task 3: Parse Nmap Results using N8N

![Step](https://img.shields.io/badge/Step-3.1-green?style=flat-square) **Create N8N Workflow Configuration**

```json
cat > workflows/nmap_parser_workflow.json << 'EOF'
{
  "name": "Nmap Results Parser",
  "nodes": [
    {
      "parameters": {
        "path": "/webhook/nmap-scan",
        "httpMethod": "POST"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "functionCode": "const scanData = items[0].json;\nconst vulnerabilities = [];\n\nfor (const host of scanData.hosts) {\n  for (const vuln of host.vulnerabilities) {\n    vulnerabilities.push({\n      ip: host.ip,\n      vulnerability: vuln.script,\n      details: vuln.output,\n      severity: vuln.output.includes('HIGH') ? 'HIGH' : \n                vuln.output.includes('MEDIUM') ? 'MEDIUM' : 'LOW'\n    });\n  }\n}\n\nreturn vulnerabilities.map(v => ({ json: v }));"
      },
      "name": "Parse Vulnerabilities",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [460, 300]
    },
    {
      "parameters": {
        "filePath": "/tmp/vulnerabilities.json",
        "jsonData": "={{ JSON.stringify($json) }}"
      },
      "name": "Save Results",
      "type": "n8n-nodes-base.writeFile",
      "typeVersion": 1,
      "position": [680, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "Parse Vulnerabilities",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse Vulnerabilities": {
      "main": [
        [
          {
            "node": "Save Results",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
EOF
```

![Step](https://img.shields.io/badge/Step-3.2-green?style=flat-square) **Test N8N Workflow**

```bash
# 📤 Send test data to N8N webhook
curl -X POST http://localhost:5678/webhook/nmap-scan \
  -H "Content-Type: application/json" \
  -d @data/scan_127_0_0_1.json

# ✅ Verify processed results
cat /tmp/vulnerabilities.json | jq '.' 2>/dev/null || cat /tmp/vulnerabilities.json
```

---

## 🧠 Task 4: Implement RAG for Enhanced Vulnerability Discovery

![Step](https://img.shields.io/badge/Step-4.1-orange?style=flat-square) **Create RAG Knowledge Base**

```json
cat > data/vulnerability_kb.json << 'EOF'
{
  "vulnerabilities": [
    {
      "cve": "CVE-2021-44228",
      "name": "Log4Shell",
      "description": "Remote code execution in Apache Log4j",
      "severity": "CRITICAL",
      "ports": ["8080", "9200", "8443"],
      "indicators": ["log4j", "apache", "java"],
      "remediation": "Update Log4j to version 2.17.0 or later"
    },
    {
      "cve": "CVE-2017-0144",
      "name": "EternalBlue",
      "description": "SMB vulnerability exploited by WannaCry",
      "severity": "HIGH",
      "ports": ["445", "139"],
      "indicators": ["smb", "windows", "ms17-010"],
      "remediation": "Apply Microsoft security update MS17-010"
    },
    {
      "cve": "CVE-2014-6271",
      "name": "Shellshock",
      "description": "Bash command injection vulnerability",
      "severity": "HIGH",
      "ports": ["80", "443", "22"],
      "indicators": ["bash", "cgi", "apache"],
      "remediation": "Update Bash to patched version"
    }
  ]
}
EOF
```

> 🎯 **TODO:** Extend the knowledge base with at least two additional CVEs relevant to your lab's target environment.

![Step](https://img.shields.io/badge/Step-4.2-orange?style=flat-square) **Create RAG Analysis Engine**

```python
cat > scripts/rag_analyzer.py << 'EOF'
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

        enhanced_results['recommendations'] = self._generate_recommendations(
            enhanced_results['enhanced_vulnerabilities']
        )

        return enhanced_results

    def _analyze_host(self, host):
        """Analyze individual host for vulnerabilities"""
        vulnerabilities = []

        for port in host['ports']:
            if port['state'] == 'open':
                port_vulns = self._check_port_vulnerabilities(
                    host['ip'], port, host.get('os', '')
                )
                vulnerabilities.extend(port_vulns)

        for vuln in host.get('vulnerabilities', []):
            enhanced_vuln = self._enhance_vulnerability(host['ip'], vuln)
            vulnerabilities.append(enhanced_vuln)

        return vulnerabilities

    def _check_port_vulnerabilities(self, ip, port, os_info):
        """Check port against vulnerability knowledge base"""
        vulnerabilities = []

        for kb_vuln in self.knowledge_base['vulnerabilities']:
            if port['port'] in kb_vuln['ports']:
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

        # 🎯 TODO: Add a MEDIUM/LOW priority bucket to complete the recommendation tiering
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
EOF

chmod +x scripts/rag_analyzer.py
```

![Step](https://img.shields.io/badge/Step-4.3-orange?style=flat-square) **Execute RAG Analysis**

```bash
# 🧠 Run RAG analysis on scan results
python3 scripts/rag_analyzer.py data/scan_127_0_0_1.json

# 📊 View enhanced results
ls -la data/rag_analysis_*.json
cat data/rag_analysis_*.json | jq '.recommendations' 2>/dev/null || grep -A 10 "recommendations" data/rag_analysis_*.json
```

---

## ⚙️ Task 5: Create Integrated Automation Pipeline

![Step](https://img.shields.io/badge/Step-5.1-red?style=flat-square) **Build Complete Automation Script**

```python
cat > scripts/automated_pipeline.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import json
import time
import sys
from datetime import datetime

def run_complete_pipeline(target):
    """Execute complete automated pipeline"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    print(f"[{datetime.now()}] Starting automated pipeline for {target}")

    print("Step 1: Running Nmap scan...")
    scan_result = subprocess.run([
        'python3', 'scripts/nmap_scanner.py', target
    ], capture_output=True, text=True)

    if scan_result.returncode != 0:
        print(f"Nmap scan failed: {scan_result.stderr}")
        return False

    target_safe = target.replace('/', '_').replace('.', '_')
    json_file = f"data/scan_{target_safe}.json"

    print("Step 2: Running RAG analysis...")
    rag_result = subprocess.run([
        'python3', 'scripts/rag_analyzer.py', json_file
    ], capture_output=True, text=True)

    if rag_result.returncode != 0:
        print(f"RAG analysis failed: {rag_result.stderr}")
        return False

    print("Step 3: Sending to N8N workflow...")
    try:
        with open(json_file, 'r') as f:
            scan_data = json.load(f)

        n8n_result = subprocess.run([
            'curl', '-X', 'POST', 'http://localhost:5678/webhook/nmap-scan',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(scan_data)
        ], capture_output=True, text=True, timeout=10)

        if n8n_result.returncode == 0:
            print("Successfully sent data to N8N")
        else:
            print("N8N webhook not available (this is optional)")

    except Exception as e:
        print(f"N8N integration skipped: {e}")

    print(f"[{datetime.now()}] Pipeline completed successfully!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 automated_pipeline.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    success = run_complete_pipeline(target)
    sys.exit(0 if success else 1)
EOF

chmod +x scripts/automated_pipeline.py
```

![Step](https://img.shields.io/badge/Step-5.2-red?style=flat-square) **Test Complete Pipeline**

```bash
# 🚀 Run complete automated pipeline
python3 scripts/automated_pipeline.py 127.0.0.1

# 📄 Verify all outputs
echo "=== Scan Results ==="
ls -la data/scan_*.json

echo "=== RAG Analysis ==="
ls -la data/rag_analysis_*.json

echo "=== N8N Processing ==="
ls -la /tmp/vulnerabilities.json 2>/dev/null || echo "N8N output not found (optional)"
```

---

## 🔬 Task 6: Verification and Testing

![Step](https://img.shields.io/badge/Step-6.1-teal?style=flat-square) **Create Verification Script**

```python
cat > scripts/verify_lab.py << 'EOF'
#!/usr/bin/env python3
import os
import json
import subprocess

def verify_installation():
    """Verify all tools are installed"""
    tools = ['nmap', 'python3', 'curl', 'docker']
    missing = []

    for tool in tools:
        result = subprocess.run(['which', tool], capture_output=True)
        if result.returncode != 0:
            missing.append(tool)

    if missing:
        print(f"Missing tools: {', '.join(missing)}")
        return False

    print("✓ All required tools installed")
    return True

def verify_outputs():
    """Verify expected output files exist"""
    # 🎯 TODO: Add any additional output files your extended pipeline produces
    expected_files = [
        'data/scan_127_0_0_1.json',
        'data/vulnerability_kb.json'
    ]

    missing = []
    for file in expected_files:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print(f"Missing output files: {', '.join(missing)}")
        return False

    print("✓ All expected output files present")
    return True

def verify_data_quality():
    """Verify data quality in output files"""
    try:
        with open('data/scan_127_0_0_1.json', 'r') as f:
            scan_data = json.load(f)

        if 'hosts' not in scan_data or len(scan_data['hosts']) == 0:
            print("✗ Scan data appears incomplete")
            return False

        print(f"✓ Scan data contains {len(scan_data['hosts'])} hosts")

        rag_files = [f for f in os.listdir('data/') if f.startswith('rag_analysis_')]
        if rag_files:
            print(f"✓ RAG analysis completed ({len(rag_files)} files)")
        else:
            print("✗ No RAG analysis files found")
            return False

        return True

    except Exception as e:
        print(f"✗ Error verifying data quality: {e}")
        return False

if __name__ == "__main__":
    print("=== Lab Verification ===")

    checks = [
        verify_installation(),
        verify_outputs(),
        verify_data_quality()
    ]

    if all(checks):
        print("\n🎉 Lab completed successfully!")
        print("All components are working correctly.")
    else:
        print("\n❌ Lab verification failed.")
        print("Please review the steps and try again.")
EOF

chmod +x scripts/verify_lab.py
python3 scripts/verify_lab.py
```

![Step](https://img.shields.io/badge/Step-6.2-teal?style=flat-square) **Generate Final Report**

```bash
cat > lab_summary.md << 'EOF'
# Lab Summary: Automated Nmap Parsing with N8N + RAG

## Completed Tasks

1. Environment Setup: Installed Nmap, N8N, Python dependencies
2. Nmap Automation: Created automated scanning with XML/JSON parsing
3. N8N Integration: Built workflow for processing scan results
4. RAG Implementation: Enhanced vulnerability discovery with knowledge base
5. Pipeline Integration: Combined all components into automated workflow

## Generated Files

- scripts/nmap_scanner.py: Automated Nmap scanning and parsing
- scripts/rag_analyzer.py: RAG-based vulnerability analysis
- scripts/automated_pipeline.py: Complete automation pipeline
- data/vulnerability_kb.json: Vulnerability knowledge base
- workflows/nmap_parser_workflow.json: N8N workflow configuration

## Key Achievements

- Automated network scanning and vulnerability detection
- Enhanced vulnerability analysis using RAG approach
- Integrated workflow automation with N8N
- Created reusable, scalable security assessment pipeline
EOF

echo "Lab Summary created: lab_summary.md"
cat lab_summary.md
```

---

## 🗺️ MITRE ATT&CK Mapping

| Technique ID | Technique Name | Tactic |
|---|---|---|
| T1046 | Network Service Discovery | Discovery |
| T1595 | Active Scanning | Reconnaissance |
| T1595.001 | Scanning IP Blocks | Reconnaissance |
| T1595.002 | Vulnerability Scanning | Reconnaissance |
| T1590.005 | IP Addresses | Reconnaissance |
| T1592.002 | Software | Reconnaissance |

---

## 🛠️ Troubleshooting

<details>
<summary>🔴 Docker permission denied when running N8N</summary>

- Confirm your user was added to the `docker` group: `groups $USER`
- Re-apply the group without logging out: `newgrp docker`
- If still failing, log out and back in to refresh group membership

</details>

<details>
<summary>🔴 N8N webhook returns connection refused</summary>

- Confirm the N8N container is still running: `docker ps`
- Verify the webhook path matches exactly: `/webhook/nmap-scan`
- Check container logs: `docker logs n8n`

</details>

<details>
<summary>🔴 Nmap scan produces empty or incomplete XML</summary>

- Confirm the target is reachable: `ping -c 3 <target>`
- Some scripts (`--script=vuln`) require root privileges — run with `sudo`
- Increase the `timeout` value in `nmap_scanner.py` for slow targets

</details>

<details>
<summary>🔴 RAG analyzer reports "No RAG analysis files found"</summary>

- Confirm `data/vulnerability_kb.json` exists and is valid JSON
- Verify the scan JSON file path passed to `rag_analyzer.py` is correct
- Check for exceptions printed during `analyze_scan_results()` execution

</details>

---

## 📝 Key Takeaways

| Concept | Summary |
|---|---|
| 📡 Automated Scanning | Nmap scans can be scripted and converted from XML into structured JSON |
| 🔗 Workflow Automation | N8N processes and routes scan data without manual intervention |
| 🧠 RAG-Enhanced Analysis | Matching scan findings against a CVE knowledge base adds context and confidence scoring |
| ⚙️ Pipeline Integration | Chaining scan → analyze → automate produces a repeatable security assessment workflow |

---

## ⚠️ Legal & Ethical Disclaimer

> This lab is intended **solely for authorized educational use** within the Al Nafi cloud training environment. All scanning techniques, tools, and scripts demonstrated here must only be used against systems and networks you own or have **explicit written authorization** to test. Unauthorized network scanning may violate computer misuse laws and terms of service. Al Nafi and the lab authors assume no liability for misuse of this material.

---

<div align="center">

**Built with ❤️ for the next generation of cybersecurity professionals**

</div>
