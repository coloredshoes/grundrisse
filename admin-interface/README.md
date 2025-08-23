# Grundrisse Admin Interface

A containerized admin interface for managing content sources in the Grundrisse project.

## Architecture

- **Backend**: FastAPI with SQLite database
- **Frontend**: React TypeScript with modern UI
- **Containerization**: Docker with docker-compose

## Features

### Current (MVP)
- ✅ Secure admin authentication
- ✅ YouTube channel registration
- ✅ Source management (list, add, delete)
- ✅ Responsive web interface
- ✅ Containerized deployment

### Planned
- [ ] Source status monitoring
- [ ] Batch source import
- [ ] RSS feed support
- [ ] Podcast source support
- [ ] Content indexing status

## Quick Start

### Using Docker (Recommended)

1. **Start the services:**
   ```bash
   cd admin-interface
   docker-compose up --build
   ```

2. **Access the interface:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

3. **Login with demo credentials:**
   - Username: `admin`
   - Password: `admin123`

### Development Setup

#### Backend Development
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend Development
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Authentication
- `POST /auth/login` - Login with username/password
- `GET /auth/me` - Get current user info

### Sources
- `GET /sources` - List all sources
- `POST /sources` - Create new source
- `DELETE /sources/{id}` - Delete source

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `password_hash`
- `created_at`

### Sources Table
- `id` (Primary Key)
- `name` - Display name for the source
- `type` - Source type (youtube, rss, podcast)
- `url` - Source URL
- `is_active` - Whether source is active
- `created_at` / `updated_at`

## User Stories Implemented

### US-001: Autenticação de Administrador ✅
- Secure login with JWT tokens
- Session management with token validation
- Automatic logout on invalid tokens

### US-002: Cadastro de Canal do YouTube ✅
- Add YouTube channels via URL
- Basic validation of input
- Store channel metadata

### US-003: Listagem de Fontes Cadastradas ✅
- View all registered sources
- Show source status and metadata
- Delete sources with confirmation

## Configuration

### Environment Variables
- `SECRET_KEY` - JWT signing key (change in production!)

### Database
- SQLite database stored in `backend/admin.db`
- Automatically initialized on first run
- Default admin user created automatically

## Security Notes

⚠️ **Important for Production:**
1. Change the `SECRET_KEY` environment variable
2. Use a proper database (PostgreSQL recommended)
3. Implement proper password hashing (currently using SHA256)
4. Add rate limiting
5. Use HTTPS
6. Implement proper CORS policies

## Development Notes

### Adding New Source Types
1. Update the `type` field options in the frontend
2. Add validation logic in the backend
3. Implement source-specific metadata collection

### Database Migrations
Currently using SQLite with simple table creation. For production:
1. Implement proper migrations
2. Use Alembic for schema changes
3. Switch to PostgreSQL or similar

## Troubleshooting

### Common Issues

**Frontend can't connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in `main.py`
- Verify API URLs in frontend components

**Docker build fails:**
- Ensure Docker and docker-compose are installed
- Check for port conflicts (3000, 8000)
- Try `docker-compose down` and rebuild

**Login fails:**
- Use default credentials: admin/admin123
- Check browser console for errors
- Verify backend logs for authentication issues

## Next Steps

1. **Implement US-004**: YouTube metadata collection
2. **Add monitoring**: Source health checks
3. **Improve security**: Better password hashing, rate limiting
4. **Add tests**: Unit and integration tests
5. **Production deployment**: Kubernetes manifests, proper secrets management