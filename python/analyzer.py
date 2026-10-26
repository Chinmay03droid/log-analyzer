#!/usr/bin/env python3

import os
import sys
import json


def read_logs(filepath):
  with open(filepath, "r") as file:
    return file.readlines()


def analyze_logs(lines):
  counts = {"INFO": 0, "WARN": 0, "ERROR": 0}

  for line in lines:
    for level in counts:
      if level in line:
        counts[level] += 1

  return counts

def generate_report(counts, filter_level=None,json_output=False):
  total = sum(counts.values())

  if filter_level and filter_level not in counts:
    error = {"error": f"Invalid log level: {filter_level}"}
    print(json.dumps(error) if json_output else error["error"])
    return

  if json_output:
    if filter_level:
      payload = {
        filter_level: counts[filter_level],
        "total": total
      }
    else:
      payload = {
          **counts,
          "total": total
      }
    print(json.dumps(payload))
    return

  print("Log Analysis Summary")
  print("---------------------")

  if total == 0:
    print("No log entries found.")
    return

  if filter_level:
    count = counts[filter_level]
    percent = (count / total) * 100
    print(f"{filter_level}: {count} ({percent:.1f}%)")
    return

  for level, count in counts.items():
    percent = (count / total) * 100
    print(f"{level}: {count} ({percent:.1f}%)")


args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
flags = [arg for arg in sys.argv[1:] if arg.startswith("--")]

if "--help" in flags:
    print ("""
Log Analyzer CLI
Usage:
  python3 analyzer.py <logfile> [LEVEL] [--json]

Arguments:
  logfile     Path to the log file
  LEVEL       Optional filter: INFO, WARN, or ERROR

Options:
  --json      Output results in JSON format
  --help      Display this help message
""")
    sys.exit(0)

LOG_FILE = args[0] if len(args) > 0 else "system.log"
CLI_FILTER = args[1].upper() if len(args) > 1 else None

ENV_LOG_LEVEL = os.getenv("LOG_LEVEL")
ENV_FILTER = ENV_LOG_LEVEL.upper() if ENV_LOG_LEVEL else None

FILTER_LEVEL = CLI_FILTER if CLI_FILTER else ENV_FILTER
JSON_OUTPUT = "--json" in flags

if not os.path.exists(LOG_FILE):
  print(f"Error: {LOG_FILE} does not exist.")
  sys.exit(1)

lines = read_logs(LOG_FILE)
counts = analyze_logs(lines)

generate_report(counts, FILTER_LEVEL,JSON_OUTPUT)
sys.exit(2 if counts["ERROR"] > 0 else 0)
