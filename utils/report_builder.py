# utils/report_builder.py

from .formatter import combined_html_report, combined_text_report

def build_action_report(summary_text, per_mailbox_important, per_mailbox_moved, per_mailbox_deleted):
    """
    Returns (html, text) versions of a summary report of all moves/deletes/etc.
    """
    html = combined_html_report(
        summary_text,
        per_mailbox_important,   # dict {mailbox: list of email dict}
        per_mailbox_moved,
        per_mailbox_deleted
    )
    text = combined_text_report(
        summary_text,
        per_mailbox_important,
        per_mailbox_moved,
        per_mailbox_deleted
    )
    return html, text

if __name__ == "__main__":
    # Very simple mock test
    test_dict = {"Gmail": [
        {"from": "an@email.com", "subject": "Test", "snippet": "Some content here."}
    ]}
    res = build_action_report(
        summary_text="Test run",
        per_mailbox_important=test_dict,
        per_mailbox_moved={},
        per_mailbox_deleted={},
    )
    print(res[0])  # HTML
    print("\n\n")
    print(res[1])  # Plain text
