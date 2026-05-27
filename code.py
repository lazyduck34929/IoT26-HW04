from flask import Flask, render_template
from gpiozero import LED


app = Flask(__name__)

pins = {
    23: {"name": "GPIO 23", "state": "GPIO.LOW", "device": LED(23)},
    24: {"name": "GPIO 24", "state": "GPIO.LOW", "device": LED(24)},
}

for pin in pins:
    pins[pin]["device"].off()


def update_pin_states():
    for pin in pins:
        if pins[pin]["device"].is_active:
            pins[pin]["state"] = "GPIO.HIGH"
        else:
            pins[pin]["state"] = "GPIO.LOW"


@app.route("/")
def main():
    update_pin_states()
    return render_template("main.html", pins=pins)


@app.route("/<change_pin>/<action>")
def action(change_pin, action):
    change_pin = int(change_pin)

    if action == "on":
        pins[change_pin]["device"].on()
    if action == "off":
        pins[change_pin]["device"].off()

    update_pin_states()
    return render_template("main.html", pins=pins)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)
