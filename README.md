# WanderMate - AI-Powered Travel Planning

WanderMate is a sophisticated web-based travel planning application built with Flask and powered by Google's Gemini AI. It provides users with personalized, AI-generated travel itineraries based on their preferences, budget, and travel mood. The application features a modern, responsive interface with comprehensive trip management capabilities.

## 🌟 Key Features

### AI-Powered Trip Planning
- **Intelligent Itinerary Generation**: Uses Google's Gemini 2.0 Flash AI model to create detailed, personalized travel plans
- **Mood-Based Planning**: Choose from Relaxed, Adventurous, Romantic, Cultural, or Budget-Friendly travel moods
- **Smart Recommendations**: AI suggests trending destinations, hotels, and activities based on user preferences

### Comprehensive Trip Management
- **Interactive Dashboard**: Visual dashboard displaying trip summaries, risk assessments, and crowd predictions
- **Trip Storage**: Persistent SQLite database for saving and managing multiple trips
- **PDF Export**: Generate professional PDF itineraries for offline access
- **Trip History**: View and manage all saved trips with detailed information

### Advanced Analytics & Insights
- **Risk Assessment**: AI-powered safety and weather risk analysis
- **Crowd Prediction**: Seasonal crowd level predictions for destinations
- **Hotel Recommendations**: Curated hotel suggestions with ratings and price ranges
- **Quick Insights**: Key tips and highlights for each destination

### User Experience
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Modern UI**: Glassmorphism design with gradient backgrounds and smooth animations
- **Real-time Planning**: AJAX-powered form submission with loading indicators
- **Intuitive Navigation**: Clean, organized interface with clear call-to-actions

## 🛠️ Technology Stack

### Backend
- **Flask 2.3.3**: Lightweight Python web framework
- **SQLAlchemy 3.0.5**: ORM for database operations
- **Google Generative AI 0.8.4**: AI integration for itinerary generation
- **ReportLab 4.0.7**: PDF generation for trip exports

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Custom styling with CSS variables and animations
- **Bootstrap 5.1.3**: Responsive grid system and components
- **JavaScript (ES6)**: Interactive functionality and AJAX requests
- **Font Awesome 6.0.0**: Icon library for UI elements

### Database & Configuration
- **SQLite**: Lightweight, file-based database
- **python-dotenv 1.0.0**: Environment variable management
- **Werkzeug 2.3.7**: WSGI utility library

## 📁 Project Structure & File Details

```
WanderMate-main/
├── app.py                    # Main Flask application entry point
├── routes.py                 # All application routes and view functions
├── models.py                 # Database models and schema definitions
├── config.py                 # Application configuration and settings
├── requirements.txt          # Python dependencies with versions
├── .env                      # Environment variables (API keys, secrets)
├── instance/
│   └── trips.db             # SQLite database file (auto-generated)
├── static/
│   ├── css/
│   │   └── style.css        # Main stylesheet with custom CSS variables
│   ├── js/
│   │   └── script.js        # Client-side JavaScript for interactions
│   └── images/
│       ├── logo1.png        # Primary logo (favicon)
│       ├── logo2.png        # Secondary logo (navbar)
│       └── loading.gif      # Loading animation for AI generation
├── templates/
│   ├── base.html            # Base template with navigation and footer
│   ├── index.html           # Landing page with hero section and features
│   ├── planner.html         # Trip planning form with mood selection
│   ├── dashboard.html       # AI-generated trip dashboard with analytics
│   ├── trips.html           # List of all saved trips
│   └── trip_detail.html     # Detailed view of individual trips
└── __pycache__/             # Python bytecode cache (auto-generated)
```

### Core Files Description

#### `app.py`
- Initializes Flask application
- Configures database and AI API
- Registers blueprints and creates database tables
- Entry point for running the development server

#### `routes.py`
- **Home Route (`/`)**: Renders landing page
- **Planner Route (`/planner`)**: Trip planning form with validation
- **Generate Route (`/generate`)**: AI itinerary generation endpoint
- **Dashboard Route (`/dashboard/<trip_id>`)**: Displays AI-generated trip details
- **Trips Route (`/trips`)**: Lists all saved trips
- **Trip Detail Route (`/trip/<trip_id>`)**: Individual trip information
- **Export Route (`/export/<trip_id>`)**: PDF generation and download, including rendering of the daily budget table
- **Delete Route (`/delete_trip/<trip_id>`)**: Trip deletion functionality

