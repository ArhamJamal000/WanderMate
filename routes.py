from flask import render_template, request, jsonify, flash, redirect, url_for, send_file
from app import app, db
from models import Trip
import google.generativeai as genai
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import re
import json

# Configure Gemini API
genai.configure(api_key=app.config['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.0-flash')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planner', methods=['GET', 'POST'])
def planner():
    if request.method == 'POST':
        return redirect(url_for('generate_itinerary'))

    # For GET request, pass today's date for min attribute
    today_str = datetime.now().strftime('%Y-%m-%d')
    return render_template('planner.html', today=today_str)

@app.route('/generate', methods=['POST'])
def generate_itinerary():
    destination = request.form.get('destination')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    travelers_str = request.form.get('travelers')
    budget_str = request.form.get('budget')
    mood = request.form.get('mood', '')
    preferences = request.form.get('preferences', '')

    # Server-side validation
    errors = []
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        travelers = int(travelers_str)
        budget = float(budget_str)
    except ValueError:
        errors.append('Invalid date, number, or budget format.')

    today = datetime.now().date()
    if start_date < today:
        errors.append('Start date cannot be in the past.')
    if end_date <= start_date:
        errors.append('End date must be after start date.')
    if travelers < 1:
        errors.append('Number of travelers must be at least 1.')
    if budget <= 0:
        errors.append('Budget must be greater than 0.')

    if errors:
        return jsonify({'error': errors[0]}), 400

    # Calculate number of days
    number_of_days = (end_date - start_date).days + 1

    # Generate itinerary using Gemini AI
    prompt = f"""
    Create a detailed travel itinerary for a trip to {destination} from {start_date} to {end_date}.
    Number of travelers: {travelers}
    Budget: ${budget}
    Mood: {mood}
    Special preferences: {preferences}
    Number of days: {number_of_days}

    Respond ONLY with a valid JSON object in the following exact format. Do not include any additional text, explanations, or markdown formatting:
    {{
      "trip_summary": {{
        "destination": "{destination}",
        "dates": "{start_date} to {end_date}",
        "travelers": "{travelers}",
        "budget": "${budget}",
        "mood": "{mood}",
        "overall_theme": "Brief description based on mood and preferences"
      }},
      "trending_places": [
        {{
          "place": "Popular Destination 1",
          "description": "Brief description of the place",
          "rating": "4.5",
          "image_url": "https://example.com/image1.jpg"
        }},
        {{
          "place": "Popular Destination 2",
          "description": "Brief description of the place",
          "rating": "4.7",
          "image_url": "https://example.com/image2.jpg"
        }},
        {{
          "place": "Popular Destination 3",
          "description": "Brief description of the place",
          "rating": "4.3",
          "image_url": "https://example.com/image3.jpg"
        }},
        {{
          "place": "Popular Destination 4",
          "description": "Brief description of the place",
          "rating": "4.6",
          "image_url": "https://example.com/image4.jpg"
        }}
      ],
      "risk_alert": {{
        "level": "Low",
        "details": "Brief safety and weather risk assessment"
      }},
      "hotel_recommendations": [
        {{
          "name": "Hotel Name 1",
          "price_range": "$100-150/night",
          "rating": "4.2",
          "highlight": "Key feature or amenity"
        }},
        {{
          "name": "Hotel Name 2",
          "price_range": "$150-200/night",
          "rating": "4.5",
          "highlight": "Key feature or amenity"
        }},
        {{
          "name": "Hotel Name 3",
          "price_range": "$200-250/night",
          "rating": "4.8",
          "highlight": "Key feature or amenity"
        }},
        {{
          "name": "Hotel Name 4",
          "price_range": "$250-300/night",
          "rating": "4.6",
          "highlight": "Key feature or amenity"
        }},
        {{
          "name": "Hotel Name 5",
          "price_range": "$300-350/night",
          "rating": "4.9",
          "highlight": "Key feature or amenity"
        }}
      ],
      "overcrowd_predictor": {{
        "level": "Medium",
        "reason": "Explanation based on season and dates"
      }},
      "quick_insights": [
        "Insight 1: Key attraction or activity",
        "Insight 2: Another key point",
        "Insight 3: Additional insight"
      ],
      "daily_plan": {{
        "Day 1": "Detailed activities for Day 1",
        "Day 2": "Detailed activities for Day 2"
      }},
      "important_notes": [
        "Note 1: Important tip or warning",
        "Note 2: Another note"
      ],
      "daily_budget_plan": [
        {{
          "day": "Day 1",
          "activities": "Brief summary of activities for Day 1",
          "estimated_spend": "$X",
          "category_breakdown": {{
            "Accommodation": "$X",
            "Food": "$X",
            "Transport": "$X",
            "Activities": "$X",
            "Miscellaneous": "$X"
          }},
          "recommendations": "Practical daily recommendations"
        }},
        {{
          "day": "Day 2",
          "activities": "Brief summary of activities for Day 2",
          "estimated_spend": "$X",
          "category_breakdown": {{
            "Accommodation": "$X",
            "Food": "$X",
            "Transport": "$X",
            "Activities": "$X",
            "Miscellaneous": "$X"
          }},
          "recommendations": "Practical daily recommendations"
        }}
      ],
      "budget_tracking": {{
        "overview": "Summarize whether the user's total budget is sufficient for their selected mood and trip duration.",
        "distribution_table": [
          {{
            "category": "Accommodation",
            "percentage": "",
            "estimated_cost": "",
            "suggestions": "e.g., choose 3-star hotels or local stays to optimize."
          }},
          {{
            "category": "Food",
            "percentage": "",
            "estimated_cost": "",
            "suggestions": "e.g., explore local street food to save."
          }},
          {{
            "category": "Transport",
            "percentage": "",
            "estimated_cost": "",
            "suggestions": "e.g., use metro or shared rides instead of taxis."
          }},
          {{
            "category": "Activities",
            "percentage": "",
            "estimated_cost": "",
            "suggestions": "e.g., combine sightseeing passes or free attractions."
          }},
          {{
            "category": "Miscellaneous",
            "percentage": "",
            "estimated_cost": "",
            "suggestions": "e.g., keep buffer for souvenirs or emergencies."
          }}
        ],
        "optimization_tips": [
          "List practical recommendations to make the most of the user's budget.",
          "If budget is high, suggest upgrades or luxury add-ons.",
          "If budget is low, suggest free or low-cost experiences."
        ]
      }}
    }}

    Rules:
    - Always respond with valid JSON only.
    - Fill all fields based on input data (destination, dates, budget, mood).
    - Risk alert and overcrowd level must match seasonal logic (e.g., high crowd in summer for popular destinations).
    - Hotel recommendations should align with the budget and mood.
    - Adjust destination recommendations and activities based on the selected mood.
    - For budget_tracking, use the following percentages based on mood:
      - Relaxed: Accommodation 35%, Food 25%, Transport 20%, Activities 15%, Miscellaneous 5%
      - Adventurous: Accommodation 25%, Food 20%, Transport 20%, Activities 30%, Miscellaneous 5%
      - Romantic: Accommodation 40%, Food 25%, Transport 10%, Activities 20%, Miscellaneous 5%
      - Cultural: Accommodation 30%, Food 25%, Transport 20%, Activities 20%, Miscellaneous 5%
      - Budget-Friendly: Accommodation 20%, Food 30%, Transport 25%, Activities 15%, Miscellaneous 10%
    - Calculate estimated_cost as percentage of total budget, ensuring total estimated costs do not exceed the budget.
    - Provide realistic estimated_cost values with currency symbols (e.g., "$120").
    - For daily_budget_plan, create an array with one object per day (total {number_of_days} days). Each day's estimated_spend should sum approximately to total_budget / {number_of_days}. Use the same mood-based percentages for category_breakdown. Include brief activities summary and practical recommendations.
    - Ensure the JSON is valid and complete.
    """

    try:
        response = model.generate_content(prompt)
        itinerary_json = response.text.strip()

        # Clean the response to extract JSON (remove markdown code blocks if present)
        itinerary_json = re.sub(r'```json\s*', '', itinerary_json)
        itinerary_json = re.sub(r'```\s*', '', itinerary_json)
        itinerary_json = itinerary_json.strip()

        # Parse the JSON response
        try:
            data = json.loads(itinerary_json)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return jsonify({'error': 'Error parsing AI response. Please try again.'}), 500

        # Extract structured data
        summary = data.get('trip_summary', {})
        trending = data.get('trending_places', [])
        risk = data.get('risk_alert', {})
        hotels = data.get('hotel_recommendations', [])
        crowd = data.get('overcrowd_predictor', {})
        insights = data.get('quick_insights', [])
        daily_plan = data.get('daily_plan', {})
        notes = data.get('important_notes', [])
        daily_budget_plan = data.get('daily_budget_plan', [])
        budget_tracking = data.get('budget_tracking', {})

        # Save trip to database (store the full JSON as itinerary)
        trip = Trip(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            travelers=travelers,
            budget=budget,
            mood=mood,
            preferences=preferences,
            itinerary=json.dumps(data)  # Store structured data as JSON string
        )
        db.session.add(trip)
        db.session.commit()

        return jsonify({'trip_id': trip.id})

    except Exception as e:
        return jsonify({'error': f'Error generating itinerary: {str(e)}'}), 500

@app.route('/dashboard/<int:trip_id>')
def dashboard(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    trip_data = json.loads(trip.itinerary)

    summary = trip_data.get('trip_summary', {})
    trending = trip_data.get('trending_places', [])
    risk = trip_data.get('risk_alert', {})
    hotels = trip_data.get('hotel_recommendations', [])
    crowd = trip_data.get('overcrowd_predictor', {})
    insights = trip_data.get('quick_insights', [])
    daily_plan = trip_data.get('daily_plan', {})
    notes = trip_data.get('important_notes', [])
    daily_budget_plan = trip_data.get('daily_budget_plan', [])
    budget_tracking = trip_data.get('budget_tracking', {})

    # Budget tracking logic
    total_budget = trip.budget
    mood = trip.mood.lower()
    mood_percentages = {
        'relaxed': {'accommodation': 0.35, 'food': 0.25, 'transport': 0.20, 'activities': 0.15, 'misc': 0.05},
        'adventurous': {'accommodation': 0.25, 'food': 0.20, 'transport': 0.20, 'activities': 0.30, 'misc': 0.05},
        'romantic': {'accommodation': 0.40, 'food': 0.25, 'transport': 0.10, 'activities': 0.20, 'misc': 0.05},
        'cultural': {'accommodation': 0.30, 'food': 0.25, 'transport': 0.20, 'activities': 0.20, 'misc': 0.05},
        'budget-friendly': {'accommodation': 0.20, 'food': 0.30, 'transport': 0.25, 'activities': 0.15, 'misc': 0.10}
    }
    percentages = mood_percentages.get(mood, mood_percentages['relaxed'])
    budget_data = []
    for cat, perc in percentages.items():
        cost = total_budget * perc
        budget_data.append({
            'category': cat.capitalize(),
            'percentage': f"{perc * 100:.0f}%",
            'cost': f"${cost:.2f}"
        })

    return render_template(
        'dashboard.html',
        itinerary=json.dumps(trip_data),
        trip_id=trip.id,
        summary=summary,
        trending=trending,
        risk=risk,
        hotels=hotels,
        crowd=crowd,
        insights=insights,
        daily_plan=daily_plan,
        notes=notes,
        daily_budget_plan=daily_budget_plan,
        budget_data=budget_data,
        budget_tracking=budget_tracking
    )

@app.route('/trips')
def trips():
    trips = Trip.query.order_by(Trip.created_at.desc()).all()
    return render_template('trips.html', trips=trips)

@app.route('/trip/<int:trip_id>')
def trip_detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('trip_detail.html', trip=trip)

@app.route('/export/<int:trip_id>')
def export_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    # Parse the itinerary JSON
    data = json.loads(trip.itinerary)

    # Create PDF with margins
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph(f"Trip to {trip.destination}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Trip Summary
    summary = data.get('trip_summary', {})
    summary_text = f"""
    Destination: {summary.get('destination', '')}<br/>
    Dates: {summary.get('dates', '')}<br/>
    Travelers: {summary.get('travelers', '')}<br/>
    Budget: {summary.get('budget', '')}<br/>
    Mood: {summary.get('mood', '')}<br/>
    Overall Theme: {summary.get('overall_theme', '')}<br/>
    """
    story.append(Paragraph("Trip Summary", styles['Heading2']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # Trending Places
    trending = data.get('trending_places', [])
    if trending:
        story.append(Paragraph("Trending Places", styles['Heading2']))
        story.append(Spacer(1, 6))
        for place in trending:
            place_text = f"• {place.get('place', '')}: {place.get('description', '')} (Rating: {place.get('rating', '')})"
            story.append(Paragraph(place_text, styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    # Risk Alert
    risk = data.get('risk_alert', {})
    if risk:
        story.append(Paragraph("Risk Alert", styles['Heading2']))
        story.append(Spacer(1, 6))
        risk_text = f"Level: {risk.get('level', '')}<br/>{risk.get('details', '')}"
        story.append(Paragraph(risk_text, styles['Normal']))
        story.append(Spacer(1, 12))

    # Hotel Recommendations
    hotels = data.get('hotel_recommendations', [])
    if hotels:
        story.append(Paragraph("Hotel Recommendations", styles['Heading2']))
        story.append(Spacer(1, 6))
        for hotel in hotels:
            hotel_text = f"• {hotel.get('name', '')}: {hotel.get('price_range', '')}, Rating: {hotel.get('rating', '')} - {hotel.get('highlight', '')}"
            story.append(Paragraph(hotel_text, styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    # Daily Plan
    daily_plan = data.get('daily_plan', {})
    if daily_plan:
        story.append(Paragraph("Daily Plan", styles['Heading2']))
        story.append(Spacer(1, 6))
        for day, activities in daily_plan.items():
            story.append(Paragraph(day, styles['Heading3']))
            story.append(Spacer(1, 6))
            story.append(Paragraph(activities, styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    # Quick Insights
    insights = data.get('quick_insights', [])
    if insights:
        story.append(Paragraph("Quick Insights", styles['Heading2']))
        story.append(Spacer(1, 6))
        for insight in insights:
            story.append(Paragraph(f"• {insight}", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    # Important Notes
    notes = data.get('important_notes', [])
    if notes:
        story.append(Paragraph("Important Notes", styles['Heading2']))
        story.append(Spacer(1, 6))
        for note in notes:
            story.append(Paragraph(f"• {note}", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    # Budget Tracking
    budget_tracking = data.get('budget_tracking', {})
    if budget_tracking:
        story.append(Paragraph("Budget Tracking", styles['Heading2']))
        story.append(Spacer(1, 6))

        # Overview
        overview = budget_tracking.get('overview', '')
        if overview:
            story.append(Paragraph(f"Overview: {overview}", styles['Normal']))
            story.append(Spacer(1, 6))

        # Distribution Table
        distribution_table = budget_tracking.get('distribution_table', [])
        if distribution_table:
            table_data = [['Category', 'Percentage (%)', 'Estimated Cost', 'Suggestions']]
            for item in distribution_table:
                table_data.append([
                    Paragraph(item.get('category', ''), styles['Normal']),
                    Paragraph(item.get('percentage', ''), styles['Normal']),
                    Paragraph(item.get('estimated_cost', ''), styles['Normal']),
                    Paragraph(item.get('suggestions', ''), styles['Normal'])
                ])

            # Create table with adjusted widths
            table = Table(table_data, colWidths=[90, 70, 80, 180])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            story.append(Spacer(1, 12))

        # Optimization Tips
        optimization_tips = budget_tracking.get('optimization_tips', [])
        if optimization_tips:
            story.append(Paragraph("Optimization Tips", styles['Heading3']))
            story.append(Spacer(1, 6))
            for tip in optimization_tips:
                story.append(Paragraph(f"• {tip}", styles['Normal']))
                story.append(Spacer(1, 6))
            story.append(Spacer(1, 12))

    # Day-wise Budget Tracing
    daily_budget_plan = data.get('daily_budget_plan', [])
    if daily_budget_plan:
        story.append(Paragraph("Day-wise Budget Tracing", styles['Heading2']))
        story.append(Spacer(1, 6))

        table_data = [['Day', 'Estimated Spend', 'Accommodation', 'Food', 'Transport', 'Activities', 'Miscellaneous', 'Recommendations']]
        for day in daily_budget_plan:
            table_data.append([
                Paragraph(day.get('day', ''), styles['Normal']),
                Paragraph(day.get('estimated_spend', ''), styles['Normal']),
                Paragraph(day.get('category_breakdown', {}).get('Accommodation', ''), styles['Normal']),
                Paragraph(day.get('category_breakdown', {}).get('Food', ''), styles['Normal']),
                Paragraph(day.get('category_breakdown', {}).get('Transport', ''), styles['Normal']),
                Paragraph(day.get('category_breakdown', {}).get('Activities', ''), styles['Normal']),
                Paragraph(day.get('category_breakdown', {}).get('Miscellaneous', ''), styles['Normal']),
                Paragraph(day.get('recommendations', ''), styles['Normal'])
            ])

        # Create table with adjusted widths
        table = Table(table_data, colWidths=[40, 60, 60, 40, 50, 50, 60, 120])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"trip_{trip.destination.replace(' ', '_')}.pdf",
        mimetype='application/pdf'
    )

@app.route('/delete_trip/<int:trip_id>', methods=['POST'])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    db.session.delete(trip)
    db.session.commit()
    return jsonify({'success': True})
