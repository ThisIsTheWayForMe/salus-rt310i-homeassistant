# SALUS RT310i API Documentation

This document provides detailed information about the SALUS cloud API used by this integration.

## API Overview

**Base URL**: `https://salus-it500.com`

The SALUS API uses:
- Form-encoded POST requests (not JSON)
- Cookie-based session management
- MD5-hashed passwords
- HTTP redirects for authentication flow

## Authentication Flow

### 1. Login Request

**Endpoint**: `POST /public/login.php`

**Request Type**: `application/x-www-form-urlencoded`

**Parameters**:
```
IDemail: user@example.com
password: <MD5_HASH_OF_PASSWORD>
login: Login
```

**Password Hashing**:
```python
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**Response**: 
- Status 302 (Redirect) on success
- Sets session cookies: `PHPSESSID`, possibly others
- Redirects to control page

### 2. Get Token

**Endpoint**: `POST /public/control.php`

**Parameters**:
```
devId: YOUR_DEVICE_ID
```

**Response**:
- HTML page containing device controls
- Session is now established via cookies

## Data Operations

### Get Device Data

**Endpoint**: `GET /public/ajax_device_values.php`

**Parameters**:
```
devId: YOUR_DEVICE_ID
current: 1
```

**Response Example**:
```json
{
  "CH1currentRoomTemp": "21.5",
  "CH1currentSetPoint": "22.0",
  "CH1heatOnOff": "1",
  "CH1heatOnOffStatus": "1",
  "CH1autoOff": "0",
  "CH1scheduleOn": "0",
  ...additional fields...
}
```

### Key Response Fields

| Field | Description | Values |
|-------|-------------|--------|
| `CH1currentRoomTemp` | Current room temperature | Float as string (e.g., "21.5") |
| `CH1currentSetPoint` | Target temperature | Float as string (e.g., "22.0") |
| `CH1heatOnOff` | Heating system status | "0" = Off, "1" = On |
| `CH1heatOnOffStatus` | Heating relay status | "0" = Off, "1" = On |
| `CH1autoOff` | Auto mode off | "0" or "1" |
| `CH1scheduleOn` | Schedule enabled | "0" or "1" |

## Control Operations

### Set Temperature

**Endpoint**: `POST /includes/set.php`

**Request Type**: `application/x-www-form-urlencoded`

**Parameters**:
```
devId: YOUR_DEVICE_ID
current_tempZ1_set: 22.0
tempUnit: 0
```

**Parameter Details**:
- `devId`: Your device identifier
- `current_tempZ1_set`: Target temperature (5.0 - 35.0)
- `tempUnit`: Temperature unit (0 = Celsius, 1 = Fahrenheit)

**Response**:
- Status 200 on success
- May return HTML or simple text confirmation

### Set HVAC Mode

**Endpoint**: `POST /includes/set.php`

**Parameters**:
```
devId: YOUR_DEVICE_ID
auto: 1
```

**Parameter Details**:
- `devId`: Your device identifier
- `auto`: Mode setting (0 = Off, 1 = On/Heat)

**Response**:
- Status 200 on success

## Session Management

### Session Cookies

The API uses cookies to maintain sessions:
- **PHPSESSID**: PHP session identifier
- Other cookies may be set by the server

### Session Lifetime

- Sessions expire after inactivity (typically 30-60 minutes)
- The integration re-authenticates automatically when needed

### Re-authentication

If a request fails with authentication error:
1. Clear cookies
2. Perform login flow again
3. Retry the original request

## Rate Limiting

### Known Limits

- The SALUS server may block IPs making excessive requests
- Recommended polling interval: **5 minutes** minimum
- Multiple rapid requests may trigger IP blocking

### IP Blocking

If your IP is blocked:
- Wait 24 hours for automatic unblock
- Restart router to get new IP (if using DHCP/PPPoE)
- Contact SALUS support for manual unblock

## Data Types

### Temperature Values

- Stored as strings in API responses
- Format: Decimal with one decimal place (e.g., "21.5")
- Range: 5.0°C to 35.0°C
- Step: 0.5°C

### Boolean Values

- Represented as strings "0" or "1"
- "0" = False/Off
- "1" = True/On

## Error Handling

### Common Error Scenarios

1. **Authentication Failure**
   - Status: 200 (doesn't redirect on POST to login.php)
   - Solution: Verify credentials

2. **Session Expired**
   - Symptoms: Unexpected redirects or empty responses
   - Solution: Re-authenticate

3. **Invalid Device ID**
   - Symptoms: No data returned or error messages
   - Solution: Verify device ID from website

4. **IP Blocked**
   - Symptoms: Connection timeout or refused
   - Solution: Wait or get new IP

## API Request Examples

### Using curl

```bash
# Login
curl -X POST https://salus-it500.com/public/login.php \
  -d "IDemail=user@example.com" \
  -d "password=$(echo -n 'yourpassword' | md5sum | cut -d' ' -f1)" \
  -d "login=Login" \
  -c cookies.txt \
  -L

