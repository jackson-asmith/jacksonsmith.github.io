#!/usr/bin/env bash
# Validates a security.txt file (RFC 9116) from a URL or a local path.
#
# Usage: check-security-txt.sh <url-or-path> [warn-days]
#
# Exit codes:
#   0  valid, and Expires is more than warn-days away
#   1  invalid, expired, or expiring within warn-days
#   2  couldn't fetch the file (unknown, not invalid)
set -euo pipefail

SOURCE="${1:?usage: check-security-txt.sh <url-or-path> [warn-days]}"
WARN_DAYS="${2:-60}"
SUMMARY="${GITHUB_STEP_SUMMARY:-/dev/null}"

fail() { echo "::error::$1"; echo "- ❌ $1" >> "$SUMMARY"; FAILED=true; }
warn() { echo "::warning::$1"; echo "- ⚠️ $1" >> "$SUMMARY"; }
ok()   { echo "✓ $1"; echo "- ✅ $1" >> "$SUMMARY"; }

FAILED=false
{
  echo "## security.txt check"
  echo "Source: \`$SOURCE\`"
  echo ""
} >> "$SUMMARY"

# Fetch. A network failure means "couldn't check", which is not the same
# as "the file is broken", so it gets its own exit code.
if [[ "$SOURCE" =~ ^https?:// ]]; then
  HEADERS=$(mktemp)
  if ! BODY=$(curl -fsS --retry 3 --retry-all-errors --max-time 15 -D "$HEADERS" "$SOURCE"); then
    STATUS=$(grep -E '^HTTP/' "$HEADERS" 2>/dev/null | tail -1 | tr -d '\r' || true)
    # 404/410 is an answer: the file is gone. Anything else (403, 5xx,
    # timeouts) means we couldn't find out.
    if [[ "$STATUS" =~ ^HTTP/[0-9.]+\ (404|410) ]]; then
      echo "::error::$SOURCE returned ${STATUS#HTTP/* }. The file is missing from the live site."
      echo "- ❌ The file is missing ($STATUS)" >> "$SUMMARY"
      exit 1
    fi
    echo "::error::Couldn't fetch $SOURCE (${STATUS:-no response}). The file's status is unknown, not necessarily broken."
    echo "- ❓ Couldn't fetch the file (${STATUS:-no response})" >> "$SUMMARY"
    exit 2
  fi
  CONTENT_TYPE=$(grep -i '^content-type:' "$HEADERS" | tail -1 | tr -d '\r' | cut -d' ' -f2- || true)
  if [[ "$CONTENT_TYPE" =~ ^text/plain ]]; then
    ok "Served as $CONTENT_TYPE"
  else
    fail "Served as '${CONTENT_TYPE:-unknown}'; RFC 9116 requires text/plain"
  fi
else
  BODY=$(cat "$SOURCE")
fi

# Field names are case-insensitive (RFC 9116, section 2.4).
field() { grep -iE "^$1:" <<< "$BODY" | sed -E "s/^[^:]+:[[:space:]]*//" | tr -d '\r' || true; }

CONTACTS=$(field Contact)
if [[ -n "$CONTACTS" ]]; then
  ok "Contact: $(head -1 <<< "$CONTACTS")"
else
  fail "Missing required Contact field"
fi

EXPIRES=$(field Expires)
EXPIRES_COUNT=$(grep -c . <<< "$EXPIRES" || true)
if [[ "$EXPIRES_COUNT" -eq 0 ]]; then
  fail "Missing required Expires field"
elif [[ "$EXPIRES_COUNT" -gt 1 ]]; then
  fail "Expires appears $EXPIRES_COUNT times; it must appear exactly once"
elif ! EXPIRES_EPOCH=$(date -u -d "$EXPIRES" +%s 2>/dev/null); then
  fail "Expires value '$EXPIRES' is not a valid date"
else
  DAYS_LEFT=$(( (EXPIRES_EPOCH - $(date -u +%s)) / 86400 ))
  if (( DAYS_LEFT < 0 )); then
    fail "Expired $(( -DAYS_LEFT )) days ago ($EXPIRES). An expired security.txt is invalid"
  elif (( DAYS_LEFT < WARN_DAYS )); then
    fail "Expires in $DAYS_LEFT days ($EXPIRES). Renew it to about 11 months out"
  else
    ok "Expires in $DAYS_LEFT days ($EXPIRES)"
    if (( DAYS_LEFT > 366 )); then
      warn "Expires is more than a year out; RFC 9116 recommends less than a year"
    fi
  fi
fi

echo "" >> "$SUMMARY"
if [[ "$FAILED" == "true" ]]; then
  exit 1
fi
