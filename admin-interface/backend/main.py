from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import hashlib
from jose import jwt
from datetime import datetime, timedelta
import os
import edgedb

app = FastAPI(title="Grundrisse Admin API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

# EdgeDB client
client = None

# Database setup
async def init_db():
    global client
    # Connect to EdgeDB instance
    client = edgedb.create_async_client(
        host=os.getenv("EDGEDB_HOST", "localhost"),
        port=int(os.getenv("EDGEDB_PORT", "5656")),
        database=os.getenv("EDGEDB_DATABASE", "grundrisse"),
    )
    
    # Create default admin user if it doesn't exist
    password_hash = hashlib.sha256("admin123".encode()).hexdigest()
    
    await client.query("""
        INSERT User {
            username := 'admin',
            password_hash := <str>$password_hash
        } UNLESS CONFLICT ON .username
    """, password_hash=password_hash)

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class Source(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    url: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class SourceCreate(BaseModel):
    name: str
    type: str
    url: str

class User(BaseModel):
    id: Optional[str] = None
    username: str

# Auth functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    if client:
        await client.aclose()

@app.post("/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()
    
    user = await client.query_single("""
        SELECT User {
            username
        }
        FILTER .username = <str>$username AND .password_hash = <str>$password_hash
    """, username=login_data.username, password_hash=password_hash)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": login_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
async def get_current_user(username: str = Depends(verify_token)):
    return {"username": username}

@app.get("/sources", response_model=List[Source])
async def get_sources(username: str = Depends(verify_token)):
    sources = await client.query("""
        SELECT Source {
            id,
            name,
            type,
            url,
            is_active,
            created_at,
            updated_at
        }
        ORDER BY .created_at DESC
    """)
    
    return [
        Source(
            id=str(source.id),
            name=source.name,
            type=source.type,
            url=source.url,
            is_active=source.is_active,
            created_at=source.created_at,
            updated_at=source.updated_at
        )
        for source in sources
    ]

@app.post("/sources", response_model=Source)
async def create_source(source: SourceCreate, username: str = Depends(verify_token)):
    new_source = await client.query_single("""
        INSERT Source {
            name := <str>$name,
            type := <str>$type,
            url := <str>$url
        }
    """, name=source.name, type=source.type, url=source.url)
    
    # Fetch the complete source with all fields
    complete_source = await client.query_single("""
        SELECT Source {
            id,
            name,
            type,
            url,
            is_active,
            created_at,
            updated_at
        }
        FILTER .id = <uuid>$id
    """, id=new_source.id)
    
    return Source(
        id=str(complete_source.id),
        name=complete_source.name,
        type=complete_source.type,
        url=complete_source.url,
        is_active=complete_source.is_active,
        created_at=complete_source.created_at,
        updated_at=complete_source.updated_at
    )

@app.delete("/sources/{source_id}")
async def delete_source(source_id: str, username: str = Depends(verify_token)):
    try:
        deleted = await client.query_single("""
            DELETE Source
            FILTER .id = <uuid>$source_id
        """, source_id=source_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Source not found")
        
        return {"message": "Source deleted successfully"}
    except edgedb.InvalidValueError:
        raise HTTPException(status_code=400, detail="Invalid source ID format")

@app.get("/")
async def root():
    return {"message": "Grundrisse Admin API", "version": "1.0.0", "database": "EdgeDB (Gel)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)