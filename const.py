"""Constants for the SALUS RT310i integration."""

DOMAIN = "salus_rt310i"

# SALUS API endpoints (based on real salus-it500.com implementation)
SALUS_BASE_URL = "https://salus-it500.com"
URL_LOGIN = f"{SALUS_BASE_URL}/public/login.php"
URL_GET_TOKEN = f"{SALUS_BASE_URL}/public/control.php"
URL_GET_DATA = f"{SALUS_BASE_URL}/public/ajax_device_values.php"
URL_SET_DATA = f"{SALUS_BASE_URL}/includes/set.php"

# Configuration
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_DEVICE_ID = "device_id"

# Attributes
ATTR_CURRENT_TEMP = "CH1currentRoomTemp"
ATTR_TARGET_TEMP = "CH1currentSetPoint"
ATTR_HVAC_MODE = "CH1heatOnOffStatus"
ATTR_HEATING_ON = "CH1heatOnOff"

# Default values
DEFAULT_NAME = "SALUS RT310i"
DEFAULT_MIN_TEMP = 5.0
DEFAULT_MAX_TEMP = 35.0
DEFAULT_TEMP_STEP = 0.5
