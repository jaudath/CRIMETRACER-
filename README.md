# CrimeTracer - Production-Grade Crime Tracking System

A comprehensive crime reporting and tracking system with AI-powered insights, animated UI, Chennai map integration, multilingual support, and robust AWS integrations with local fallbacks.

## 🚀 Features

### Core Functionality
- **Single Entry Point**: Run entire backend with `python main.py`
- **Chennai Hero Map**: Interactive Google Maps with police station markers
- **Complete Complaint Flow**: Camera capture, GPS, auto-station assignment, tracking
- **Police Dashboard**: Station-scoped case management with visualizations
- **Admin Portal**: User approval, analytics, case reassignment
- **Real-time Updates**: Status tracking with 24-hour victim confirmation window

### AI & ML Integration
- **XGBoost Models**: ML predictions with robust rule-based fallback
- **Gemini AI**: AI-generated precautions with curated fallbacks
- **BNS Mapping**: Legal section suggestions with anti-plagiarism compliance
- **Smart Station Assignment**: GPS-based nearest station calculation

### AWS Integration (with Fallbacks)
- **S3 Storage**: File uploads with local filesystem fallback
- **SNS Messaging**: SMS notifications with mock SMS fallback
- **CloudWatch**: Structured logging with local file fallback
- **Lambda**: Background jobs with in-app processing fallback

### Security & Privacy
- **JWT Authentication**: Token-based security with version invalidation
- **Password Security**: Bcrypt hashing with strength validation
- **Role-Based Access**: Police, Admin, and Public access controls
- **PII Protection**: Server-side data visibility enforcement
- **Rate Limiting**: Complaint submission and API abuse prevention

### Multilingual Support
- **6 Languages**: English, Tamil, Telugu, Hindi, Kannada, Malayalam
- **Complete Translation**: UI, messages, validation, admin interfaces
- **Fallback System**: Missing keys default to English

### Database Support
- **Primary**: PostgreSQL for production
- **Fallback**: SQLite for development/testing
- **Auto-Migration**: Tables created automatically on startup

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- Optional: PostgreSQL database
- Optional: AWS account for cloud features

## 🛠️ Quick Setup

### Backend Setup

1. **Clone and Setup Environment**
```bash
cd "Crime Tracer"
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
# Copy example environment file
copy .env.example .env

# Edit .env with your configuration
# At minimum, set JWT_SECRET to a secure random string
```

4. **Run the System**
```bash
# Start backend server (creates database automatically)
python main.py

# Optional: Seed stations from CSV
python main.py --seed-stations /path/to/officer_roster_enriched.csv

# Server runs on http://0.0.0.0:8000
```
YOUTUBE LINK : https://www.youtube.com/watch?v=RVe4sQ6lcLE
### Frontend Setup

1. **Initialize Frontend**
```bash
cd frontend
npm install

# Create .env for frontend
echo VITE_API_URL=http://localhost:8000 > .env

# Start development server
npm run dev

# Frontend runs on http://localhost:5173
```

## 🗺️ Chennai Map Integration

The system includes an embedded Chennai map with police station markers:

```html
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d248756.07885882704!2d80.20867324999999!3d13.04752545!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a5265ea4f7d3361%3A0x6e61a70b6863d433!2sChennai%2C%20Tamil%20Nadu!5e0!3m2!1sen!2sin!4v1758724448814!5m2!1sen!2sin" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
```

Interactive markers show police stations from the database and allow users to select reporting stations.

## 🔄 API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed system status

### Authentication
- `POST /auth/police/register` - Police registration (requires admin approval)
- `POST /auth/police/login` - Police login
- `POST /auth/admin/login` - Admin login
- `GET /auth/me` - Current user profile
- `POST /auth/logout` - Invalidate token

### Complaints
- `POST /complaints` - File new complaint
- `GET /complaints/{complaint_id}` - Get complaint details
- `GET /complaints?phone={phone}` - Track by phone
- `PUT /complaints/{complaint_id}/status` - Update status (police only)
- `POST /complaints/{complaint_id}/verify-closure` - Victim confirmation

### Stations
- `GET /stations` - List all stations
- `GET /stations/nearest?lat={lat}&lng={lng}` - Find nearest stations
- `GET /stations/{station_id}` - Station details

### ML & AI
- `POST /ml/predict` - Get ML severity prediction
- `POST /ml/precautions` - Get AI safety precautions
- `GET /ml/health` - Model status

### Admin
- `GET /admin/pending-police` - Pending registrations
- `POST /admin/police/{police_id}/approve` - Approve user
- `GET /admin/analytics` - System analytics

## 🏗️ Project Structure

```
Crime Tracer/
├── main.py                 # Single entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── bns_sections_cleaned.json # Legal sections data
├── backend/               # Backend modules
│   ├── models.py         # Database models
│   ├── db.py            # Database connection
│   ├── auth_router.py   # Authentication
│   ├── complaint_router.py # Complaint management
│   ├── stations_router.py # Station management
│   ├── ml_router.py     # ML predictions
│   ├── aws_utils.py     # AWS integrations
│   └── geo_utils.py     # Geospatial utilities
├── frontend/             # React frontend
│   ├── src/
│   ├── package.json
│   └── ...
├── logs/                 # Application logs
├── uploads/              # Local file storage
└── models/               # ML model artifacts
```

