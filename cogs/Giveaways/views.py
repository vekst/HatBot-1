from secrets import token_hex

import discord
from discord import ui

from snapcogs.bot import Bot
from snapcogs.utils.db import read_sql_query

from .base import SQL, Giveaway


class GiveawayView(ui.View):
    def __init__(
        self,
        bot: Bot,
        giveaway: Giveaway,
        *,
        components_id: dict[str, str] | None = None
    ):
        # do stuff here?
        super().__init__(timeout=None)
        if components_id is None:
            components_id = {
                "button": token_hex(16),
            }
        self.components_id = components_id
        self.bot = bot
        self.giveaway = giveaway

        enter_button = ui.Button(
            label="Enter!",
            emoji="\N{WRAPPED PRESENT}",
            style=discord.ButtonStyle.green,
            custom_id=components_id["button"],
        )
        enter_button.callback = self.on_enter
        self.add_item(enter_button)

    async def on_enter(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await self._add_entry(interaction.user)
        await interaction.response.send_message(
            "Thank you for entering the giveaway!", ephemeral=True
        )

    async def _add_entry(self, user: discord.User | discord.Member):
        """Add the entry to the DB."""

        await self.bot.db.execute(
            read_sql_query(SQL / "add_entry.sql"),
            {
                "giveaway_id": self.giveaway.giveaway_id,
                "user_id": user.id,
            },
        )

        await self.bot.db.commit()
