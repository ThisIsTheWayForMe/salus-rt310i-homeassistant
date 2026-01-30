# Changelog

All notable changes to the SALUS RT310i integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-30

### Added - Schedule Management Feature! 📅

#### New Schedule Platform
- **Switch Platform** - Added schedule management via switches
  - Schedule Master Switch - Enable/disable all schedules
  - 3 Pre-built Schedule Templates:
    - Comfort Schedule (21°C comfort, 18°C away)
    - Eco Schedule (19°C comfort, 16°C away)
    - Work From Home Schedule (optimized for home office)

#### New Schedule Services
- **set_schedule** - Apply pre-built schedule templates
  - Quick activation of Comfort, Eco, or Work From Home schedules
  - Simple schedule selection

- **create_custom_schedule** - Build your own schedules
  - Define custom time periods
  - Separate weekday/weekend schedules
  - Full temperature control

- **apply_schedule_period** - Manual period application
  - Set specific time periods
  - Select days of week
  - Temporary overrides

#### Schedule Features
- **3 Ready-to-Use Templates**:
  - Comfort: Balanced comfort schedule
  - Eco: Energy-saving schedule
  - Work From Home: Optimized for remote work

- **Smart Schedule Management**:
  - Only one template active at a time
  - Master enable/disable control
  - State persistence across restarts
  - Detailed schedule attributes

#### Documentation
- **SCHEDULES.md** - Complete schedule guide
  - Template descriptions
  - Custom schedule creation
  - Dashboard examples
  - Automation examples
  - Best practices

- **Enhanced Dashboard Examples**:
  - Schedule Management Dashboard (#7)
  - Weekly Schedule Planner (#8)
  - Schedule control panels
  - Visual schedule viewers

#### Integration Enhancements
- 4 new switch entities per device
- Schedule state tracking
- Rich state attributes
- Automation-ready design

### Changed
- Updated README with schedule features
- Enhanced services.yaml with 3 new services
- Updated dashboard examples (now 8 total)
- Improved automation examples

### Technical Details
- Switch platform implementation
- RestoreEntity for state persistence
- Coordinator integration
- Service registration
- Template-based schedules

## [1.0.0] - 2024-01-29 Initial Release

#### Core Features
- Climate platform for SALUS RT310i thermostat
- Real SALUS API implementation (based on salusfy project)
- Support for RT310i and iT500 models
- UI-based configuration flow
- Device ID requirement for setup

#### Climate Entity Features
- Current temperature display
- Target temperature control (5-35°C, 0.5° steps)
- HVAC mode switching (Heat, Off)
- Temperature unit: Celsius
- Automatic polling every 5 minutes

#### Platforms
- **Sensor Platform** - Added 6 new sensors for comprehensive monitoring:
  - Target Temperature sensor
  - Heating Demand percentage sensor
  - Last Update timestamp sensor
  - Operation Mode sensor
  - Frost Protection temperature sensor (when available)
  - Additional state attributes on all sensors

- **Binary Sensor Platform** - Added 6 status indicators:
  - Heating Active sensor (with heating relay status)
  - Connection Status sensor
  - Schedule Active sensor
  - Holiday Mode sensor (when available)
  - Low Temperature Alarm sensor (when available)
  - High Temperature Alarm sensor (when available)

#### API Implementation
- MD5-hashed password authentication
- Cookie-based session management
- Form-encoded POST requests
- Endpoints:
  - Login: `/public/login.php`
  - Token: `/public/control.php`
  - Get Data: `/public/ajax_device_values.php`
  - Set Data: `/includes/set.php`

#### Documentation
- Complete README with setup instructions
- API documentation with examples
- Installation guide
- Quick start guide
- Technical documentation

#### Safety Features
- IP blocking awareness
- Rate limiting considerations (5-minute polling)
- Automatic session refresh
- Error handling and retry logic

### Known Issues
- SALUS server may block IP if polling too frequently
- No local control (cloud-based only)
- Some advanced features depend on device capabilities

---

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/salus_rt310i/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/salus_rt310i/discussions)
- **Documentation**: See README.md and docs folder

---

## Credits

Inspired by work from:
- [salusfy](https://github.com/floringhimie/salusfy) by @floringhimie 
- Home Assistant community contributions

## License

MIT License - See LICENSE file for details
