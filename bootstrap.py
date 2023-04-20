from tusk.api.app import app
from dotenv import load_dotenv
import uvicorn

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("tusk.api.app:app", host="0.0.0.0", port=8888)