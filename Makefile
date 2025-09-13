# Makefile for Docker Compose workflow and Python dependencies

# Default target
.PHONY: all
all: build up

# Build Docker images
.PHONY: build
build:
	docker compose build

# Start containers in detached mode
.PHONY: upmake up

up:
	docker compose up -d

# Stop and remove containers, networks, volumes
.PHONY: down
down:
	docker compose down

# Start all stopped services
.PHONY: start
start:
	docker compose start

# Stop all running services
.PHONY: stop
stop:
	docker compose stop

# Start/Stop individual services
.PHONY: start-stt stop-stt
start-stt:
	docker compose start stt-server

stop-stt:
	docker compose stop stt-server

.PHONY: start-tts stop-tts
start-tts:
	docker compose start tts-server

stop-tts:
	docker compose stop tts-server

.PHONY: start-itt stop-itt
start-itt:
	docker compose start itt-server

stop-itt:
	docker compose stop itt-server

.PHONY: start-tti stop-tti
start-tti:
	docker compose start tti-server

stop-tti:
	docker compose stop tti-server

.PHONY: start-itv stop-itv
start-itv:
	docker compose start itv-server

stop-itv:
	docker compose stop itv-server

# Logs for specific services
.PHONY: logs-stt-f
logs-stt-f:
	clear && docker compose logs -f stt-server

.PHONY: logs-stt
logs-stt:
	clear && docker compose logs stt-server

.PHONY: logs-tts-f
logs-tts-f:
	clear && docker compose logs -f tts-server

.PHONY: logs-tts
logs-tts:
	clear && docker compose logs tts-server

.PHONY: logs-itt-f
logs-itt-f:
	clear && docker compose logs -f itt-server

.PHONY: logs-itt
logs-itt:
	clear && docker compose logs itt-server

.PHONY: logs-tti-f
logs-tti-f:
	clear && docker compose logs -f tti-server

.PHONY: logs-tti
logs-tti:
	clear && docker compose logs tti-server

.PHONY: logs-itv-f
logs-itv-f:
	clear && docker compose logs -f itv-server

.PHONY: logs-itv
logs-itv:
	clear && docker compose logs itv-server

.PHONY: logs-f
logs-f:
	clear && docker compose logs -f

.PHONY: logs
logs:
	clear && docker compose logs

# Dependency installation commands per server

.PHONY: deps-stt
deps-stt:
	@echo "Installing dependencies in Speech-to-Text-Server"
	@sh -c 'cd Speech-to-Text-Server && uv lock && uv sync --frozen --no-cache'

.PHONY: deps-tts
deps-tts:
	@echo "Installing dependencies in Text-to-Speech-Server"
	@sh -c 'cd Text-to-Speech-Server && uv lock && uv sync --frozen --no-cache'

.PHONY: deps-itt
deps-itt:
	@echo "Installing dependencies in Image-to-Text-Server"
	@sh -c 'cd Image-to-Text-Server && uv lock && uv sync --frozen --no-cache'

.PHONY: deps-tti
deps-tti:
	@echo "Installing dependencies in Text-to-Image-Server"
	@sh -c 'cd Text-to-Image-Server && uv lock && uv sync --frozen --no-cache'

.PHONY: deps-itv
deps-itv:
	@echo "Installing dependencies in Image-to-Video-Server"
	@sh -c 'cd Image-to-Video-Server && uv lock && uv sync --frozen --no-cache'

.PHONY: deps-all
deps-all: deps-stt deps-tts deps-itt deps-tti deps-itv
	@echo "✅ All dependencies installed."