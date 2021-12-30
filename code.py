import adafruit_requests
import socketpool
import ssl
import wifi
from adafruit_funhouse import FunHouse

funhouse = FunHouse(default_bg=None)

DELAY = 60
FEED = "temperature"
TEMPERATURE_OFFSET = (
    5  # Degrees C to adjust the temperature to compensate for board produced heat
)

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


secrets = get_secrets()
requests = setup_requests(secrets)


def log_data():
    cel_temp = funhouse.peripherals.temperature - TEMPERATURE_OFFSET
    fahr_temp = (9/5) * cel_temp + 32
    print("Logging Temperature")
    print("Temperature %0.1F" % (fahr_temp))
    # Turn on WiFi
    funhouse.network.enabled = True
    # Connect to WiFi
    funhouse.network.connect()
    # Push to IO using REST
    # funhouse.push_to_io(FEED, fahr_temp)

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
    print("Sleeping for {} seconds...".format(DELAY))
    funhouse.enter_light_sleep(DELAY)
