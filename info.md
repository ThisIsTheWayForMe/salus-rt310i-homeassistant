# SALUS RT310i Technical Documentation

## Overview

This integration uses the **real SALUS API** at salus-it500.com, based on reverse engineering work from the Home Assistant community.

## Architecture

```
salus_rt310i/
├── __init__.py          # Main integration setup
├── config_flow.py       # UI configuration flow
├── const.py            # Real API endpoints
├── climate.py          # Climate entity implementation
├── salus_api.py        # Real SALUS API client
├── manifest.json       # Integration metadata
├── translations/       # Localization files
└── API_DOCUMENTATION.md # Detailed API reference
```

## SALUS API

### Base URL
`https://salus-it500.com`

### Authentication
- MD5-hashed passwords
- Cookie-based sessions
- Two-step login process

### Endpoints
- Login: `/public/login.php`
- Token: `/public/control.php`
- Get Data: `/public/ajax_device_values.php`
- Set Data: `/includes/set.php`

### Data Format
- Form-encoded POST (not JSON)
- Temperature values as strings
- Boolean values as "0"/"1" strings

## Key Features

✅ **Real API Implementation**
- Based on salusfy project reverse engineering
- Tested with RT310i and iT500 thermostats
- Production-ready code

✅ **Robust Error Handling**
- Automatic session refresh
- IP blocking detection
- Retry logic

✅ **Home Assistant Integration**
- Config flow for easy setup
- Standard climate entity
- Update coordinator pattern

## Configuration

Required information:
1. **Username** - Your salus-it500.com email
2. **Password** - Your account password
3. **Device ID** - From the website URL

## Data Fields

The API returns these key fields:
- `CH1currentRoomTemp` - Current temperature
- `CH1currentSetPoint` - Target temperature
- `CH1heatOnOff` - Heating status

See `API_DOCUMENTATION.md` for complete field reference.

## Rate Limiting

**IMPORTANT**: The SALUS API may block your IP if you:
- Poll more frequently than every 5 minutes
- Make excessive requests
- Have multiple failed logins

**Recommended**: 5-minute polling interval (default)

## Customization

### Change Polling Interval

Edit `__init__.py`:
```python
SCAN_INTERVAL = timedelta(minutes=5)  # Change as needed
```

⚠️ **Warning**: Intervals < 5 minutes may cause IP blocking

### Add Additional Sensors

The API returns many fields that could be exposed as sensors:
- Frost protection temperature
- Holiday mode status
- Schedule status
- Temperature alarms

See `API_DOCUMENTATION.md` for available fields.

## Troubleshooting

### Debug Logging

```yaml
logger:
  default: info
  logs:
    custom_components.salus_rt310i: debug
```

### Common Issues

1. **IP Blocked** - Wait 24h or restart router
2. **Session Expired** - Integration auto-refreshes
3. **Wrong Device ID** - Check salus-it500.com URL

