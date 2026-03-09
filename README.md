# Daily Briefing Skill for Claude Code

A Claude Code skill that generates a personalized daily briefing by summarizing your email newsletters and curating healthtech news from the web — then sends it directly to your inbox.

## What It Does

Every morning, this skill:

1. **Fetches newsletters** from your Gmail (Substack, Morning Brew, beehiiv, etc.)
2. **Summarizes each one** — covering all key topics, not just the headline
3. **Curates healthtech news** from the web across 4 focused sections:
   - AI in Public Health (community health lens)
   - Home Healthcare & Supply-Side Marketplace
   - HealthTech Startup Deals (India + US/Global)
   - Digital Health & HealthTech India
4. **Sends formatted HTML emails** directly to your inbox via Gmail API
5. **Deduplicates across runs** — tracks previously shared articles and themes so you never see the same story twice

## Two Emails Per Run

| Email | Recipients | Content |
|-------|-----------|---------|
| **Daily Briefing** | You | Newsletter digest + healthtech deep-dive |
| **HealthTech Daily** | Your team | Healthtech section only (standalone branding) |

## Examples

See what the output looks like:
- [Full Briefing](examples/example-briefing.html) — newsletter summaries + healthtech
- [HealthTech Daily](examples/example-healthtech.html) — standalone healthtech email

## Setup

### 1. Install the Skill

Copy the skill files to your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/daily-briefing
cp SKILL.md ~/.claude/skills/daily-briefing/
cp -r scripts ~/.claude/skills/daily-briefing/
cp -r references ~/.claude/skills/daily-briefing/
```

### 2. Configure Gmail MCP

The skill uses Gmail MCP tools to search and read your newsletters. Make sure you have the Gmail MCP server connected in Claude Code.

### 3. Set Up Auto-Send (Optional)

To send emails directly instead of creating drafts, set up the Gmail API send script:

```bash
cd scripts
python3 -m venv venv
venv/bin/pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Then follow the instructions in [scripts/SETUP.md](scripts/SETUP.md) to configure OAuth credentials.

### 4. Schedule It (Optional)

For automatic daily runs, the recommended approach is a **wrapper script** that reads SKILL.md and passes it directly to Claude (since Claude can't discover custom skills in headless mode):

```bash
# scripts/run-briefing.sh does this automatically
chmod +x scripts/run-briefing.sh
```

Then set up a macOS LaunchAgent or cron job. See [references/scheduling.md](references/scheduling.md).

## Usage

Run the skill interactively in Claude Code:

```
/daily-briefing
```

Or run it headlessly via the wrapper script:

```bash
./scripts/run-briefing.sh
```

## Customization

The skill is fully customizable via `SKILL.md`. You can:

- **Change newsletter sources** — edit the Gmail search queries in Step 1
- **Change healthtech focus areas** — edit the search queries and trusted sources in Step 3
- **Add/remove sections** — the healthtech deep-dive has 4 subsections you can modify
- **Change recipients** — edit the email addresses in Step 4
- **Change the design** — edit the inline CSS design system in Step 4

## Freshness & Dedup

The skill includes built-in protections against stale or repeated content:

- **Two-pass date verification** — parses dates from URLs, then uses WebFetch to verify ambiguous publication dates. Rejects anything older than 48 hours.
- **URL + headline dedup** — tracks all shared articles in `data/sent-articles.log` to prevent repeats across runs.
- **Thematic dedup** — tracks topic themes so you don't see "Budget 2026 healthcare analysis" three days in a row from different publications.

## How It Works

```
Gmail (newsletters) ──┐
                       ├──> Claude summarizes & composes ──> Gmail API sends
Web Search (healthtech)┘
```

The skill is a single `SKILL.md` file that instructs Claude Code to:
1. Search Gmail for newsletters from the last 24 hours
2. Read and summarize each newsletter (covering all topics, not just the lead)
3. Run web searches for healthtech news across trusted sources
4. Verify article freshness (URL date parsing + WebFetch)
5. Check dedup log to skip previously shared articles and themes
6. Compose two HTML emails with inline CSS (Gmail-safe)
7. Send them via the Gmail API send script

## Project Structure

```
daily-briefing-skill/
├── SKILL.md                    # The skill definition (the brain)
├── scripts/
│   ├── send_email.py           # Gmail API auto-send script
│   ├── run-briefing.sh         # Wrapper for headless/scheduled runs
│   ├── SETUP.md                # OAuth setup instructions
│   └── .gitignore              # Excludes credentials & venv
├── data/
│   └── sent-articles.log       # Dedup log (auto-created on first run)
├── references/
│   └── scheduling.md           # Cron / LaunchAgent setup
├── examples/
│   ├── example-briefing.html   # Sample full briefing email
│   └── example-healthtech.html # Sample healthtech-only email
└── README.md
```

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Gmail MCP server connected
- Python 3.9+ (for auto-send script)
- Google Cloud project with Gmail API enabled (for auto-send)

## License

MIT
