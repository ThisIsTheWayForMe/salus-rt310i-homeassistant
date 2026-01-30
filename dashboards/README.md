# SALUS RT310i Dashboard Examples

This directory contains pre-built Lovelace dashboard cards for your SALUS RT310i thermostat.

## Quick Setup

1. Copy any of the YAML examples below
2. Go to your Lovelace dashboard
3. Click "Edit Dashboard" → "Add Card" → "Manual"
4. Paste the YAML
5. Replace `YOUR_DEVICE_ID` with your actual device ID

## Available Dashboards

### 1. Minimal Card (`minimal.yaml`)
### 2. Detailed Card (`detailed.yaml`)
### 3. Energy Dashboard (`energy.yaml`)
### 4. Mobile Compact (`mobile.yaml`)

---

## 1. Minimal Card

Simple and clean thermostat control.

```yaml
type: thermostat
entity: climate.salus_rt310i_YOUR_DEVICE_ID
name: Living Room
```

---

## 2. Detailed Dashboard Card

Full-featured card with all sensors and controls.

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.salus_rt310i_YOUR_DEVICE_ID
    name: SALUS Thermostat
    features:
      - type: climate-hvac-modes
        hvac_modes:
          - heat
          - 'off'
  
  - type: entities
    title: Status
    entities:
      - entity: sensor.salus_rt310i_YOUR_DEVICE_ID_operation_mode
        name: Mode
        icon: mdi:thermostat-auto
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating
        name: Heating Active
      - entity: sensor.salus_rt310i_YOUR_DEVICE_ID_heating_demand
        name: Heating Demand
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_schedule
        name: Schedule
      - type: divider
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_connection
        name: Connection Status
      - entity: sensor.salus_rt310i_YOUR_DEVICE_ID_last_update
        name: Last Updated
  
  - type: button
    name: Boost Heating (30 min)
    icon: mdi:fire
    tap_action:
      action: call-service
      service: salus_rt310i.boost_heating
      service_data:
        entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        duration: 30
```

---

## 3. Energy Monitoring Dashboard

Track heating activity and temperature trends.

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.salus_rt310i_YOUR_DEVICE_ID
  
  - type: gauge
    entity: sensor.salus_rt310i_YOUR_DEVICE_ID_heating_demand
    name: Heating Demand
    min: 0
    max: 100
    severity:
      green: 0
      yellow: 50
      red: 80
  
  - type: history-graph
    title: Temperature History (24h)
    hours_to_show: 24
    refresh_interval: 300
    entities:
      - entity: climate.salus_rt310i_YOUR_DEVICE_ID
        name: Current
      - entity: sensor.salus_rt310i_YOUR_DEVICE_ID_target_temp
        name: Target
  
  - type: history-graph
    title: Heating Activity (24h)
    hours_to_show: 24
    refresh_interval: 300
    entities:
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating
        name: Heating On
```

---

## 4. Mobile Compact Card

Optimized for mobile devices.

```yaml
type: vertical-stack
cards:
  - type: custom:button-card
    entity: climate.salus_rt310i_YOUR_DEVICE_ID
    name: Thermostat
    show_state: true
    show_icon: true
    icon: mdi:thermostat
    styles:
      card:
        - height: 80px
      name:
        - font-size: 16px
        - font-weight: bold
      state:
        - font-size: 20px
    tap_action:
      action: more-info
  
  - type: horizontal-stack
    cards:
      - type: button
        entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating
        name: Heating
        show_state: true
        icon: mdi:fire
      - type: button
        entity: sensor.salus_rt310i_YOUR_DEVICE_ID_operation_mode
        name: Mode
        show_state: true
        icon: mdi:cog
  
  - type: entities
    entities:
      - entity: sensor.salus_rt310i_YOUR_DEVICE_ID_heating_demand
        name: Demand
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_schedule
        name: Schedule
```

---

## 5. Advanced Control Panel

With quick action buttons.

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.salus_rt310i_YOUR_DEVICE_ID
    name: SALUS RT310i
  
  - type: horizontal-stack
    cards:
      - type: button
        name: Boost 30m
        icon: mdi:fire-circle
        tap_action:
          action: call-service
          service: salus_rt310i.boost_heating
          service_data:
            entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
            duration: 30
        hold_action:
          action: call-service
          service: salus_rt310i.boost_heating
          service_data:
            entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
            duration: 60
      
      - type: button
        name: Boost 1h
        icon: mdi:fire
        tap_action:
          action: call-service
          service: salus_rt310i.boost_heating
          service_data:
            entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
            duration: 60
      
      - type: button
        name: Comfort
        icon: mdi:sofa
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
            temperature: 21
      
      - type: button
        name: Eco
        icon: mdi:leaf
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
            temperature: 18
  
  - type: glance
    entities:
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating
        name: Heating
      - entity: sensor.salus_rt310i_YOUR_DEVICE_ID_heating_demand
        name: Demand
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_schedule
        name: Schedule
      - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_connection
        name: Online