# Get device data
curl -X GET "https://salus-it500.com/public/ajax_device_values.php?devId=YOUR_DEVICE_ID&current=1" \
  -b cookies.txt

# Set temperature
curl -X POST https://salus-it500.com/includes/set.php \
  -d "devId=YOUR_DEVICE_ID" \
  -d "current_tempZ1_set=22.0" \
  -d "tempUnit=0" \
  -b cookies.txt
```

### Using Python aiohttp

```python
import aiohttp
import hashlib

async def login_and_get_data(username, password, device_id):
    async with aiohttp.ClientSession() as session:
        # Login
        password_hash = hashlib.md5(password.encode()).hexdigest()
        login_data = {
            'IDemail': username,
            'password': password_hash,
            'login': 'Login'
        }
        
        async with session.post(
            'https://salus-it500.com/public/login.php',
            data=login_data,
            allow_redirects=False
        ) as resp:
            print(f"Login status: {resp.status}")
        
        # Get token
        async with session.post(
            'https://salus-it500.com/public/control.php',
            data={'devId': device_id}
        ) as resp:
            print(f"Token status: {resp.status}")
        
        # Get device data
        async with session.get(
            f'https://salus-it500.com/public/ajax_device_values.php',
            params={'devId': device_id, 'current': 1}
        ) as resp:
            data = await resp.json()
            print(f"Temperature: {data.get('CH1currentRoomTemp')}°C")
            return data
```

## Additional Device Fields

The API returns many additional fields that could be used for future enhancements:

- `CH1tempCutoutStatus`: Temperature cutout status
- `CH1tempLowAlarmStatus`: Low temperature alarm
- `CH1tempHighAlarmStatus`: High temperature alarm
- `CH1frostProtectionTemp`: Frost protection temperature
- `deviceLockedStatus`: Device lock status
- `holidayEnabled`: Holiday mode enabled
- `progMode`: Programming mode
- Various time and schedule related fields

## Best Practices

1. **Minimize API Calls**
   - Cache data when possible
   - Use 5-minute polling minimum
   - Batch operations when feasible

2. **Handle Sessions Properly**
   - Reuse session cookies
   - Re-authenticate on session expiry
   - Don't create multiple sessions

3. **Error Recovery**
   - Implement exponential backoff
   - Retry with fresh authentication
   - Log errors for debugging

4. **User Experience**
   - Show connection status
   - Indicate when data is stale
   - Provide clear error messages

## Security Considerations

1. **Password Storage**
   - Never log passwords
   - Use Home Assistant's encrypted storage
   - Hash passwords only for transmission

2. **Session Security**
   - Sessions are tied to IP address
   - Don't share session cookies
   - Clear sessions on logout

3. **Data Privacy**
   - Temperature data is personal
   - API calls expose user habits
   - Consider privacy implications

## Disclaimer

This is unofficial API documentation. The SALUS API may change without notice. Use at your own risk.
