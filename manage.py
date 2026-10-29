"""Command-line helper for the local test app. Run from the project folder.

Examples:
  python manage.py init-db
  python manage.py ensure-researcher
  python manage.py create-researcher
  python manage.py seed-fictional --count 12
  python manage.py count
"""
import argparse
import getpass
import sys

from app import services
from app.db import connect, init_db
from config import DEFAULT_DATABASE


def _prompt_for_account(conn):
    print("Create a researcher account for LOCAL TEST access only.")
    username = input("Username (3-32 letters, digits, dot, dash or underscore): ").strip()
    password = getpass.getpass("Password (at least 10 characters; typing is hidden): ")
    confirm = getpass.getpass("Repeat password: ")
    if password != confirm:
        print("ERROR: the two passwords do not match. Nothing was saved.")
        return 1
    try:
        services.create_researcher(conn, username, password)
    except ValueError as exc:
        print(f"ERROR: {exc}. Nothing was saved.")
        return 1
    print(f"Researcher account created: {username}")
    return 0


def cmd_init_db(_args):
    init_db(DEFAULT_DATABASE)
    print("Database is ready in the instance folder.")
    return 0


def cmd_ensure_researcher(_args):
    init_db(DEFAULT_DATABASE)
    conn = connect(DEFAULT_DATABASE)
    try:
        if services.researcher_count(conn) > 0:
            print("A researcher account already exists. Nothing was changed.")
            return 0
        return _prompt_for_account(conn)
    finally:
        conn.close()


def cmd_create_researcher(_args):
    init_db(DEFAULT_DATABASE)
    conn = connect(DEFAULT_DATABASE)
    try:
        return _prompt_for_account(conn)
    finally:
        conn.close()


def cmd_seed_fictional(args):
    init_db(DEFAULT_DATABASE)
    conn = connect(DEFAULT_DATABASE)
    try:
        inserted = services.seed_fictional(conn, args.count)
        print(f"Inserted {inserted} fictional TEST records.")
        return 0
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    finally:
        conn.close()


def cmd_count(_args):
    init_db(DEFAULT_DATABASE)
    conn = connect(DEFAULT_DATABASE)
    try:
        counts = services.summary_counts(conn)
        print(f"Total records: {counts['total']}")
        print(f"Test records: {counts['test_count']}")
        return 0
    finally:
        conn.close()


def build_parser():
    parser = argparse.ArgumentParser(description="Local test app helper (fictional data only).")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init-db", help="create the database tables if missing")
    sub.add_parser("ensure-researcher", help="create the first researcher account if none exists")
    sub.add_parser("create-researcher", help="create a researcher account")
    seed = sub.add_parser("seed-fictional", help="insert fictional TEST records")
    seed.add_argument("--count", type=int, default=10)
    sub.add_parser("count", help="show record counts")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    handlers = {
        "init-db": cmd_init_db,
        "ensure-researcher": cmd_ensure_researcher,
        "create-researcher": cmd_create_researcher,
        "seed-fictional": cmd_seed_fictional,
        "count": cmd_count,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
