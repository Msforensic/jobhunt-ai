"""
============================================================
  MADHURESH SHUKLA — AI JOB HUNTING AGENT
  Complete automation system for cybersecurity job search
  
  SETUP: pip install anthropic requests pandas openpyxl schedule
  RUN:   python agent.py
============================================================
"""

import anthropic
import json
import os
import csv
import time
import schedule
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION — Edit these before running
# ─────────────────────────────────────────────
CONFIG = {
    # Your Anthropic API key — get from console.anthropic.com
    "api_key": "YOUR_ANTHROPIC_API_KEY_HERE",

    # Your details (pre-filled from your profile)
    "candidate": {
        "name": "Dr. Madhuresh Shukla",
        "email": "madhureshshukla88@gmail.com",
        "phone": "+91 9483840500",
        "linkedin": "linkedin.com/in/madhureshshukla",
        "location": "Chandigarh, India",
        "target_cities": ["Bengaluru", "Hyderabad", "Gurugram", "Delhi NCR", "Mumbai", "Remote"],
        "target_roles": [
            "CISO", "Chief Information Security Officer",
            "Head of Security Operations", "SOC Director",
            "DFIR Manager", "DFIR Consultant",
            "Cyber Risk Manager", "GRC Lead",
            "Cybersecurity Manager", "Security Operations Head",
            "Cybersecurity Consultant", "Security Architect"
        ],
        "salary_min_lpa": 35,
        "salary_target_lpa": 50,
        "notice_period_days": 90,
    },

    # Email settings for sending automated follow-ups (optional)
    "email": {
        "enabled": False,  # Set True to enable email automation
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "madhureshshukla88@gmail.com",
        "sender_password": "YOUR_APP_PASSWORD",  # Use Gmail App Password
    },

    # Data files
    "files": {
        "applications": "data/applications.csv",
        "contacts": "data/contacts.csv",
        "companies": "data/companies.csv",
        "posts": "data/linkedin_posts.csv",
        "log": "data/agent_log.txt",
    }
}

# Your profile summary — used by AI for all personalised generation
PROFILE = """
Name: Dr. Madhuresh Shukla
Experience: 20+ years, Indian Air Force, Cybersecurity
Current Role: Senior Cybersecurity Leader, IAF Chandigarh (Jan 2022–Present)

KEY ACHIEVEMENTS:
- Built and led enterprise SOC: 500+ endpoints, 50+ critical servers
- Managed Rs. 80 Crore cybersecurity programme (SOC + DFIR lab from scratch)
- Led 1,000+ high-severity cyber investigations, 99.8% success rate
- Achieved DFIR laboratory accreditation in 18 months
- Trained 75+ cybersecurity analysts
- Managed Rs. 15 Crore annual budget

RESEARCH & PUBLICATIONS:
- Elsevier Q1 Journal: Android Malware Detection Framework (Accepted 2025)
- Scopus-Indexed Journal: Data Encryption & Privacy (2024)
- RACS Conference paper (2024), ICONIC Conference paper (2024)
- Patent in development: Hybrid Android Malware Detection Framework
- PhD pursuing: Lovely Professional University (Cybersecurity)

CERTIFICATIONS (24 total):
CEH, ECSA, ISO 27001 ISMS, EnCase DF120, TPRM (SecurityScorecard),
DPDPA, Certified Ransomware Protection Officer, CDAC Cybersecurity,
CDAC Mobile App Security, FTK Imager, DFIR Training (BasisTech),
Lean Six Sigma Green Belt (Grant Thornton), Operational Excellence (Grant Thornton),
Power BI, Business Analyst (IMI Delhi), AI & Advanced Analytics, CISSP (In Progress)

EDUCATION:
- IIM Shillong — Management Essentials (2025–2026)
- MBA IT — LPU (2025–2027, In Progress)
- MTech Computer Science — Karnataka State Open University
- MCA — IK Gujral Punjab Technical University

TECHNICAL SKILLS:
DFIR Tools: Cellebrite UFED, MSAB XRY, Magnet AXIOM, EnCase, FTK, Autopsy
Security: SIEM, IDS/IPS, EDR, Wireshark, pfSense, Metasploit, IDA Pro, Ghidra
Frameworks: NIST CSF, ISO 27001, MITRE ATT&CK, DPDPA
Scripting: Python, PowerShell, Bash

SEEKING: CISO | SOC Head | DFIR Lead | Cybersecurity Manager | Cyber Risk Consultant
LOCATIONS: Bengaluru | Hyderabad | Gurugram | Delhi NCR | Mumbai | Remote
TARGET SALARY: Rs. 45–65 LPA
"""


