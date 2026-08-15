# Roblox Limited Item Monitor

A lightweight, automated Python service designed to track resale prices of Roblox Limited items, evaluate discount thresholds against Rolimon's Recent Average Price (RAP), and dispatch instant notifications via Discord webhooks and optional desktop alerts.

---

## Zero Host Dependencies (Container-First)

This project is built container-first. You do **not** need Python, `pip`, or any Python libraries installed on your host computer. When running with Docker or Docker Compose:
- Docker automatically downloads Python (`python:3.11-slim`) inside the container.
- Docker executes `pip install -r requirements.txt` internally during the image build process.
- The application runs completely isolated inside the Docker container.

The only software required on your computer is Docker (or Docker Desktop).

---

## Key Features

- Automated Resale Price Monitoring: Polls the Roblox Economy API at configurable intervals.
- Rolimon's RAP Integration: Fetches real-time Recent Average Price (RAP) metrics for accurate valuation.
- Discord Webhook Alerts: Sends rich embeds containing item thumbnails, current resale price, original price, RAP, discount percentage, and catalog links.
- Environment Variable & JSON Configuration: Supports 12-Factor application principles for seamless containerized deployments.
- Docker & Docker Compose Support: Package-ready container deployment with a non-root security context.
- Cross-Platform Compatibility: Graceful degradation of platform-specific features (such as Windows desktop notifications) when deployed on Linux or headless servers.

---

## Architecture Overview

```
+--------------------------+       +-------------------------+
|   Roblox Economy API     |       |   Rolimon's Item API    |
| (Resale Lowest Price)    |       |       (RAP Value)       |
+------------+-------------+       +------------+------------+
             |                                  |
             +----------------+-----------------+
                              |
                              v
             +----------------------------------+
             |   Roblox Limited Monitor Service |
             +----------------+-----------------+
                              |
                              v
             +----------------------------------+
             |     Discord Webhook Dispatch     |
             +----------------------------------+
```

---

## Configuration

The application can be configured using `config.json` or by setting environment variables. Environment variables take precedence over settings in `config.json`.

### Configuration Schema (`config.json`)

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

### Environment Variables

| Variable | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| `DISCORD_WEBHOOK_URL` | String | Discord Webhook endpoint URL | None |
| `ITEM_ID` | Integer | Roblox Asset ID of the limited item | `1016143686` |
| `CHECK_INTERVAL` | Integer | Polling interval in seconds (minimum 60s recommended) | `65` |
| `DISCOUNT_PERCENT` | Float | Minimum discount percentage required to trigger alert | `10.0` |
| `DISCORD_NOTIFICATIONS` | Boolean | Enable or disable Discord webhook dispatch (`true`/`false`) | `true` |
| `WINDOWS_NOTIFICATIONS` | Boolean | Enable desktop toast notifications on Windows (`true`/`false`) | `false` |
| `OPEN_BROWSER` | Boolean | Automatically open catalog link in default browser (`true`/`false`) | `false` |
| `PLAY_SOUND` | Boolean | Play sound alert on deal detection (`true`/`false`) | `false` |

---

## Deployment & Setup

### Option 1: Running with Docker Compose (Recommended)

No local Python installation required.

1. Clone the repository:

   ```bash
   git clone https://github.com/fordimalanda/roblox-limited-sniper.git
   cd roblox-limited-sniper
   ```

2. Edit `config.json` or set environment variables in your environment.

3. Launch the container service:

   ```bash
   docker compose up -d --build
   ```

4. View service logs:

   ```bash
   docker compose logs -f
   ```

5. Stop the container:

   ```bash
   docker compose down
   ```

---

### Option 2: Running with Docker CLI

No local Python installation required.

1. Build the Docker image (Docker installs Python and pip packages inside the image):

   ```bash
   docker build -t roblox-limited-monitor .
   ```

2. Run the container:

   ```bash
   docker run -d \
     --name roblox-monitor \
     --restart unless-stopped \
     -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..." \
     -e ITEM_ID=1016143686 \
     -e DISCOUNT_PERCENT=10 \
     roblox-limited-monitor
   ```

---

### Option 3: Manual Local Setup (Optional for Python developers)

If you prefer running directly on your host machine without Docker:

#### Prerequisites

- Python 3.10 or higher installed locally

#### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/fordimalanda/roblox-limited-sniper.git
   cd roblox-limited-sniper
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/macOS
   # .venv\Scripts\activate     # On Windows
   ```

3. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute the monitoring script:

   ```bash
   python main.py
   ```

---

## API Endpoints Used

### 1. Roblox Economy API
- Purpose: Retrieves asset metadata and lowest resale price.
- Endpoint: `https://economy.roblox.com/v2/assets/{item_id}/details`

### 2. Rolimon's Item Details API
- Purpose: Obtains item Recent Average Price (RAP) metrics.
- Endpoint: `https://api.rolimons.com/items/v2/itemdetails`

---

## Rate Limiting & Operational Best Practices

- Recommended Polling Interval: Keep `CHECK_INTERVAL` at 60 seconds or higher to avoid triggering HTTP 429 Rate Limit responses from Roblox endpoints.
- Webhook Privacy: Never expose or commit Discord Webhook URLs publicly in source control. Use environment variables for production environments.

---

## Project File Structure

```
roblox-limited-sniper/
├── .dockerignore
├── config.json
├── Dockerfile
├── docker-compose.yml
├── main.py
├── README.md
└── requirements.txt
```

---

## License

This project is open-source software licensed under the [MIT License](LICENSE).
