# HA Parking Monitor

## Overview
**HA Parking Monitor** is a custom Home Assistant integration that allows ANPR (Automatic Number Plate Recognition) cameras to send data to Home Assistant. It updates sensors with detected vehicle registration marks (VRMs), direction, and timestamps. It can also track parked vehicles.

## Features
- Supports multiple ANPR cameras
- Stores last detected VRM and direction (towards, away, static)
- Records timestamps for arrivals, departures, and parking
- Maintains a history of detected vehicles
- Tracks parked vehicles with timestamps

---

## Installation via HACS (Recommended)

### **1. Add to HACS**
1. **Go to HACS → Integrations**.
2. **Add a Custom Repository**:
   ```
   https://github.com/knaps151/HA-Parking-Monitor
   ```
   - Select **"Integration"** as the category.
3. Search for **HA Parking Monitor** in HACS and install it.
4. Restart Home Assistant.

---

### **2. Configure via UI (No `configuration.yaml` Required)**
1. **Go to Home Assistant → Settings → Devices & Services**.
2. Click **+ Add Integration** and search for **HA Parking Monitor**.
3. Enter:
   - **Allowed VRMs**
   - **Webhook Token**
   - **History Size**
4. Save and restart Home Assistant.

✅ **This method stores settings in `.storage/` instead of `configuration.yaml`.**

---

## **(Optional) Manual Configuration via `configuration.yaml`**
If you prefer manual configuration, you **can still** add this to `configuration.yaml`:

```yaml
ha_parking_monitor:
  allowed_vrms:
    - "AB12CDE"
    - "XY34FGH"
  webhook_token: "my_secure_token"
  history_size: 15
```

Then restart Home Assistant.

---

## **Webhook API**

The integration exposes a webhook that allows ANPR cameras to send data. The webhook URL is:

```
http://homeassistant.local:8123/api/webhook/ha_parking_monitor
```

### **Example JSON Payload**
```json
{
  "token": "my_secure_token",
  "camera_id": "gate1",
  "vrm": "AB12CDE",
  "direction": "towards",
  "timestamp": "2025-01-31T14:30:00Z"
}
```

---

## **License**
MIT License

For more details, see [HA Parking Monitor on GitHub](https://github.com/knaps151/HA-Parking-Monitor).
