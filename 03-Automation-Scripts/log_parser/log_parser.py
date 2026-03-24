"""
Log Parser — AI-Assisted Log Analysis Tool
===========================================

解析工業設備或應用程式日誌，自動識別錯誤模式並摘要告警資訊。

使用方式：
    python log_parser.py --log_file /var/log/app.log
    python log_parser.py --log_file /var/log/app.log --level ERROR --output report.txt

功能：
    - 依嚴重等級過濾日誌條目 (DEBUG / INFO / WARNING / ERROR / CRITICAL)
    - 統計各等級出現次數
    - 提取含有關鍵字的條目（可自訂）
    - 輸出純文字摘要報告
"""

import argparse
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# 常數 / Constants
# ---------------------------------------------------------------------------

LOG_LEVEL_ORDER = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# 標準 Python logging 格式：2024-01-01 12:00:00,000 - NAME - LEVEL - message
LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}[,.]?\d*)"
    r".*?\b(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\b"
    r"\s*[-:]?\s*(?P<message>.+)"
)

# 預設關鍵字告警清單（可依專案調整）
DEFAULT_KEYWORDS = [
    "exception",
    "traceback",
    "connection refused",
    "timeout",
    "out of memory",
    "segfault",
    "disk full",
    "failed",
]


# ---------------------------------------------------------------------------
# 解析邏輯 / Parsing Logic
# ---------------------------------------------------------------------------


def parse_log_file(path: str) -> list[dict]:
    """讀取日誌檔，逐行解析並回傳結構化條目清單。"""
    entries = []
    log_path = Path(path)

    if not log_path.exists():
        print(f"[ERROR] Log file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with log_path.open(encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.rstrip()
            if not line:
                continue
            match = LOG_PATTERN.search(line)
            if match:
                entries.append({
                    "lineno": lineno,
                    "timestamp": match.group("timestamp"),
                    "level": match.group("level"),
                    "message": match.group("message").strip(),
                    "raw": line,
                })
            else:
                # 保留無法解析的行（例如 traceback 後續行）
                entries.append({
                    "lineno": lineno,
                    "timestamp": None,
                    "level": "UNKNOWN",
                    "message": line,
                    "raw": line,
                })
    return entries


def filter_by_level(entries: list[dict], min_level: str) -> list[dict]:
    """過濾出嚴重等級 >= min_level 的條目。"""
    if min_level not in LOG_LEVEL_ORDER:
        return entries
    threshold = LOG_LEVEL_ORDER.index(min_level)
    return [
        e for e in entries
        if e["level"] in LOG_LEVEL_ORDER and LOG_LEVEL_ORDER.index(e["level"]) >= threshold
    ]


def find_keyword_entries(entries: list[dict], keywords: list[str]) -> list[dict]:
    """回傳包含指定關鍵字的條目。"""
    kw_lower = [k.lower() for k in keywords]
    return [
        e for e in entries
        if any(kw in e["message"].lower() for kw in kw_lower)
    ]


# ---------------------------------------------------------------------------
# 報告產生 / Report Generation
# ---------------------------------------------------------------------------


def build_report(entries: list[dict], keywords: list[str]) -> str:
    """產生純文字摘要報告。"""
    lines = []
    lines.append("=" * 70)
    lines.append("  Log Analysis Report")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)

    # 統計各等級數量
    level_counts = Counter(e["level"] for e in entries)
    lines.append("\n[Summary] Log Level Distribution:")
    for level in LOG_LEVEL_ORDER + ["UNKNOWN"]:
        count = level_counts.get(level, 0)
        if count:
            lines.append(f"  {level:<10} {count:>6} entries")

    # 關鍵字告警
    kw_entries = find_keyword_entries(entries, keywords)
    lines.append(f"\n[Alerts] Keyword Matches ({len(kw_entries)} entries):")
    if kw_entries:
        for e in kw_entries[:20]:  # 最多顯示 20 筆
            ts = e["timestamp"] or "N/A"
            lines.append(f"  Line {e['lineno']:>5} | {ts} | {e['level']:<8} | {e['message'][:100]}")
        if len(kw_entries) > 20:
            lines.append(f"  ... and {len(kw_entries) - 20} more")
    else:
        lines.append("  No keyword matches found.")

    # ERROR / CRITICAL 詳細清單
    errors = filter_by_level(entries, "ERROR")
    lines.append(f"\n[Errors] ERROR+ Entries ({len(errors)} total):")
    for e in errors[:30]:
        ts = e["timestamp"] or "N/A"
        lines.append(f"  Line {e['lineno']:>5} | {ts} | {e['level']:<8} | {e['message'][:120]}")
    if len(errors) > 30:
        lines.append(f"  ... and {len(errors) - 30} more")

    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI 入口 / Entry Point
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI-Assisted Log Parser")
    parser.add_argument("--log_file", required=True, help="Path to log file")
    parser.add_argument(
        "--level",
        default="WARNING",
        choices=LOG_LEVEL_ORDER,
        help="Minimum log level to include in report",
    )
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=DEFAULT_KEYWORDS,
        help="Keywords to flag in alerts",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Save report to file (default: print to stdout)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    all_entries = parse_log_file(args.log_file)
    report = build_report(all_entries, args.keywords)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"[INFO] Report saved to: {args.output}")
    else:
        print(report)
