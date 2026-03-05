---
name: daily-briefing
description: Generate a daily briefing that summarizes the user's email newsletters from the last 24 hours, adds a healthtech deep-dive (India + US), delivers it as a formatted email, and creates a podcast audio version. Use this skill whenever the user asks for their daily briefing, newsletter summary, morning digest, daily roundup, or wants to catch up on what they missed. Also triggers on '/daily-briefing'.
---

# Daily Briefing

You are building a personalized daily briefing for the user. The briefing has three parts:

1. **Newsletter Digest** — summaries of newsletters received in the last 24 hours
2. **HealthTech Deep-Dive** — curated headlines from the web about healthtech in India and the US
3. **Delivery** — a formatted HTML email sent to the user's inbox + a podcast MP3

## Step 1: Fetch Newsletters from Gmail

Search Gmail for newsletters from the last 24 hours using these queries (run both, deduplicate by message ID):

```
label:news newer_than:1d
```
```
from:substack.com newer_than:1d
```

Also search for known newsletter senders:
```
newer_than:1d (from:morningbrew.com OR from:community.morningbrew.com OR from:beehiiv.com)
```

Use `gmail_search_messages` with `maxResults: 50` for each query. Collect all unique message IDs.

If no "news" label results come back, rely on the substack + known senders queries.

Then read each message using `gmail_read_message` to get the full content. Do this in parallel batches of 5-10 to stay efficient.

### Filtering out noise

Not everything from these senders is a newsletter. Skip messages that are:
- Substack "liked" or "commented" notifications (from reaction@mg1.substack.com)
- Transactional emails (order confirmations, shipping updates, account alerts)
- Pure promotional/sales emails with no editorial content

Keep messages that have substantial editorial content — articles, analysis, market updates, curated links, etc.

## Step 2: Summarize Each Newsletter

For each newsletter, extract:
- **Source**: sender name (e.g., "Morning Brew", "a16z")
- **Headline**: the subject line or main topic
- **Summary**: Cover ALL the key topics in the newsletter, not just the lead story. If a newsletter discussed 3 different things, mention all 3 so the reader knows whether to click through. Use bullet points or semicolons to separate distinct topics. Be specific — include numbers, names, and takeaways, not vague generalities.
- **Category**: tag it as one of: Tech, Business, Finance, Healthcare, Markets, AI, Other
- **Gmail Link**: construct a clickable link to the email using: `https://mail.google.com/mail/u/0/#inbox/<messageId>`

Group the summaries by category in the final output.

## Step 3: HealthTech Deep-Dive

The healthtech section has four focused subsections. For each, run targeted web searches using the trusted sources and focus areas below. Go for substance — specific numbers, company names, deal sizes, policy details. Skip hospital IT, traditional healthcare operations, and generic "AI will change everything" fluff.

### Trusted Sources (prioritize results from these domains)

**India**: YourStory, Inc42, Tracxn, ET HealthWorld, MedicalBuyer, Digital Health News (digitalhealthnews.com), APAC News Network
**US/Global**: STAT News, Rock Health, Fierce Healthcare, MobiHealthNews, Digital Health News, HealthTech Magazine

### Source Diversity Rule

Don't over-index on any single source. In particular, cap digitalhealthnews.com at 1-2 articles max across the entire healthtech section — only include them if the article is genuinely high-quality and relevant, not just because it showed up in search results. Spread across multiple sources for a well-rounded view.

### Linking Rule

Always link to the **specific article page URL**, not the site's homepage or section page. The reader needs to be able to click through and land on the exact story. If you can't find a direct article URL from search results, note the source but don't fake a link.

### Subsection A: AI in Public Health (Bahaar lens)

Context: The user works with Bahaar, a company focused on using AI to build community health access — early diagnostics, health knowledge delivery, and basic healthcare in rural/semi-urban India where access is limited.

Search queries (run 2-3):
- `site:yourstory.com OR site:inc42.com OR site:digitalhealthnews.com "community health" OR "public health" OR "rural health" AI India` (current week/month)
- `"community health workers" OR "primary care" AI diagnostics rural` (current month)
- `"public health AI" OR "community health AI" global examples` (current month)

