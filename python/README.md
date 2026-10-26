# Log Analyzer CLI Tool

A Python-based Linux command-line tool to analyze log files and summarize
INFO, WARN and ERROR messages. The tool is containerized with Docker, supports JSON output, and is designed for automation and cloud workflows.


## Features
- Analyze log files for INFO, WARN, and ERROR levels
- Percentage based summaries
- Filters by log level (e.g. ERROR, WARN, INFO)
- JSON output for automation and CI/CD
- Proper Unix exit codes
- Dockerized with non root users
- Runtime configuration via CLI args and environment variables
- Automation script with threshold-based logic

## Requirements
- Python 3.10+ (local run)
- Docker (recommended)
- 'jq' (for automation script)

## Usage

Analyze a log file:
```bash
./analyzer.py system.log
