# 🎩 Roblox Limited Monitor

A Python-based Roblox Limited item monitor that tracks resale prices, calculates discounts, gets RAP from Rolimon's API, and sends alerts through Discord.

---

# ✨ Features

✅ Monitor Roblox Limited items  
✅ Get live resale prices from Roblox API  
✅ Get RAP (Recent Average Price) from Rolimon's API  
✅ Discord webhook notifications  
✅ Item thumbnail in Discord embeds  
✅ Windows desktop notifications  
✅ Browser auto-open on deals  
✅ Sound alerts  
✅ Custom discount percentage  
✅ Configurable checking interval  

---

# 📸 Example Alert

Discord alert includes:

- Item name
- Current price
- Starting price
- RAP
- Discount percentage
- Item ID
- Roblox catalog link
- Item thumbnail

Example:

```
🎉 Roblox Deal Found!

White Sparkle Time Fedora

Current Price:
27,000,000 Robux

Starting Price:
30,000,000 Robux

RAP:
3,410,356 Robux

Discount:
10.00%
```

---

# ⚙️ Installation

## 1. Install Python

Python 3.10+ recommended.

Download:

https://www.python.org/downloads/

---

## 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Roblox-Limited-Monitor.git
```

Enter the folder:

```bash
cd Roblox-Limited-Monitor
```

---

## 3. Install requirements

```bash
pip install -r requirements.txt
```

---

# 🔧 Configuration

Edit `config.json`

Example:

```json
{
    "webhook_url": "YOUR_DISCORD_WEBHOOK",
    "check_interval": 65,
    "item_id": 1016143686,
    "discount_percent": 10,
    "open_browser": true,
    "discord_notifications": true,
    "windows_notifications": true,
    "play_sound": true
}
```

---

# 🔗 Getting a Discord Webhook

1. Open your Discord server

2. Go to:

```
Server Settings
→ Integrations
→ Webhooks
→ New Webhook
```

3. Copy the webhook URL

4. Replace:

```
YOUR_DISCORD_WEBHOOK
```

with your webhook.

---

# ▶️ Running

Start the monitor:

```bash
python main.py
```

Example output:

```
Monitoring White Sparkle Time Fedora

Starting Price: 30,000,000 Robux
Required Discount: 10%

RAP: 3,410,356 Robux

Alert Price: 27,000,000 Robux
```

---

# 🔌 APIs Used

## Roblox Economy API

Used for:

- Item information
- Current resale price

Endpoint:

```
https://economy.roblox.com/v2/assets/{asset_id}/details
```

---

## Rolimon's API

Used for:

- RAP data

Endpoint:

```
https://api.rolimons.com/items/v2/itemdetails
```

---

# ⚠️ Notes

- Do not check too frequently.
- Recommended interval:
  - 60+ seconds for Roblox price checks
  - RAP only needs updating occasionally

- Keep your Discord webhook private.

---

# 📦 Requirements

Python packages:

```
requests
win11toast
```

Install:

```bash
pip install -r requirements.txt
```

---

# 🚀 Future Features

Possible improvements:

- Multiple item monitoring
- Proxy support
- Value tracking
- Trade calculator
- Limited stock alerts
- Price history graphs
- GUI version

---

# 📜 License

Free to use and modify.
