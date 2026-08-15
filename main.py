#!/usr/bin/env python3
"""
Roblox Limited Items Price Monitor
Tracks Roblox limited item resale prices, checks discounts against Rolimon's RAP,
and notifies users via Discord webhooks, desktop toasts, and sound alerts.
"""

import json
import os
import sys
import time
import signal
import logging
import webbrowser
from datetime import datetime
from typing import Optional, Dict, Any

import requests

# Optional platform-specific imports
try:
    from win11toast import toast
except Exception:
    toast = None

try:
    import winsound
except Exception:
    winsound = None


# Terminal ANSI Color Codes
class Colors:
    GREEN = "\033[38;5;46m"
    YELLOW = "\033[38;5;220m"
    BLUE = "\033[38;5;39m"
    RED = "\033[38;5;196m"
    CYAN = "\033[38;5;51m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("RobloxMonitor")


def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from JSON file with Environment Variable overrides."""
    config: Dict[str, Any] = {
        "webhook_url": "YOUR_DISCORD_WEBHOOK",
        "check_interval": 65,
        "item_id": 1016143686,
        "discount_percent": 10.0,
        "open_browser": False,
        "discord_notifications": True,
        "windows_notifications": False,
        "play_sound": False
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            logger.warning(f"Could not read {config_path}: {e}")

    # Environment variable overrides (useful for Docker containerization)
    if os.getenv("DISCORD_WEBHOOK_URL"):
        config["webhook_url"] = os.getenv("DISCORD_WEBHOOK_URL")
    elif os.getenv("WEBHOOK_URL"):
        config["webhook_url"] = os.getenv("WEBHOOK_URL")

    if os.getenv("ITEM_ID"):
        try:
            config["item_id"] = int(os.getenv("ITEM_ID"))
        except ValueError:
            pass

    if os.getenv("CHECK_INTERVAL"):
        try:
            config["check_interval"] = int(os.getenv("CHECK_INTERVAL"))
        except ValueError:
            pass

    if os.getenv("DISCOUNT_PERCENT"):
        try:
            config["discount_percent"] = float(os.getenv("DISCOUNT_PERCENT"))
        except ValueError:
            pass

    if os.getenv("OPEN_BROWSER") is not None:
        config["open_browser"] = os.getenv("OPEN_BROWSER").lower() in ("true", "1", "yes")

    if os.getenv("DISCORD_NOTIFICATIONS") is not None:
        config["discord_notifications"] = os.getenv("DISCORD_NOTIFICATIONS").lower() in ("true", "1", "yes")

    if os.getenv("WINDOWS_NOTIFICATIONS") is not None:
        config["windows_notifications"] = os.getenv("WINDOWS_NOTIFICATIONS").lower() in ("true", "1", "yes")

    if os.getenv("PLAY_SOUND") is not None:
        config["play_sound"] = os.getenv("PLAY_SOUND").lower() in ("true", "1", "yes")

    return config


def get_rolimons_rap(item_id: int) -> Optional[int]:
    """Fetch Recent Average Price (RAP) for an item from Rolimon's API."""
    url = "https://api.rolimons.com/items/v2/itemdetails"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        item_data = data.get("items", {}).get(str(item_id))
        if item_data and len(item_data) > 2:
            return item_data[2]
    except Exception as e:
        logger.warning(f"Failed to fetch RAP from Rolimon's API: {e}")
    return None


