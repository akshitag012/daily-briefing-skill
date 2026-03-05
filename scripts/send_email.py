#!/usr/bin/env python3
"""
send_email.py - Send HTML emails via Gmail API (OAuth 2.0)

Usage:
    send_email.py --to "addr1,addr2" --subject "Subject" --html /path/to/file.html
    send_email.py --to "addr1" --subject "Subject" --body "Plain text body"

First run will open a browser for OAuth authorization.
Subsequent runs use the saved token (auto-refreshes).
"""

import argparse
import base64
import re
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    """Authenticate and return a Gmail API service object."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...", file=sys.stderr)
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(
                    f"ERROR: {CREDENTIALS_FILE} not found.\n"
                    "Download OAuth credentials from Google Cloud Console\n"
                    "and save as credentials.json in the scripts/ directory.",
                    file=sys.stderr,
                )
                sys.exit(1)
            print("First-time authorization: opening browser...", file=sys.stderr)
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())
        print(f"Token saved to {TOKEN_FILE}", file=sys.stderr)

    return build("gmail", "v1", credentials=creds)


def create_message(to, subject, body_html=None, body_text=None):
    """Create a MIME message for the Gmail API."""
    if body_html:
        message = MIMEMultipart("alternative")
        plain_fallback = re.sub(r"<[^>]+>", "", body_html)
        plain_fallback = re.sub(r"\s+", " ", plain_fallback).strip()
        message.attach(MIMEText(plain_fallback, "plain"))
        message.attach(MIMEText(body_html, "html"))
    else:
        message = MIMEText(body_text or "", "plain")

    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}


def main():
    parser = argparse.ArgumentParser(description="Send HTML email via Gmail API")
    parser.add_argument("--to", required=True, help="Comma-separated recipient addresses")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--html", help="Path to HTML file for email body")
    parser.add_argument("--body", help="Plain text body (if --html not provided)")
    args = parser.parse_args()

    if not args.html and not args.body:
        parser.error("Either --html or --body is required")

    body_html = None
    body_text = None

    if args.html:
        html_path = Path(args.html)
        if not html_path.exists():
            print(f"ERROR: HTML file not found: {args.html}", file=sys.stderr)
            sys.exit(1)
        body_html = html_path.read_text(encoding="utf-8")
        print(f"Loaded HTML ({len(body_html)} chars) from {args.html}", file=sys.stderr)
    else:
        body_text = args.body

    service = get_gmail_service()

    msg = create_message(args.to, args.subject, body_html=body_html, body_text=body_text)
    result = service.users().messages().send(userId="me", body=msg).execute()

    msg_id = result.get("id", "unknown")
    print(f"Email sent successfully! Message ID: {msg_id}")


if __name__ == "__main__":
    main()
