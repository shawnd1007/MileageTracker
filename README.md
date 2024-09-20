# MileageTracker
Mileage Tracker App is a Flask-based app that calculates mileage between multiple locations using Google Maps API. It generates PDF reports with trip details, directions, and reimbursement amounts. Deployed on Azure, it’s also available as a native iOS app using WKWebView for mobile access.

The Mileage Tracker App is a web-based application built with Flask and deployed on Azure, designed to help users track and calculate mileage for business trips. The app allows users to input multiple locations, calculates the total mileage between them using the Google Maps API, and generates a downloadable PDF report of the trip, including turn-by-turn directions and a route map.

The app is also packaged as a native iOS app using WKWebView to display the web application, allowing for seamless use across mobile devices.

Key Features
Multi-Location Input: Users can enter multiple locations to calculate the distance between them.
Google Maps Integration: Utilizes the Google Maps API to calculate driving directions and distances.
Dynamic PDF Generation: Automatically generates a PDF report detailing trip information, including:
Total distance traveled.
IRS standard mileage rate for reimbursement.
Turn-by-turn driving directions.
A map of the route with markers for start and end locations.
Responsive Design: Optimized for mobile devices and desktop browsers.
iOS Compatibility: The app is wrapped in a native iOS app using WKWebView and can be run on iPhones via Xcode.
Technologies Used
Backend: Flask, Python
Frontend: HTML, CSS (Bootstrap), JavaScript
APIs: Google Maps API (Geocoding and Directions)
PDF Generation: ReportLab (for generating the PDF report)
Mobile Integration: WKWebView (iOS)
How It Works
Users enter their name, date, description of the trip, and an IRS mileage rate (default set to $0.67 per mile).
Users input two or more locations.
The app calculates the driving route between each location and displays the total distance.
A PDF is generated, containing:
Personal trip details.
Distance and reimbursement rate.
Map and driving directions for each leg of the trip.
The app is deployed on Azure and can also be accessed via a native iOS app.
Setup & Installation
Clone the Repository:
bash
Copy code
git clone https://github.com/yourusername/mileage-tracker-app.git
cd mileage-tracker-app
Install Dependencies:
bash
Copy code
pip install -r requirements.txt
Run the App:
bash
Copy code
python app.py
Deploy to iOS (Optional):
Open the project in Xcode.
Set up a WKWebView to point to your Flask app URL on Azure.