# ─────────────────────────────────────────────
# AI CLIENT
# ─────────────────────────────────────────────
def get_ai_client():
    return anthropic.Anthropic(api_key=CONFIG["api_key"])


def ask_ai(prompt, system_prompt=None, max_tokens=2000):
    """Send a prompt to Claude and return the response text."""
    client = get_ai_client()
    system = system_prompt or (
        "You are an expert cybersecurity career coach and professional writer. "
        "You help senior cybersecurity leaders transition from government/defence to the private sector in India. "
        "You are precise, professional, and always output exactly what is asked — no extra commentary."
    )
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


# ─────────────────────────────────────────────
# DATA MANAGEMENT
# ─────────────────────────────────────────────
def ensure_data_files():
    """Create data directory and CSV files if they don't exist."""
    Path("data").mkdir(exist_ok=True)

    files_headers = {
        CONFIG["files"]["applications"]: [
            "id", "date_applied", "company", "role_title", "location",
            "platform", "job_url", "salary_band", "contact_name",
            "contact_linkedin", "status", "follow_up_date", "follow_up_sent",
            "interview_date", "interview_notes", "outcome", "salary_offered", "notes"
        ],
        CONFIG["files"]["contacts"]: [
            "id", "name", "current_company", "role", "relationship",
            "linkedin_url", "email", "phone", "date_contacted",
            "message_sent", "response_received", "response_notes",
            "follow_up_date", "status"
        ],
        CONFIG["files"]["companies"]: [
            "id", "company", "sector", "tier", "hq_city", "career_page_url",
            "linkedin_url", "ciso_name", "ciso_linkedin", "hr_name",
            "hr_linkedin", "applied", "date_applied", "notes"
        ],
        CONFIG["files"]["posts"]: [
            "id", "week", "date_published", "topic", "content",
            "impressions", "reactions", "comments", "shares", "notes"
        ],
    }

    for filepath, headers in files_headers.items():
        if not Path(filepath).exists():
            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    print("✅ Data files ready.")


def log(message):
    """Log a message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(CONFIG["files"]["log"], "a") as f:
        f.write(entry + "\n")


def load_csv(filepath):
    """Load a CSV file and return list of dicts."""
    if not Path(filepath).exists():
        return []
    with open(filepath, "r") as f:
        return list(csv.DictReader(f))


def save_to_csv(filepath, row_dict):
    """Append a row to a CSV file."""
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row_dict.keys())
        writer.writerow(row_dict)


def update_csv_row(filepath, row_id, updates):
    """Update a specific row in CSV by id."""
    rows = load_csv(filepath)
    headers = list(rows[0].keys()) if rows else []
    for row in rows:
        if row.get("id") == str(row_id):
            row.update(updates)
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def next_id(filepath):
    """Get next sequential ID for a CSV file."""
    rows = load_csv(filepath)
    if not rows:
        return 1
    return max(int(r.get("id", 0)) for r in rows) + 1


# ─────────────────────────────────────────────
# AGENT TASKS — Each task uses AI
# ─────────────────────────────────────────────

class ResumeAgent:
    """Tailors your resume for specific job descriptions."""

    def tailor_resume(self, job_title, company, job_description):
        """Generate a tailored resume summary and key bullets for a specific JD."""
        log(f"📄 Tailoring resume for: {job_title} at {company}")

        prompt = f"""
You are tailoring a resume for this specific job application.

CANDIDATE PROFILE:
{PROFILE}

TARGET ROLE: {job_title}
COMPANY: {company}
JOB DESCRIPTION:
{job_description}

Your task:
1. Write a tailored 4-line Professional Summary that mirrors keywords from the JD
2. List the top 10 keywords from the JD that match the candidate's experience
3. Write 3 tailored bullet points for the most recent role that directly address JD requirements
4. Write a 3-sentence cover letter opening paragraph

