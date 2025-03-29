# FastAPI Tutorial

## Setup

### Activate virtual environment

```
# On Windows
.\venv\Scripts\activate

# On Unix/Linux
source ./venv/bin/activate
```

### Initialize Database

```
python -c "from app.database import engine; from app.models.models import base; base.metadata.create_all(bind=engine)"
```

### Run Application

```
# Option 1
python -m app.main

# Option 2
uvicorn app.main:app --reload --host localhost --port 5000
```


## API Documentation

When the server is running, you can access:
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc