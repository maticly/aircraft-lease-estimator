!pip install flask flask-cors
import pandas as pd
import numpy as np
import airportsdata
from ipywidgets import Text, IntText, VBox, Output, Button, HBox
from IPython.display import display
from geopy.distance import geodesic

# DATA DEFINITION
aircraft_data = {
    "Boeing 737-800": {
        "fuel_burn": 2.6,
        "crew": 5,
        "pilots": 2,
        "range": 2935,
        "base_price": 255000,
        "economy": 175,
        "business": 18,
        "economy_min": 162,
        "economy_max": 189,
        "business_min": 12,
        "business_max": 24
    },
    "Boeing 737 MAX 8": {
        "fuel_burn": 2.2,
        "crew": 5,
        "pilots": 2,
        "range": 3550,
        "base_price": 340000,
        "economy": 192,
        "business": 18,
        "economy_min": 174,
        "economy_max": 210,
        "business_min": 12,
        "business_max": 24
    },
    "Boeing 747-400 VIP": {
        "fuel_burn": 10,
        "crew": 10,
        "pilots": 2,
        "range": 7700,
        "base_price": 1500000,
        "economy": 0,
        "business": 100,
        "economy_min": 0,
        "economy_max": 0,
        "business_min": 50,
        "business_max": 200
    },
    "Boeing 767-300 HD": {
        "fuel_burn": 5.0,
        "crew": 7,
        "pilots": 2,
        "range": 6000,
        "base_price": 700000,
        "economy": 200,
        "business": 30,
        "economy_min": 180,
        "economy_max": 220,
        "business_min": 20,
        "business_max": 40
    },
    "Boeing 777-300ER": {
        "fuel_burn": 6.2,
        "crew": 8,
        "pilots": 2,
        "range": 7370,
        "base_price": 1300000,
        "economy": 423,
        "business": 50,
        "economy_min": 396,
        "economy_max": 451,
        "business_min": 40,
        "business_max": 60
    },
    "Boeing 787-9": {
        "fuel_burn": 5.4,
        "crew": 9,
        "pilots": 2,
        "range": 7530,
        "base_price": 1300000,
        "economy": 268,
        "business": 25,
        "economy_min": 240,
        "economy_max": 296,
        "business_min": 0,
        "business_max": 50
    },
    "Airbus A320": {
        "fuel_burn": 2.4,
        "crew": 5,
        "pilots": 2,
        "range": 3500,
        "base_price": 260000,
        "economy": 163,
        "business": 14,
        "economy_min": 140,
        "economy_max": 186,
        "business_min": 8,
        "business_max": 20
    },
    "Airbus A321": {
        "fuel_burn": 2.8,
        "crew": 5,
        "pilots": 2,
        "range": 3600,
        "base_price": 300000,
        "economy": 205,
        "business": 26,
        "economy_min": 185,
        "economy_max": 236,
        "business_min": 16,
        "business_max": 36
    },
    "Airbus A321neo": {
        "fuel_burn": 2.25,
        "crew": 5,
        "pilots": 2,
        "range": 4350,
        "base_price": 385000,
        "economy": 215,
        "business": 26,
        "economy_min": 190,
        "economy_max": 240,
        "business_min": 16,
        "business_max": 36
    },
    "Airbus A220": {
        "fuel_burn": 2.0,
        "crew": 4,
        "pilots": 2,
        "range": 3575,
        "base_price": 235000,
        "economy": 120,
        "business": 14,
        "economy_min": 100,
        "economy_max": 140,
        "business_min": 8,
        "business_max": 20
    },
    "Airbus A330-300": {
        "fuel_burn": 5.4,
        "crew": 8,
        "pilots": 2,
        "range": 6350,
        "base_price": 775000,
        "economy": 296,
        "business": 35,
        "economy_min": 277,
        "economy_max": 315,
        "business_min": 20,
        "business_max": 50
    },
    "Airbus A330neo": {
        "fuel_burn": 4.9,
        "crew": 8,
        "pilots": 2,
        "range": 7200,
        "base_price": 925000,
        "economy": 290,
        "business": 40,
        "economy_min": 280,
        "economy_max": 300,
        "business_min": 30,
        "business_max": 50
    },
    "Airbus A350": {
        "fuel_burn": 5.3,
        "crew": 10,
        "pilots": 2,
        "range": 8100,
        "base_price": 1300000,
        "economy": 325,
        "business": 40,
        "economy_min": 300,
        "economy_max": 350,
        "business_min": 30,
        "business_max": 50
    }
}

seat_pricing_hour = {"economy": 30, "business": 100}
fuel_per_gallon = 3.83
airport_fees = {"Major Hub": 20000, "Regional": 10000, "Small": 5000}
crew_cost_per_hour = 50
pilot_cost_per_hour = 150
carbon_offset_fee = 0.05
maintenance_cost_per_hour = 500
insurance_multiplier = 0.05

# HELPER FUNCTIONS
def calculate_fuel_cost(aircraft_model, distance):
    aircraft = aircraft_data[aircraft_model]
    gallons_needed = aircraft["fuel_burn"] * distance
    return gallons_needed * fuel_per_gallon

def calculate_airport_fees(airport_class, stopovers):
    return airport_fees.get(airport_class, 0) * stopovers

