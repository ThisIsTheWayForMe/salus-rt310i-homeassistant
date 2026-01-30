# 📅 SALUS RT310i Schedule Management Guide

Complete guide to creating and managing heating schedules with your SALUS thermostat.

## 🎯 Overview

The SALUS RT310i integration includes powerful scheduling features:
- **3 Pre-Built Templates** - Ready-to-use schedules
- **Custom Schedules** - Create your own
- **Visual Schedule Editor** - Easy configuration
- **Automation Integration** - Dynamic schedule changes

---

## 📋 Pre-Built Schedule Templates

### 1. Comfort Schedule (Default)

Balanced schedule for maximum comfort.

**Weekdays (Mon-Fri):**
- 06:00 - 08:00: **21°C** (Morning warm-up)
- 08:00 - 17:00: **18°C** (Away during day)
- 17:00 - 22:00: **21°C** (Evening comfort)
- 22:00 - 06:00: **17°C** (Night setback)

**Weekends (Sat-Sun):**
- 07:00 - 23:00: **21°C** (All day comfort)
- 23:00 - 07:00: **17°C** (Night setback)

**Best For:**
- Traditional work schedule
- Families with kids
- Standard 9-5 routine

### 2. Eco Schedule

Energy-saving schedule with lower temperatures.

**Weekdays (Mon-Fri):**
- 06:00 - 08:00: **19°C** (Morning)
- 08:00 - 17:00: **16°C** (Away)
- 17:00 - 22:00: **19°C** (Evening)
- 22:00 - 06:00: **16°C** (Night)

**Weekends (Sat-Sun):**
- 07:00 - 23:00: **19°C** (Day)
- 23:00 - 07:00: **16°C** (Night)

**Best For:**
- Energy conscious users
- Well-insulated homes
- Cost savings priority

### 3. Work From Home Schedule

Optimized for home office workers.

**Weekdays (Mon-Fri):**
- 06:00 - 08:00: **21°C** (Morning)
- 08:00 - 12:00: **20°C** (Work morning)
- 12:00 - 13:00: **21°C** (Lunch break)
- 13:00 - 17:00: **20°C** (Work afternoon)
- 17:00 - 22:00: **21°C** (Evening)
- 22:00 - 06:00: **17°C** (Night)

**Weekends (Sat-Sun):**
- 08:00 - 23:00: **21°C** (Day)
- 23:00 - 08:00: **17°C** (Night)

**Best For:**
- Remote workers
- Home office setups
- All-day home presence

---

## 🚀 Quick Start - Using Pre-Built Templates

### Method 1: Using Switches

```yaml
# Turn on Comfort schedule
service: switch.turn_on
target:
  entity_id: switch.salus_YOUR_DEVICE_ID_schedule_comfort

# Turn on Eco schedule
service: switch.turn_on
target:
  entity_id: switch.salus_YOUR_DEVICE_ID_schedule_eco

# Turn on Work From Home schedule
service: switch.turn_on
target:
  entity_id: switch.salus_YOUR_DEVICE_ID_schedule_working_from_home
```

### Method 2: Using Service

```yaml
# Apply Comfort schedule
service: salus_rt310i.set_schedule
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  schedule_name: comfort
```

### Method 3: Using Dashboard

Add schedule switches to your dashboard:

```yaml
type: entities
title: Heating Schedules
entities:
  - entity: switch.salus_YOUR_DEVICE_ID_schedule_master
    name: Schedule Enabled
  - type: divider
  - entity: switch.salus_YOUR_DEVICE_ID_schedule_comfort
    name: Comfort Mode
  - entity: switch.salus_YOUR_DEVICE_ID_schedule_eco
    name: Eco Mode
  - entity: switch.salus_YOUR_DEVICE_ID_schedule_working_from_home
    name: Work From Home
```

---

## 🎨 Creating Custom Schedules

### Using the Service

