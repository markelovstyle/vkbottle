from typing import Dict, NoReturn

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser import ABCStateDispenser
from vkbottle.dispatch.views import ABCView
from vkbottle.modules import logger
from .abc import ABCRouter


class BotRouter(ABCRouter):
    async def route(self, event: dict, ctx_api: "ABCAPI") -> NoReturn:  # type: ignore
        logger.debug("Routing update {}".format(event))

        for view in self.views.values():
            if not await view.process_event(event):
                continue
            await view.handle_event(event, ctx_api, self.state_dispenser)

    def construct(
        self, views: Dict[str, "ABCView"], state_dispenser: ABCStateDispenser
    ) -> "BotRouter":
        self.views = views
        self.state_dispenser = state_dispenser
        return self
