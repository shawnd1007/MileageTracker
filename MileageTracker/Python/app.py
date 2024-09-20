from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import googlemaps
import requests
from io import BytesIO
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'N_82JzE4KleqPVvhdnieXUz63o241Vx46m4Uvsx00mg'  # Replace with a secure secret key

# Replace with your actual Google Maps API key
GMAPS_API_KEY = 'AIzaSyDBE9McUJQwVXX3avAGsWevb_BuwyK3368'
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# Ensure the 'static/images' directory exists
os.makedirs('static/images', exist_ok=True)

# Context processor to make 'datetime' available in templates
@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        description = request.form.get('description')
        irs_rate = request.form.get('irs_rate')
        locations = request.form.getlist('locations')

        # Input validation
        if not name or not date or not description or not irs_rate:
            flash('Please fill out all fields.')
            return redirect(url_for('index'))

        if len(locations) < 2:
            flash('Please enter at least two locations.')
            return redirect(url_for('index'))

        try:
            irs_rate = float(irs_rate)
        except ValueError:
            flash('Please enter a valid number for IRS Rate.')
            return redirect(url_for('index'))

        # Process the locations and generate the PDF report
        try:
            total_distance = 0
            legs = []

            for i in range(len(locations) - 1):
                origin = locations[i]
                destination = locations[i + 1]

                # Geocode addresses
                geocode_origin = gmaps.geocode(origin)
                geocode_destination = gmaps.geocode(destination)
                if not geocode_origin or not geocode_destination:
                    raise ValueError("Geocoding failed for one of the locations.")

                formatted_origin = geocode_origin[0]['formatted_address']
                formatted_destination = geocode_destination[0]['formatted_address']

                # Get directions
                directions_result = gmaps.directions(formatted_origin, formatted_destination, mode="driving")
                if not directions_result:
                    raise ValueError(f"No route found between {formatted_origin} and {formatted_destination}")

                leg = directions_result[0]['legs'][0]
                distance_text = leg['distance']['text']
                distance_value = leg['distance']['value'] / 1609.34  # Convert meters to miles
                total_distance += distance_value

                # Get turn-by-turn directions
                steps = leg['steps']
                turn_by_turn = []
                for step in steps:
                    instructions = step['html_instructions']
                    # Remove HTML tags from instructions
                    clean_instructions = re.sub('<[^<]+?>', '', instructions)
                    turn_by_turn.append(clean_instructions)

                # Get static map image
                polyline = directions_result[0]['overview_polyline']['points']
                map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&path=enc:{polyline}&markers=color:blue|label:S|{formatted_origin}&markers=color:red|label:E|{formatted_destination}&key={GMAPS_API_KEY}"
                response = requests.get(map_url)
                response.raise_for_status()
                image_filename = f"static/images/route_{i}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                with open(image_filename, 'wb') as img_file:
                    img_file.write(response.content)

                legs.append({
                    'origin': formatted_origin,
                    'destination': formatted_destination,
                    'distance_text': distance_text,
                    'distance_value': distance_value,
                    'turn_by_turn': turn_by_turn,
                    'map_image': image_filename
                })

            # Calculate total reimbursement
            total_reimbursement = total_distance * irs_rate

            # Generate the PDF report
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer)
            styles = getSampleStyleSheet()
            story = []

            # Add personal details
            story.append(Paragraph(f"<b>Name:</b> {name}", styles['Normal']))
            story.append(Paragraph(f"<b>Date:</b> {date}", styles['Normal']))
            story.append(Paragraph(f"<b>Description:</b> {description}", styles['Normal']))
            story.append(Spacer(1, 12))

            # Add IRS rate and total reimbursement
            story.append(Paragraph(f"<b>IRS Standard Mileage Rate:</b> ${irs_rate:.2f} per mile", styles['Normal']))
            story.append(Paragraph(f"<b>Total Distance:</b> {total_distance:.2f} miles", styles['Normal']))
            story.append(Paragraph(f"<b>Total Reimbursement:</b> ${total_reimbursement:.2f}", styles['Normal']))
            story.append(Spacer(1, 12))

            # Add route details
            for idx, leg in enumerate(legs):
                story.append(Paragraph(f"<b>Route {idx + 1}:</b>", styles['Heading2']))
                story.append(Paragraph(f"From: {leg['origin']}", styles['Normal']))
                story.append(Paragraph(f"To: {leg['destination']}", styles['Normal']))
                story.append(Paragraph(f"Distance: {leg['distance_text']}", styles['Normal']))
                story.append(Spacer(1, 12))

                # Add map image
                img = Image(leg['map_image'])
                img.drawHeight = 4 * inch * img.drawHeight / img.drawWidth
                img.drawWidth = 6 * inch
                story.append(img)
                story.append(Spacer(1, 12))

                # Add turn-by-turn directions
                story.append(Paragraph("<b>Turn-by-Turn Directions:</b>", styles['Heading3']))
                for step in leg['turn_by_turn']:
                    story.append(Paragraph(step, styles['Normal']))
                story.append(PageBreak())

            doc.build(story)
            pdf_buffer.seek(0)

            # Send the PDF file as a response
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name='mileage_report.pdf',
                mimetype='application/pdf'
            )

        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('index'))

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
