# 🛡️ JobHunt AI — AI Career Agent for Senior Cybersecurity Professionals

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Claude](https://img.shields.io/badge/AI-Claude%20Sonnet-orange.svg)](https://anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Domain: Cybersecurity](https://img.shields.io/badge/domain-cybersecurity-red.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **The only AI job hunting agent built specifically for senior cybersecurity professionals — CISO, SOC Head, DFIR Lead — transitioning from government and defence to the private sector in India.**

---

## 🎯 The Problem This Solves

Generic job tools are built for software engineers applying to 200 companies. Senior cybersecurity leaders face a completely different challenge:

- **Defence-to-private translation gap** — 20 years of IAF SOC leadership doesn't map cleanly to private sector JDs
- **Keyword mismatch** — ATS systems reject resumes that don't mirror the exact JD language
- **No outreach templates** — Cold messages to CISOs and Big 4 partners require a very different tone than junior job applications
- **Invisible expertise** — Elsevier Q1 publications and DFIR lab accreditations mean nothing if they're buried on page 2

**JobHunt AI solves every one of these problems** — using Claude AI to translate your defence credentials into private sector language, tailor every application, and automate every repetitive communication.

---

## ✨ What Makes This Different

| Generic AI Job Tools | JobHunt AI |
|---------------------|------------|
| Built for software engineers | Built for cybersecurity leaders |
| Generic resume rewriting | NIST/ISO 27001/MITRE ATT&CK keyword matching |
| Mass application automation | Precision targeting — 5 tailored > 50 generic |
| No domain expertise | Deep SOC/DFIR/GRC context baked in |
| Replaces human judgment | Augments senior professional strategy |

**The core insight:** At CISO and SOC Head level, 70% of roles are filled before public posting — through referrals and direct outreach. This agent optimises for that reality.

---

## 🚀 Features

### 📄 AI Resume Tailoring
Paste any job description → Claude rewrites your professional summary and key bullets to mirror the JD's exact keywords — SIEM, EDR, MITRE ATT&CK, ISO 27001, threat hunting — whatever they use.

### ✉️ Personalised Outreach Generation
- **Recruiter messages** — Korn Ferry, Michael Page, Randstad India style outreach
- **Hiring manager DMs** — Direct, peer-to-peer tone for CISOs and security directors
- **Network reconnects** — Warm messages to IAF/govt colleagues now in private sector
- **Post-interview thank-you** — 3-sentence notes that stand out

### 📝 12-Week LinkedIn Content Calendar
Generate a full quarter of cybersecurity thought leadership posts — DFIR lessons, DPDPA analysis, malware research insights, SOC-building advice — all in your voice, ready to publish.

### 📊 Application Pipeline Tracker
CSV-based tracker with automated follow-up reminders. Never let a promising application go cold again.

### 🤖 AI Pipeline Analysis
Claude reviews your entire application history and gives you weekly strategic advice — which channels are working, which companies are most promising, what to change.

### 🎯 Interview Preparation
Company-specific research + likely questions + answer frameworks using your actual career numbers. Built for the "no private sector experience" objection every defence veteran faces.

### 💰 Salary Negotiation Scripts
Word-for-word negotiation scripts calibrated to Indian cybersecurity market rates — Rs. 35–65 LPA for senior roles.

### 🗓️ Automated Scheduler
Monday morning: LinkedIn post + weekly plan. Daily: follow-up reminders. Friday: AI pipeline review. All automated.

---

## 🧱 Architecture

```
JobHunt AI
│
├── Core Orchestrator (agent.py)
│   └── Anthropic Claude Sonnet API
│
├── Sub-Agents
│   ├── ResumeAgent        — JD analysis + keyword matching + tailoring
│   ├── OutreachAgent      — 5 message types, context-aware generation
│   ├── ContentAgent       — 12-week LinkedIn post calendar
│   ├── TrackerAgent       — CSV pipeline + follow-up logic + AI analysis
│   └── InterviewAgent     — Company research + prep + negotiation
│
├── Scheduler              — Automated daily/weekly task runner
├── Config (YAML)          — Candidate profile + API keys
└── Data (CSV)             — Applications, contacts, posts, logs
```

**Why Python + Claude API (not a web framework)?**

This is intentionally a command-line agent, not a web app. Senior professionals spend their time in email and terminal — not browser dashboards. The CLI design means zero dependencies on external services, runs completely locally, and costs ~Rs. 200/month vs. Rs. 2,000+/month for SaaS alternatives.

---

## ⚙️ Quick Start

```bash
# 1. Clone
git clone https://github.com/Msforensic/jobhunt-ai.git
cd jobhunt-ai

# 2. Install
pip install -r requirements.txt

# 3. Try the demo (no API key needed)
python demo.py

# 4. Configure
cp config.example.yaml config.yaml
# Add your Anthropic API key (free at console.anthropic.com)

# 5. Run
python -m jobhunt_ai
```

**Cost:** API calls cost approximately Rs. 200–300/month for daily use. Free $5 credits at signup cover 2–3 weeks.

---

## 📖 CLI Usage

```bash
# Tailor resume to a specific JD
python -m jobhunt_ai tailor --company "Deloitte India" --role "DFIR Manager" --jd-file jd.txt

# Generate outreach messages
python -m jobhunt_ai outreach recruiter --name "Kiran Mehta" --company "Michael Page"
python -m jobhunt_ai outreach manager --name "Rahul Sharma" --company "HSBC GCC" --role "SOC Director"

# Generate LinkedIn posts
python -m jobhunt_ai post --week 1          # Single post
python -m jobhunt_ai post --all             # All 12 weeks

# Track applications
python -m jobhunt_ai track add --company "PwC India" --role "Cyber Risk Manager" --location "Bengaluru" --platform "LinkedIn"
python -m jobhunt_ai track report           # Daily pipeline report
python -m jobhunt_ai track followups        # What needs follow-up today
python -m jobhunt_ai track analyse          # AI strategic advice

# Interview prep
python -m jobhunt_ai interview --company "EY India" --role "GRC Consultant"

# Start automated scheduler
python -m jobhunt_ai schedule
```

---

## 🎯 Who This Is For

**Ideal user:**
- 10–25 years in cybersecurity (government, defence, or large enterprise)
- Targeting: CISO, Head of Security Operations, SOC Director, DFIR Lead, GRC Manager
- Location: India (language and market context tuned for Indian private sector)
- Transitioning from public to private sector

**Not the right tool for:**
- Entry-level or junior candidates
- Mass application automation ("spray and pray")
- Non-cybersecurity domains

---

## 🗺️ Roadmap

- [x] Core agent with 15 functions
- [x] CLI with full argument support
- [x] CSV pipeline tracker with automated reminders
- [x] 12-week LinkedIn content calendar
- [x] Automated scheduler
- [ ] **Cybersecurity job scraper** — auto-fetch from Naukri, LinkedIn, iimjobs filtered for security roles
- [ ] **MITRE ATT&CK role mapper** — map your experience to specific ATT&CK domains and suggest roles
- [ ] **Skill gap analyser** — compare your profile to JD requirements and suggest certifications
- [ ] **Phishing job detector** — flag suspicious job postings using NLP (a natural fit for a DFIR expert)
- [ ] **Streamlit dashboard** — visual pipeline and analytics view
- [ ] **WhatsApp reminder integration** — push follow-up reminders to phone

---

## 👤 Built By

**Dr. Madhuresh Shukla** — Cybersecurity Executive, 20+ years Indian Air Force

- Built and led a 24x7 SOC and accredited DFIR laboratory from scratch (Rs. 80 Crore programme)
- Led 1,000+ high-severity cyber investigations (99.8% success rate)
- Published: [Elsevier Q1 Journal, 2025](https://www.sciencedirect.com) | Scopus Indexed, 2024
- PhD Candidate, Cybersecurity — Lovely Professional University
- Currently transitioning from IAF to private sector — **this tool is what I use in my own job search**

> *"I built this because every AI job tool I found was designed for software engineers applying to 200 companies. I needed something that understood what 'led 1,000 DFIR investigations' means in a CISO interview, and could translate 20 years of defence operations into language a Big 4 partner would hire for."*

---

## 🤝 Contributing

Contributions welcome — especially from:
- Cybersecurity professionals who want domain-specific features
- Python developers who want to add the job scraper or dashboard
- Defence veterans who can test the India-market accuracy

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

*If this helps your job search, please ⭐ star it and share with other cybersecurity professionals making the transition.*
