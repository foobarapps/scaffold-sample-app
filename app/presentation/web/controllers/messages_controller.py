import asyncio
import datetime
import json
import uuid

from quart import ResponseReturnValue
from scaffold.uuid7 import uuid7
from scaffold.web import (
    BaseController,
    controller,
    error_handler,
    login_required,
    route,
)
from werkzeug.exceptions import Unauthorized

from app.application.services.message_service import MessageService


@controller(name="messages", url_prefix="/messages")
class MessagesController(BaseController):
    def __init__(
        self,
        message_service: MessageService,
    ) -> None:
        self.message_service = message_service

    @error_handler(Unauthorized)
    def handle_unauthorized(self, exception: Unauthorized) -> ResponseReturnValue:
        return self.redirect(self.url_for("home.index"))

    @route("/")
    @login_required
    async def index(self) -> ResponseReturnValue:
        user_id = self.session["user_id"]
        messages = await self.message_service.get_messages_for_conversation(user_id)
        return await self.render_template("messages/index.html", messages=messages)

    @route("/", websocket=True)
    @login_required
    async def websockets(self) -> None:
        user_id = self.session["user_id"]
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.receive_websocket_messages(user_id))
                tg.create_task(self.send_websocket_messages(user_id))

        except asyncio.CancelledError:
            # Handle disconnection here
            raise

    async def receive_websocket_messages(
        self,
        user_id: uuid.UUID,
    ) -> None:
        while True:
            data = json.loads(await self.websocket.receive())

            await self.message_service.send_user_message(
                user_id=user_id,
                message_id=uuid7(),
                content=data["content"],
                sent_at=datetime.datetime.now(),
            )

    async def send_websocket_messages(
        self,
        user_id: uuid.UUID,
    ) -> None:
        async for message in self.message_service.subscribe_to_user_messages(user_id=user_id):
            response = await self.render_template(
                "messages/partials/conversation.html",
                messages=[message],
            )
            await self.websocket.send(response)