```yaml
service: salus_rt310i.create_custom_schedule
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  name: "My Custom Schedule"
  weekday_periods:
    - start: "05:30"
      end: "07:30"
      temp: 22
    - start: "07:30"
      end: "16:30"
      temp: 17
    - start: "16:30"
      end: "23:00"
      temp: 21
    - start: "23:00"
      end: "05:30"
      temp: 16
  weekend_periods:
    - start: "08:00"
      end: "22:00"
      temp: 21
    - start: "22:00"
      end: "08:00"
      temp: 17
```

### Schedule Period Format

Each period must have:
```yaml
- start: "HH:MM"  # 24-hour format
  end: "HH:MM"    # 24-hour format
  temp: 21        # Temperature in °C
```

**Important Rules:**
- Times in 24-hour format
- Periods should cover full 24 hours
- No overlapping periods
- Temperature: 5-35°C

---

## ⚙️ Advanced Schedule Features

### Apply Single Period

Manually override with a specific time period:

```yaml
service: salus_rt310i.apply_schedule_period
target:
  entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
data:
  start_time: "06:00"
  end_time: "08:00"
  temperature: 21
  days:
    - mon
    - tue
    - wed
    - thu
    - fri
```

### Temporary Schedule Override

Use automation to temporarily modify schedule:

```yaml
automation:
  - alias: "Weekend Party Mode"
    trigger:
      platform: state
      entity_id: input_boolean.party_mode
      to: "on"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.salus_YOUR_DEVICE_ID_schedule_master
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 23
```

---

## 📱 Dashboard Examples

### Schedule Control Panel

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Heating Schedule
    entities:
      - entity: switch.salus_YOUR_DEVICE_ID_schedule_master
        name: Schedule Mode
        icon: mdi:calendar-clock
      
      - type: section
        label: Active Schedule
      
      - type: attribute
        entity: switch.salus_YOUR_DEVICE_ID_schedule_master
        attribute: active_schedule
        name: Current Template
  
  - type: horizontal-stack
    cards:
      - type: button
        entity: switch.salus_YOUR_DEVICE_ID_schedule_comfort
        name: Comfort
        icon: mdi:sofa
        tap_action:
          action: toggle
      
      - type: button
        entity: switch.salus_YOUR_DEVICE_ID_schedule_eco
        name: Eco
        icon: mdi:leaf
        tap_action:
          action: toggle
      
      - type: button
        entity: switch.salus_YOUR_DEVICE_ID_schedule_working_from_home
        name: WFH
        icon: mdi:home-account
        tap_action:
          action: toggle
```

### Schedule Viewer

Shows current schedule details:

```yaml
type: markdown
content: >
  ## {{ states.switch.salus_YOUR_DEVICE_ID_schedule_comfort.attributes.weekday_periods[0].temp }}°C

  **Current Schedule:**
  {{ state_attr('switch.salus_YOUR_DEVICE_ID_schedule_master', 'active_schedule') or 'None' }}
  
  **Status:**
  {{ 'Active' if is_state('switch.salus_YOUR_DEVICE_ID_schedule_master', 'on') else 'Disabled' }}
```

---

## 🤖 Automation Examples

### Auto-Switch Schedules

Switch between schedules based on day:

```yaml
automation:
  - alias: "Weekend Schedule"
    trigger:
      - platform: time
        at: "00:00:01"
    condition:
      - condition: time
        weekday:
          - sat
          - sun
    action:
      - service: salus_rt310i.set_schedule
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          schedule_name: comfort
  
  - alias: "Weekday Schedule"
    trigger:
      - platform: time
        at: "00:00:01"
    condition:
      - condition: time
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
    action:
      - service: salus_rt310i.set_schedule
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          schedule_name: working_from_home
```

### Presence-Based Schedule Override

Disable schedule when away:

```yaml
automation:
  - alias: "Away - Disable Schedule"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "not_home"
        for:
          minutes: 30
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.salus_YOUR_DEVICE_ID_schedule_master
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 16
  
  - alias: "Home - Resume Schedule"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "home"
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.salus_YOUR_DEVICE_ID_schedule_master
```

### Holiday Mode Schedule

Special schedule for holidays:

```yaml
automation:
  - alias: "Holiday Schedule"
    trigger:
      - platform: state
        entity_id: calendar.holidays
        to: "on"
    action:
      - service: salus_rt310i.create_custom_schedule
        data:
          name: "Holiday Schedule"
          weekday_periods:
            - start: "08:00"
              end: "22:00"
              temp: 21
            - start: "22:00"
              end: "08:00"
              temp: 18
          weekend_periods:
            - start: "08:00"
              end: "22:00"
              temp: 21
            - start: "22:00"
              end: "08:00"
              temp: 18
