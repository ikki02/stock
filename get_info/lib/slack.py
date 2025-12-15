import logging

from slack_sdk.webhook import WebhookClient

logger = logging.getLogger(__name__)


def notify_slack(url: str, text: str) -> None:
    webhook = WebhookClient(url)

    response = webhook.send(
        text=text,
    )

    logger.debug(f"Slack通知ステータスコード: {response.status_code}")
