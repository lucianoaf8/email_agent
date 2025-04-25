# utils/formatter.py

from typing import List, Dict

def html_email_list(title, emails: List[Dict]):
    """Create an HTML email list section."""
    if not emails:
        return f"<p>No emails.</p>"
    html = [f"<h3>{title}</h3>", "<ul>"]
    for e in emails:
        html.append(
            f"<li><b>{e.get('subject','(No subject)')}</b><br>"
            f"From: <em>{e.get('from','')}</em><br>"
            f"<span style='font-size:smaller;color:gray'>{e.get('snippet','')}</span></li>"
        )
    html.append("</ul>")
    return "\n".join(html)

def text_email_list(title, emails: List[Dict]):
    """Create a plain text email list section."""
    if not emails:
        return f"{title}: No emails."
    lines = [f"{title}:"]
    for e in emails:
        lines.append(
            f"Subject: {e.get('subject','')}\nFrom: {e.get('from','')}\nSnippet: {e.get('snippet','')}\n"
        )
    return "\n".join(lines)

def combined_html_report(summary_text, per_box_important, per_box_moved, per_box_deleted):
    """Produce a full HTML report for summary mail."""
    html = [
        "<h2>Daily Email Summary</h2>",
        f"<p><b>Summary:</b> {summary_text}</p>"
    ]
    # Section: Important (moved-to-folder)
    for box, emails in per_box_important.items():
        html.append(html_email_list(f"Moved to Important in {box}", emails))

    # Section: Receipts (or whatever you choose) moved
    for box, emails in per_box_moved.items():
        html.append(html_email_list(f"These receipts (and similar) were moved in {box}", emails))

    # Section: Junk/Deleted
    for box, emails in per_box_deleted.items():
        html.append(html_email_list(f"Deleted as Junk in {box}", emails))

    return "\n".join(html)

def combined_text_report(summary_text, per_box_important, per_box_moved, per_box_deleted):
    lines = [f"Daily Email Summary\n", f"Summary: {summary_text}\n"]
    for box, emails in per_box_important.items():
        lines.append(text_email_list(f"Moved to Important in {box}", emails))
    for box, emails in per_box_moved.items():
        lines.append(text_email_list(f"Moved to Receipts/etc. in {box}", emails))
    for box, emails in per_box_deleted.items():
        lines.append(text_email_list(f"Deleted as Junk in {box}", emails))
    return "\n\n".join(lines)

if __name__ == "__main__":
    # Minimal quick test
    testlist = [
        {"from": "a@x.com", "subject": "hello new offer", "snippet": "test snippet"},
        {"from": "b@y.com", "subject": "invoice #22", "snippet": "hi, see attached"},
    ]
    print(html_email_list("Promotions", testlist))
    print(text_email_list("Promotions", testlist))