Format your response as JSON:
{{
  "professional_summary": "...",
  "matching_keywords": ["kw1", "kw2", ...],
  "tailored_bullets": ["bullet1", "bullet2", "bullet3"],
  "cover_letter_opening": "..."
}}
"""
        response = ask_ai(prompt)
        try:
            # Extract JSON from response
            start = response.find("{")
            end = response.rfind("}") + 1
            result = json.loads(response[start:end])
            self._save_tailored_resume(job_title, company, result)
            return result
        except:
            return {"raw_response": response}

    def _save_tailored_resume(self, job_title, company, result):
        """Save tailored resume content to a text file."""
        filename = f"data/resume_{company.replace(' ','_')}_{job_title.replace(' ','_')}.txt"
        with open(filename, "w") as f:
            f.write(f"TAILORED RESUME — {job_title} at {company}\n")
            f.write("=" * 60 + "\n\n")
            f.write("PROFESSIONAL SUMMARY:\n")
            f.write(result.get("professional_summary", "") + "\n\n")
            f.write("MATCHING KEYWORDS:\n")
            f.write(", ".join(result.get("matching_keywords", [])) + "\n\n")
            f.write("TAILORED BULLETS (Most Recent Role):\n")
            for b in result.get("tailored_bullets", []):
                f.write(f"• {b}\n")
            f.write("\nCOVER LETTER OPENING:\n")
            f.write(result.get("cover_letter_opening", "") + "\n")
        log(f"✅ Saved tailored resume to {filename}")


class OutreachAgent:
    """Generates personalised outreach messages for any contact."""

    def generate_recruiter_message(self, recruiter_name, company, specialisation="cybersecurity"):
        """Generate a personalised recruiter outreach message."""
        log(f"✉️ Generating recruiter message for {recruiter_name} at {company}")

        prompt = f"""
Generate a personalised LinkedIn outreach message to an executive recruiter.

SENDER: Dr. Madhuresh Shukla (profile below)
RECRUITER NAME: {recruiter_name}
RECRUITER COMPANY: {company}
RECRUITER SPECIALISATION: {specialisation}

{PROFILE}

Rules:
- Maximum 150 words
- Professional, confident tone — not desperate
- Mention 3 specific credentials that matter to this recruiter
- Clear ask at the end
- Do NOT use generic phrases like "I hope this message finds you well"
- Sound like a senior executive, not a job seeker

Output only the message text, nothing else.
"""
        return ask_ai(prompt, max_tokens=300)

    def generate_hiring_manager_message(self, manager_name, company, role, company_context=""):
        """Generate a direct hiring manager outreach message."""
        log(f"✉️ Generating hiring manager message for {manager_name} at {company}")

        prompt = f"""
Generate a personalised LinkedIn message to a hiring manager.

SENDER: Dr. Madhuresh Shukla
RECIPIENT: {manager_name}
COMPANY: {company}
ROLE INTERESTED IN: {role}
COMPANY CONTEXT (what you know about them): {company_context}

{PROFILE}

Rules:
- Maximum 120 words
- Lead with one specific thing about their company/team (use company_context)
- Reference 2 specific achievements from the profile that are directly relevant
- Confident ask — "Would you be open to a brief conversation?"
- Do NOT start with "I"
- Sound senior and peer-to-peer, not junior and deferential

Output only the message text, nothing else.
"""
        return ask_ai(prompt, max_tokens=300)

    def generate_network_message(self, contact_name, contact_company, shared_background="IAF"):
        """Generate a warm network message to a former colleague."""
        log(f"✉️ Generating network message for {contact_name}")

        prompt = f"""
Generate a warm LinkedIn message to reconnect with a former colleague.

SENDER: Dr. Madhuresh Shukla (IAF, cybersecurity, transitioning to private sector)
RECIPIENT: {contact_name} (now at {contact_company})
SHARED BACKGROUND: {shared_background}

{PROFILE}

Rules:
- Maximum 100 words
- Warm and genuine — not transactional
- Acknowledge their private sector journey
- Make a simple, easy-to-say-yes-to ask
- No pressure, no desperation

Output only the message text, nothing else.
"""
        return ask_ai(prompt, max_tokens=250)

    def generate_followup_message(self, contact_name, company, role, days_since_apply):
        """Generate a follow-up message after applying."""
        log(f"✉️ Generating follow-up for {role} at {company}")

        prompt = f"""