#### `models.py`
- **Trip Model**: SQLAlchemy model with fields for:
  - Basic info: destination, dates, travelers, budget
  - Preferences: mood, special requirements
  - AI data: JSON-stored itinerary from Gemini API
  - Metadata: creation timestamp

#### `config.py`
- Environment variable loading with python-dotenv
- Configuration class with:
  - SECRET_KEY for session security
  - SQLite database URI
  - SQLAlchemy settings
  - GEMINI_API_KEY for AI integration

#### `requirements.txt`
- Flask ecosystem dependencies
- AI and PDF generation libraries
- Environment management tools

### Template Files

#### `base.html`
- HTML5 structure with Bootstrap integration
- Responsive navigation bar with logo
- Footer with branding
- Flash message display system
- Font Awesome and custom CSS imports

#### `index.html`
- Hero section with call-to-action
- Feature showcase cards
- Trending destinations grid
- How-it-works step visualization

#### `planner.html`
- Trip planning form with validation
- Mood selection with emoji indicators
- Date range and budget inputs
- AJAX submission with loading states

#### `dashboard.html`
- Bento box layout for trip information
- AI-generated insights and recommendations
- Risk and crowd level indicators
- Hotel suggestions with ratings
- Day-wise Budget Tracing section with Bootstrap table

#### `trips.html`
- Card-based trip listing
- Action buttons for view/export/delete
- Empty state for no trips

#### `trip_detail.html`
- Detailed trip information display
- Bento grid layout
- Quick insights and notes sections

### Static Assets

#### `style.css`
- CSS custom properties (variables) for theming
- Glassmorphism effects and gradients
- Responsive design with media queries
- Animation keyframes and transitions
- Bento box styling and layouts

#### `script.js`
- Trip deletion confirmation and AJAX
- Form submission handling
- Dynamic UI updates
- Error handling and user feedback

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google Gemini API key

### Step-by-Step Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd WanderMate-main
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the root directory
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     SECRET_KEY=your_secret_key_here
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   - Open your browser and navigate to `http://localhost:5000`
   - Start planning your AI-powered trips!

## 📖 Usage Guide

### Planning a Trip
1. **Access Planner**: Click "Plan Trip" from the navigation
2. **Fill Details**: Enter destination, dates, travelers, and budget
3. **Select Mood**: Choose your travel mood (Relaxed, Adventurous, etc.)
4. **Add Preferences**: Include special requirements or preferences
5. **Generate**: Click "Start Planning" to trigger AI generation

### Managing Trips
1. **View Trips**: Access "My Trips" to see all saved itineraries
2. **Dashboard**: Click "View Details" for comprehensive trip information
3. **Export**: Download trips as PDF for offline use
4. **Delete**: Remove unwanted trips with confirmation

### Understanding AI Features
- **Trip Summary**: Overview with destination, dates, and budget
- **Trending Places**: AI-recommended attractions with ratings
- **Risk Alerts**: Safety and weather assessments
- **Hotel Recommendations**: Curated accommodation options
- **Crowd Predictor**: Seasonal crowd level analysis
- **Daily Plans**: Detailed day-by-day itineraries
- **Important Notes**: Key tips and warnings

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Required for AI itinerary generation
- `SECRET_KEY`: Flask session security (auto-generated if not provided)

### Database
- SQLite database created automatically in `instance/trips.db`
- Tables created on first run via `db.create_all()`

### Customization
- Modify CSS variables in `style.css` for theming
- Update AI prompts in `routes.py` for different generation styles
- Adjust PDF layout in the export route

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/AmazingFeature`
3. **Commit Changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push Branch**: `git push origin feature/AmazingFeature`
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add docstrings to new functions
- Test changes thoroughly before submitting
- Update README for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support & Contact

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check this README for detailed information

## 🙏 Acknowledgments

- **Google Gemini AI**: For powering intelligent trip planning
- **Flask Framework**: For the robust web foundation
- **Bootstrap**: For responsive UI components
- **Font Awesome**: For beautiful icons
- **Unsplash**: For destination imagery

---

**Happy Traveling with WanderMate! 🌍✈️**
