import uuid

from quart import ResponseReturnValue
from scaffold.web import BaseController, controller, route

from app.application.services.user_service import UserService
from app.presentation.web.forms import SignUpForm


@controller(name="users")
class UsersController(BaseController):
    def __init__(
        self,
        user_service: UserService,
    ) -> None:
        self.user_service = user_service

    @route("/")
    async def index(self) -> ResponseReturnValue:
        if "user_id" in self.session:
            return self.redirect(self.url_for("messages.index"))

        form = SignUpForm()
        return await self.render_template("users/index.html", form=form)

    @route("/", methods=["POST"])
    async def create(self) -> ResponseReturnValue:
        form = SignUpForm(await self.request.form)

        if form.validate():
            user_id = uuid.uuid4()
            await self.user_service.sign_up_user(user_id=user_id, email=form.email.data)
            self.session["user_id"] = user_id
            return self.redirect(self.url_for(".index"))

        return await self.render_template("users/index.html", form=form)
