from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import jwt
import datetime
import hashlib
import os

# Configuração da aplicação
app = FastAPI(title="Evil Force JWT Auth API", version="1.1.0")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações JWT
SECRET_KEY = "evil_force_jwt_secret_key_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Modelos Pydantic
class UserBase(BaseModel):
    username: str
    permissions: List[str]

class UserCreate(UserBase):
    id: int
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    permissions: Optional[List[str]] = None

class User(UserBase):
    id: int
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Novo modelo para login
class LoginRequest(BaseModel):
    username: str
    password: str

# Dados em memória (em produção, use um banco de dados)
users_db = {
    1: {
        "id": 1, "username": "admin", "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "permissions": ["admin", "user"], "is_active": True
    },
    2: {
        "id": 2, "username": "user", "password": hashlib.sha256("user123".encode()).hexdigest(),
        "permissions": ["user"], "is_active": True
    }
}

# Funções auxiliares
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    for user in users_db.values():
        if user["username"] == username:
            return user
    return None

# Dependências
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Endpoints
@app.get("/api", include_in_schema=False)
async def api_root():
    """Endpoint de verificação de status para a API."""
    return {"message": "Evil Force JWT Auth API", "version": "1.1.0"}

@app.post("/api/login", response_model=Token)
async def login(form_data: LoginRequest):
    user = get_user(form_data.username)
    if not user or hashlib.sha256(form_data.password.encode()).hexdigest() != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Gera ui_permissions para o token
    ui_perms = {p: True for p in user['permissions']}
    all_perms = [
        "tab_dashboard", "tab_scan", "tab_jwt", "tab_fuzzing", "tab_osint",
        "tab_shodan", "tab_sql", "tab_crypto", "tab_wordlist", "tab_pipeline",
        "tab_fake_pix", "tab_database", "tab_settings", "chat_valac",
        "notifications", "vpn_manager"
    ]
    for p in all_perms:
        if p not in ui_perms:
            ui_perms[p] = False
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user["username"],
            "id": user["id"],
            "ui_permissions": ui_perms,
            "role": "admin" if "admin" in user["permissions"] else "user"
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users", response_model=List[User])
async def read_users():
    return [User(**user) for user in users_db.values()]

@app.post("/api/users", response_model=User)
async def create_user(user: UserCreate):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail=f"User ID {user.id} already exists")
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = {
        "id": user.id, 
        "username": user.username, 
        "password": hashlib.sha256(user.password.encode()).hexdigest(),
        "permissions": user.permissions, 
        "is_active": True
    }
    users_db[user.id] = new_user
    return User(**new_user)

@app.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user = users_db[user_id]
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password"] = hashlib.sha256(update_data["password"].encode()).hexdigest()
        
    for key, value in update_data.items():
        db_user[key] = value
        
    return User(**db_user)

@app.delete("/api/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}

@app.get("/api/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Retorna informações do usuário atual (requer token)"""
    return User(**{k: v for k, v in current_user.items() if k != "password"})

@app.get("/")
async def root():
    return {"message": "Evil Force JWT Auth API", "version": "1.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 