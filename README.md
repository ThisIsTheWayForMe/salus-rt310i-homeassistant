# SALUS RT310i Thermostat Integration for Home Assistant

This custom integration allows you to control your SALUS RT310i (and compatible iT500) thermostat through Home Assistant using the SALUS cloud API at salus-it500.com.

## Features

### Core Features
- 🌡️ View current and target temperature
- 🎯 Set target temperature (5-35°C, 0.5° steps)
- 🔥 Change HVAC mode (Off, Heat)
- 🔄 Automatic device polling (every 5 minutes)
- ☁️ Cloud-based integration using official SALUS API

### Advanced Sensors
- 📊 **Heating Demand** - Real-time heating demand percentage
- 🔌 **Connection Status** - Monitor API connectivity
- 📅 **Schedule Status** - Track if schedule is active
- ⏰ **Last Update** - When data was last refreshed
- 🎛️ **Operation Mode** - Current operating mode (Off/Manual/Schedule/Auto)
- ❄️ **Frost Protection** - Frost protection temperature setting
- 🏖️ **Holiday Mode** - Holiday mode status (if available)
- ⚠️ **Temperature Alarms** - Low/high temperature alerts

### Custom Services
- 🚀 **Boost Heating** - Temporarily boost heating for X minutes
- 🧊 **Frost Protection** - Enable/disable frost protection mode
- 🏝️ **Holiday Mode** - Set holiday mode with custom temperature
- 📅 **Schedule Management** - Create and manage heating schedules ⭐ NEW!
  - 3 pre-built templates (Comfort, Eco, Work From Home)
  - Custom schedule creation
  - Period-based control
  - Visual schedule editor

### Schedule Templates
- 📅 **Comfort Schedule** - Balanced 21°C/18°C schedule
- 💚 **Eco Schedule** - Energy-saving 19°C/16°C schedule
- 🏠 **Work From Home** - Optimized for home office (20-21°C)
- ✏️ **Custom Schedules** - Create your own time periods

### Pre-Built Dashboards
- 📱 **6 Ready-to-Use Dashboard Templates**
  - Minimal Card - Simple thermostat control
  - Detailed Card - Full status and controls
  - Energy Dashboard - Temperature history and heating activity
  - Mobile Compact - Optimized for phones
  - Advanced Control Panel - Quick action buttons
  - Picture Elements - Beautiful visual layout

### Automation Examples
- ⏰ Temperature schedules (morning, night, weekend)
- 🏠 Presence detection (away mode, welcome home)
- 🌤️ Weather-based control (cold days, sunny days)
- 💰 Energy saving (peak hours, window detection)
- 📢 Smart notifications (temperature alerts, daily reports)
- 🎭 Advanced scenarios (gradual cooling, activity-based)

See the `/dashboards` and `/automations` folders for complete examples!

## Supported Devices

- SALUS RT310i
- SALUS iT500
- Other SALUS thermostats compatible with salus-it500.com

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed in your Home Assistant instance
2. Add this repository as a custom repository in HACS:
   - Go to HACS → Integrations
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add the URL of this repository
   - Select "Integration" as the category
3. Click "Install"
4. Restart Home Assistant

### Manual Installation

1. Download the `salus_rt310i` folder from this repository
2. Copy it to your Home Assistant `custom_components` directory
   - The path should be: `<config_dir>/custom_components/salus_rt310i/`
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "SALUS RT310i"
4. Enter your SALUS account credentials:
   - **Username/Email**: The email address you use to log into salus-it500.com
   - **Password**: Your SALUS account password
   - **Device ID**: Your thermostat's device ID (see below for how to find it)

### Finding Your Device ID

