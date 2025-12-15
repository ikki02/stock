import argparse
import logging
import os

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Specify WebHookURL to notify a slack channel.",
    )
    parser.add_argument(
        "--slack_webhook_url", type=str, default=os.getenv("WEBHOOK_URL"), help="WebHookURL to notify a slack channel."
    )
    args = parser.parse_args()
    logger.debug(f"Slack Webhook: {args.slack_webhook_url}")
    return args
