import sys
import json
from pathlib import Path

# корень проекта в sys.path, чтобы были видны модули config и models из корня репозитория
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

docs_path = PROJECT_ROOT / "docs.json"

from main import app

if __name__ == "__main__":
    docs = app.openapi()

    with open(docs_path, 'w', encoding="utf-8") as file:
        json.dump(app.openapi(), 
                  file,
                  indent=2,
                  ensure_ascii=False)