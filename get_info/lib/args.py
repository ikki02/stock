import argparse
import logging
import os

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--symbol", type=str, default="7203.T", help="stock symbol to get price."
    )
    parser.add_argument(
        "--slack_webhook_url", type=str, default=os.getenv("WEBHOOK_URL"), help="WebHookURL to notify a slack channel."
    )
    args = parser.parse_args()
    if args.slack_webhook_url:
        logger.debug(f"Slack Webhook: {args.slack_webhook_url}")
    return args
