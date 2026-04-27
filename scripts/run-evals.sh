#!/usr/bin/env bash
set -euo pipefail

EVAL_NAME="${EVAL_NAME:-all}"
MODEL="${MODEL:-llama3.2}"
MIN_PASS_RATE="${MIN_PASS_RATE:-0.80}"

EVALS_JSON="minottobot/evals/evals.json"
SKILL_MD="minottobot/SKILL.md"
OLLAMA_URL="http://localhost:11434/api/generate"

# Determine next iteration number
LATEST_N=0
if ls -d minottobot-workspace/iteration-* 2>/dev/null | grep -q .; then
  LATEST_N=$(ls -d minottobot-workspace/iteration-* | sort -V | tail -1 | grep -oE '[0-9]+$')
fi
NEXT_N=$((LATEST_N + 1))
ITERATION="iteration-${NEXT_N}"
WORKSPACE="minottobot-workspace/${ITERATION}"
mkdir -p "$WORKSPACE"

# Persist iteration name for downstream steps
echo "$ITERATION" > /tmp/eval_iteration_name

echo "==> Eval run: ${ITERATION} | model: ${MODEL} | filter: ${EVAL_NAME}"

# Select evals to run
if [[ "$EVAL_NAME" == "all" ]]; then
  EVALS=$(jq -c '.evals[]' "$EVALS_JSON")
else
  EVALS=$(jq -c --arg name "$EVAL_NAME" '.evals[] | select(.name == $name)' "$EVALS_JSON")
  if [[ -z "$EVALS" ]]; then
    echo "ERROR: eval '${EVAL_NAME}' not found in ${EVALS_JSON}"
    exit 1
  fi
fi

SYSTEM_PROMPT=$(cat "$SKILL_MD")
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

ollama_generate() {
  local system="$1" prompt="$2" use_json="${3:-false}"
  local payload
  if [[ "$use_json" == "true" ]]; then
    payload=$(jq -n \
      --arg model "$MODEL" \
      --arg system "$system" \
      --arg prompt "$prompt" \
      '{model: $model, system: $system, prompt: $prompt, stream: false, format: "json"}')
  else
    payload=$(jq -n \
      --arg model "$MODEL" \
      --arg system "$system" \
      --arg prompt "$prompt" \
      '{model: $model, system: $system, prompt: $prompt, stream: false}')
  fi
  curl -sf "$OLLAMA_URL" -H 'Content-Type: application/json' -d "$payload" | jq -r '.response // empty'
}

TOTAL_PASS=0
TOTAL_ASSERTIONS=0
TOTAL_DURATION_MS=0
EVAL_COUNT=0

while IFS= read -r eval_entry; do
  EVAL_NAME_ENTRY=$(echo "$eval_entry" | jq -r '.name')
  PROMPT=$(echo "$eval_entry" | jq -r '.prompt')
  ASSERTIONS_JSON=$(echo "$eval_entry" | jq '.assertions')

  EVAL_DIR="${WORKSPACE}/eval-${EVAL_NAME_ENTRY}/with_skill"
  mkdir -p "$EVAL_DIR"

  echo "--> ${EVAL_NAME_ENTRY}"

  START_MS=$(($(date +%s%N) / 1000000))

  OUTPUT=$(ollama_generate "$SYSTEM_PROMPT" "$PROMPT" false) || true
  echo "$OUTPUT" > "${EVAL_DIR}/output.md"
  RUN_EXIT=$([ -n "$OUTPUT" ] && echo 0 || echo 1)

  ASSERTIONS_NUMBERED=$(echo "$ASSERTIONS_JSON" | jq -r 'to_entries[] | "\(.key+1). \(.value)"')
  GRADE_SYSTEM="You are a strict evaluator. Evaluate assertions against an audit report. Respond with valid JSON only, no markdown."
  GRADE_PROMPT="Audit output:
---
${OUTPUT}
---

