from pathlib import Path
from app import create_app

Path('instance').mkdir(exist_ok=True)
app = create_app()
