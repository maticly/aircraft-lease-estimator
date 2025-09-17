# ✈️ Aircraft Lease Estimator – Backend + UI
Estimate the operational cost of leasing commercial aircraft based on route, aircraft model, seating configuration, and airport class. This backend powers a dynamic leasing calculator with real-world aviation data and interactive UI integration.

📦 Tech Stack
Python: Core language

Flask: RESTful API

Pandas & NumPy: Data manipulation

Geopy: Distance calculations

airportsdata: IATA airport metadata

ipywidgets: UI prototyping (Colab)

Flask-CORS: Cross-origin support

🚀 Features
Aircraft-specific fuel burn, crew, and seating data

Modular cost estimation:

Fuel, crew, pilot, maintenance, insurance

Airport fees and carbon offset

Seat-based revenue modeling

Airport search via IATA codes and geolocation

Flask API endpoint for frontend integration

Interactive widgets for Colab-based UI testing

📂 Project Structure
Code
├── aircraft_data.py         # Aircraft specs and pricing
├── cost_calculator.py       # Modular cost functions
├── airport_utils.py         # Airport search and filtering
├── ui_widgets.ipynb         # Colab-based interactive UI
├── app.py                   # Flask backend with /calculate route
🧪 API Documentation (Swagger-style)
POST /calculate
Estimate flight distance and time between two airports.

Request Body:

json
{
  "origin": "JFK",
  "destination": "LAX"
}
Response:

json
{
  "distance": 2475,
  "flight_hours": 5.5
}
Future endpoints could include /estimate for full cost breakdown.

🛠️ Setup Instructions
bash
pip install flask flask-cors pandas numpy geopy airportsdata ipywidgets
python app.py
