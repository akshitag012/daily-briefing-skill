# Gmail API Auto-Send Setup

One-time setup to enable the daily briefing skill to send emails directly (not just create drafts).

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in as `aksh.ganesh@gmail.com`
3. Click the project dropdown at the top → **New Project**
4. Name: `daily-briefing-sender`
5. Click **Create**, then select the new project

## Step 2: Enable the Gmail API

1. In the left sidebar: **APIs & Services** → **Library**
2. Search for **Gmail API**
3. Click it, then click **Enable**

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** user type → **Create**
3. Fill in:
   - App name: `Daily Briefing Sender`
   - User support email: `aksh.ganesh@gmail.com`
   - Developer contact: `aksh.ganesh@gmail.com`
4. Click **Save and Continue**
5. On Scopes page → **Add or Remove Scopes** → find and select:
   - `https://www.googleapis.com/auth/gmail.send`
6. Click **Update** → **Save and Continue**
7. On Test Users page → **Add Users** → add `aksh.ganesh@gmail.com`
8. Click **Save and Continue** → **Back to Dashboard**

**Important:** Click **Publish App** on the OAuth consent screen. This prevents the refresh token from expiring after 7 days. Since the app only uses `gmail.send` scope and only you use it, Google won't require a security review.

## Step 4: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `daily-briefing-cli`
5. Click **Create**
6. Click **Download JSON**
7. Move/rename the downloaded file to:
   ```
   /Users/akshita/skills/skills/daily-briefing/scripts/credentials.json
   ```

## Step 5: First-Time Authorization

Run this test command in your terminal:

```bash
/Users/akshita/skills/skills/daily-briefing/scripts/venv/bin/python \
    /Users/akshita/skills/skills/daily-briefing/scripts/send_email.py \
    --to "aksh.ganesh@gmail.com" \
    --subject "Test - Gmail API Send" \
    --body "This is a test email. If you see this, auto-send is working!"
```

What happens:
1. A browser window opens with Google's consent screen
2. Sign in and click **Allow**
3. The script saves a `token.json` file (used for all future runs)
4. A test email is sent to your inbox

After this, all future runs (including cron/launchd) work automatically without a browser.

## Troubleshooting

**Token expired / authorization error:**
Re-run the test command above from a terminal with browser access.

**`credentials.json` not found:**
Download it again from Google Cloud Console → Credentials → your OAuth client → Download JSON.

**Rate limits:**
Gmail API allows 250 emails/day. The briefing sends 2 per day — no issues.
