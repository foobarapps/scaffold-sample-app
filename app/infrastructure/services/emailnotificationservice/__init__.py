from typing import override

from scaffold.email_notification_service import (
    EmailNotificationService as BaseEmailNotificationService,
)
from scaffold.email_notification_service import Message

from app.application.interfaces.notification_service import NotificationService


class EmailNotificationService(BaseEmailNotificationService, NotificationService):
    @override
    async def send_welcome_message(self, email: str) -> None:
        text = await self.render_template("text/welcome.txt")

        message = Message(
            subject="Welcome!",
            recipients=[email],
            sender=self.default_sender_email,
            body=text,
        )
        await self.mail_sender.send(message)