def calculate_crew_cost(aircraft_model, flight_hours):
    crew_count = aircraft_data[aircraft_model]["crew"]
    return crew_count * crew_cost_per_hour * flight_hours

def calculate_pilot_cost(aircraft_model, flight_hours):
    pilot_count = aircraft_data[aircraft_model]["pilots"]
    return pilot_count * pilot_cost_per_hour * flight_hours

def calculate_maintenance_cost(flight_hours):
    return flight_hours * maintenance_cost_per_hour

def calculate_insurance_cost(aircraft_model):
    base_price = aircraft_data[aircraft_model]["base_price"]
    return base_price * insurance_multiplier

def calculate_carbon_offset_cost(distance):
    return carbon_offset_fee * distance

def calculate_seat_cost(aircraft_model, economy_seats, business_seats):
    aircraft = aircraft_data[aircraft_model]
    if not (aircraft["economy_min"] <= economy_seats <= aircraft["economy_max"]):
        raise ValueError(f"Economy seats must be between {aircraft['economy_min']} and {aircraft['economy_max']}.")
    if not (aircraft["business_min"] <= business_seats <= aircraft["business_max"]):
        raise ValueError(f"Business seats must be between {aircraft['business_min']} and {aircraft['business_max']}.")

    economy_cost = economy_seats * seat_pricing_hour["economy"]
    if economy_seats > aircraft["economy_min"]:
        economy_cost += (economy_seats - aircraft["economy_min"]) * seat_pricing_hour["economy"]

    business_cost = business_seats * seat_pricing_hour["business"]
    if business_seats > aircraft["business_min"]:
        business_cost += (business_seats - aircraft["business_min"]) * seat_pricing_hour["business"]

    return economy_cost + business_cost

def calculate_total_price(aircraft_model, distance, flight_hours, airport_class, economy_seats, business_seats, stopovers=1):
    fuel_cost = calculate_fuel_cost(aircraft_model, distance)
    airport_fees_cost = calculate_airport_fees(airport_class, stopovers)
    crew_cost = calculate_crew_cost(aircraft_model, flight_hours)
    pilot_cost = calculate_pilot_cost(aircraft_model, flight_hours)
    maintenance_cost = calculate_maintenance_cost(flight_hours)
    insurance_cost = calculate_insurance_cost(aircraft_model)
    carbon_offset = calculate_carbon_offset_cost(distance)
    seat_cost = calculate_seat_cost(aircraft_model, economy_seats, business_seats)

    total_cost = (fuel_cost + airport_fees_cost + crew_cost + pilot_cost +
                  maintenance_cost + insurance_cost + carbon_offset + seat_cost)
    return round(total_cost, 2)

# AIRPORT SEARCH FUNCTIONALITY
airports = airportsdata.load("IATA")
airport_list = [{"code": code, "name": data.get("name", "Unknown"), "city": data.get("city", "Unknown"),
                 "country": data.get("country", "Unknown"), "lat": data.get("lat", 0.0), "lon": data.get("lon", 0.0)}
                for code, data in airports.items()]

def filter_airports(search_query):
    search_query = search_query.lower()
    return [airport for airport in airport_list if search_query in airport["code"].lower() or
            search_query in airport["name"].lower() or search_query in airport["city"].lower()][:10]

# INTERACTIVE UI ELEMENTS
departure_search = Text(placeholder="Search departure airport...", description="Departure:")
arrival_search = Text(placeholder="Search arrival airport...", description="Arrival:")
aircraft_model_input = Text(placeholder="Enter aircraft model...", description="Aircraft:")
distance_output = IntText(description="Distance (miles):", disabled=True)
flight_hours_input = IntText(description="Flight Hours:")
economy_seats_input = IntText(description="Economy Seats:")
business_seats_input = IntText(description="Business Seats:")
stopovers_input = IntText(description="Stopovers:")
airport_class_input = Text(placeholder="Enter airport class...", description="Airport Class:")
calculate_button = Button(description="Calculate")
output = Output()

def calculate_flight_costs(_):
    try:
        departure = filter_airports(departure_search.value)[0]
        arrival = filter_airports(arrival_search.value)[0]
        distance = int(geodesic((departure["lat"], departure["lon"]), (arrival["lat"], arrival["lon"])).miles)
        distance_output.value = distance

        total_cost = calculate_total_price(
            aircraft_model_input.value,
            distance,
            flight_hours_input.value,
            airport_class_input.value,
            economy_seats_input.value,
            business_seats_input.value,
            stopovers_input.value
        )
        with output:
            output.clear_output()
            print(f"Total Estimated Flight Cost: ${total_cost}")
    except Exception as e:
        with output:
            output.clear_output()
            print(f"Error: {e}")

calculate_button.on_click(calculate_flight_costs)

ui = VBox([
    HBox([departure_search, arrival_search]),
    aircraft_model_input,
    distance_output,
    flight_hours_input,
    economy_seats_input,
    business_seats_input,
    stopovers_input,
    airport_class_input,
    calculate_button,
    output
])

display(ui)

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Example route: Calculate flight distance
@app.route('/calculate', methods=['POST'])
def calculate_distance():
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')

    # Mock response
    if origin and destination:
        response = {
            "distance": 500,
            "flight_hours": 1.5
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Invalid input"}), 400

# Run the Flask app
app.run(host='0.0.0.0', port=5000)

