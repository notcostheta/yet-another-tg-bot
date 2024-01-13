from bot import app
from bot.utils.logging import LOGGER

LOGGER(__name__).info("client successfully initiated....")
if __name__ == "__main__":
    app.run()
