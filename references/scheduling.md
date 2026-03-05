# Scheduling the Daily Briefing

## Option 1: Cron Job (Simpler)

Add this to your crontab (`crontab -e`):

```cron
# Run daily briefing at 7:00 AM every day
0 7 * * * /usr/local/bin/claude -p "Run my /daily-briefing skill" --allowedTools "mcp__claude_ai_Gmail__*,WebSearch,Bash" 2>&1 >> ~/daily-briefing.log
```

Adjust the path to `claude` based on your installation. Check with `which claude`.

## Option 2: macOS LaunchAgent (More Reliable)

Create a plist file at `~/Library/LaunchAgents/com.dailybriefing.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.dailybriefing</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/claude</string>
        <string>-p</string>
        <string>Run my /daily-briefing skill</string>
        <string>--allowedTools</string>
        <string>mcp__claude_ai_Gmail__*,WebSearch,Bash</string>
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
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.dailybriefing.plist
```

Unload it:
```bash
launchctl unload ~/Library/LaunchAgents/com.dailybriefing.plist
```

## Verifying

Check if the agent is loaded:
```bash
launchctl list | grep dailybriefing
```

Check logs:
```bash
tail -f /tmp/daily-briefing.log
```
