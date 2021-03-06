import adafruit_requests
import socketpool
import ssl
import wifi
from adafruit_datetime import datetime
from adafruit_funhouse import FunHouse

funhouse = FunHouse(default_bg=None)

DELAY = 60
FEED = "temperature"
TEMPERATURE_OFFSET = (
    5  # Degrees C to adjust the temperature to compensate for board produced heat
)
HOUR_START = 21
HOUR_END = 7

# Turn things off
funhouse.peripherals.dotstars.fill(0)
funhouse.display.brightness = 0
funhouse.network.enabled = False


def get_secrets():
    # Get wifi details and more from a secrets.py file
    try:
        from secrets import secrets
        return secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise


def setup_requests(secrets):
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    return requests


def get_time(secrets) -> datetime:
    aio_username = secrets["aio_username"]
    aio_key = secrets["aio_key"]
    location = secrets["timezone"]
    TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s" % (
        aio_username, aio_key
    )
    TIME_URL += "&fmt=%25Y-%25m-%25dT%25H%3A%25M%3A%25S.%25L"
    datetime_str = requests.get(TIME_URL).text
    return datetime.fromisoformat(datetime_str)


def calibrate_temp(temperature):
    return temperature - TEMPERATURE_OFFSET


def convert_to_fahr(cel_temp):
    return (9 / 5) * cel_temp + 32


secrets = get_secrets()
requests = setup_requests(secrets)


def log_data():
    cel_temp = calibrate_temp(funhouse.peripherals.temperature)
    fahr_temp = convert_to_fahr(cel_temp)
    print("Logging Temperature")
    print("Temperature %0.1F" % (fahr_temp))
    # Turn on WiFi
    funhouse.network.enabled = True
    # Connect to WiFi
    funhouse.network.connect()
    # Push to IO using REST
    # funhouse.push_to_io(FEED, fahr_temp)

    current_datetime = get_time(secrets)
    if current_datetime.hour >= HOUR_END and current_datetime.hour < HOUR_START:
        print("Current date time %s" % (current_datetime.isoformat()))
        print("Sleeping during the day...")
        return

    response = requests.post(secrets["server_url"], json={
        "temperature": fahr_temp,
        "input_device_name": secrets["server_device_name"],
        "password": secrets["server_password"],
    })

    response_json = response.json()
    new_state = response_json["new_state"]
    if new_state is None:
        print("No status change")
    elif new_state:
        print("Toggling device on!")
    else:
        print("Toggling device off!")

    # Turn off WiFi
    funhouse.network.enabled = False


while True:
    log_data()
    print("Will check back in {} seconds...".format(DELAY))
    funhouse.enter_light_sleep(DELAY)
