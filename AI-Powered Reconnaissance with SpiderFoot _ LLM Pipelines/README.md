<div align="center">

# 🕵️‍♂️ AI-Powered Reconnaissance with SpiderFoot + LLM Pipelines

### 🧠 Red Team Operations | Al Nafi Cybersecurity Training Platform

![OSINT](https://img.shields.io/badge/OSINT-Reconnaissance-1B1B32?style=for-the-badge&logo=spyofferings&logoColor=white)
![SpiderFoot](https://img.shields.io/badge/SpiderFoot-Automation-00599C?style=for-the-badge&logo=spider&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?style=for-the-badge&logo=ollama&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Cloud%20Lab-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=flat-square)
![Duration](https://img.shields.io/badge/Duration-2--3%20Hours-blue?style=flat-square)
![Category](https://img.shields.io/badge/Category-Reconnaissance-orange?style=flat-square)
![Certification](https://img.shields.io/badge/Maps%20to-Red%20Team%20Operator%20Adversary%20Emulation-critical?style=flat-square)

</div>

---

## 📚 Table of Contents

- [🎯 Learning Objectives](#-learning-objectives)
- [✅ Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [🚀 Task 1: Set up SpiderFoot for OSINT Collection](#-task-1-set-up-spiderfoot-for-osint-collection)
- [🤖 Task 2: Integrate LLM for Data Parsing and Summarization](#-task-2-integrate-llm-for-data-parsing-and-summarization)
- [⚙️ Task 3: Automate Reconnaissance Workflows](#️-task-3-automate-reconnaissance-workflows)
- [🔬 Verification and Testing](#-verification-and-testing)
- [🗺️ MITRE ATT&CK Mapping](#️-mitre-attck-mapping)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📝 Key Takeaways](#-key-takeaways)
- [⚠️ Legal & Ethical Disclaimer](#️-legal--ethical-disclaimer)

---

## 🎯 Learning Objectives

| # | Objective |
|---|-----------|
| 1 | 🔎 Install and configure SpiderFoot for automated OSINT collection |
| 2 | 🧩 Integrate local LLM capabilities for intelligent data parsing and summarization |
| 3 | 🔗 Create automated reconnaissance workflows combining OSINT tools with AI analysis |
| 4 | 🛡️ Develop practical skills in AI-enhanced cybersecurity reconnaissance |

## ✅ Prerequisites

| Requirement | Details |
|---|---|
| 💻 Linux CLI | Basic command-line knowledge |
| 🕵️ OSINT Fundamentals | Understanding of reconnaissance concepts and techniques |
| 🐍 Python | Familiarity with scripting |
| 🔐 Cybersecurity Basics | General security fundamentals |

---

## 🖥️ Lab Environment

> Al Nafi provides a **Linux-based cloud machine** for this lab. Click **Start Lab** to access your dedicated environment. The machine is provisioned bare metal with no pre-installed tools — you will install every component during the exercises.

---

## 🚀 Task 1: Set up SpiderFoot for OSINT Collection

![Step](https://img.shields.io/badge/Step-1.1-blue?style=flat-square) **System Preparation and Dependencies**

Update the system and install required packages:

```bash
# 📦 Update package lists and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# 🧰 Install Python, pip, git, and build tools
sudo apt install -y python3 python3-pip git curl wget build-essential
```

![Step](https://img.shields.io/badge/Step-1.2-blue?style=flat-square) **Install SpiderFoot**

Clone and set up SpiderFoot:

```bash
# 📂 Move into the /opt directory
cd /opt

# ⬇️ Clone the official SpiderFoot repository
sudo git clone https://github.com/smicallef/spiderfoot.git

# 🔑 Fix ownership so your user can operate on the folder
sudo chown -R $USER:$USER spiderfoot
cd spiderfoot

# 📥 Install Python dependencies
pip3 install -r requirements.txt
```

![Step](https://img.shields.io/badge/Step-1.3-blue?style=flat-square) **Configure SpiderFoot**

Start the SpiderFoot web interface:

```bash
# 🌐 Launch SpiderFoot's web UI, listening on all interfaces, port 5001
python3 sf.py -l 0.0.0.0:5001
```

Open a new terminal and verify SpiderFoot is running:

```bash
# ✅ Confirm the service responds
curl -s http://localhost:5001 | grep -i spiderfoot
```

![Step](https://img.shields.io/badge/Step-1.4-blue?style=flat-square) **Test Basic OSINT Collection**

Create a test scan using SpiderFoot's command-line interface:

```bash
cd /opt/spiderfoot

# 🎯 TODO: Replace 'example.com' with your assigned lab target domain
python3 sf.py -s example.com -t DOMAIN_NAME -m sfp_dnsresolve,sfp_whois,sfp_subdomain_enum -q
```

---

## 🤖 Task 2: Integrate LLM for Data Parsing and Summarization

![Step](https://img.shields.io/badge/Step-2.1-purple?style=flat-square) **Install Local LLM Framework**

Install Ollama for local LLM deployment:

```bash
# 🧠 Install Ollama runtime
curl -fsSL https://ollama.ai/install.sh | sh

# ▶️ Start the Ollama service in the background
ollama serve &
sleep 10
```

![Step](https://img.shields.io/badge/Step-2.2-purple?style=flat-square) **Deploy Lightweight LLM Model**

Pull and run a lightweight model suitable for text analysis:

```bash
# ⬇️ Pull a lightweight chat-tuned model
ollama pull llama2:7b-chat

# 📋 Confirm the model is installed
ollama list
```

![Step](https://img.shields.io/badge/Step-2.3-purple?style=flat-square) **Create LLM Integration Script**

Create a Python script to interface with the LLM:

```bash
mkdir -p /opt/recon-ai
cd /opt/recon-ai
```

Create the LLM integration script:

```python
cat > llm_analyzer.py << 'EOF'
#!/usr/bin/env python3
import requests
import json
import sys

class LLMAnalyzer:
    def __init__(self, model="llama2:7b-chat"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def analyze_osint_data(self, data, analysis_type="summary"):
        prompts = {
            "summary": f"Analyze this OSINT data and provide a concise security summary: {data}",
            "threats": f"Identify potential security threats from this reconnaissance data: {data}",
            "recommendations": f"Provide security recommendations based on this OSINT information: {data}"
        }

        # 🎯 TODO: Add an additional analysis_type of your choice (e.g. "attack_surface")
        payload = {
            "model": self.model,
            "prompt": prompts.get(analysis_type, prompts["summary"]),
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Connection error: {str(e)}"

if __name__ == "__main__":
    analyzer = LLMAnalyzer()
    if len(sys.argv) > 1:
        result = analyzer.analyze_osint_data(sys.argv[1])
        print(result)
    else:
        print("Usage: python3 llm_analyzer.py 'data_to_analyze'")
EOF

chmod +x llm_analyzer.py
```

![Step](https://img.shields.io/badge/Step-2.4-purple?style=flat-square) **Test LLM Integration**

Test the LLM analyzer with sample data:

```bash
# 🧪 Run a sample OSINT string through the analyzer
python3 llm_analyzer.py "Domain: example.com, IP: 93.184.216.34, Subdomains: www.example.com, mail.example.com"
```

---

## ⚙️ Task 3: Automate Reconnaissance Workflows

![Step](https://img.shields.io/badge/Step-3.1-green?style=flat-square) **Create SpiderFoot Data Extraction Script**

```python
cat > spiderfoot_extractor.py << 'EOF'
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
            # 🎯 TODO: Adjust the LIMIT to control how many recent findings are pulled
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
EOF

chmod +x spiderfoot_extractor.py
```

![Step](https://img.shields.io/badge/Step-3.2-green?style=flat-square) **Create Automated Reconnaissance Pipeline**

```python
cat > recon_pipeline.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import json
import time
import sys
from llm_analyzer import LLMAnalyzer
from spiderfoot_extractor import SpiderFootExtractor

class ReconPipeline:
    def __init__(self):
        self.analyzer = LLMAnalyzer()
        self.extractor = SpiderFootExtractor()

    def run_spiderfoot_scan(self, target, modules="sfp_dnsresolve,sfp_whois,sfp_subdomain_enum"):
        print(f"Starting SpiderFoot scan for: {target}")
        cmd = [
            "python3", "/opt/spiderfoot/sf.py",
            "-s", target,
            "-t", "DOMAIN_NAME",
            "-m", modules,
            "-q"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("SpiderFoot scan completed successfully")
                return True
            else:
                print(f"SpiderFoot scan failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("SpiderFoot scan timed out")
            return False

    def analyze_results(self):
        print("Extracting SpiderFoot results...")
        time.sleep(5)  # Allow database to update

        summary = self.extractor.get_latest_scan_summary()
        if "error" in summary:
            print(f"Error extracting data: {summary['error']}")
            return None

        print("Analyzing results with LLM...")
        analysis_data = json.dumps(summary)

        # 🎯 TODO: Add a third analysis call (e.g. "attack_surface") once you extend llm_analyzer.py
        threat_analysis = self.analyzer.analyze_osint_data(analysis_data, "threats")
        recommendations = self.analyzer.analyze_osint_data(analysis_data, "recommendations")

        return {
            "raw_summary": summary,
            "threat_analysis": threat_analysis,
            "recommendations": recommendations
        }

    def generate_report(self, target, analysis):
        report = f"""
# AI-Powered Reconnaissance Report for {target}

## Raw Data Summary
- Total Findings: {analysis['raw_summary']['total_findings']}
- Domains Found: {len(analysis['raw_summary']['domains'])}
- IP Addresses: {len(analysis['raw_summary']['ips'])}
- Email Addresses: {len(analysis['raw_summary']['emails'])}

## AI Threat Analysis
{analysis['threat_analysis']}

## AI Security Recommendations
{analysis['recommendations']}

Generated by AI-Powered Reconnaissance Pipeline
"""

        filename = f"recon_report_{target.replace('.', '_')}.md"
        with open(filename, 'w') as f:
            f.write(report)

        print(f"Report saved to: {filename}")
        return filename

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 recon_pipeline.py <target_domain>")
        sys.exit(1)

    target = sys.argv[1]
    pipeline = ReconPipeline()

    if pipeline.run_spiderfoot_scan(target):
        analysis = pipeline.analyze_results()
        if analysis:
            pipeline.generate_report(target, analysis)
            print("Reconnaissance pipeline completed successfully!")
        else:
            print("Failed to analyze results")
    else:
        print("Failed to run SpiderFoot scan")

if __name__ == "__main__":
    main()
EOF

chmod +x recon_pipeline.py
```

![Step](https://img.shields.io/badge/Step-3.3-green?style=flat-square) **Test Complete Automation Pipeline**

```bash
cd /opt/recon-ai

# 🎯 TODO: Swap in your assigned lab target domain
python3 recon_pipeline.py example.com
```

![Step](https://img.shields.io/badge/Step-3.4-green?style=flat-square) **Verify Results**

```bash
# 📄 List and inspect the generated report
ls -la *.md
cat recon_report_example_com.md
```

![Step](https://img.shields.io/badge/Step-3.5-green?style=flat-square) **Create Batch Processing Script**

```python
cat > batch_recon.py << 'EOF'
#!/usr/bin/env python3
import sys
import time
from recon_pipeline import ReconPipeline

def batch_reconnaissance(targets_file):
    pipeline = ReconPipeline()

    with open(targets_file, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]

    for target in targets:
        print(f"\n{'='*50}")
        print(f"Processing target: {target}")
        print(f"{'='*50}")

        if pipeline.run_spiderfoot_scan(target):
            analysis = pipeline.analyze_results()
            if analysis:
                pipeline.generate_report(target, analysis)
            time.sleep(10)  # Delay between scans
        else:
            print(f"Failed to scan {target}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 batch_recon.py targets.txt")
        sys.exit(1)

    batch_reconnaissance(sys.argv[1])
EOF

chmod +x batch_recon.py
```

Create a sample targets file:

```bash
# 🎯 TODO: Replace these with domains authorized for your lab engagement
cat > targets.txt << 'EOF'
example.com
google.com
github.com
EOF
```

Test batch processing with one target:

```bash
echo "example.com" > test_target.txt
python3 batch_recon.py test_target.txt
```

---

## 🔬 Verification and Testing

**Verify All Components**

```bash
# 🧠 Check Ollama
curl -s http://localhost:11434/api/tags | jq .

# 🕷️ Check SpiderFoot database
ls -la /opt/spiderfoot/spiderfoot.db

# 📊 Check generated reports
ls -la /opt/recon-ai/*.md
```

**Performance Test**

```bash
cd /opt/recon-ai
time python3 recon_pipeline.py example.com
```

---

## 🗺️ MITRE ATT&CK Mapping

| Technique ID | Technique Name | Tactic |
|---|---|---|
| T1596 | Search Open Technical Databases | Reconnaissance |
| T1596.001 | DNS/Passive DNS | Reconnaissance |
| T1596.002 | WHOIS | Reconnaissance |
| T1590 | Gather Victim Network Information | Reconnaissance |
| T1591 | Gather Victim Org Information | Reconnaissance |
| T1589 | Gather Victim Identity Information | Reconnaissance |
| T1597 | Search Closed Sources | Reconnaissance |

---

## 🛠️ Troubleshooting

<details>
<summary>🔴 SpiderFoot web UI won't start / port already in use</summary>

- Confirm nothing else is bound to port 5001: `sudo lsof -i :5001`
- Kill any stale SpiderFoot process and restart: `pkill -f sf.py`
- Try an alternate port: `python3 sf.py -l 0.0.0.0:5002`

</details>

<details>
<summary>🔴 Ollama model fails to pull or run</summary>

- Verify the Ollama service is active: `curl -s http://localhost:11434/api/tags`
- Re-run `ollama serve &` if the API isn't responding
- Confirm sufficient disk space for the model (`df -h`)

</details>

<details>
<summary>🔴 "SpiderFoot database not found" error</summary>

- Ensure at least one scan has completed before running the extractor
- Confirm the path in `SpiderFootExtractor` matches your actual `spiderfoot.db` location
- Re-run a scan via the CLI or web UI to regenerate the database

</details>

<details>
<summary>🔴 LLM analysis returns connection errors</summary>

- Confirm Ollama is running on `localhost:11434`
- Increase the `timeout` value in `llm_analyzer.py` for slower hardware
- Check that the model name in `LLMAnalyzer` matches an installed model (`ollama list`)

</details>

---

## 📝 Key Takeaways

| Concept | Summary |
|---|---|
| 🕷️ Automated OSINT | SpiderFoot automates domain, WHOIS, and subdomain reconnaissance at scale |
| 🧠 Local LLM Analysis | Ollama enables on-box, privacy-preserving AI summarization of recon data |
| 🔗 Pipeline Automation | Chaining OSINT collection with LLM analysis produces structured, actionable reports |
| 📈 Scalability | Batch processing extends the pipeline across multiple targets efficiently |

---

## ⚠️ Legal & Ethical Disclaimer

> This lab is intended **solely for authorized educational use** within the Al Nafi cloud training environment. All reconnaissance techniques, tools, and scripts demonstrated here must only be used against systems and domains you own or have **explicit written authorization** to test. Unauthorized OSINT collection or scanning against third-party assets may violate computer misuse laws and terms of service. Al Nafi and the lab authors assume no liability for misuse of this material.

---

<div align="center">

**Built with ❤️ for the next generation of cybersecurity professionals**

</div>