## 🔐 Security Features

### Authentication & Authorization
- JWT tokens with configurable expiration
- Password strength validation
- Token version for mass invalidation
- Role-based route protection

### Data Protection
- PII filtering based on user roles
- Server-side access control
- File upload validation
- Rate limiting protection

### Anti-Plagiarism Compliance
- All AI outputs include disclaimer
- BNS sections are paraphrased interpretations
- Source attribution for all AI-generated content
- No verbatim copying of statutory text

## 🌍 Multilingual Support

### Supported Languages
1. **English** (en) - Default
2. **Tamil** (ta) - தமிழ்
3. **Telugu** (te) - తెలుగు
4. **Hindi** (hi) - हिन्दी
5. **Kannada** (kn) - ಕನ್ನಡ
6. **Malayalam** (ml) - മലയാളം

### Implementation
- Frontend: `react-i18next` with resource files
- Backend: Localized error messages and responses
- Fallback: English for missing translations
- Persistence: User language preference in localStorage

## 📊 Monitoring & Analytics

### Health Checks
```bash
# Check system health
curl http://localhost:8000/health

# Check ML model status  
curl http://localhost:8000/ml/health

# Check AWS services
curl http://localhost:8000/admin/analytics
```

### Logging
- Structured logging with rotation
- CloudWatch integration (optional)
- Error tracking and monitoring
- Performance metrics

## 🚨 Fallback Systems

### Database
- PostgreSQL → SQLite fallback
- Automatic table creation
- Connection pooling with health checks

### File Storage
- S3 → Local filesystem fallback  
- Automatic directory creation
- File validation and security

### Messaging
- SNS SMS → Mock SMS fallback
- Message queuing and retry logic
- Notification templates

### ML/AI
- XGBoost → Rule-based fallback
- Gemini AI → Curated responses
- Confidence scoring

## ⚙️ Configuration

### Essential Settings
```env
# Security (REQUIRED)
JWT_SECRET=your-secure-random-string

# Database (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:pass@localhost/db

# AWS (Optional - enables cloud features)
AWS_ACCESS_KEY_ID=your-key
S3_BUCKET=your-bucket
SNS_TOPIC_ARN=your-topic
```

### Advanced Settings
- Rate limiting configuration
- File upload limits
- Victim confirmation windows
- ML model paths
- Logging levels

## 🧪 Testing

### Manual Acceptance Tests

1. **System Startup**
   - [ ] `python main.py` starts without errors
   - [ ] Database tables created automatically
   - [ ] Health endpoint returns system status

2. **Complaint Filing**
   - [ ] GPS capture works or graceful fallback
   - [ ] Camera capture or file upload fallback
   - [ ] Nearest station auto-assignment
   - [ ] Complaint ID generation (CT-{timestamp})
   - [ ] SMS notification or mock display

3. **Tracking**
   - [ ] Lookup by complaint ID shows details
   - [ ] Lookup by phone shows list or sends SMS
   - [ ] BNS suggestions with disclaimer
   - [ ] AI precautions or fallback messages

4. **Police Workflow**
   - [ ] Registration requires admin approval
   - [ ] Login with approved account
   - [ ] Station-scoped complaint view
   - [ ] Case acceptance (atomic operation)
   - [ ] Status updates propagate to tracking

5. **Admin Functions**
   - [ ] Approve pending registrations
   - [ ] View global analytics
   - [ ] Reassign cases
   - [ ] System health monitoring

6. **Fallback Testing**
   - [ ] Run without AWS credentials (local mode)
   - [ ] Run without ML models (rule-based)
   - [ ] Run without Gemini key (curated responses)

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - System will fallback to SQLite

2. **File Upload Errors**
   - Check upload directory permissions
   - Verify S3 credentials (if using)
   - System will fallback to local storage

3. **SMS Not Sending**
   - Verify SNS configuration
   - Check phone number format
   - System will show mock SMS content

4. **ML Predictions Failing**
   - Check models directory exists
   - Verify model file formats
   - System will use rule-based fallback

### Logs Location
- Application logs: `logs/crimetracer.log`
- Error logs: Console output
- CloudWatch: If AWS configured

## 📞 Support

### System Requirements
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB recommended  
- Storage: 10GB for system + uploads
- Network: Internet for AWS features

### Performance Guidelines
- Expected load: 1000 complaints/day
- Database scaling: PostgreSQL recommended for production
- File storage scaling: S3 recommended for production
- Caching: Redis recommended for high-traffic deployments

---

**CrimeTracer** - Building safer communities through technology 🛡️

For issues or questions, please check the logs and ensure all prerequisites are met. The system is designed to be robust with multiple fallback mechanisms to ensure continuous operation.
