#!/usr/bin/env bash
# Point git at the in-tree hooks directory so the repo-managed pre-commit
# hook runs on every commit. Idempotent — safe to re-run.

set -euo pipefail

cd "$(dirname "$0")/.."
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push

echo "git hooks now read from .githooks/ — pre-commit and pre-push are active."
