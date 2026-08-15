# Roblox Limited Monitor

[![CI & Docker Build Check](https://github.com/fordimalanda/roblox-limited-sniper/actions/workflows/ci.yml/badge.svg)](https://github.com/fordimalanda/roblox-limited-sniper/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, lightweight monitoring daemon built in Python for real-time tracking of Roblox Limited item resale prices. The service evaluates resale listings against Rolimon's Recent Average Price (RAP) metrics and dispatches instant structured telemetry alerts via Discord Webhooks, desktop toasts, and audio cues.

---

## Executive Overview

Roblox Limited Monitor provides automated valuation tracking and arbitrage detection for collectible items on the Roblox Marketplace. Designed adhering to 12-Factor App methodology, it runs out of the box as a zero-host-dependency containerized microservice or as a standalone CLI daemon.

### Key Architectural Capabilities

- **Automated Price Telemetry**: Continuously monitors lowest resale prices via official Roblox Economy endpoints.
- **RAP Market Valuation**: Integrates Rolimon's Market API to correlate resale asking prices against market-verified Recent Average Price (RAP) data.
- **Multi-Channel Dispatch Engine**: Emits rich Discord embeds with high-resolution thumbnails, precise price deltas, percentage discounts, and deep links.
- **Zero-Host Container Deployment**: Fully containerized with Python 3.11-slim, pre-packaged dependencies, non-root execution (`appuser`), and multi-stage build optimization.
- **Dynamic Configuration Layer**: Accepts configuration via standard JSON descriptors or environment variable overrides for Kubernetes and Docker Compose orchestrations.
- **Fault-Tolerant Platform Abstraction**: Features graceful degradation for platform-specific capabilities (Windows toast notifications, audio playback, browser opening) when executing in headless Linux container environments.

---

## System Architecture

```
+---------------------------+       +----------------------------+
|    Roblox Economy API     |       |    Rolimon's Item API      |
|  (Catalog Resale Engine)  |       |     (RAP Data Aggregator)  |
+-------------+-------------+       +-------------+--------------+
              |                                   |
              +-----------------+-----------------+
                                |
                                v
             +------------------------------------+
             |   Roblox Limited Monitor Daemon    |
             |   (Threshold & Arbitrage Engine)   |
             +------------------+-----------------+
                                |
                                v
             +------------------------------------+
             |      Discord Webhook Dispatcher    |
             +------------------------------------+
```

---

## Configuration Reference

Configuration is evaluated hierarchically: **Environment Variables** take precedence over **`config.json`** values.

### Environment Variables & Parameter Matrix

| Setting Key | Environment Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `webhook_url` | `DISCORD_WEBHOOK_URL` | String | `""` | Target Discord Webhook URL for alerting |
| `item_id` | `ITEM_ID` | Integer | `1016143686` | Roblox Asset ID of the targeted limited item |
| `check_interval` | `CHECK_INTERVAL` | Integer | `65` | Polling frequency in seconds (minimum 60s recommended) |
| `discount_percent` | `DISCOUNT_PERCENT` | Float | `10.0` | Target discount threshold percentage required for alert |
| `discord_notifications` | `DISCORD_NOTIFICATIONS` | Boolean | `true` | Enable or disable Discord notification dispatches |
| `windows_notifications` | `WINDOWS_NOTIFICATIONS` | Boolean | `false` | Enable Windows native toast alerts (Windows host only) |
| `open_browser` | `OPEN_BROWSER` | Boolean | `false` | Auto-launch catalog link in default web browser upon deal |
| `play_sound` | `PLAY_SOUND` | Boolean | `false` | Trigger audio alert on deal detection (Windows host only) |

### Descriptor File Schema (`config.json`)

```json
{
  "webhook_url": "YOUR_DISCORD_WEBHOOK_URL",
  "check_interval": 65,
  "item_id": 1016143686,
  "discount_percent": 10.0,
  "open_browser": false,
  "discord_notifications": true,
  "windows_notifications": false,
  "play_sound": false
}
```

---

## Quick Start Guide

### Container Deployment (Docker Compose - Recommended)

No local Python installation is required. Docker automatically provisions Python, installs dependencies inside the isolated image layer, and executes the process under a non-root security context.

1. Fork and clone the repository:
   - Click the **Fork** button at the top right of this GitHub page to create a copy under your account.
   - Clone your personal fork (replace `YOUR_GITHUB_USERNAME` with your actual GitHub username):
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/roblox-limited-sniper.git
   cd roblox-limited-sniper
   ```

2. Provision configuration (via `config.json` or inline environment variables):
   ```bash
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your/webhook/url"
   ```

3. Launch daemon:
   ```bash
   docker compose up -d --build
   ```

4. Stream runtime logs:
   ```bash
   docker compose logs -f
   ```

5. Stop daemon:
   ```bash
   docker compose down
   ```

---

### Docker CLI Execution

```bash
docker run -d \
  --name roblox-limited-monitor \
  --restart unless-stopped \
  -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your/webhook/url" \
  -e ITEM_ID=1016143686 \
  -e DISCOUNT_PERCENT=10.0 \
  -e CHECK_INTERVAL=65 \
  roblox-limited-monitor:latest
```

---

## Standalone Host Execution (Developer Setup)

For environments running outside container orchestration:

### Requirements
- Python 3.10+
- `pip` package manager

### Setup Steps
```bash
# Initialize virtual environment
python -m venv .venv

# Activate environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
# .venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Run monitor
python main.py
```

---

## Continuous Integration & Quality Assurance

This repository includes a production GitHub Actions workflow (`.github/workflows/ci.yml`) enforcing:
- Python abstract syntax tree (AST) compilation validation.
- JSON configuration schema sanity checks.
- Isolated container image build verification via Docker Buildx.

---

## External Data Services

### 1. Roblox Economy v2 API
- **Endpoint**: `https://economy.roblox.com/v2/assets/{item_id}/details`
- **Purpose**: Fetches asset metadata, item title, and current lowest resale price (`CollectibleLowestResalePrice`).

### 2. Rolimon's Item Metrics API
- **Endpoint**: `https://api.rolimons.com/items/v2/itemdetails`
- **Purpose**: Retrieves current Recent Average Price (RAP) metrics to assess arbitrage value.

---

## Operational Safeguards & Security

- **Rate Limit Compliance**: Ensure `CHECK_INTERVAL` is maintained at `>= 60` seconds to mitigate HTTP `429 Too Many Requests` responses from upstream APIs.
- **Secret Isolation**: Webhook URLs must be managed via secret environment variables and never committed to source control.
- **Container Isolation**: The provided Dockerfile enforces process execution under unprivileged user `appuser` (UID 1000).

---

## Directory Topology

```
roblox-limited-sniper/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI workflow
├── .dockerignore           # Container build exclusion rules
├── config.json             # Service configuration descriptor
├── Dockerfile              # OCI container image definition
├── docker-compose.yml      # Multi-container orchestration specification
├── main.py                 # Core application entrypoint & monitoring logic
├── README.md               # Project documentation
└── requirements.txt        # Python dependency manifest
```

---

## License

Distributed under the MIT License. See `LICENSE` for full terms and conditions.
