#!/usr/bin/env python3
"""Increments a streak counter and updates a marked section in README.md.

Safe to run repeatedly: if the counter file or markers don't exist yet,
it creates them. If the markers already exist, it replaces only the
content between them, leaving the rest of the README untouched.
"""
import re
from datetime import timezone, datetime
from pathlib import Path

COUNTER_FILE = Path("streak_count.txt")
README_FILE = Path("README.md")
START_MARKER = "<!--START_SECTION:streak-->"
END_MARKER = "<!--END_SECTION:streak-->"


def get_count() -> int:
    if COUNTER_FILE.exists():
        try:
            return int(COUNTER_FILE.read_text().strip())
        except ValueError:
            return 0
    return 0


def main() -> None:
    count = get_count() + 1
    COUNTER_FILE.write_text(str(count))

    today = datetime.now(timezone.utc).date().isoformat()
    block = (
        f"{START_MARKER}\n"
        f"🔥 Kept Active: **{count}** days (last updated {today} UTC)\n"
        f"{END_MARKER}"
    )

    if README_FILE.exists():
        content = README_FILE.read_text()
        if START_MARKER in content and END_MARKER in content:
            pattern = re.compile(
                re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
                re.DOTALL,
            )
            content = pattern.sub(block, content)
        else:
            content = content.rstrip() + "\n\n" + block + "\n"
    else:
        content = f"# Jasiri-w\n\n{block}\n"

    README_FILE.write_text(content)
    print(f"Streak updated to {count}")


if __name__ == "__main__":
    main()
