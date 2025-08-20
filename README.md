# EconoVision
An interactive web dashboard for visualizing global economic data from the World Bank.  
This application allows users to filter and compare economic indicators across various countries and timeframes, with data presented through a series of dynamic, responsive charts.

## 🚀 Live Demo
[View EconoVision on Render](https://worldbank-dashboard.onrender.com/)

## ⚡ Features
- 🌍 Filter and compare countries by **economic indicators**  
- 📊 Select **custom year ranges** for comparison  
- 📈 Dynamic, responsive charts powered by **Chart.js**  
- 🎛 Interactive dropdowns for **country & indicator** selection  
- 🚀 Deployed seamlessly with **Render**  

## 🛠 Tech Stack
- **Backend:** Django  
- **Frontend:** HTML, CSS, Bootstrap  
- **Charts:** Chart.js  
- **Hosting:** Render  

## ⚙️ Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/econovision.git
   cd econovision

2. **Create & Activate Virtual Environment**
    ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows

4. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    python manage.py collectstatic
    
6. **Run Migrations & Populate Countries**
   ```bash
   python manage.py migrate
   python manage.py populate_countries
   
8. **Start Development Server**
   ```bash
   python manage.py runserver

9. **Open 👉 http://127.0.0.1:8000/  in your browser 🎉**

## 🔧 How It Works
1. A user selects filter criteria on the frontend and clicks "Apply".

2. The JavaScript sends a fetch request to the backend Django API endpoint (/dashboard/api/indicator-data/).

3. The Django view first checks the local database for the requested data.

4. Cache Hit: If the data exists, it is returned immediately as JSON.

5. Cache Miss: If the data is not in the database, the backend makes a request to the external World Bank API.

6. The data received from the World Bank is saved to the local database for future requests and then returned as JSON to the frontend.

7. The frontend JavaScript receives the JSON data and dynamically updates all the charts.

## 🌐 API Endpoint

### `GET /dashboard/api/indicator-data/`

### 🔹 Request Parameters
- **indicator** → *(string, required)* World Bank indicator code (e.g., `NY.GDP.MKTP.CD`)  
- **countries** → *(string, required)* Comma-separated ISO country codes (e.g., `IN,US,CN`)  
- **start_year** → *(integer, required)* Start year for the data range (e.g., `2000`)  
- **end_year** → *(integer, required)* End year for the data range (e.g., `2023`)  

## 🗂 Django URL Configurations

### 🔹 Project Level (`dashboard_project/urls.py`)
This file includes global routes such as **admin panel**, app-level routes, and authentication routes.

- **/admin/** → Django Admin Panel  
- **/** → Includes all routes from `dashboard_app`  
- **/accounts/** → Built-in Django authentication (login/logout/password reset etc.)  

  ```python
   urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard app routes (landing, dashboard, signup, API, etc.)
    path("", include("dashboard_app.urls")),

    # Authentication (login/logout/password management)
    path("accounts/", include("django.contrib.auth.urls")),
  ]

### 🔹 App Level (dashboard_app/urls.py)

- This file contains routes specific to the dashboard application.
- / → Landing page
- /dashboard/ → Dashboard main view
- /signup/ → User signup view
- /dashboard/api/indicator-data/ → API endpoint for indicator data
- 
  ```python
  urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/api/indicator-data/", views.get_indicator_data, name="indicator_data"),
  ]

## 💡 Future Improvements

- More Indicators & Countries: Expand the list of available economic indicators.
- Data Export: Add functionality to export chart data as CSV or chart images as PNG.
- User-Saved Views: Allow users to save their favorite filter combinations.
- Advanced Analytics: Incorporate statistical analysis like moving averages or year-over-year growth.


## 👥 Contributing

Feel free to fork this repo, open issues, and submit PRs to improve EconoVision.

   
