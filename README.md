# 🤖 AI Job Hunting Agent — Dr. Madhuresh Shukla
## Complete Automation System for Cybersecurity Job Search

---

## WHAT THIS AGENT DOES

This AI agent automates your entire job hunting process using Claude AI:

| Task | What the agent does |
|------|---------------------|
| Resume tailoring | Reads any job description and rewrites your summary + bullets to match |
| Recruiter outreach | Generates personalised messages for each recruiter |
| Hiring manager DMs | Writes direct, senior-to-senior outreach messages |
| Network messages | Crafts warm reconnect messages to IAF/govt contacts |
| Follow-up messages | Automatically flags and drafts follow-ups when due |
| Thank-you notes | Post-interview thank-you in 2 minutes |
| LinkedIn posts | Generates 12 weeks of content in one go |
| Daily reports | Shows your full pipeline status every morning |
| AI pipeline analysis | Claude reviews your applications and gives strategic advice |
| Interview prep | Company-specific research + likely questions + your answer frameworks |
| Salary negotiation | Word-for-word negotiation scripts for specific offers |
| Scheduler | Runs Monday tasks, daily check-ins, Friday reviews automatically |

---

## SETUP — 5 MINUTES

### Step 1: Install Python (if not already installed)
Download from: https://python.org/downloads
Choose Python 3.10 or higher.

### Step 2: Install required packages
Open Terminal (Mac/Linux) or Command Prompt (Windows) and run:
```
pip install anthropic schedule pandas openpyxl
```

### Step 3: Get your Anthropic API key
1. Go to: https://console.anthropic.com
2. Sign up (free account gives $5 credits — enough for ~500 messages)
3. Click "API Keys" → "Create Key"
4. Copy the key (starts with sk-ant-...)

### Step 4: Add your API key to the agent
Open `agent.py` in any text editor (Notepad, VS Code, etc.)
Find this line near the top:
```python
"api_key": "YOUR_ANTHROPIC_API_KEY_HERE",
```
Replace `YOUR_ANTHROPIC_API_KEY_HERE` with your actual key.

### Step 5: Run the agent
```
python agent.py
```

---

## DAILY USAGE — How to use it every day

### Morning routine (5 minutes):
1. Run `python agent.py`
2. Choose option 9 — Daily pipeline report
3. Choose option 13 — Check follow-ups due
4. Send any flagged follow-ups

### When you find a job to apply for:
1. Choose option 1 — Tailor resume (paste the JD)
2. Copy the tailored summary into your resume
3. Apply on the platform
4. Choose option 8 — Add to tracker
5. If you found the hiring manager: Choose option 3 — Generate their message

### Monday morning (10 minutes):
1. Choose option 14 — Run Monday tasks
2. This generates your LinkedIn post + weekly plan automatically

### Before an interview:
1. Choose option 11 — Generate interview prep
2. Review the company research + likely questions
3. Practise your answers using the frameworks provided

### After receiving an offer:
1. Choose option 12 — Salary negotiation script
2. Follow the script word for word

---

## FILE STRUCTURE

```
job_agent/
├── agent.py              ← Main agent (run this)
├── requirements.txt      ← Python packages needed
├── README.md             ← This file
└── data/                 ← All your data (auto-created)
    ├── applications.csv  ← Application tracker
    ├── contacts.csv      ← Network contacts
    ├── companies.csv     ← Target companies
    ├── linkedin_posts.csv ← Generated posts
    ├── agent_log.txt     ← Activity log
    ├── resume_*.txt      ← Tailored resumes per role
    ├── post_week*.txt    ← LinkedIn posts per week
    └── interview_prep_*.txt ← Interview prep per company
```

---

## COST ESTIMATE

Using Claude Sonnet via API:
- Each resume tailoring: ~Rs. 2–3
- Each message generated: ~Re. 1
- Each LinkedIn post: ~Rs. 2
- Daily report: ~Re. 0.50
- Full month of usage: ~Rs. 200–300 total

Free Anthropic credits ($5) will last approximately 2–3 weeks of daily use.

---

## ADVANCED: Automated Scheduler

To run the agent automatically every day (without opening it manually):

**Option A — Run manually each morning:**
Just open Terminal and type `python agent.py` each morning.

**Option B — Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task → "Job Agent Daily"
3. Trigger: Daily at 8:30 AM
4. Action: Start Program → python.exe
5. Arguments: `C:\path\to\job_agent\agent.py --schedule`

**Option C — Mac/Linux Cron:**
```
crontab -e
# Add this line (runs at 8:30 AM every weekday):
30 8 * * 1-5 cd /path/to/job_agent && python agent.py --schedule
```

**Option D — Keep it running in background:**
Choose option 15 in the menu — "Start automated scheduler"
Leave the terminal open. It will run all tasks automatically.

---

## WHAT TO DO THIS WEEK

### Day 1 (Today):
- [ ] Complete setup (steps 1–5 above)
- [ ] Run agent → Option 9 (daily report)
- [ ] Run agent → Option 6 (generate Week 1 LinkedIn post)
- [ ] Publish that post on LinkedIn

### Day 2:
- [ ] Find 3 job descriptions online
- [ ] Run agent → Option 1 for each (tailor resume)
- [ ] Apply to each role
- [ ] Run agent → Option 8 to track each application
- [ ] Find hiring managers → Run agent → Option 3

### Day 3:
- [ ] Run agent → Option 2 (message 3 executive recruiters)
- [ ] Run agent → Option 4 (message 5 IAF network contacts)

### Day 7:
- [ ] Run agent → Option 7 (generate all 12 LinkedIn posts at once)
- [ ] Schedule them in LinkedIn's native scheduler

---

## SUPPORT

If you get an error, check:
1. Your API key is correct in agent.py
2. You have internet connection
3. You ran `pip install anthropic schedule pandas openpyxl`

For API issues: https://docs.anthropic.com
For Python issues: https://python.org/doc

---

*Built specifically for Dr. Madhuresh Shukla's cybersecurity job search transition.*
*Your profile data is pre-loaded — the agent knows your full background and generates content specific to you.*
