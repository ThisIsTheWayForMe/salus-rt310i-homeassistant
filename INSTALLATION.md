# Installation Guide

## Prerequisites

- Home Assistant 2023.1.0 or later
- HACS (Home Assistant Community Store) installed
- SALUS RT310i thermostat with cloud account

## Step-by-Step Installation

### Method 1: HACS (Recommended)

1. **Open HACS**
   - Navigate to HACS in your Home Assistant sidebar
   - Click on "Integrations"

2. **Add Custom Repository**
   - Click the three dots menu (⋮) in the top right
   - Select "Custom repositories"
   - Add the repository URL: `https://github.com/yourusername/salus_rt310i`
   - Select category: "Integration"
   - Click "Add"

3. **Install the Integration**
   - Search for "SALUS RT310i" in HACS
   - Click on the integration
   - Click "Download"
   - Restart Home Assistant

4. **Configure the Integration**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "SALUS RT310i"
   - Enter your SALUS cloud credentials
   - Click "Submit"

### Method 2: Manual Installation

1. **Download the Integration**
   - Download the latest release from GitHub
   - Or clone the repository: `git clone https://github.com/yourusername/salus_rt310i.git`

2. **Copy to Home Assistant**
   - Copy the `salus_rt310i` folder to `<config>/custom_components/`
   - Your final path should be: `<config>/custom_components/salus_rt310i/`

3. **Restart Home Assistant**
   - Restart your Home Assistant instance

4. **Configure the Integration**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "SALUS RT310i"
   - Enter your SALUS cloud credentials
   - Click "Submit"

## Configuration

### Required Information

You'll need your SALUS cloud account credentials:
- **Username/Email**: The email address you use to log into the SALUS app
- **Password**: Your SALUS account password

### Finding Your Credentials

If you're not sure about your SALUS account credentials:

1. Download the SALUS Smart Home app (iOS/Android)
2. If you can log in successfully, use those same credentials
3. If you've forgotten your password, use the app's password recovery feature

## Verification

After installation, verify everything is working:

1. **Check Devices**
   - Go to Settings → Devices & Services
   - Find "SALUS RT310i Thermostat"
   - Click on it to see your devices

2. **Check Entities**
   - You should see climate entities for each thermostat
   - Entity IDs will be like: `climate.salus_rt310i_[device_name]`

3. **Test Control**
   - Try changing the temperature
   - Try changing the HVAC mode
   - Changes should appear in the SALUS app within a few minutes

## Troubleshooting

### Integration Not Appearing

- Clear browser cache
- Restart Home Assistant completely (not just reload)
- Check logs: Settings → System → Logs

### Authentication Failed

- Double-check username and password
- Ensure you're using the correct SALUS account (not installer account)
- Try logging into the SALUS app to verify credentials

### Thermostats Not Showing

- Wait 5-10 minutes for initial sync
- Check that thermostats are online in the SALUS app
- Reload the integration: Settings → Devices & Services → SALUS RT310i → ⋮ → Reload

### Getting Help

If you encounter issues:
1. Enable debug logging (see README.md)
2. Check Home Assistant logs
3. Create an issue on GitHub with:
   - Home Assistant version
   - Integration version
   - Error messages from logs
   - Steps to reproduce

## Updating

### Via HACS

1. Go to HACS → Integrations
2. Find "SALUS RT310i"
3. Click "Update" if available
4. Restart Home Assistant

### Manual Update

1. Download the latest version
2. Replace the `custom_components/salus_rt310i/` folder
3. Restart Home Assistant

## Uninstallation

1. Go to Settings → Devices & Services
2. Find "SALUS RT310i Thermostat"
3. Click the three dots (⋮)
4. Select "Delete"
5. Optionally remove the integration files from `custom_components/`
