# Quick Start Guide - SALUS RT310i Integration

## ✅ READY TO USE!

This integration now uses the **real SALUS API** based on the salus-it500.com implementation. It's ready to use with your RT310i or iT500 thermostat!

## 5-Minute Setup

### 1. Get Your Device ID

Before installing, you need your device ID:

1. Go to [https://salus-it500.com](https://salus-it500.com)
2. Log in with your SALUS account
3. Click on your thermostat
4. Look at the URL in your browser
5. Copy the device ID from the URL

Example: `https://salus-it500.com/public/control.php?devId=ABC123XYZ`
Your device ID is: `ABC123XYZ`

### 2. Install via HACS

```
HACS → Integrations → ⋮ → Custom repositories
Add: https://github.com/yourusername/salus_rt310i
Category: Integration
```

### 3. Restart Home Assistant

### 4. Add Integration

```
Settings → Devices & Services → Add Integration → SALUS RT310i
```

### 5. Enter Credentials

- **Username**: your-email@example.com
- **Password**: your-password
- **Device ID**: ABC123XYZ (from step 1)

### 6. Done!

Your thermostat will appear as a climate entity.

## API Details

This integration uses the real SALUS API at salus-it500.com:

- **Base URL**: https://salus-it500.com
- **Authentication**: MD5-hashed password
- **Session**: Cookie-based
- **Data format**: Form data (not JSON)
- **Polling interval**: 5 minutes

### Data Fields

The API returns temperature data in these fields:
- `CH1currentRoomTemp` - Current room temperature
- `CH1currentSetPoint` - Target temperature setpoint
- `CH1heatOnOff` - Heating on/off status

## Common Issues

### "Cannot Connect"
→ Check your credentials at https://salus-it500.com
→ Verify device ID is correct

### "Invalid Auth"
→ Make sure you can log in to the website
→ Password is case-sensitive

### IP Blocked
→ SALUS may block your IP if you poll too frequently
→ Wait 24 hours or restart your router for new IP
→ Contact SALUS support if persistent

### Temperature Not Updating
→ Integration polls every 5 minutes
→ Check logs for API errors
→ Verify thermostat is online at salus-it500.com

## File Structure

```
salus_rt310i/
├── __init__.py           ← Integration setup
├── config_flow.py        ← Configuration UI
├── const.py             ← API URLs (REAL endpoints)
├── climate.py           ← Climate entity
├── salus_api.py         ← API client (REAL implementation)
├── manifest.json        ← Metadata
├── hacs.json           ← HACS config
├── translations/
│   └── en.json         ← UI text
└── README.md           ← Documentation
```

## API Implementation Notes

The integration uses:

1. **Login Flow**:
   - POST to `/public/login.php` with MD5-hashed password
   - Stores session cookies
   - Gets token from `/public/control.php`

2. **Get Data**:
   - GET `/public/ajax_device_values.php?devId=XXX&current=1`
   - Returns JSON with temperature data

3. **Set Temperature**:
   - POST to `/includes/set.php`
   - Form data: `devId`, `current_tempZ1_set`, `tempUnit`

4. **Set Mode**:
   - POST to `/includes/set.php`
   - Form data: `devId`, `auto` (1=on, 0=off)

## Debugging

Enable debug logging:

```yaml
logger:
  default: info
  logs:
    custom_components.salus_rt310i: debug
```

Then check logs for:
- Login success/failure
- API responses
- Temperature values
- Error messages

## Next Steps

1. Test with your thermostat
2. Create automations
3. Add to dashboards
4. Share feedback!

## Need Help?

1. Check Home Assistant logs
2. Verify credentials at salus-it500.com
3. Look for error messages in debug logs
4. Create GitHub issue with logs
