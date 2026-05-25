import time

from services.telegram_bot import get_updates, handle_callback
from services.logger import logger


def start_listener():
    """
    Poll Telegram for button clicks and handle them.
    """

    logger.info("Telegram listener started")

    offset = None

    while True:

        try:
            updates = get_updates(offset)

            if not updates or "result" not in updates:
                time.sleep(2)
                continue

            for update in updates["result"]:

                offset = update["update_id"] + 1

                if "callback_query" not in update:
                    continue

                callback = update["callback_query"]

                data = callback.get("data")

                chat_id = callback["message"]["chat"]["id"]

                result = handle_callback(data)

                logger.info(f"Telegram action received: {result}")

                # OPTIONAL: respond back to user
                if result["action"] == "approve":
                    logger.info("Tweet APPROVED")

                elif result["action"] == "reject":
                    logger.info("Tweet REJECTED")

                elif result["action"] == "regenerate":
                    logger.info("Tweet REGEN requested")

            time.sleep(1)

        except Exception as e:
            logger.error(f"Listener error: {e}")
            time.sleep(3)