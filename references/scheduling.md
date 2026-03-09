# Scheduling the Daily Briefing

**Important:** Claude Code cannot discover custom skills when running headlessly (e.g., `claude -p "Run my /daily-briefing skill"` won't work). Use the wrapper script `scripts/run-briefing.sh` which reads `SKILL.md` and passes it directly as the prompt.

## Option 1: macOS LaunchAgent (Recommended)

LaunchAgent catches up on missed runs when your Mac wakes from sleep (cron does not).

Create `~/Library/LaunchAgents/com.dailybriefing.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.dailybriefing</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/daily-briefing-skill/scripts/run-briefing.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/daily-briefing.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/daily-briefing-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>/Users/your-username</string>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/your-username</string>
</dict>
</plist>
```

Replace `/path/to/daily-briefing-skill/` and `/Users/your-username` with your actual paths.

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.dailybriefing.plist
```

Unload it:
```bash
launchctl unload ~/Library/LaunchAgents/com.dailybriefing.plist
```

## Option 2: Cron Job

Simpler but does NOT catch up on missed runs if your Mac was asleep.

```bash
crontab -e
```

Add:
```cron
0 7 * * * /bin/bash /path/to/daily-briefing-skill/scripts/run-briefing.sh 2>&1 >> /tmp/daily-briefing.log
```

## Verifying

Check if the LaunchAgent is loaded:
```bash
launchctl list | grep dailybriefing
```

Check logs:
```bash
tail -f /tmp/daily-briefing.log
```
