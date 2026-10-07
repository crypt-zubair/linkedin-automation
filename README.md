# LinkedIn Tech Fact Autopilot

A 30-day, zero-touch LinkedIn technology-fact posting system.

## What it does
Each scheduled run selects one unused fact, asks a local Ollama model to rewrite only that fact, runs deterministic checks plus a strict AI fact-fidelity check, stores the result in SQLite, and publishes through LinkedIn's official Posts API when live mode is enabled.

The AI is the writer, not the source of truth. Facts live in data/facts.json.

## Project structure
- app/config.py - environment and paths
- app/database.py - SQLite history and duplicate protection
- app/selector.py - unused fact selection
- app/generator.py - local Ollama generation
- app/checker.py - quality and factual-consistency gate
- app/linkedin.py - LinkedIn Posts API publisher
- app/main.py - complete daily workflow
- data/facts.json - 30 fact records
- scripts/setup.ps1 - Windows environment setup
- scripts/run_daily.ps1 - scheduled runner
- scripts/install_task.ps1 - Windows Task Scheduler installer
- tests/test_core.py - basic regression tests

## Setup
1. Install Python 3.13+ and Ollama.
2. Run PowerShell script: powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
3. Pull the model: ollama pull llama3.2
4. Copy .env.example to .env.
5. Keep TEST_MODE=true during testing.

## Dry run
Run:
python -m unittest discover -s tests -v
python -m app.main

The dry run saves a TEST_SAVED record and does not publish to LinkedIn.

The factual checker is fail-closed: if its AI comparison cannot run, the candidate is rejected instead of being published.

## LinkedIn setup
Create/configure a LinkedIn developer application and obtain member-posting permission. Put the access token in LINKEDIN_ACCESS_TOKEN and the member URN in LINKEDIN_PERSON_URN inside the local .env file.

The Posts API uses the REST posts endpoint, X-Restli-Protocol-Version 2.0.0, and a LinkedIn-Version header. The configured version is 202609 and can be changed through .env.

Never commit .env, tokens, or client secrets.

## Go live
After the dry run is correct, change TEST_MODE=false and run:
python -m app.main

Only after that succeeds should you install the daily task:
powershell -ExecutionPolicy Bypass -File .\scripts\install_task.ps1

The default schedule is 9:00 AM every day. The task is configured to start when available, allow battery operation, and retry failed runs.

MAX_POSTS=30 stops the system after 30 successful saved or published posts.

## Duplicate protection
SQLite records the fact ID after a successful dry-run save or live publish. The selector ignores used IDs, so the same fact is not selected again.

## Failure behavior
Ollama and LinkedIn errors are logged to logs/autopilot.log. A failed live publish is not marked as successfully used.

## Token note
LinkedIn member access tokens have finite lifetimes. Programmatic refresh tokens are available only for approved LinkedIn programs, so this project does not pretend every developer app can silently refresh forever. For a 30-day test, a normal valid member access token is sufficient if it remains valid for the test period.

## Security
Never commit client secrets, access tokens, refresh tokens, .env files, data/token.json, or the SQLite database.
