# fetcher/imap_actions.py

import imaplib

def move_email(imap_conn: imaplib.IMAP4_SSL, msg_uid: str, target_folder: str):
    """Move an email (by UID) to the target_folder. Gmail's folder separator is '/'. """
    # Move (RFC6851, not all servers support): if not, fallback to copy+delete
    # UID Move is best, fallback to copy/delete
    res = imap_conn.uid('MOVE', msg_uid, target_folder)
    if res[0] == 'OK':
        return True
    # If move unsupported (e.g. IMAP error), fallback to copy+delete
    imap_conn.uid('COPY', msg_uid, target_folder)
    imap_conn.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
    imap_conn.expunge()
    return True

def delete_email(imap_conn: imaplib.IMAP4_SSL, msg_uid: str):
    """Delete email (by UID)."""
    imap_conn.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
    imap_conn.expunge()
    return True

def batch_move(imap_conn, msg_uids, target_folder):
    moved = []
    for uid in msg_uids:
        if move_email(imap_conn, uid, target_folder):
            moved.append(uid)
    return moved

def batch_delete(imap_conn, msg_uids):
    deleted = []
    for uid in msg_uids:
        if delete_email(imap_conn, uid):
            deleted.append(uid)
    return deleted

if __name__ == "__main__":
    print("This module is for use from the main orchestration script.")