Generate a polite follow-up LinkedIn message after applying for a job.

SENDER: Dr. Madhuresh Shukla
RECIPIENT: {contact_name} (hiring manager/HR at {company})
ROLE: {role}
DAYS SINCE APPLICATION: {days_since_apply}

{PROFILE}

Rules:
- Maximum 80 words
- Polite, not pushy
- Restate ONE compelling credential
- Simple ask to confirm application received or timeline
- Professional close

Output only the message text, nothing else.
"""
        return ask_ai(prompt, max_tokens=200)

    def generate_thankyou_message(self, interviewer_name, company, role, topic_discussed):
        """Generate a post-interview thank-you message."""
        log(f"✉️ Generating thank-you for interview at {company}")

        prompt = f"""
Generate a post-interview thank-you message.

SENDER: Dr. Madhuresh Shukla
INTERVIEWER: {interviewer_name} at {company}
ROLE: {role}
KEY TOPIC DISCUSSED: {topic_discussed}

Rules:
- Exactly 3 sentences
- Thank them, reference the specific topic discussed, reaffirm enthusiasm
- Professional and warm, not sycophantic
- End with looking forward to next steps

Output only the message text, nothing else.
"""
        return ask_ai(prompt, max_tokens=150)


class LinkedInContentAgent:
    """Generates weekly LinkedIn posts to build visibility."""

    POST_TOPICS = [
        ("What 1,000 DFIR investigations taught me about incident response", "DFIR practitioners, SOC managers, CISOs"),
        ("India's DPDPA Act: what every CISO needs to do RIGHT NOW", "CISOs, GRC professionals, compliance teams"),
        ("5 mistakes most organisations make when building a SOC from scratch", "Security leaders, IT managers, startups"),
        ("My Elsevier Q1 paper on Android malware: the finding that surprised me", "Security researchers, threat intel teams"),
        ("How defence cybersecurity translates to the private sector — and where the gaps are", "Veterans transitioning, hiring managers"),
        ("The MITRE ATT&CK technique I see most abused in real investigations", "SOC analysts, threat hunters, blue teams"),
        ("Why most cyber forensics labs in India fail the legal test", "Legal, compliance, DFIR professionals"),
        ("20 years in cybersecurity: what I know now that I wish I knew at the start", "Everyone — high engagement career post"),
        ("The DFDP Act enforcement: 3 things Indian CISOs are not doing yet", "CISOs, compliance officers"),
        ("How I achieved DFIR lab accreditation in 18 months — the exact steps", "Security operations teams"),
        ("Android malware is evolving: static analysis is no longer enough", "Security researchers, malware analysts"),
        ("Budget reality: how to defend a Rs. 15 Crore cybersecurity spend to leadership", "CISOs, security managers"),
    ]

    def generate_post(self, topic=None, audience=None, week_number=1):
        """Generate a complete LinkedIn post."""
        if topic is None:
            idx = (week_number - 1) % len(self.POST_TOPICS)
            topic, audience = self.POST_TOPICS[idx]

        log(f"📝 Generating LinkedIn post: {topic}")

        prompt = f"""
Write a LinkedIn post for Dr. Madhuresh Shukla, a senior cybersecurity executive.

TOPIC: {topic}
TARGET AUDIENCE: {audience}
WEEK: {week_number}

WRITER'S BACKGROUND:
{PROFILE}

POST REQUIREMENTS:
- Maximum 1,200 characters (LinkedIn optimal length)
- First line must be a HOOK that stops scrolling — provocative question or bold statement
- Write in first person, personal and genuine voice
- Include 2–3 specific numbers or facts from the writer's actual experience
- 3 key takeaways in a scannable format
- End with an engagement question to drive comments
- Include 5 relevant hashtags at the very end
- Tone: authoritative but approachable, like a respected mentor sharing hard-won wisdom
- Do NOT start with "I" as the very first word
- Do NOT use buzzwords like "synergy", "leverage", "game-changer"

