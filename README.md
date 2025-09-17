# ✈️ Aircraft Lease Estimator – Backend + UI

Estimate the operational cost of leasing commercial aircraft based on route, aircraft model, seating configuration, and airport class. This backend powers a dynamic leasing calculator with real-world aviation data and interactive UI integration.

---

##🔗 Live Demos & Interactive Tools
**📊 Backend – Colab Notebook**
- [Colab Notebook – Backend](https://colab.research.google.com/drive/1hX0ezbuSTbUB39hfB4iXGDlhASeDt_-y?usp=sharing)

**🎨 Frontend – CodePen UI**
- [CodePen UI – Frontend](https://codepen.io/Mati-the-vuer/full/ogvpgbd)

## 📦 Tech Stack

- **Python**: Core language
- **Flask**: RESTful API
- **Pandas & NumPy**: Data manipulation
- **Geopy**: Distance calculations
- **airportsdata**: IATA airport metadata
- **ipywidgets**: UI prototyping (Colab)
- **Flask-CORS**: Cross-origin support

---

## 🚀 Features

- Aircraft-specific fuel burn, crew, and seating data
- Modular cost estimation:
  - Fuel, crew, pilot, maintenance, insurance
  - Airport fees and carbon offset
  - Seat-based revenue modeling
- Airport search via IATA codes and geolocation
- Flask API endpoint for frontend integration
- Interactive widgets for Colab-based UI testing

---

## 📂 Project Structure+
├── aircraft_data.py # Aircraft specs and pricing 
├── cost_calculator.py # Modular cost functions 
├── airport_utils.py # Airport search and filtering 
├── ui_widgets.ipynb # Colab-based interactive UI 
├── app.py # Flask backend with /calculate route


---

## 🧪 API Documentation

### `POST /calculate`

Estimate flight distance and time between two airports.

**Request Body:**

{
  "origin": "JFK",
  "destination": "LAX"
}
