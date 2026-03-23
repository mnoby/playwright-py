# ── Makefile ───────────────────────────────────────────────────────────────
.PHONY: build test-dev test-stg test-local-dev test-local-stg clean

# Build Docker image
build:
	docker compose build

# Run tests inside Docker ─────────────────────────────────────────────────

## Run full suite in dev
test-dev:
	docker compose run --rm playwright-dev

## Run full suite in staging
test-stg:
	docker compose run --rm playwright-stg

## Run only smoke tests in dev
smoke-dev:
	docker compose run --rm playwright-dev --env dev -m smoke

## Run only smoke tests in staging
smoke-stg:
	docker compose run --rm playwright-stg --env stg -m smoke

# Run tests locally (no Docker) ───────────────────────────────────────────

## Local dev run (loads .env.dev)
test-local-dev:
	set -a && . .env.dev && set +a && pytest --env dev

## Local staging run (loads .env.stg)
test-local-stg:
	set -a && . .env.stg && set +a && pytest --env stg

# Cleanup
clean:
	docker compose down --volumes --remove-orphans
	rm -rf reports/screenshots/* reports/videos/*