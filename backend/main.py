from backend.api.endpoints.v1.chat_message_service import app
import uvicorn
from loguru import logger

def main():
    logger.info("initializing!\n\n")
    uvicorn.run(app, host="0.0.0.0", port=9012)


if __name__ == "__main__":
    main()
