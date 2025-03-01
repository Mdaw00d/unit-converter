import streamlit as st
import pint 

# Set up unit registry
ureg = pint.UnitRegistry()

# Streamlit app title
st.title("CONVERTO")

# Comprehensive unit mapping (friendly name to pint unit)
unit_mapping = {
    # Length
    "meters": "meter",
    "kilometers": "kilometer",
    "centimeters": "centimeter",
    "millimeters": "millimeter",
    "miles": "mile",
    "yards": "yard",
    "feet": "foot",
    "inches": "inch",

    # Weight
    "kilograms": "kilogram",
    "grams": "gram",
    "pounds": "pound",
    "ounces": "ounce",

    # Volume
    "liters": "liter",
    "milliliters": "milliliter",
    "gallons": "gallon",
    "cups": "cup",

    # Area
    "square meters": "m**2",
    "square kilometers": "km**2",
    "square miles": "mile**2",
    "acres": "acre",
    "hectares": "hectare",
    "square yards": "yd**2",
    "square feet": "ft**2",
    "square inches": "in**2",

    # Data Transfer Rate
    "bits per second": "bit / second",
    "kilobits per second": "kilobit / second",
    "megabits per second": "megabit / second",
    "gigabits per second": "gigabit / second",

    # Digital Storage
    "bits": "bit",
    "kilobits": "kilobit",
    "megabits": "megabit",
    "gigabits": "gigabit",
    "terabits": "terabit",
    "bytes": "byte",
    "kilobytes": "kilobyte",
    "megabytes": "megabyte",
    "gigabytes": "gigabyte",
    "terabytes": "terabyte",

    # Energy
    "joules": "joule",
    "kilojoules": "kilojoule",
    "calories": "calorie",
    "kilocalories": "kilocalorie",
    "watt hours": "watt_hour",
    "kilowatt hours": "kilowatt_hour",

    # Frequency
    "hertz": "hertz",
    "kilohertz": "kilohertz",
    "megahertz": "megahertz",
    "gigahertz": "gigahertz",

    # Plane Angle
    "degrees": "degree",
    "radians": "radian",
    "gradians": "gradian",

    # Pressure
    "pascals": "pascal",
    "hectopascals": "hectopascal",
    "kilopascals": "kilopascal",
    "bars": "bar",
    "psi": "psi",
    "atmospheres": "atmosphere",

    # Speed
    "meters per second": "meter/second",
    "kilometers per hour": "kilometer/hour",
    "miles per hour": "mile/hour",
    "knots": "knot"
}

# Supported categories and units
unit_categories = {
    "Length": ["meters", "kilometers", "centimeters", "millimeters", "miles", "yards", "feet", "inches"],
    "Weight": ["kilograms", "grams", "pounds", "ounces"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liters", "milliliters", "gallons", "cups"],
    "Area": list(unit_mapping.keys() & {
        "square meters", "square kilometers", "square miles", "acres", "hectares", "square yards", "square feet", "square inches"
    }),
    "Data Transfer Rate": ["bits per second", "kilobits per second", "megabits per second", "gigabits per second"],
    "Digital Storage": ["bits", "kilobits", "megabits", "gigabits", "terabits", "bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"],
    "Energy": ["joules", "kilojoules", "calories", "kilocalories", "watt hours", "kilowatt hours"],
    "Frequency": ["hertz", "kilohertz", "megahertz", "gigahertz"],
    "Fuel Economy": ["kilometers per liter", "miles per gallon"],
    "Plane Angle": ["degrees", "radians", "gradians"],
    "Pressure": ["pascals", "hectopascals", "kilopascals", "bars", "psi", "atmospheres"],
    "Speed": ["meters per second", "kilometers per hour", "miles per hour", "knots"],
}

# Select category
category = st.selectbox("Select Category", list(unit_categories.keys()))

# Select units (from and to)
units = unit_categories[category]
from_unit = st.selectbox("Convert from", units)
to_unit = st.selectbox("Convert to", units)

# Input value
value = st.number_input("Enter value to convert", value=0.0)

# Temperature handling - special case
def convert_temperature(value, from_unit, to_unit):
    if from_unit == "celsius" and to_unit == "fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return (value - 32) * 5/9
    elif from_unit == "celsius" and to_unit == "kelvin":
        return value + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        return value - 273.15
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        return (value - 32) * 5/9 + 273.15
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        return (value - 273.15) * 9/5 + 32
    else:
        return value  # Same unit conversion

# Conversion logic
if st.button("Convert"):
    try:
        if category == "Temperature":
            result = convert_temperature(value, from_unit, to_unit)

        elif category == "Fuel Economy":
            if from_unit == "kilometers per liter" and to_unit == "miles per gallon":
                result = value * 2.35215
            elif from_unit == "miles per gallon" and to_unit == "kilometers per liter":
                result = value / 2.35215
            else:
                result = value

        else:
            # Always apply the unit mapping
            from_unit_pint = unit_mapping.get(from_unit, from_unit.replace(" ", "_"))
            to_unit_pint = unit_mapping.get(to_unit, to_unit.replace(" ", "_"))

            quantity = value * ureg(from_unit_pint)
            result = quantity.to(to_unit_pint).magnitude

        st.success(f"{value} {from_unit} = {result:.3f} {to_unit}")

    except Exception as e:
        st.error(f"Conversion error: {e}")