```

---

## 💡 Schedule Design Tips

### 1. Temperature Transitions

Allow gradual temperature changes:
```yaml
# Instead of: 17°C → 21°C instantly
# Use gradual steps:
- 06:00: 18°C  # Start warming
- 06:30: 19°C  # Continue
- 07:00: 21°C  # Target reached
```

### 2. Overlap Prevention

Ensure no gaps or overlaps:
```yaml
# Good:
- start: "06:00", end: "08:00", temp: 21
- start: "08:00", end: "17:00", temp: 18

# Bad (gap):
- start: "06:00", end: "08:00", temp: 21
- start: "09:00", end: "17:00", temp: 18  # 8:00-9:00 undefined!
```

### 3. Energy Optimization

Strategic temperature timing:
- Lower temp during cheapest electricity hours
- Pre-heat before waking up
- Reduce temp 30 min before leaving
- Night setback for energy savings

### 4. Comfort Zones

Different temperatures for different activities:
- **Sleep**: 16-18°C
- **Work**: 19-20°C
- **Living**: 20-22°C
- **Mornings**: 21-22°C

---

## 🔍 Monitoring Schedules

### View Active Schedule

```yaml
# Check which schedule is active
{{ state_attr('switch.salus_YOUR_DEVICE_ID_schedule_master', 'active_schedule') }}

# Check if schedule is enabled
{{ states('switch.salus_YOUR_DEVICE_ID_schedule_master') }}
```

### Schedule Effectiveness

Track how well your schedule is working:

```yaml
# Create a template sensor
template:
  - sensor:
      - name: "Schedule Compliance"
        state: >
          {% set current = states('climate.salus_rt310i_YOUR_DEVICE_ID') | float %}
          {% set target = state_attr('climate.salus_rt310i_YOUR_DEVICE_ID', 'temperature') | float %}
          {% set diff = (current - target) | abs %}
          {{ 100 - (diff * 20) }}
        unit_of_measurement: "%"
```

---

## 📊 Schedule Comparison

| Feature | Comfort | Eco | Work From Home |
|---------|---------|-----|----------------|
| Weekday Morning | 21°C | 19°C | 21°C |
| Weekday Day | 18°C | 16°C | 20°C |
| Weekday Evening | 21°C | 19°C | 21°C |
| Night Temp | 17°C | 16°C | 17°C |
| Weekend Day | 21°C | 19°C | 21°C |
| Energy Efficiency | ★★★☆☆ | ★★★★★ | ★★★☆☆ |
| Comfort Level | ★★★★★ | ★★★☆☆ | ★★★★★ |

---

## 🆘 Troubleshooting

### Schedule Not Activating

1. Check master schedule switch is ON
2. Verify only one template is active
3. Check automation triggers
4. Review Home Assistant logs

### Temperature Not Following Schedule

1. Verify schedule periods cover 24 hours
2. Check for manual overrides
3. Ensure no conflicting automations
4. Review period start/end times

### Can't Create Custom Schedule

1. Validate YAML format
2. Check time format (HH:MM)
3. Ensure no period overlaps
4. Verify temperature ranges (5-35°C)

---

## 🎯 Best Practices

1. **Start Simple** - Use a template, then customize
2. **Test Gradually** - Try one day before full week
3. **Monitor First Week** - Adjust based on actual comfort
4. **Document Changes** - Note what works and what doesn't
5. **Seasonal Adjustments** - Update for summer/winter

---

## 📚 Additional Resources

- **Dashboard Templates**: See `/dashboards/README.md`
- **Automations**: See `/automations/README.md`
- **Services**: See `services.yaml`
- **API Docs**: See `API_DOCUMENTATION.md`

---

*Create the perfect heating schedule for your lifestyle!* 🌡️✨