1. Log in to [https://salus-it500.com](https://salus-it500.com) with your email and password
2. Click on your thermostat device
3. Look at the URL in your browser's address bar
4. The device ID will be visible in the URL (usually a long alphanumeric string)
5. Copy this device ID and paste it into the Home Assistant configuration

Example URL: `https://salus-it500.com/public/control.php?devId=YOUR_DEVICE_ID_HERE`

## Usage

Once configured, your thermostat will appear as a climate entity in Home Assistant. You can:

- View it in the Climate dashboard
- Add it to Lovelace cards
- Use it in automations and scripts
- Control it via voice assistants (if configured)

### Available Entities

After setup, you'll have access to:

**Climate Entity:**
- `climate.salus_rt310i_YOUR_DEVICE_ID` - Main thermostat control

**Sensors:**
- `sensor.salus_rt310i_YOUR_DEVICE_ID_target_temp` - Target temperature
- `sensor.salus_rt310i_YOUR_DEVICE_ID_heating_demand` - Heating demand percentage
- `sensor.salus_rt310i_YOUR_DEVICE_ID_operation_mode` - Current mode (Off/Manual/Schedule/Auto)
- `sensor.salus_rt310i_YOUR_DEVICE_ID_last_update` - Last update timestamp
- `sensor.salus_rt310i_YOUR_DEVICE_ID_frost_protection` - Frost protection temp (if available)

**Binary Sensors:**
- `binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating` - Heating active status
- `binary_sensor.salus_rt310i_YOUR_DEVICE_ID_connection` - Connection status
- `binary_sensor.salus_rt310i_YOUR_DEVICE_ID_schedule` - Schedule active
- `binary_sensor.salus_rt310i_YOUR_DEVICE_ID_holiday_mode` - Holiday mode (if available)
- `binary_sensor.salus_rt310i_YOUR_DEVICE_ID_low_temp_alarm` - Low temp alarm (if available)
- `binary_sensor.salus_rt310i_YOUR_DEVICE_ID_high_temp_alarm` - High temp alarm (if available)

**Schedule Switches:** ⭐ NEW!
- `switch.salus_rt310i_YOUR_DEVICE_ID_schedule_master` - Enable/disable schedules
- `switch.salus_rt310i_YOUR_DEVICE_ID_schedule_comfort` - Comfort schedule template
- `switch.salus_rt310i_YOUR_DEVICE_ID_schedule_eco` - Eco schedule template
- `switch.salus_rt310i_YOUR_DEVICE_ID_schedule_working_from_home` - Work from home template

### Pre-Built Dashboards

Check out the `/dashboards` folder for 6 ready-to-use Lovelace card templates:

1. **Minimal Card** - Simple and clean
2. **Detailed Card** - Full status with all sensors
3. **Energy Dashboard** - Temperature history and heating activity graphs
4. **Mobile Compact** - Optimized for mobile devices
5. **Advanced Control Panel** - Quick action buttons for common tasks
6. **Picture Elements** - Beautiful visual dashboard

[View Dashboard Examples →](dashboards/README.md)

### Custom Services

Use these services for advanced control:

#### Boost Heating
```yaml
service: salus_rt310i.boost_heating
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  duration: 30  # minutes
  temperature: 24  # optional, defaults to current + 2°C
```

#### Set Frost Protection
```yaml
service: salus_rt310i.set_frost_protection
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  enabled: true
  temperature: 5
```

#### Set Holiday Mode
```yaml
service: salus_rt310i.set_holiday_mode
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  enabled: true
  temperature: 15
```

#### Set Schedule ⭐ NEW!
```yaml
service: salus_rt310i.set_schedule
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  schedule_name: comfort  # or eco, working_from_home
```

#### Create Custom Schedule ⭐ NEW!
```yaml
service: salus_rt310i.create_custom_schedule
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  name: "My Schedule"
  weekday_periods:
    - start: "06:00"
      end: "08:00"
      temp: 21
    - start: "08:00"
      end: "22:00"
      temp: 19
    - start: "22:00"
      end: "06:00"
      temp: 17
  weekend_periods:
    - start: "08:00"
      end: "23:00"
      temp: 21
    - start: "23:00"
      end: "08:00"
      temp: 17
```

#### Apply Schedule Period ⭐ NEW!
```yaml
service: salus_rt310i.apply_schedule_period
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  start_time: "06:00"
  end_time: "08:00"
  temperature: 21
  days: ["mon", "tue", "wed", "thu", "fri"]
```

### Automation Examples

The `/automations` folder contains ready-to-use automation examples:

- **Temperature Schedules** - Morning warm-up, night setback, weekend schedules
- **Presence Detection** - Away mode, welcome home, proximity-based pre-heating
- **Weather-Based Control** - Cold day boost, sunny day optimization
- **Energy Saving** - Peak hours reduction, window open detection
- **Notifications** - Temperature alerts, heating issues, daily reports
- **Advanced Scenarios** - Gradual cooling, activity-based heating, holiday mode

[View Automation Examples →](automations/README.md)

### Basic Examples

#### Simple Thermostat Card
```yaml
type: thermostat
entity: climate.salus_rt310i_YOUR_DEVICE_ID
name: Living Room
```

#### Morning Warm-Up Automation

```yaml
automation:
  - alias: "Morning Warm-Up"
    trigger:
      platform: time
      at: "06:30:00"
    condition:
      condition: time
      weekday:
        - mon
        - tue
        - wed
        - thu
        - fri
    action:
      service: climate.set_temperature
      target:
        entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
      data:
        temperature: 21
```

#### Boost Heating Button

```yaml
type: button
name: Boost 30 min
icon: mdi:fire
tap_action:
  action: call-service
  service: salus_rt310i.boost_heating
  service_data:
    entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
    duration: 30
```

For more examples, see the [Dashboards](dashboards/README.md) and [Automations](automations/README.md) folders.

## API Information

This integration uses the official SALUS cloud API at salus-it500.com. The integration:
- Logs in using MD5-hashed credentials
- Maintains session cookies for subsequent requests
- Polls the API every 5 minutes for updates
- Sends immediate commands when you change settings

**Note:** The SALUS API may rate-limit or block your IP if you poll too frequently or make too many requests. The default 5-minute polling interval is designed to be respectful of their servers.

## Known Issues

### IP Blocking

The salus-it500.com server may block your IP address if it detects unusual activity. This can happen if:
- You poll too frequently
- Multiple instances access the same account
- Your IP makes too many failed login attempts

**Solutions:**
- Restart your router to get a new IP (if using DHCP/PPPoE)
- Wait 24 hours for the block to expire
- Contact SALUS support for assistance
- Use only one Home Assistant instance per account

## Troubleshooting

### Cannot connect to SALUS servers

- Check your internet connection
- Verify your SALUS account credentials at https://salus-it500.com
- Check if your IP has been blocked (see Known Issues)
- Ensure the device ID is correct

### Invalid authentication

- Double-check username and password
- Make sure you can log in to https://salus-it500.com
- Verify the device ID matches your thermostat

### Thermostat not responding

- The integration polls every 5 minutes by default
- Changes may take a few moments to reflect
- Check Home Assistant logs for errors
- Verify your thermostat is online in the SALUS app/website

### Enable Debug Logging

Add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.salus_rt310i: debug
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

This integration is based on research from the Home Assistant community, particularly the [salusfy](https://github.com/floringhimie/salusfy) project by floringhimie, which demonstrated the SALUS API implementation.

## License

This project is licensed under the MIT License.

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by SALUS. Use at your own risk. The authors are not responsible for any damage to your thermostat or heating system.