```

---

## 6. Picture Elements Dashboard

Beautiful visual dashboard (requires custom images).

```yaml
type: picture-elements
image: /local/thermostat-background.jpg
elements:
  - type: state-label
    entity: climate.salus_rt310i_YOUR_DEVICE_ID
    attribute: current_temperature
    style:
      top: 30%
      left: 50%
      font-size: 48px
      font-weight: bold
      color: white
      text-shadow: 2px 2px 4px rgba(0,0,0,0.8)
  
  - type: state-label
    entity: sensor.salus_rt310i_YOUR_DEVICE_ID_target_temp
    prefix: "Target: "
    suffix: "°C"
    style:
      top: 45%
      left: 50%
      font-size: 24px
      color: white
      text-shadow: 1px 1px 2px rgba(0,0,0,0.8)
  
  - type: state-icon
    entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating
    style:
      top: 60%
      left: 50%
      --mdc-icon-size: 60px
    tap_action:
      action: more-info
```

---

## Tips for Customization

### Change Colors
```yaml
styles:
  card:
    - background-color: '#1a1a1a'
  name:
    - color: '#00aaff'
```

### Add Icons
```yaml
icon: mdi:thermometer
# Find more icons at: https://materialdesignicons.com/
```

### Conditional Visibility
```yaml
conditions:
  - entity: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating
    state: 'on'
```

---

## Requirements

Some cards require custom components:
- **button-card**: Install via HACS for advanced button customization
- **mini-graph-card**: For compact graphs

Install these through HACS → Frontend for best results.

---

## Need Help?

Check the main README.md for more information or create an issue on GitHub.

---

## 7. Schedule Management Dashboard

Complete schedule control interface.

```yaml
type: vertical-stack
cards:
  # Current Status
  - type: glance
    title: Schedule Status
    entities:
      - entity: switch.salus_rt310i_YOUR_DEVICE_ID_schedule_master
        name: Enabled
      - entity: sensor.salus_rt310i_YOUR_DEVICE_ID_operation_mode
        name: Mode
      - entity: climate.salus_rt310i_YOUR_DEVICE_ID
        name: Current
  
  # Schedule Templates
  - type: entities
    title: Schedule Templates
    entities:
      - entity: switch.salus_rt310i_YOUR_DEVICE_ID_schedule_comfort
        name: Comfort Schedule
        icon: mdi:sofa
        secondary_info: "21°C comfort, 18°C away"
      
      - entity: switch.salus_rt310i_YOUR_DEVICE_ID_schedule_eco
        name: Eco Schedule
        icon: mdi:leaf
        secondary_info: "19°C comfort, 16°C away"
      
      - entity: switch.salus_rt310i_YOUR_DEVICE_ID_schedule_working_from_home
        name: Work From Home
        icon: mdi:home-account
        secondary_info: "20°C work, 21°C breaks"
  
  # Quick Actions
  - type: horizontal-stack
    cards:
      - type: button
        name: Morning Boost
        icon: mdi:weather-sunny
        tap_action:
          action: call-service
          service: salus_rt310i.apply_schedule_period
          service_data:
            entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
            start_time: "06:00"
            end_time: "09:00"
            temperature: 22
            days: ["mon", "tue", "wed", "thu", "fri"]
      
      - type: button
        name: Night Mode
        icon: mdi:weather-night
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
            temperature: 17
      
      - type: button
        name: Away
        icon: mdi:home-export-outline
        tap_action:
          action: call-service
          service: switch.turn_off
          service_data:
            entity_id: switch.salus_rt310i_YOUR_DEVICE_ID_schedule_master
```

---

## 8. Weekly Schedule Planner

Visual weekly schedule overview.

```yaml
type: markdown
title: Weekly Heating Schedule
content: >
  ## Current Schedule: {{ state_attr('switch.salus_rt310i_YOUR_DEVICE_ID_schedule_master', 'active_schedule') or 'None' }}
  
  {% set schedule = state_attr('switch.salus_rt310i_YOUR_DEVICE_ID_schedule_comfort', 'weekday_periods') %}
  
  ### Weekday Schedule (Mon-Fri)
  {% for period in schedule %}
  - **{{ period.start }} - {{ period.end }}**: {{ period.temp }}°C
  {% endfor %}
  
  {% set weekend = state_attr('switch.salus_rt310i_YOUR_DEVICE_ID_schedule_comfort', 'weekend_periods') %}
  
  ### Weekend Schedule (Sat-Sun)
  {% for period in weekend %}
  - **{{ period.start }} - {{ period.end }}**: {{ period.temp }}°C
  {% endfor %}
  
  ---
  
  **Status**: {{ 'Active ✅' if is_state('switch.salus_rt310i_YOUR_DEVICE_ID_schedule_master', 'on') else 'Disabled ❌' }}
```

