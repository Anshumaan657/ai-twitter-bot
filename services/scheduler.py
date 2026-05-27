import time
import schedule

from main import main

from services.logger import logger


# -----------------------------
# PIPELINE LOCK
# -----------------------------
is_running = False


# -----------------------------
# JOB
# -----------------------------
def run_pipeline():

    global is_running

    # Prevent overlapping jobs
    if is_running:

        logger.warning(
            "Previous pipeline still running"
        )

        return

    try:

        is_running = True

        logger.info(
            "Running scheduled pipeline..."
        )

        main()

        logger.info(
            "Pipeline completed"
        )

    except Exception as e:

        logger.error(
            f"Scheduler error: {e}"
        )

    finally:

        is_running = False


# -----------------------------
# RUN IMMEDIATELY ON STARTUP
# -----------------------------
run_pipeline()


# -----------------------------
# SCHEDULE EVERY 6 HOURS
# -----------------------------
schedule.every(6).hours.do(
    run_pipeline
)


logger.info(
    "Scheduler started..."
)


# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    try:

        schedule.run_pending()

        time.sleep(30)

    except KeyboardInterrupt:

        logger.info(
            "Scheduler stopped manually"
        )

        break

    except Exception as e:

        logger.error(
            f"Scheduler loop error: {e}"
        )

        time.sleep(10)