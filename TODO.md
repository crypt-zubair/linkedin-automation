# Project checklist

## Built
- [x] Verified fact database
- [x] Unused-fact selector
- [x] Local Ollama post generation
- [x] Multiple writing styles
- [x] Basic quality checker
- [x] SQLite history
- [x] LinkedIn Posts API adapter
- [x] Windows Task Scheduler scripts
- [x] Basic tests

## Before live publishing
- [ ] Install Ollama and pull the selected model
- [ ] Create/configure LinkedIn developer app
- [ ] Ensure the app has the required member-posting permission
- [ ] Put the LinkedIn access token and person URN into local .env
- [ ] Keep TEST_MODE=true for the first dry run
- [ ] Run the tests
- [ ] Run a dry run and inspect the generated post
- [ ] Change TEST_MODE=false only after the dry run is correct
- [ ] Install the daily Windows Task Scheduler job

## Safety
- Never commit .env, tokens, refresh tokens, or client secrets.
- The model rewrites supplied facts; it is not the source of truth.
- Successful fact IDs are never reused.
