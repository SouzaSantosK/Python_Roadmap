from flask import render_template, request
from main import app

LENGTH_CONVERSIONS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.34,
}

WEIGHT_CONVERSIONS = {
    "mg": 0.001,
    "g": 1,
    "kg": 1000,
    "oz": 28.3495,
    "lb": 453.592,
}


@app.route("/length", methods=["GET", "POST"])
def length_converter():
    data = None
    if request.method == "POST":
        try:
            val = float(request.form.get("unit-value"))
            unit_from = request.form.get("convert-from")
            unit_to = request.form.get("convert-to")

            if not unit_from or not unit_to:
                raise ValueError("Please, select the units of measurement.")

            if val < 0:
                raise ValueError("The value cannot be negative.")

            result = val

            if unit_from != unit_to:
                meters = val * LENGTH_CONVERSIONS[unit_from]
                result = meters / LENGTH_CONVERSIONS[unit_to]

            data = {
                "original_val": val,
                "unit_from": unit_from,
                "result": round(result, 4),
                "unit_to": unit_to,
            }

        except ValueError as e:
            data = {"error": str(e)}
        except KeyError:
            data = {"error": "Measurement unit invalid."}
        except Exception:
            data = {"error": "Unexpected error."}

    return render_template("length.html", data=data)


@app.route("/weight", methods=["GET", "POST"])
def weight_converter():
    data = None
    if request.method == "POST":
        try:
            val = float(request.form.get("unit-value"))
            unit_from = request.form.get("convert-from")
            unit_to = request.form.get("convert-to")

            if not unit_from or not unit_to:
                raise ValueError("Please, select the units of measurement.")

            if val < 0:
                raise ValueError("The value cannot be negative.")

            result = val

            if unit_from != unit_to:
                gram = val * WEIGHT_CONVERSIONS[unit_from]
                result = gram / WEIGHT_CONVERSIONS[unit_to]

            data = {
                "original_val": val,
                "unit_from": unit_from,
                "result": round(result, 4),
                "unit_to": unit_to,
            }
        except ValueError as e:
            data = {"error": str(e)}
        except KeyError:
            data = {"error": "Measurement unit invalid."}
        except Exception:
            data = {"error": "Unexpected error."}

    return render_template("weight.html", data=data)


@app.route("/temperature", methods=["GET", "POST"])
def temperature_converter():
    data = None
    if request.method == "POST":
        try:
            val = float(request.form.get("unit-value"))
            unit_from = request.form.get("convert-from")
            unit_to = request.form.get("convert-to")

            if not unit_from or not unit_to:
                raise ValueError("Please, select the units of measurement.")

            result = val
            if unit_from != unit_to:
                celsius = val

                if unit_from == "f":
                    celsius = (val - 32) * 5 / 9
                elif unit_from == "k":
                    celsius = val - 273.15

                if unit_to == "f":
                    result = (celsius * 9 / 5) + 32
                elif unit_to == "k":
                    result = celsius + 273.15
                else:
                    result = celsius

            data = {
                "original_val": val,
                "unit_from": unit_from,
                "result": round(result, 4),
                "unit_to": unit_to,
            }

        except ValueError as e:
            data = {"error": str(e)}

    return render_template("temperature.html", data=data)