What to include:
- AI tools for community health workers, frontline health, ASHA workers
- Diagnostic AI for low-resource settings (point-of-care, mobile-based)
- Health knowledge delivery to underserved populations
- Global examples India could learn from (e.g., AI health programs in Africa, Southeast Asia, Latin America)
- Government digital health programs (Ayushman Bharat Digital Mission updates, ABDM)

What to skip: Hospital EHR systems, enterprise health IT, insurance tech

Capture 3-5 stories. For each: headline, **direct link to the specific article page** (not the site homepage), 2-sentence summary, and a one-line "Bahaar relevance" note explaining why it matters for community health work.

### Subsection B: Home Healthcare & Supply-Side Marketplace (POTIA lens)

Context: The user works with POTIA Medical, a home healthcare company in India. The core challenge is supply-side engagement — recruiting, training, and retaining healthcare workers (nurses, attendants, physiotherapists) who are often from small towns and villages with limited formal education. POTIA operates as a marketplace connecting patients who need home care with these workers. The user wants to learn from how other marketplace companies (Swiggy, Uber, Urban Company, Snabbit, Porter) solve similar supply-side problems, as well as track home healthcare industry trends.

Search queries (run 2-3):
- `"home healthcare" OR "home care" India startup OR company OR funding` (current month)
- `"Urban Company" OR "Swiggy" OR "Porter" OR "Snabbit" gig worker retention OR training OR supply side` (current month)
- `"home healthcare" OR "home nursing" marketplace OR platform worker engagement` (current month)

What to include:
- Home healthcare companies in India and globally — funding, launches, expansions (e.g., Portea, Care24, Sukino, Nightingales, MediBuddy home care)
- Supply-side marketplace strategies: how gig/service platforms recruit, train, retain, and engage blue-collar or semi-skilled workers
- Worker training and upskilling programs — especially mobile-first, vernacular, or low-literacy approaches
- Technology for field workforce management — apps, scheduling, quality monitoring, worker incentives
- Regulatory changes affecting home healthcare in India
- Global home healthcare trends that could apply to India

What to skip: Hospital staffing, enterprise HR tech, B2B SaaS for large healthcare systems

Capture 3-5 stories. For each: headline, **direct link to the specific article page** (not the site homepage), 2-sentence summary, and a one-line "POTIA relevance" note explaining why it matters for home healthcare supply-side operations.

### Subsection C: HealthTech Startup Deals

Search queries (run 2-3):
- `site:yourstory.com OR site:inc42.com OR site:tracxn.com healthtech funding India` (current week/month)
- `site:statnews.com OR site:rockhealth.com OR site:fiercehealthcare.com healthtech funding OR "series A" OR "series B" OR acquisition` (current week/month)
- `"digital health" OR healthtech startup funding round` (current week)

What to include:
- Seed, Series A/B/C rounds with deal sizes and investors
- Acquisitions and exits
- New healthtech startups launching
- Mental health startups specifically (the user is interested in this space)
- Companies like Eka Care and their competitors

Format: For each deal, capture company name, what they do, round size, key investors, region (India/US/Global), and a **direct link to the specific article** (not the site homepage). Aim for 3-5 deals per region.

### Subsection D: Digital Health & HealthTech India

Broader trends, infrastructure, and notable company moves.

Search queries (run 2-3):
- `"digital health India" OR "health tech India" OR "ABDM" trends` (current month)
- `"Eka Care" OR "digital health India" startup launches partnerships` (current month)
- `"mental health" startup OR app India OR US` (current month)

What to include:
- Digital health infrastructure (ABDM, health IDs, interoperability)
- Companies like Eka Care — product launches, expansions, partnerships
- Mental health innovation (apps, AI therapy, telepsychiatry)
- Digital health policy and regulation changes
- Interesting US/global digital health trends relevant to India

Capture 3-5 stories with headline, **direct link to the specific article page** (not the site homepage), and 2-sentence summary.

## Step 4: Compose the Briefing Email

Create a clean, well-formatted HTML email. Use this structure:

```
Subject: Daily Briefing — [Today's Date, e.g., "March 4, 2026"]
```

### Email Structure

