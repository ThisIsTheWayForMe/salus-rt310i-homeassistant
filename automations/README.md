# SALUS RT310i Automation Examples

Smart automation ideas for your SALUS thermostat.

## Table of Contents

1. [Temperature Schedules](#temperature-schedules)
2. [Presence Detection](#presence-detection)
3. [Weather-Based Control](#weather-based-control)
4. [Energy Saving](#energy-saving)
5. [Notifications](#notifications)
6. [Advanced Scenarios](#advanced-scenarios)

---

## Temperature Schedules

### Morning Warm-Up

Heat the house before you wake up.

```yaml
automation:
  - alias: "Morning Warm-Up"
    description: "Heat house 30 minutes before wake-up time"
    trigger:
      - platform: time
        at: "06:30:00"
    condition:
      - condition: time
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 21
```

### Night Time Setback

Lower temperature at bedtime.

```yaml
automation:
  - alias: "Night Setback"
    description: "Lower temperature at night"
    trigger:
      - platform: time
        at: "22:30:00"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 17
```

### Weekend Schedule

Different schedule for weekends.

```yaml
automation:
  - alias: "Weekend Morning"
    description: "Later wake-up on weekends"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: time
        weekday:
          - sat
          - sun
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 21
```

---

## Presence Detection

### Away Mode

Lower temperature when everyone leaves.

```yaml
automation:
  - alias: "Away Mode - Lower Temperature"
    description: "Set eco temperature when house is empty"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "not_home"
        for:
          minutes: 30
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 16
      - service: notify.mobile_app
        data:
          title: "🏠 Away Mode"
          message: "Temperature lowered to 16°C"
```

### Welcome Home

Boost heating when arriving home.

```yaml
automation:
  - alias: "Welcome Home - Boost Heat"
    description: "Boost heating when arriving home"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "home"
    condition:
      - condition: numeric_state
        entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        attribute: current_temperature
        below: 19
    action:
      - service: salus_rt310i.boost_heating
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          duration: 60
          temperature: 22
      - service: notify.mobile_app
        data:
          title: "🔥 Welcome Home"
          message: "Heating boosted to 22°C for 1 hour"
```

### Proximity-Based Pre-Heating

Start heating when approaching home.

```yaml
automation:
  - alias: "Pre-Heat When Approaching"
    description: "Start heating when within 5km of home"
    trigger:
      - platform: numeric_state
        entity_id: proximity.home
        below: 5
    condition:
      - condition: state
        entity_id: group.all_persons
        state: "not_home"
      - condition: numeric_state
        entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        attribute: current_temperature
        below: 18
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 20
```

---

## Weather-Based Control

### Cold Day Boost

Increase temperature on very cold days.

```yaml
automation:
  - alias: "Cold Day Temperature Boost"
    description: "Increase target temp when outdoor temp is very low"
    trigger:
      - platform: numeric_state
        entity_id: weather.home
        attribute: temperature
        below: 0
        for:
          hours: 1
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 22
```

### Sunny Day Optimization

Lower heating when sun is shining.

```yaml
automation:
  - alias: "Sunny Day - Lower Heating"
    description: "Reduce heating on sunny days"
    trigger:
      - platform: state
        entity_id: weather.home
        attribute: condition
        to: "sunny"
    condition:
      - condition: time
        after: "09:00:00"
        before: "16:00:00"
      - condition: numeric_state
        entity_id: sun.sun
        attribute: elevation
        above: 20
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 19
```

---

## Energy Saving

### Peak Hours Reduction

Lower temperature during peak electricity hours.

```yaml
automation:
  - alias: "Peak Hours - Reduce Heating"
    description: "Lower temp during peak electricity pricing"
    trigger:
      - platform: time
        at: "17:00:00"
    condition:
      - condition: time
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 19
  
  - alias: "Off-Peak Hours - Resume Heating"
    description: "Resume normal temp after peak hours"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 21
```

### Window Open Detection

Turn off heating when windows are open.

```yaml
automation:
  - alias: "Window Open - Heating Off"
    description: "Turn off heating when window is opened"
    trigger:
      - platform: state
        entity_id: binary_sensor.window_living_room
        to: "on"
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          hvac_mode: "off"
      - service: notify.mobile_app
        data:
          title: "🪟 Window Opened"
          message: "Heating turned off to save energy"
  
  - alias: "Window Closed - Heating On"
    description: "Resume heating when window is closed"
    trigger:
      - platform: state
        entity_id: binary_sensor.window_living_room
        to: "off"
        for:
          minutes: 2
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          hvac_mode: "heat"
```

---

## Notifications

### Temperature Alerts

Alert when temperature is too low.

```yaml
automation:
  - alias: "Low Temperature Alert"
    description: "Notify when temperature drops too low"
    trigger:
      - platform: numeric_state
        entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        attribute: current_temperature
        below: 15
        for:
          minutes: 30
    action:
      - service: notify.mobile_app
        data:
          title: "❄️ Low Temperature Alert"
          message: "Home temperature is {{ states('climate.salus_rt310i_YOUR_DEVICE_ID') }}°C"
          data:
            actions:
              - action: "BOOST_HEATING"
                title: "Boost Heating"
```

### Heating Stuck Alert

Alert if heating is on but temperature not rising.

```yaml
automation:
  - alias: "Heating Not Working Alert"
    description: "Alert if heating is on but temp not rising"
    trigger:
      - platform: state
        entity_id: binary_sensor.salus_rt310i_YOUR_DEVICE_ID_heating
        to: "on"
        for:
          hours: 2
    condition:
      - condition: template
        value_template: >
          {% set current = state_attr('climate.salus_rt310i_YOUR_DEVICE_ID', 'current_temperature') %}
          {% set target = state_attr('climate.salus_rt310i_YOUR_DEVICE_ID', 'temperature') %}
          {{ current < target - 2 }}
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Heating Issue"
          message: "Heating has been on for 2 hours but temperature not reaching target"
```

### Daily Heating Report

Send daily heating activity summary.

```yaml
automation:
  - alias: "Daily Heating Report"
    description: "Send heating summary every evening"
    trigger:
      - platform: time
        at: "21:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "📊 Daily Heating Report"
          message: >
            Today's heating stats:
            Current: {{ state_attr('climate.salus_rt310i_YOUR_DEVICE_ID', 'current_temperature') }}°C
            Heating was active: {{ states('sensor.salus_rt310i_YOUR_DEVICE_ID_heating_demand') }}%
            Status: {{ states('sensor.salus_rt310i_YOUR_DEVICE_ID_operation_mode') }}
```

---

## Advanced Scenarios

### Smart Night Mode

Gradually lower temperature at night.

```yaml
automation:
  - alias: "Gradual Night Cooling"
    description: "Gradually lower temperature over 2 hours"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 20
      - delay:
          minutes: 30
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 19
      - delay:
          minutes: 30
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 18
      - delay:
          minutes: 30
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 17
```

### Adaptive Heating Based on Activity

Adjust based on motion sensors.

```yaml
automation:
  - alias: "Activity-Based Heating"
    description: "Boost temp when motion detected in evening"
    trigger:
      - platform: state
        entity_id: binary_sensor.living_room_motion
        to: "on"
    condition:
      - condition: time
        after: "17:00:00"
        before: "23:00:00"
      - condition: numeric_state
        entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        attribute: current_temperature
        below: 20
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 21
```

### Holiday Mode

Automatic holiday mode with date range.

```yaml
automation:
  - alias: "Holiday Mode Start"
    description: "Activate holiday mode"
    trigger:
      - platform: time
        at: "00:00:00"
    condition:
      - condition: template
        value_template: >
          {% set start_date = '2024-12-20' %}
          {% set end_date = '2025-01-05' %}
          {% set today = now().date() | string %}
          {{ start_date <= today <= end_date }}
    action:
      - service: salus_rt310i.set_holiday_mode
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          enabled: true
          temperature: 15
```

---

## Voice Control Examples

### Alexa/Google Home Routines

```yaml
# Example voice commands after setup:
# "Alexa, boost the heating"
# "Hey Google, set thermostat to comfort mode"
# "Alexa, what's the current temperature?"

script:
  boost_heating_voice:
    alias: "Boost Heating"
    sequence:
      - service: salus_rt310i.boost_heating
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          duration: 30
  
  comfort_mode:
    alias: "Comfort Mode"
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 21
  
  eco_mode:
    alias: "Eco Mode"
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.salus_rt310i_YOUR_DEVICE_ID
        data:
          temperature: 18
```

---

## Tips for Creating Automations

1. **Test First**: Test automations manually before enabling them
2. **Use Conditions**: Prevent unwanted triggers with conditions
3. **Add Delays**: Use delays to avoid rapid changes
4. **Monitor**: Check automation traces to debug issues
5. **Notifications**: Add notifications to track automation activity

---

## Debugging Automations

Enable automation traces in Home Assistant:
1. Go to Settings → Automations & Scenes
2. Click on your automation
3. Click "Traces" to see execution history

---

## Need More Ideas?

Check out the [Home Assistant Cookbook](https://www.home-assistant.io/cookbook/) for more automation examples!
