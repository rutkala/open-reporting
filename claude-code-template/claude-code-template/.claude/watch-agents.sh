#!/bin/bash
# Agent Activity Monitor (Terminal) — macOS/Linux version
tail -f "$(dirname "$0")/agent-activity.log"
