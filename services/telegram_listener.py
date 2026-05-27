import time

from services.logger import logger

from services.telegram_bot import (
    get_updates,
    parse_callback,
    send_message
)

from services.database import (
    update_tweet_status,
    get_tweet_by_id,
    save_tweet
)


def start_listener():
    """
    Telegram polling listener.
    """

    logger.info("Telegram listener started")

    offset = None

    while True:

        try:

            updates = get_updates(offset)

            if not updates or "result" not in updates:
                time.sleep(1)
                continue

            for update in updates["result"]:

                offset = update["update_id"] + 1

                # DEBUG
                if "message" in update:
                    print(update)

                # ONLY CALLBACKS
                if "callback_query" not in update:
                    continue

                callback = update["callback_query"]
                data = callback.get("data")

                result = parse_callback(data)

                if not result:
                    continue

                chat_id = callback["message"]["chat"]["id"]

                logger.info(f"Callback received: {result}")

                tweet_id = result["tweet_id"]
                action = result["action"]

                # -------------------------
                # APPROVE
                # -------------------------
                if action == "approve":

                    update_tweet_status(tweet_id, "approved")

                    send_message(
                        chat_id,
                        f"✅ Tweet {tweet_id} approved"
                    )

                # -------------------------
                # REJECT
                # -------------------------
                elif action == "reject":

                    update_tweet_status(tweet_id, "rejected")

                    send_message(
                        chat_id,
                        f"❌ Tweet {tweet_id} rejected"
                    )

                # -------------------------
                # REGENERATE (REAL FLOW NOW)
                # -------------------------
                elif action == "regenerate":

                    old_tweet = get_tweet_by_id(tweet_id)

                    if not old_tweet:
                        send_message(chat_id, "⚠️ Tweet not found")
                        continue

                    # mark old as rejected
                    update_tweet_status(tweet_id, "rejected")

                    # create new pending tweet
                    new_tweet_id = save_tweet(
                        tweet_text=old_tweet[1],
                        article_title=old_tweet[2],
                        score=old_tweet[3]
                    )

                    send_message(
                        chat_id,
                        f"🔁 Regenerated!\n"
                        f"Old: {tweet_id}\n"
                        f"New: {new_tweet_id}"
                    )

                else:
                    logger.warning(f"Unknown action: {action}")

            time.sleep(1)

        except Exception as e:
            logger.error(f"listener error: {e}")
            time.sleep(2)