Output only the post text and hashtags. Nothing else.
"""
        post_text = ask_ai(prompt, max_tokens=600)

        # Save to CSV
        post_id = next_id(CONFIG["files"]["posts"])
        save_to_csv(CONFIG["files"]["posts"], {
            "id": post_id,
            "week": week_number,
            "date_published": "",
            "topic": topic,
            "content": post_text,
            "impressions": "",
            "reactions": "",
            "comments": "",
            "shares": "",
            "notes": f"Generated {datetime.date.today()}"
        })

        # Save to readable file
        filename = f"data/post_week{week_number:02d}_{topic[:30].replace(' ','_')}.txt"
        with open(filename, "w") as f:
            f.write(f"WEEK {week_number} LINKEDIN POST\n")
            f.write(f"Topic: {topic}\n")
            f.write(f"Audience: {audience}\n")
            f.write("=" * 50 + "\n\n")
            f.write(post_text)
        log(f"✅ Post saved to {filename}")
        return post_text


class ApplicationTrackerAgent:
    """Manages your application pipeline and generates reminders."""

    def add_application(self, company, role, location, platform, job_url="",
                        salary_band="", contact_name="", contact_linkedin=""):
        """Add a new application to the tracker."""
        app_id = next_id(CONFIG["files"]["applications"])
        today = datetime.date.today().isoformat()
        follow_up = (datetime.date.today() + datetime.timedelta(days=7)).isoformat()

        row = {
            "id": app_id,
            "date_applied": today,
            "company": company,
            "role_title": role,
            "location": location,
            "platform": platform,
            "job_url": job_url,
            "salary_band": salary_band,
            "contact_name": contact_name,
            "contact_linkedin": contact_linkedin,
            "status": "Applied",
            "follow_up_date": follow_up,
            "follow_up_sent": "No",
            "interview_date": "",
            "interview_notes": "",
            "outcome": "Pending",
            "salary_offered": "",
            "notes": ""
        }
        save_to_csv(CONFIG["files"]["applications"], row)
        log(f"✅ Application added: {role} at {company} (ID: {app_id})")
        return app_id

    def get_followups_due(self):
        """Return applications that need a follow-up today or earlier."""
        today = datetime.date.today().isoformat()
        apps = load_csv(CONFIG["files"]["applications"])
        due = [
            a for a in apps
            if a.get("follow_up_date", "") <= today
            and a.get("follow_up_sent", "No") == "No"
            and a.get("status", "") in ["Applied", "In Process"]
        ]
        return due

    def generate_daily_report(self):
        """Generate a daily status report of your job search."""
        apps = load_csv(CONFIG["files"]["applications"])
        contacts = load_csv(CONFIG["files"]["contacts"])

        total = len(apps)
        by_status = {}
        for a in apps:
            s = a.get("status", "Unknown")
            by_status[s] = by_status.get(s, 0) + 1

        followups_due = self.get_followups_due()

        report = f"""
╔══════════════════════════════════════════════════╗
║     DAILY JOB SEARCH REPORT — {datetime.date.today()}     
╠══════════════════════════════════════════════════╣

📊 APPLICATION PIPELINE:
   Total Applications: {total}
   Applied (pending): {by_status.get('Applied', 0)}
   In Process:        {by_status.get('In Process', 0)}
   Interviews:        {by_status.get('Interview', 0)}
   Offers:            {by_status.get('Offer', 0)}
   Rejected:          {by_status.get('Rejected', 0)}

⚡ ACTION REQUIRED TODAY:
   Follow-ups due:    {len(followups_due)}
"""
        if followups_due:
            report += "\n   FOLLOW-UP THESE NOW:\n"
            for a in followups_due:
                report += f"   → {a['role_title']} at {a['company']} (Applied: {a['date_applied']})\n"

        report += f"""
📅 WEEKLY TARGETS:
   Applications sent:  track this manually
   Network messages:   target 5/week
   LinkedIn post:      target 1/week
   Recruiter contacts: target 2/week

╚══════════════════════════════════════════════════╝
"""
        print(report)
        log("📊 Daily report generated")
        return report

    def analyse_pipeline_with_ai(self):
        """Use AI to analyse your pipeline and give strategic advice."""
        apps = load_csv(CONFIG["files"]["applications"])
        if not apps:
            return "No applications yet. Start applying!"

        summary = json.dumps(apps[:20], indent=2)  # Last 20 applications

        prompt = f"""
Analyse this job application pipeline for Dr. Madhuresh Shukla and give specific, actionable advice.

PIPELINE DATA (last 20 applications):
{summary}

