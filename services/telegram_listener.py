import time

from services.logger import logger

from services.telegram_bot import (
    get_updates,
    parse_callback,
    send_message
)

from services.database import (
    update_tweet_status
)


def start_listener():
    """
    Telegram polling listener.
    """

    logger.info(
        "Telegram listener started"
    )

    offset = None

    while True:

        try:

            updates = get_updates(offset)

            if (
                not updates
                or "result" not in updates
            ):

                time.sleep(1)

                continue

            for update in updates["result"]:

                offset = (
                    update["update_id"] + 1
                )

                # DEBUG TELEGRAM CHAT ID
                if "message" in update:

                    print(update)

                # CALLBACKS
                if "callback_query" not in update:
                    continue

                callback = update[
                    "callback_query"
                ]

                data = callback.get("data")

                result = parse_callback(data)

                if not result:
                    continue

                logger.info(
                    f"Callback received: "
                    f"{result}"
                )

                chat_id = (
                    callback["message"]["chat"]["id"]
                )

                # APPROVE
                if result["action"] == "approve":

                    update_tweet_status(
                        result["tweet_id"],
                        "approved"
                    )

                    logger.info(
                        f"Tweet "
                        f"{result['tweet_id']} "
                        f"APPROVED"
                    )

                    send_message(
                        chat_id,
                        f"✅ Tweet "
                        f"{result['tweet_id']} "
                        f"approved"
                    )

                # REJECT
                elif result["action"] == "reject":

                    update_tweet_status(
                        result["tweet_id"],
                        "rejected"
                    )

                    logger.info(
                        f"Tweet "
                        f"{result['tweet_id']} "
                        f"REJECTED"
                    )

                    send_message(
                        chat_id,
                        f"❌ Tweet "
                        f"{result['tweet_id']} "
                        f"rejected"
                    )

                # REGENERATE
                elif result["action"] == "regenerate":

                    logger.info(
                        f"Tweet "
                        f"{result['tweet_id']} "
                        f"REGENERATE requested"
                    )

                    send_message(
                        chat_id,
                        f"🔁 Regeneration requested "
                        f"for Tweet "
                        f"{result['tweet_id']}"
                    )

            time.sleep(1)

        except Exception as e:

            logger.error(
                f"listener error: {e}"
            )

            time.sleep(2)