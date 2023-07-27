import logging
from typing import Sequence

from slack_sdk import WebhookClient
from slack_sdk.models.blocks import TextObject, HeaderBlock, ContextBlock, ButtonElement, ActionsBlock, SectionBlock, \
    DividerBlock, Block

from src.notification.notificationClient import NotificationClient
from src.record import Record

class SlackClient(NotificationClient):

    def __init__(self, webhook_url):
        self.webhook = WebhookClient(url=webhook_url)

    def notify_new_record(self, record: Record):
        message_blocks = [DividerBlock(), SectionBlock(
                text=TextObject(text=f"*{record.metadata.publisher}* published a new dataset at M Cube Datahub :tada:",

                                type="mrkdwn"))]
        message_blocks.extend(self.build_record_message_blocks(record))
        self.__send(message_blocks)

    def notify_updated_record(self, record: Record):
        message_blocks = [DividerBlock(), SectionBlock(
            text=TextObject(text=f"*{record.metadata.publisher}* updated the following dataset at M Cube Datahub "
                                 f":bookmark:",

                            type="mrkdwn"))]
        message_blocks.extend(self.build_record_message_blocks(record))
        self.__send(message_blocks)

    def __send(self, message_blocks: Sequence[Block]):
        response = self.webhook.send(blocks=message_blocks)
        if not (response.status_code == 200 and response.body == "ok"):
            logging.error(f"Slack message has not been sent")
    @staticmethod
    def build_record_message_blocks(record: Record):
        blocks = [
            HeaderBlock(
                text=record.metadata.title
            )]

        context_elements = []
        if record.metadata.description:
            description = record.metadata.description
            description = NotificationClient.clean_html_str(description)
            description = NotificationClient.shorten_string(description)
            context_elements.append(
                TextObject(text=f"*Description*: {description}",
                           type="mrkdwn")
            )
        if record.metadata.creators:
            context_elements.append(
                TextObject(
                    text="*Authors*: " + " ".join([creator.person_or_org.name for creator in record.metadata.creators]),
                    type="mrkdwn")
            )
        if context_elements:
            blocks.append(ContextBlock(elements=context_elements))

        button = ButtonElement(
            text="Take me there!",
            style="primary",
            url=record.links.latest_html.unicode_string())

        blocks.append(ActionsBlock(elements=[button]))

        return blocks