def get_roblox_item_details(item_id: int) -> Dict[str, Any]:
    """Fetch item details from Roblox Economy API."""
    url = f"https://economy.roblox.com/v2/assets/{item_id}/details"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def send_discord_webhook(
    webhook_url: str,
    item_name: str,
    item_id: int,
    current_price: int,
    original_price: int,
    discount: float,
    rap: Optional[int]
) -> bool:
    """Send alert notification embed to Discord webhook."""
    if not webhook_url or webhook_url == "YOUR_DISCORD_WEBHOOK":
        return False

    embed = {
        "title": "Roblox Deal Found!",
        "description": f"**{item_name}**",
        "color": 65280,  # Green (#00FF00)
        "fields": [
            {
                "name": "Current Price",
                "value": f"{current_price:,} Robux",
                "inline": True
            },
            {
                "name": "Starting Price",
                "value": f"{original_price:,} Robux",
                "inline": True
            },
            {
                "name": "RAP",
                "value": f"{rap:,} Robux" if rap is not None else "Unknown",
                "inline": True
            },
            {
                "name": "Discount",
                "value": f"{discount:.2f}%",
                "inline": True
            },
            {
                "name": "Item ID",
                "value": str(item_id),
                "inline": True
            }
        ],
        "thumbnail": {
            "url": f"https://tr.rbxcdn.com/{item_id}/420/420/Image/Png"
        },
        "url": f"https://www.roblox.com/catalog/{item_id}",
        "footer": {
            "text": "Roblox Limited Monitor"
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        response = requests.post(
            webhook_url,
            json={"username": "Limited Monitor", "embeds": [embed]},
            timeout=10
        )
        if response.status_code == 204:
            return True
        logger.error(f"Discord Webhook returned status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Error sending Discord notification: {e}")
    return False


def send_windows_notification(item_name: str, current_price: int, discount: float) -> None:
    """Send Windows desktop notification toast if supported."""
    if toast is None:
        return
    try:
        toast(
            "Roblox Deal Found!",
            f"{item_name}\n{current_price:,} Robux\n{discount:.2f}% OFF",
            duration="long"
        )
    except Exception as e:
        logger.debug(f"Desktop notification failed: {e}")


def play_sound_alert() -> None:
    """Play alert sound on supported platforms."""
    if winsound is None:
        return
    try:
        winsound.Beep(1500, 700)
        winsound.MessageBeep()
    except Exception as e:
        logger.debug(f"Audio playback failed: {e}")


def open_catalog_browser(item_id: int) -> None:
    """Open Roblox catalog page in system default browser."""
    try:
        webbrowser.open(f"https://www.roblox.com/catalog/{item_id}")
    except Exception as e:
        logger.debug(f"Failed to open browser: {e}")


def monitor_loop(config: Dict[str, Any]) -> None:
    """Main execution loop for monitoring Roblox limited item prices."""
    webhook_url = config.get("webhook_url", "")
    item_id = int(config["item_id"])
    discount_percent = float(config["discount_percent"])
    check_interval = int(config["check_interval"])

    if webhook_url == "YOUR_DISCORD_WEBHOOK" and config.get("discord_notifications", True):
        logger.warning("Discord webhook URL is set to default. Update config.json or set WEBHOOK_URL environment variable.")

    logger.info("Initializing item details...")

    try:
        data = get_roblox_item_details(item_id)
    except Exception as e:
        logger.error(f"Failed to fetch initial item data for ID {item_id}: {e}")
        sys.exit(1)

    item_name = data.get("Name", f"Item #{item_id}")
    collectibles = data.get("CollectiblesItemDetails") or {}
    original_price = collectibles.get("CollectibleLowestResalePrice")

    if original_price is None:
        logger.error(f"No resale price available for item '{item_name}' (ID: {item_id}).")
        sys.exit(1)

    rap = get_rolimons_rap(item_id)
    alert_price = int(original_price * (1 - discount_percent / 100))

    print("\n" + "=" * 50)
    print(f"{Colors.GREEN}{Colors.BOLD}Monitoring Item:{Colors.RESET} {item_name}")
    print(f"{Colors.YELLOW}Starting Price:{Colors.RESET} {original_price:,} Robux")
    print(f"{Colors.YELLOW}Required Discount:{Colors.RESET} {discount_percent:.1f}%")
    print(f"{Colors.YELLOW}Target Alert Price:{Colors.RESET} {alert_price:,} Robux")
    if rap:
        print(f"{Colors.YELLOW}Rolimon's RAP:{Colors.RESET} {rap:,} Robux")
    else:
        print(f"{Colors.YELLOW}Rolimon's RAP:{Colors.RESET} Unknown")
    print("=" * 50 + "\n")

    last_alert_price: Optional[int] = None

    while True:
        try:
            now = datetime.now().strftime("%H:%M:%S")
            data = get_roblox_item_details(item_id)
            collectibles = data.get("CollectiblesItemDetails") or {}
            current_price = collectibles.get("CollectibleLowestResalePrice")

            if current_price is None:
                print(f"{Colors.YELLOW}[{now}] No active resale listings found.{Colors.RESET}")
                time.sleep(check_interval)
                continue

            discount = ((original_price - current_price) / original_price) * 100.0

            if discount >= discount_percent and current_price != last_alert_price:
                print(
                    f"{Colors.GREEN}[{now}] DEAL DETECTED! "
                    f"{item_name} at {current_price:,} Robux "
                    f"({discount:.2f}% OFF){Colors.RESET}"
                )

                if config.get("discord_notifications", True):
                    send_discord_webhook(
                        webhook_url, item_name, item_id,
                        current_price, original_price, discount, rap
                    )

                if config.get("windows_notifications", False):
                    send_windows_notification(item_name, current_price, discount)

                if config.get("open_browser", False):
                    open_catalog_browser(item_id)

                if config.get("play_sound", False):
                    play_sound_alert()

                last_alert_price = current_price
            else:
                print(
                    f"{Colors.BLUE}[{now}] {item_name} | "
                    f"Current: {current_price:,} Robux | "
                    f"Discount: {discount:.2f}%{Colors.RESET}"
                )

        except requests.RequestException as e:
            print(f"{Colors.RED}[Error] Network error while polling Roblox API: {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[Error] Unexpected exception: {e}{Colors.RESET}")

        time.sleep(check_interval)


def handle_shutdown(signum, frame):
    """Graceful termination handler for Docker/signals."""
    print(f"\n{Colors.YELLOW}Shutting down Roblox Limited Monitor...{Colors.RESET}")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    config = load_config()
    monitor_loop(config)


if __name__ == "__main__":
    main()
