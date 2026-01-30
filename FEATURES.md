# SALUS RT310i - Complete Feature List

## 🎯 Overview

The SALUS RT310i integration provides comprehensive control and monitoring of your SALUS thermostat with advanced features, custom services, and beautiful dashboards.

---

## 🌡️ Core Climate Control

### Temperature Management
- ✅ **Current Temperature Display** - Real-time room temperature
- ✅ **Target Temperature Control** - Set from 5°C to 35°C in 0.5°C steps
- ✅ **Precision Control** - 0.5°C increments for exact comfort
- ✅ **HVAC Modes** - Heat and Off modes supported

### Device Information
- ✅ **Device ID Tracking** - Unique identifier for each thermostat
- ✅ **Manufacturer Info** - SALUS branding
- ✅ **Model Recognition** - RT310i and iT500 support

---

## 📊 Sensors (6 Total)

### 1. Target Temperature Sensor
- **Entity**: `sensor.salus_rt310i_{device_id}_target_temp`
- **Type**: Temperature
- **Unit**: °C
- **State Class**: Measurement
- **Description**: Current target temperature setting

### 2. Heating Demand Sensor
- **Entity**: `sensor.salus_rt310i_{device_id}_heating_demand`
- **Type**: Percentage
- **Unit**: %
- **Icon**: 🔥 (mdi:fire)
- **Description**: Calculated heating demand based on temperature difference
- **Algorithm**: 
  - 0% when heating is off
  - Scales from 0-100% based on temperature gap
  - Max 5°C difference = 100% demand

### 3. Last Update Sensor
- **Entity**: `sensor.salus_rt310i_{device_id}_last_update`
- **Type**: Timestamp
- **Icon**: 🕐 (mdi:clock-outline)
- **Description**: When data was last successfully retrieved from API

### 4. Operation Mode Sensor
- **Entity**: `sensor.salus_rt310i_{device_id}_operation_mode`
- **Type**: Text
- **Icon**: 🎛️ (mdi:thermostat-auto)
- **Possible Values**:
  - `Off` - Heating disabled
  - `Manual` - Manual temperature control
  - `Schedule` - Following programmed schedule
  - `Auto` - Automatic mode
  - `Unknown` - Cannot determine mode
- **Attributes**:
  - `heating_enabled` - Boolean
  - `schedule_enabled` - Boolean
  - `auto_mode` - Boolean

### 5. Frost Protection Sensor
- **Entity**: `sensor.salus_rt310i_{device_id}_frost_protection`
- **Type**: Temperature
- **Unit**: °C
- **Icon**: ❄️ (mdi:snowflake-alert)
- **Description**: Frost protection temperature setting
- **Availability**: Only when device supports frost protection

### 6. (Future) Additional Sensors
- Battery level (if available)
- Signal strength (if available)
- Outdoor temperature (if available)

---

## 🔌 Binary Sensors (6 Total)

### 1. Heating Active
- **Entity**: `binary_sensor.salus_rt310i_{device_id}_heating`
- **Type**: Heat
- **Description**: True when heating relay is active
- **Attributes**:
  - `relay_status` - Physical relay state
  - `temperature_difference` - Gap to target temp

### 2. Connection Status
- **Entity**: `binary_sensor.salus_rt310i_{device_id}_connection`
- **Type**: Connectivity
- **Description**: Connection to SALUS cloud API
- **Attributes**:
  - `last_success` - ISO timestamp of last successful update
  - `last_error` - Error message (if any)

### 3. Schedule Active
- **Entity**: `binary_sensor.salus_rt310i_{device_id}_schedule`
- **Type**: Generic
- **Icon**: 📅 (mdi:calendar-clock)
- **Description**: True when schedule is enabled
- **Attributes**:
  - `program_mode` - Current program mode

### 4. Holiday Mode
- **Entity**: `binary_sensor.salus_rt310i_{device_id}_holiday_mode`
- **Type**: Generic
- **Icon**: 🏖️ (mdi:beach)
- **Description**: True when holiday mode is active
- **Availability**: Only when device supports holiday mode

### 5. Low Temperature Alarm
- **Entity**: `binary_sensor.salus_rt310i_{device_id}_low_temp_alarm`
- **Type**: Problem
- **Description**: True when temperature drops below alarm threshold
- **Availability**: Only when device supports temperature alarms

### 6. High Temperature Alarm
- **Entity**: `binary_sensor.salus_rt310i_{device_id}_high_temp_alarm`
- **Type**: Problem
- **Description**: True when temperature exceeds alarm threshold
- **Availability**: Only when device supports temperature alarms

---

## 🛠️ Custom Services (3 Total)

### 1. Boost Heating
- **Service**: `salus_rt310i.boost_heating`
- **Description**: Temporarily increase heating for a specified duration
- **Parameters**:
  - `entity_id` (required) - Climate entity to control
  - `duration` (required) - Duration in minutes (5-120)
  - `temperature` (optional) - Target temp during boost (defaults to current + 2°C)
- **Use Cases**:
  - Quick warm-up when arriving home
  - Temporary comfort boost
  - Morning wake-up routine
  - Guest comfort
- **Example**:
  ```yaml
  service: salus_rt310i.boost_heating
  data:
    entity_id: climate.salus_rt310i_ABC123
    duration: 30
    temperature: 24
  ```

### 2. Set Frost Protection
- **Service**: `salus_rt310i.set_frost_protection`
- **Description**: Enable or disable frost protection mode
- **Parameters**:
  - `entity_id` (required) - Climate entity to control
  - `enabled` (required) - Enable/disable frost protection
  - `temperature` (optional) - Frost protection temperature (5-15°C)
- **Use Cases**:
  - Holiday/vacation mode
  - Unoccupied property protection
  - Winter property maintenance
  - Pipe freeze prevention
