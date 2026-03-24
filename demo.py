"""
QUICK DEMO MODE — Run this if you want to test the agent
without setting up an API key first.

This shows you exactly what each feature produces,
using pre-generated sample outputs.

Run: python demo.py
"""

import datetime

print("""
╔══════════════════════════════════════════════════════════╗
║    🤖 AI JOB HUNTING AGENT — DEMO MODE                 ║
║    Dr. Madhuresh Shukla — Cybersecurity Executive       ║
╚══════════════════════════════════════════════════════════╝
""")

print("This demo shows you exactly what the agent produces.")
print("Once you add your API key to agent.py, every output is LIVE and personalised.\n")

print("="*60)
print("DEMO 1 — TAILORED RESUME SUMMARY")
print("(For: CISO role at HSBC India GCC)")
print("="*60)
print("""
PROFESSIONAL SUMMARY (generated in ~8 seconds):

Results-driven Cybersecurity Executive with 20+ years leading enterprise 
SOC operations, DFIR programmes, and cyber risk governance for mission-critical 
environments. Proven ability to establish SOC and cyber-forensics capabilities 
from the ground up — including a Rs. 80 Crore programme delivering 24x7 
operations and accredited DFIR laboratory. Deep expertise in ISO 27001, NIST, 
MITRE ATT&CK, and DPDPA compliance, with a research publication in Elsevier Q1 
on advanced malware detection. Seeking CISO role at HSBC to drive cyber 
resilience across banking infrastructure.

MATCHING KEYWORDS FOUND IN HSBC JD:
SOC, DFIR, ISO 27001, NIST, cyber risk, governance, incident response,
threat intelligence, regulatory compliance, budget management, SIEM, EDR
""")

print("="*60)
print("DEMO 2 — RECRUITER OUTREACH MESSAGE")
print("(For: Kiran Mehta, Michael Page India)")
print("="*60)
print("""
MESSAGE (generated in ~5 seconds):

Hi Kiran,

With 20+ years leading enterprise SOC and DFIR operations for the Indian Air 
Force — including a Rs. 80 Crore programme and 1,000+ cyber investigations — 
I am now moving to the private sector in a CISO or Security Operations Head capacity.

My Elsevier Q1 publication in Android malware detection, 24 active certifications 
(CEH, ECSA, ISO 27001, EnCase, TPRM, DPDPA), and CISSP in progress make me 
competitive for senior roles at MNCs and Big 4 firms.

Targeting: Bengaluru | Hyderabad | Gurugram | Delhi NCR | Remote
LinkedIn: linkedin.com/in/madhureshshukla

If you are working on relevant cybersecurity mandates, I'd welcome a conversation.
""")

print("="*60)
print("DEMO 3 — LINKEDIN POST (Week 1)")
print("="*60)
print("""
POST (generated in ~10 seconds):

After 1,000+ cyber investigations, here's the one thing that separates 
effective incident response from chaos.

Most organisations focus on detection tools. The real differentiator is 
what happens in the first 40 minutes.

From two decades of leading DFIR operations — including building a 24x7 SOC 
and accredited forensics laboratory from scratch — here's what I've learned:

1. Containment before analysis.
   Isolate first. Understand second. The instinct to investigate immediately 
   costs organisations hours they can't afford.

2. Evidence integrity is non-negotiable.
   Forensic admissibility is decided in the first hour. If your team doesn't 
   follow chain-of-custody from minute one, the investigation is already compromised.

3. Communication runs parallel to response.
   Your CEO needs a status update 30 minutes in. Build that into your playbook 
   or you'll be answering calls instead of containing the incident.

What's the biggest gap you see in incident response in your organisation?

#DFIR #IncidentResponse #Cybersecurity #SOC #CyberDefence
""")

print("="*60)
print("DEMO 4 — DAILY PIPELINE REPORT")
print("="*60)
print(f"""
╔══════════════════════════════════════════════════╗
║     DAILY JOB SEARCH REPORT — {datetime.date.today()}     
╠══════════════════════════════════════════════════╣

📊 APPLICATION PIPELINE:
   Total Applications: 12
   Applied (pending):  7
   In Process:         3
   Interviews:         1
   Offers:             0
   Rejected:           1

⚡ ACTION REQUIRED TODAY:
   Follow-ups due:    2

   FOLLOW-UP THESE NOW:
   → DFIR Manager at Deloitte India (Applied: 8 days ago)
   → Cybersecurity Manager at HSBC GCC (Applied: 8 days ago)

📅 WEEKLY TARGETS:
   Applications sent:  3/5 this week
   Network messages:   4/5 this week  
   LinkedIn post:      ✅ Published Monday
   Recruiter contacts: 2/2 this week

╚══════════════════════════════════════════════════╝
""")

print("="*60)
print("DEMO 5 — AI PIPELINE ANALYSIS")
print("="*60)
print("""
AI ADVICE (generated in ~15 seconds):

Looking at your pipeline, I see 3 patterns worth addressing:

1. HIGH RESPONSE RATE from Big 4 consulting (Deloitte, EY) vs near-zero 
   from IT services (TCS, Infosys). This suggests your DFIR depth resonates 
   with consulting firms who need to sell that expertise. Double down here — 
   add KPMG and PwC forensics practices to your list immediately.

2. Your applications to MNC GCCs are going silent likely because they are 
   filtering on "private sector experience." Your follow-up message to hiring 
   managers at HSBC and Deutsche Bank should lead with your IIM Shillong 
   programme and your TPRM certification — these are private-sector-speak signals.

3. The Deloitte application is 8 days old with no response. Generate a follow-up 
   NOW (option 13). Applications past 10 days with no response have <15% 
   chance of moving forward without a nudge.

3 ACTIONS FOR NEXT 48 HOURS:
→ Send follow-up to Deloitte hiring manager today
→ Apply to KPMG India forensics practice (your strongest fit)  
→ Post your DPDPA LinkedIn piece this Thursday — it will attract BFSI CISOs
""")

print("\n" + "="*60)
print("✅ THAT IS WHAT THE LIVE AGENT PRODUCES — FOR REAL")
print("="*60)
print("""
SETUP TAKES 5 MINUTES:

1. pip install anthropic schedule pandas openpyxl
2. Get API key: https://console.anthropic.com (free $5 credits)
3. Add key to agent.py line 28
4. python agent.py

The live agent does all of this for REAL companies and REAL job descriptions
that you paste in — personalised to your exact profile and the specific role.

Cost: ~Rs. 2–3 per resume tailoring. ~Rs. 200/month total.
That is less than one chai per day to automate your entire job search.
""")
