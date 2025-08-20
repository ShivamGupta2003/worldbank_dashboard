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

10. **Open 👉 http://127.0.0.1:8000/  in your browser 🎉**

## 👥 Contributing

Feel free to fork this repo, open issues, and submit PRs to improve EconoVision.


   
