"""Start the local test server. It listens only on this computer (127.0.0.1)."""
import logging
import os

from app import create_app


def main():
    port = int(os.environ.get("APP_PORT", "5000"))
    # Hide per-request log lines in the terminal. Errors still show.
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app = create_app()
    print(f"Local test server: http://127.0.0.1:{port}")
    print("Fictional data only. Press Ctrl+C to stop.")
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