CANDIDATE PROFILE:
{PROFILE}

Analyse:
1. What patterns do you see in the pipeline?
2. Which applications look most promising and why?
3. What should Madhuresh do differently this week?
4. Are there any red flags (e.g. too many rejections from a certain type of role)?
5. Give 3 specific actions for the next 48 hours.

Be direct and specific. Maximum 400 words.
"""
        return ask_ai(prompt, max_tokens=600)


class InterviewPrepAgent:
    """Generates interview prep materials for specific companies/roles."""

    def generate_company_research(self, company, role):
        """Generate company research and prep questions for an interview."""
        log(f"🎯 Generating interview prep for {role} at {company}")

        prompt = f"""
Generate interview preparation materials for this specific interview.

CANDIDATE: Dr. Madhuresh Shukla
COMPANY: {company}
ROLE: {role}

{PROFILE}

Generate:
1. 5 things to research about {company} before the interview (what to look for)
2. 5 questions they will likely ask — with tailored answer frameworks using the candidate's actual experience
3. 5 questions the candidate should ask the interviewer
4. 3 potential concerns they might raise about the candidate (no private sector experience, etc.) and how to address them
5. One key message to leave them with at the end

Format clearly with headers. Be specific to this company and role.
Maximum 600 words.
"""
        prep = ask_ai(prompt, max_tokens=800)

        filename = f"data/interview_prep_{company.replace(' ','_')}_{role.replace(' ','_')}.txt"
        with open(filename, "w") as f:
            f.write(f"INTERVIEW PREP — {role} at {company}\n")
            f.write(f"Generated: {datetime.date.today()}\n")
            f.write("=" * 60 + "\n\n")
            f.write(prep)
        log(f"✅ Interview prep saved to {filename}")
        return prep

    def generate_salary_negotiation_script(self, company, role, offered_salary, target_salary):
        """Generate a salary negotiation script for a specific offer."""
        prompt = f"""
Generate a salary negotiation script for Dr. Madhuresh Shukla.

COMPANY: {company}
ROLE: {role}
OFFER RECEIVED: Rs. {offered_salary} LPA
TARGET SALARY: Rs. {target_salary} LPA

{PROFILE}

Write a specific, word-for-word negotiation script covering:
1. How to respond when the offer comes in (email or phone)
2. The counter-proposal language — confident, not aggressive
3. What to say if they push back
4. What to say if they say the band is fixed
5. When to accept and what to say