- **Example**:
  ```yaml
  service: salus_rt310i.set_frost_protection
  data:
    entity_id: climate.salus_rt310i_ABC123
    enabled: true
    temperature: 5
  ```

### 3. Set Holiday Mode
- **Service**: `salus_rt310i.set_holiday_mode`
- **Description**: Enable or disable holiday mode with custom temperature
- **Parameters**:
  - `entity_id` (required) - Climate entity to control
  - `enabled` (required) - Enable/disable holiday mode
  - `temperature` (optional) - Temperature during holiday (5-25°C)
- **Use Cases**:
  - Extended absences
  - Vacation energy saving
  - Seasonal property closure
  - Temporary low-heat mode
- **Example**:
  ```yaml
  service: salus_rt310i.set_holiday_mode
  data:
    entity_id: climate.salus_rt310i_ABC123
    enabled: true
    temperature: 15
  ```

---

## 📱 Pre-Built Dashboards (6 Templates)

### 1. Minimal Card
- **Complexity**: Basic
- **Best For**: Simple control
- **Components**: Standard thermostat card
- **Screen**: All devices

### 2. Detailed Card
- **Complexity**: Intermediate
- **Best For**: Full monitoring
- **Components**: 
  - Thermostat card
  - Status entities card
  - Boost button
- **Entities Shown**: 7+
- **Screen**: Desktop/Tablet

### 3. Energy Dashboard
- **Complexity**: Advanced
- **Best For**: Energy tracking
- **Components**:
  - Thermostat card
  - Heating demand gauge
  - 24-hour temperature history
  - 24-hour heating activity
- **Screen**: Desktop/Tablet

### 4. Mobile Compact
- **Complexity**: Basic
- **Best For**: Phone usage
- **Components**:
  - Compact button card
  - Horizontal status cards
  - Key sensors only
- **Screen**: Mobile phones

### 5. Advanced Control Panel
- **Complexity**: Advanced
- **Best For**: Power users
- **Components**:
  - Thermostat card
  - 4 quick action buttons (Boost 30m, Boost 1h, Comfort, Eco)
  - Status glance card
- **Screen**: All devices

### 6. Picture Elements
- **Complexity**: Advanced
- **Best For**: Visual appeal
- **Components**:
  - Background image
  - Large temperature display
  - Heating status icon
- **Requires**: Custom background image
- **Screen**: Desktop/Tablet

---

## 🤖 Automation Capabilities

### Temperature Schedules
- Morning warm-up routines
- Night time setbacks
- Weekend schedules
- Weekday vs weekend timing
- Gradual temperature changes

### Presence-Based
- Away mode activation
- Welcome home boost
- Proximity-based pre-heating
- Zone occupancy detection
- Multi-person presence logic

### Weather Integration
- Cold day temperature boost
- Sunny day heating reduction
- Wind-based adjustments
- Forecast-based planning
- Seasonal adaptations

### Energy Optimization
- Peak hours reduction
- Off-peak heating boost
- Window open detection
- Door sensor integration
- Smart meter coordination

### Notifications
- Low temperature alerts
- Heating failure detection
- Daily summary reports
- Weekly statistics
- Connection loss alerts

### Advanced Scenarios
- Activity-based heating
- Room-by-room control
- Guest mode activation
- Sleep mode routines
- Wake-up sequences

---

## 🔧 Technical Capabilities

### API Integration
- Real SALUS API at salus-it500.com
- MD5-hashed authentication
- Cookie-based sessions
- Form-encoded requests
- Automatic session refresh

### Update Management
- 5-minute polling interval
- Configurable update frequency
- Automatic retry on failure
- Exponential backoff
- Rate limiting awareness

### Error Handling
- Connection failure recovery
- Session expiry handling
- IP blocking detection
- Graceful degradation
- Detailed error logging

### Data Validation
- Temperature range checking
- Type conversion
- Null value handling
- Invalid data filtering
- State consistency

---

## 📈 Performance Features

### Efficient Polling
- 5-minute default interval (safe)
- Configurable down to 3 minutes (not recommended)
- Smart retry logic
- Minimal API calls

### Resource Usage
- Async operations throughout
- Session reuse
- Cookie caching
- Minimal memory footprint

### Reliability
- Automatic reconnection
- Session refresh
- Error recovery
- Connection monitoring

---

## 🎨 Customization Options

### Entity Customization
- Rename entities
- Change icons
- Set custom colors
- Add to groups
- Create templates

### Dashboard Flexibility
- 6 base templates
- Full YAML customization
- Custom card options
- Theme integration
- Responsive layouts

### Automation Freedom
- Unlimited automations
- Complex conditions
- Multi-action sequences
- Template sensors
- Script integration

---

## 📚 Documentation

### Included Docs
- ✅ README.md - Main documentation
- ✅ API_DOCUMENTATION.md - Complete API reference
- ✅ INSTALLATION.md - Setup guide
- ✅ QUICKSTART.md - Quick setup
- ✅ CHANGELOG.md - Version history
- ✅ FEATURES.md - This file
- ✅ dashboards/README.md - Dashboard templates
- ✅ automations/README.md - Automation examples

### Additional Resources
- GitHub Issues for support
- Home Assistant forums
- Community contributions

---

## 🏆 Why Choose This Integration?

1. **Most Complete** - More sensors and features than any other SALUS integration
2. **Well Documented** - Extensive docs, examples, and guides
3. **Ready to Use** - Pre-built dashboards and automations


---

## 📞 Support

- **Documentation**: Read the docs folder
- **Examples**: Check dashboards and automations folders
- **Issues**: GitHub issue tracker
- **Community**: Home Assistant forums

---

*Last Updated: January 30, 2026*
*Version: 1.1.0*
