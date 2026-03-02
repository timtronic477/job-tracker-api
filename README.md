# Job Application Tracker API

A RESTful API for tracking job applications with advanced filtering, search, and analytics capabilities. Built with FastAPI and PostgreSQL, fully containerized with Docker.

🔗 **Live Demo:** https://job-tracker-api-rm4v.onrender.com/docs

---

## Features

- **Full CRUD Operations** — Create, read, update, and delete job applications
- **Advanced Search** — Case-insensitive text search across company and position fields
- **Date Filtering** — Query applications from the last N days
- **Flexible Sorting** — Sort by date, company, position, or status
- **Pagination** — Handle large datasets efficiently with limit/offset
- **Analytics** — Track total applications, offers, and acceptance rates
- **Status Filtering** — Filter active applications (applied/interviewing)

---

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Containerization:** Docker & Docker Compose
- **Deployment:** Render
- **Language:** Python 3.12

---

## API Documentation

Interactive API documentation available at `/docs` endpoint.

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/applications` | Get all applications (with sorting & pagination) |
| POST | `/applications` | Create new application |
| GET | `/applications/{id}` | Get single application |
| PUT | `/applications/{id}` | Update application |
| DELETE | `/applications/{id}` | Delete application |
| GET | `/applications/search?query={text}` | Search by company or position |
| GET | `/applications/recent?days={n}` | Get applications from last N days |
| GET | `/applications/active` | Get active applications (applied/interviewing) |
| GET | `/applications/stats` | Get analytics (total, offers, acceptance rate) |

### Example Request
```bash
curl -X POST "https://job-tracker-api-rm4v.onrender.com/applications" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Google",
    "position": "Software Engineer",
    "status": "applied",
    "notes": "Applied through referral"
  }'
```

---

## Local Setup

### Prerequisites

- Docker & Docker Compose installed
- Git

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/job-tracker-api.git
   cd job-tracker-api
```

2. **Create `.env` file**
```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=job_tracker
   DATABASE_URL=postgresql://postgres:your_password@db:5432/job_tracker
```

3. **Start the application**
```bash
   docker-compose up --build
```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - API: http://localhost:8000

---

## Database Schema
```sql
applications
├── id (Integer, Primary Key)
├── company (String, Required)
├── position (String, Required)
├── status (String, Default: "applied")
├── notes (Text, Optional)
├── created_at (Timestamp)
└── updated_at (Timestamp)
```

---

## Project Structure
```
job-tracker-api/
├── main.py              # FastAPI application & routes
├── models.py            # SQLAlchemy database models
├── database.py          # Database connection & session management
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Multi-container orchestration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not in repo)
```

---

## Future Improvements

- [ ] User authentication (JWT tokens)
- [ ] Email reminders for follow-ups
- [ ] Export data to CSV/PDF
- [ ] Application timeline tracking
- [ ] Interview scheduling integration

---

## Author

**Your Name**
- GitHub: [timtronic477](https://github.com/timtronic477/)
- LinkedIn: [Timothy Balilo](https://linkedin.com/in/timothy-balilo)

---

## License

MIT License - feel free to use this project for learning or as a template for your own applications.