Tone: confident senior executive, not desperate. This person has strong credentials.
Maximum 400 words.
"""
        return ask_ai(prompt, max_tokens=600)


class WeeklyScheduler:
    """Runs automated weekly tasks on a schedule."""

    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.outreach_agent = OutreachAgent()
        self.content_agent = LinkedInContentAgent()
        self.tracker = ApplicationTrackerAgent()
        self.interview_prep = InterviewPrepAgent()
        self.week_number = self._get_week_number()

    def _get_week_number(self):
        posts = load_csv(CONFIG["files"]["posts"])
        return len(posts) + 1

    def monday_tasks(self):
        """Run every Monday morning."""
        log("🗓️ MONDAY TASKS STARTING")
        print("\n" + "="*50)
        print("🗓️  MONDAY — Weekly Job Search Launch")
        print("="*50)

        # Generate weekly LinkedIn post
        print("\n📝 Generating this week's LinkedIn post...")
        post = self.content_agent.generate_post(week_number=self.week_number)
        print("\n--- POST CONTENT ---")
        print(post)
        print("-------------------")
        print("👆 Copy and paste this into LinkedIn. Best time: 8–10 AM today.")

        # Daily report
        self.tracker.generate_daily_report()

        # Check follow-ups
        followups = self.tracker.get_followups_due()
        if followups:
            print(f"\n⚡ {len(followups)} follow-ups due today!")
            for a in followups:
                print(f"\nGenerating follow-up message for {a['role_title']} at {a['company']}...")
                msg = self.outreach_agent.generate_followup_message(
                    a.get("contact_name", "Hiring Manager"),
                    a["company"],
                    a["role_title"],
                    (datetime.date.today() - datetime.date.fromisoformat(a["date_applied"])).days
                )
                print(f"\nSend this to {a.get('contact_name','the hiring manager')}:")
                print(msg)

        self.week_number += 1

    def daily_checkin(self):
        """Run every weekday at 9 AM."""
        log("☀️ Daily check-in")
        self.tracker.generate_daily_report()

    def friday_review(self):
        """Run every Friday for weekly review."""
        log("📊 FRIDAY REVIEW")
        print("\n" + "="*50)
        print("📊  FRIDAY — Weekly Review")
        print("="*50)
        analysis = self.tracker.analyse_pipeline_with_ai()
        print("\nAI PIPELINE ANALYSIS:")
        print(analysis)

    def start_scheduler(self):
        """Start the automated scheduler."""
        print("\n🤖 JOB HUNTING AGENT STARTING...")
        print("Scheduled tasks:")
        print("  • Every weekday at 09:00 — Daily check-in and follow-up reminders")
        print("  • Every Monday at 08:00 — LinkedIn post generation + weekly plan")
        print("  • Every Friday at 17:00 — Pipeline review and AI analysis")
        print("\nPress Ctrl+C to stop.\n")

        schedule.every().monday.at("08:00").do(self.monday_tasks)
        schedule.every().day.at("09:00").do(self.daily_checkin)
        schedule.every().friday.at("17:00").do(self.friday_review)

        while True:
            schedule.run_pending()
            time.sleep(60)


# ─────────────────────────────────────────────
# INTERACTIVE MENU
# ─────────────────────────────────────────────
def interactive_menu():
    resume_agent = ResumeAgent()
    outreach_agent = OutreachAgent()
    content_agent = LinkedInContentAgent()
    tracker = ApplicationTrackerAgent()
    interview_agent = InterviewPrepAgent()
    scheduler = WeeklyScheduler()

    while True:
        print("\n" + "="*55)
        print("🤖  DR. MADHURESH SHUKLA — AI JOB HUNTING AGENT")
        print("="*55)
        print("1.  📄  Tailor resume for a specific job")
        print("2.  ✉️   Generate recruiter outreach message")
        print("3.  ✉️   Generate hiring manager message")
        print("4.  ✉️   Generate network/warm contact message")
        print("5.  ✉️   Generate post-interview thank-you")
        print("6.  📝  Generate this week's LinkedIn post")
        print("7.  📊  Generate all 12 LinkedIn posts (3-month plan)")
        print("8.  ➕  Add new application to tracker")
        print("9.  📊  View daily pipeline report")
        print("10. 🤖  AI analysis of my pipeline")
        print("11. 🎯  Generate interview prep for a company")
        print("12. 💰  Generate salary negotiation script")
        print("13. ⚡  Check follow-ups due today")
        print("14. 🗓️  Run Monday tasks now (post + report)")
        print("15. 🚀  Start automated scheduler")
        print("0.  Exit")
        print("-"*55)

        choice = input("Enter choice: ").strip()

        if choice == "0":
            print("Good luck with your search! 🎯")
            break

        elif choice == "1":
            company = input("Company name: ").strip()
            role = input("Role title: ").strip()
            print("Paste the job description (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "":
                    if lines and lines[-1] == "":
                        break
                lines.append(line)
            jd = "\n".join(lines)
            result = resume_agent.tailor_resume(role, company, jd)
            print("\n✅ TAILORED CONTENT:")
            print(f"\nPROFESSIONAL SUMMARY:\n{result.get('professional_summary','')}")
            print(f"\nKEYWORDS TO ADD: {', '.join(result.get('matching_keywords',[]))}")
            print(f"\nCOVER LETTER OPENING:\n{result.get('cover_letter_opening','')}")

        elif choice == "2":
            name = input("Recruiter name: ").strip()
            company = input("Recruiter company: ").strip()
            spec = input("Their specialisation (default: cybersecurity): ").strip() or "cybersecurity"
            msg = outreach_agent.generate_recruiter_message(name, company, spec)
            print(f"\n✅ MESSAGE FOR {name}:\n\n{msg}")

        elif choice == "3":
            name = input("Hiring manager name: ").strip()
            company = input("Company: ").strip()
            role = input("Role you're interested in: ").strip()
            context = input("What you know about their company/team (optional): ").strip()
            msg = outreach_agent.generate_hiring_manager_message(name, company, role, context)
            print(f"\n✅ MESSAGE FOR {name}:\n\n{msg}")

        elif choice == "4":
            name = input("Contact name: ").strip()
            company = input("Their current company: ").strip()
            msg = outreach_agent.generate_network_message(name, company)
            print(f"\n✅ MESSAGE FOR {name}:\n\n{msg}")

        elif choice == "5":
            name = input("Interviewer name: ").strip()
            company = input("Company: ").strip()
            role = input("Role: ").strip()
            topic = input("Key topic discussed in interview: ").strip()
            msg = outreach_agent.generate_thankyou_message(name, company, role, topic)
            print(f"\n✅ THANK-YOU MESSAGE:\n\n{msg}")

        elif choice == "6":
            week = int(input("Week number: ").strip() or "1")
            post = content_agent.generate_post(week_number=week)
            print(f"\n✅ LINKEDIN POST:\n\n{post}")

        elif choice == "7":
            print("\n⏳ Generating all 12 LinkedIn posts (this takes 2–3 minutes)...")
            for week in range(1, 13):
                print(f"  Generating week {week}...")
                content_agent.generate_post(week_number=week)
                time.sleep(1)  # Rate limit buffer
            print("✅ All 12 posts saved to data/ folder!")

        elif choice == "8":
            company = input("Company: ").strip()
            role = input("Role title: ").strip()
            location = input("Location: ").strip()
            platform = input("Platform (LinkedIn/Naukri/Direct/Referral): ").strip()
            url = input("Job URL (optional): ").strip()
            salary = input("Salary band from JD (optional): ").strip()
            contact = input("Hiring manager/HR name (optional): ").strip()
            contact_li = input("Their LinkedIn URL (optional): ").strip()
            app_id = tracker.add_application(company, role, location, platform, url, salary, contact, contact_li)
            print(f"✅ Application #{app_id} added! Follow-up reminder set for 7 days from now.")

        elif choice == "9":
            tracker.generate_daily_report()

        elif choice == "10":
            print("⏳ Analysing your pipeline with AI...")
            analysis = tracker.analyse_pipeline_with_ai()
            print(f"\n🤖 AI ANALYSIS:\n\n{analysis}")

        elif choice == "11":
            company = input("Company name: ").strip()
            role = input("Role: ").strip()
            prep = interview_agent.generate_company_research(company, role)
            print(f"\n✅ INTERVIEW PREP:\n\n{prep}")

        elif choice == "12":
            company = input("Company: ").strip()
            role = input("Role: ").strip()
            offered = input("Salary offered (LPA): ").strip()
            target = input("Your target salary (LPA): ").strip()
            script = interview_agent.generate_salary_negotiation_script(company, role, offered, target)
            print(f"\n✅ NEGOTIATION SCRIPT:\n\n{script}")

        elif choice == "13":
            due = tracker.get_followups_due()
            if not due:
                print("✅ No follow-ups due today!")
            else:
                print(f"\n⚡ {len(due)} follow-ups due:")
                for a in due:
                    print(f"\n→ {a['role_title']} at {a['company']} (Applied: {a['date_applied']})")
                    gen = input("  Generate follow-up message? (y/n): ").strip()
                    if gen.lower() == "y":
                        msg = outreach_agent.generate_followup_message(
                            a.get("contact_name", "Hiring Manager"),
                            a["company"], a["role_title"],
                            max(1, (datetime.date.today() - datetime.date.fromisoformat(a["date_applied"])).days)
                        )
                        print(f"\n  MESSAGE:\n{msg}")

        elif choice == "14":
            scheduler.monday_tasks()

        elif choice == "15":
            scheduler.start_scheduler()

        else:
            print("Invalid choice. Try again.")


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Initialising AI Job Hunting Agent for Dr. Madhuresh Shukla...")

    # Check API key
    if CONFIG["api_key"] == "YOUR_ANTHROPIC_API_KEY_HERE":
        print("\n⚠️  SETUP REQUIRED:")
        print("1. Get your API key from: https://console.anthropic.com")
        print("2. Open agent.py and replace YOUR_ANTHROPIC_API_KEY_HERE with your key")
        print("3. Run: pip install anthropic schedule pandas openpyxl")
        print("4. Run: python agent.py\n")
        exit(1)

    ensure_data_files()
    interactive_menu()