Evaluate each assertion. Respond with this JSON structure only:
{\"assertions\": [{\"assertion\": \"...\", \"pass\": true, \"evidence\": \"direct quote from output\"}], \"summary\": \"...\"}

Assertions:
${ASSERTIONS_NUMBERED}"

  GRADE_RAW=$(ollama_generate "$GRADE_SYSTEM" "$GRADE_PROMPT" true) || true
  GRADE_EXIT=0

  if echo "$GRADE_RAW" | jq -e '.assertions' > /dev/null 2>&1; then
    echo "$GRADE_RAW" > "${EVAL_DIR}/grading.json"
    PASS_COUNT=$(echo "$GRADE_RAW" | jq '[.assertions[] | select(.pass == true)] | length')
    ASSERTION_COUNT=$(echo "$GRADE_RAW" | jq '.assertions | length')
    SUMMARY=$(echo "$GRADE_RAW" | jq -r '.summary // ""')
  else
    GRADE_EXIT=1
    ASSERTION_COUNT=$(echo "$ASSERTIONS_JSON" | jq 'length')
    PASS_COUNT=0
    SUMMARY="Grading parse error: model did not return valid JSON"
    jq -n \
      --argjson assertions "$ASSERTIONS_JSON" \
      --arg summary "$SUMMARY" \
      '{assertions: [$assertions[] | {assertion: ., pass: false, evidence: "grading error"}], summary: $summary}' \
      > "${EVAL_DIR}/grading.json"
  fi

  END_MS=$(($(date +%s%N) / 1000000))
  DURATION_MS=$((END_MS - START_MS))

  jq -n \
    --argjson duration "$DURATION_MS" \
    --argjson run_exit "$RUN_EXIT" \
    --argjson grade_exit "$GRADE_EXIT" \
    '{duration_ms: $duration, run_exit_code: $run_exit, grade_exit_code: $grade_exit}' \
    > "${EVAL_DIR}/timing.json"

  PASS_RATE=$(jq -n --argjson p "$PASS_COUNT" --argjson t "$ASSERTION_COUNT" '$p / $t')
  echo "    ${PASS_COUNT}/${ASSERTION_COUNT} passed (pass_rate: ${PASS_RATE})"

  jq -n \
    --arg name "$EVAL_NAME_ENTRY" \
    --argjson pass_count "$PASS_COUNT" \
    --argjson total "$ASSERTION_COUNT" \
    --argjson pass_rate "$PASS_RATE" \
    --argjson duration "$DURATION_MS" \
    --argjson run_exit "$RUN_EXIT" \
    --argjson grade_exit "$GRADE_EXIT" \
    --arg summary "$SUMMARY" \
    '{name: $name, with_skill: {pass_count: $pass_count, total: $total, pass_rate: $pass_rate, duration_ms: $duration, run_exit_code: $run_exit, grade_exit_code: $grade_exit, summary: $summary}}' \
    > "${TEMP_DIR}/${EVAL_NAME_ENTRY}.json"

  TOTAL_PASS=$((TOTAL_PASS + PASS_COUNT))
  TOTAL_ASSERTIONS=$((TOTAL_ASSERTIONS + ASSERTION_COUNT))
  TOTAL_DURATION_MS=$((TOTAL_DURATION_MS + DURATION_MS))
  EVAL_COUNT=$((EVAL_COUNT + 1))

done <<< "$EVALS"

PER_EVAL=$(find "$TEMP_DIR" -name '*.json' | sort | xargs jq -s '.')
MEAN_PASS_RATE=$(jq -n --argjson p "$TOTAL_PASS" --argjson t "$TOTAL_ASSERTIONS" '$p / $t')
MEAN_DURATION=$(jq -n --argjson d "$TOTAL_DURATION_MS" --argjson c "$EVAL_COUNT" '$d / $c')

jq -n \
  --arg iteration "$ITERATION" \
  --arg generated_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg model "$MODEL" \
  --argjson per_eval "$PER_EVAL" \
  --argjson mean_pass_rate "$MEAN_PASS_RATE" \
  --argjson total_pass "$TOTAL_PASS" \
  --argjson total_assertions "$TOTAL_ASSERTIONS" \
  --argjson mean_duration "$MEAN_DURATION" \
  '{
    iteration: $iteration,
    generated_at: $generated_at,
    model: $model,
    mode: "with_skill",
    per_eval: $per_eval,
    aggregates: {
      with_skill: {
        mean_pass_rate: $mean_pass_rate,
        total_assertions_passed: $total_pass,
        total_assertions: $total_assertions,
        mean_duration_ms: $mean_duration
      }
    }
  }' > "${WORKSPACE}/benchmark.json"

echo "==> benchmark.json: ${TOTAL_PASS}/${TOTAL_ASSERTIONS} passed (mean_pass_rate: ${MEAN_PASS_RATE})"

if ! jq -n --argjson r "$MEAN_PASS_RATE" --argjson t "$MIN_PASS_RATE" '$r >= $t' | grep -q true; then
  echo "ERROR: mean_pass_rate ${MEAN_PASS_RATE} < threshold ${MIN_PASS_RATE}"
  exit 1
fi

echo "==> Done. Results: ${WORKSPACE}"