The email should be clean and scannable. Use inline CSS (Gmail strips <style> tags). Design guidelines:
- Max width: 600px, centered
- Font: system font stack (-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif)
- Background: #f5f5f5, content area: white
- Section headers: bold, dark color, with a subtle bottom border
- Each newsletter summary: headline as a link, category tag as a colored pill/badge, summary text below
- HealthTech section: split into India / US subsections with flag indicators
- Footer: "Generated by your Daily Briefing skill" with timestamp

Color coding for category badges:
- Tech: #2563eb (blue)
- Finance/Markets: #059669 (green)
- Healthcare: #dc2626 (red)
- Business: #d97706 (amber)
- AI: #7c3aed (purple)
- Other: #6b7280 (gray)

### Email Content Sections

1. **Header**: "Your Daily Briefing" + date
2. **Quick Stats**: "X newsletters summarized | Y healthtech stories"
3. **Newsletter Digest** (grouped by category):
   - Each item: [Category Badge] **Headline** (linked to Gmail message)
   - Summary paragraph
4. **HealthTech Deep-Dive** (four subsections):
   - **AI in Public Health** (Bahaar lens) — community health, rural access, global examples. Each item includes a "Bahaar relevance" note.
   - **Home Healthcare & Supply-Side Marketplace** (POTIA lens) — home care industry, gig worker engagement, marketplace strategies. Each item includes a "POTIA relevance" note.
   - **Startup Deals** — funding rounds, India vs US/Global, with deal sizes and investors
   - **Digital Health & HealthTech India** — trends, Eka Care, mental health, infrastructure
5. **Footer**

### Two Emails

This skill generates **two separate emails** per run:

#### Email 1: Full Briefing → your-email@gmail.com
Contains everything: Newsletter Digest (Part 1) + HealthTech Deep-Dive (Part 2). Subject: `Daily Briefing — [Date]`

#### Email 2: HealthTech-Only Briefing → teammate1@gmail.com, teammate2@gmail.com
Contains **only** the HealthTech Deep-Dive (Part 2: Sections A, B, C, D). No newsletter digest. This is a standalone email with its own header/branding:
- Subject: `HealthTech Daily — [Date]`
- Header: "HealthTech Daily" instead of "Your Daily Briefing"
- Quick Stats: "Y healthtech stories across 4 sections" (no newsletter count)
- Same design language as the full briefing but self-contained — should not look like a chopped excerpt

Use the same inline CSS design system, section colors, and card styles for the healthtech email.

### Sending

Save each email's HTML to a temp file, then send it directly using the Gmail API send script. Run both via the Bash tool:

#### Email 1: Full Briefing
```bash
/Users/akshita/skills/skills/daily-briefing/scripts/venv/bin/python \
    /Users/akshita/skills/skills/daily-briefing/scripts/send_email.py \
    --to "your-email@gmail.com" \
    --subject "Daily Briefing — [Date]" \
    --html /tmp/daily-briefing-YYYY-MM-DD-full.html
```

#### Email 2: HealthTech-Only Briefing
```bash
/Users/akshita/skills/skills/daily-briefing/scripts/venv/bin/python \
    /Users/akshita/skills/skills/daily-briefing/scripts/send_email.py \
    --to "teammate1@gmail.com, teammate2@gmail.com" \
    --subject "HealthTech Daily — [Date]" \
    --html /tmp/daily-briefing-YYYY-MM-DD-healthtech.html
```

Check exit code and stdout for confirmation ("Email sent successfully!").

#### Fallback
If the send script fails (token expired, script not set up), fall back to creating drafts using `gmail_create_draft` with `contentType: "text/html"` and tell the user the drafts need manual sending.

## Step 5: Podcast (DISABLED)

Podcast generation is currently disabled. When re-enabled, it should use ElevenLabs or Sarvam TTS (not macOS `say`) and should be a direct read-through of the briefing content above — not a generic news summary.

## Scheduling (Cron Setup)

For automatic daily runs, the user can set up a cron job or launchd plist. Read `references/scheduling.md` for the setup instructions.

## Notes

- The whole process should take 2-3 minutes to run
- If Gmail MCP tools aren't available, tell the user they need to be connected
- If web search isn't available, skip the healthtech section and note it in the email
- Always tell the user what you found and what you're including before sending
