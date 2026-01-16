from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS設定 (Reactからのアクセスを許可) ---
# Viteのデフォルトポートは "http://localhost:5173" です
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # すべてのメソッド (GET, POSTなど) を許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# --- エンドポイント定義 ---
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/data")
def get_data():
    return {"data": [1, 2, 3, 4, 5]}