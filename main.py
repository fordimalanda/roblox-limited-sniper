import requests
import time
from datetime import datetime
import json
import webbrowser
from win11toast import toast

with open("config.json", "r") as f:
    config = json.load(f)



WEBHOOK_URL = config["webhook_url"]
item_id = int(config["item_id"])
discount_percent = float(config["discount_percent"])
CHECK_INTERVAL = int(config["check_interval"])
if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK":
    raise Exception("Put your real Discord webhook in config.json")


def get_rap(item_id):
    url = "https://api.rolimons.com/items/v2/itemdetails"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    item = data.get("items", {}).get(str(item_id))

    if item:
        return item[2]  # RAP value

    return None


def send_discord(item_name, item_id, current_price, original_price, discount, rap):
    embed = {
        "title": "🎉 Roblox Deal Found!",
        "description": f"**{item_name}**",
        "color": 0x00FF00,

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
                "value": f"{rap:,} Robux" if rap else "Unknown",
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
            "text": "github.com/vvxlx"
        },

        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


    response = requests.post(
        WEBHOOK_URL,
        json={
            "username": "Limited Monitor",
            "embeds": [embed]
        },
        timeout=10
    )


    if response.status_code != 204:
        print("Discord webhook error:")
        print(response.text)


class Red:
    RED1 = '\033[91m'        # Bright Light Red
    RED2 = '\033[31m'        # Standard Red
    RED3 = '\033[1;31m'      # Bold Red
    RED4 = '\033[38;5;196m'  # Vivid Pure Red
    RED5 = '\033[38;5;160m'  # Crimson Red
    RED6 = '\033[38;5;124m'  # Dark Red
    RED7 = '\033[38;5;88m'   # Deep Maroon
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'


class Green:
    GREEN1 = '\033[92m'      # Bright Light Green
    GREEN2 = '\033[32m'      # Standard Green
    GREEN3 = '\033[1;32m'    # Bold Green
    GREEN4 = '\033[38;5;46m'   # Neon Green
    GREEN5 = '\033[38;5;34m'   # Forest Green
    GREEN6 = '\033[38;5;22m'   # Dark Green
    GREEN7 = '\033[38;5;28m'   # Emerald Green
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'


class Blue:
    BLUE1 = '\033[94m'       # Bright Light Blue
    BLUE2 = '\033[34m'       # Standard Blue
    BLUE3 = '\033[1;34m'     # Bold Blue
    BLUE4 = '\033[38;5;39m'   # Deep Sky Blue
    BLUE5 = '\033[38;5;27m'   # Royal Blue
    BLUE6 = '\033[38;5;21m'   # Dark Blue
    BLUE7 = '\033[38;5;18m'   # Navy Blue
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'


class Yellow:
    YELLOW1 = '\033[93m'     # Bright Light Yellow
    YELLOW2 = '\033[33m'     # Standard Yellow
    YELLOW3 = '\033[1;33m'   # Bold Yellow
    YELLOW4 = '\033[38;5;226m' # Pure Electric Yellow
    YELLOW5 = '\033[38;5;220m' # Gold Yellow
    YELLOW6 = '\033[38;5;214m' # Amber / Orange-Yellow
    YELLOW7 = '\033[38;5;172m' # Dark Ochre
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'


class Purple:
    PURPLE1 = '\033[95m'     # Bright Light Magenta / Purple
    PURPLE2 = '\033[35m'     # Standard Magenta / Purple
    PURPLE3 = '\033[1;35m'   # Bold Purple
    PURPLE4 = '\033[38;5;141m' # Soft Pastel Purple
    PURPLE5 = '\033[38;5;129m' # Medium Violet
    PURPLE6 = '\033[38;5;93m'  # Deep Purple
    PURPLE7 = '\033[38;5;55m'  # Dark Indigo / Violet
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'


class Cyan:
    CYAN1 = '\033[96m'       # Bright Light Cyan
    CYAN2 = '\033[36m'       # Standard Cyan
    CYAN3 = '\033[1;36m'     # Bold Cyan
    CYAN4 = '\033[38;5;51m'   # Electric Aqua
    CYAN5 = '\033[38;5;45m'   # Medium Cyan
    CYAN6 = '\033[38;5;37m'   # Dark Cyan
    CYAN7 = '\033[38;5;30m'   # Deep Teal
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'


class Style:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'



try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False



url = f"https://economy.roblox.com/v2/assets/{item_id}/details"


def get_item():
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


# Get initial item data
data = get_item()

item_name = data["Name"]

original_price = (
    data.get("CollectiblesItemDetails", {})
    .get("CollectibleLowestResalePrice")
)

if original_price is None:
    raise Exception("No resale price found for this item.")


# Get RAP from Rolimons
rap = get_rap(item_id)


print(f"\n{Green.GREEN4}Monitoring {Style.BOLD}{item_name}{Style.RESET}")
print(f"{Yellow.YELLOW5}Starting Price:{Style.RESET} {original_price:,} Robux")
print(f"{Yellow.YELLOW5}Required Discount:{Style.RESET} {discount_percent}%")
if rap:
    print(
        f"{Yellow.YELLOW5}RAP:{Style.RESET} "
        f"{rap:,} Robux"
    )
else:
    print(
        f"{Yellow.YELLOW5}RAP:{Style.RESET} Unknown"
    )

alert_price = int(original_price * (1 - discount_percent / 100))

print(
    f"{Yellow.YELLOW5}Alert Price:{Style.RESET} "
    f"{alert_price:,} Robux\n"
)


last_alert_price = None


while True:
    try:
        data = get_item()

        current_price = (
            data.get("CollectiblesItemDetails", {})
            .get("CollectibleLowestResalePrice")
        )

        now = datetime.now().strftime("%H:%M:%S")


        if current_price is None:
            print(
                f"{Yellow.YELLOW4}[{now}] "
                f"No resale listings found.{Style.RESET}"
            )

            time.sleep(CHECK_INTERVAL)
            continue


        discount = (
            (original_price - current_price)
            / original_price
        ) * 100


        if discount >= discount_percent and current_price != last_alert_price:

            print(
                f"{Green.GREEN4}[{now}] "
                f"GOOD DEAL FOUND! "
                f"{current_price:,} Robux "
                f"({discount:.2f}% OFF){Style.RESET}"
            )


            # Discord alert
            if config.get("discord_notifications", True):
                send_discord(
                    item_name,
                    item_id,
                    current_price,
                    original_price,
                    discount,
                    rap
                )


            # Windows notification
            if config.get("windows_notifications", True):
                toast(
                    "Roblox Deal Found!",
                    f"{item_name}\n"
                    f"{current_price:,} Robux\n"
                    f"{discount:.2f}% OFF",
                    duration="long"
                )


            # Open Roblox page
            if config.get("open_browser", True):
                webbrowser.open(
                    f"https://www.roblox.com/catalog/{item_id}"
                )


            # Sound alert
            if config.get("play_sound", True) and HAS_SOUND:
                winsound.Beep(1500, 700)
                winsound.MessageBeep()


            last_alert_price = current_price



        else:

            print(
                f"{Blue.BLUE4}[{now}] "
                f"{item_name} | "
                f"{current_price:,} Robux | "
                f"{discount:.2f}% OFF{Style.RESET}"
            )


        time.sleep(CHECK_INTERVAL)


    except Exception as e:

        print(
            f"{Red.RED4}Error: {e}{Style.RESET}"
        )

        time.sleep(CHECK_INTERVAL)
