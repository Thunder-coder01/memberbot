import discord
from discord.ext.commands import (
    AutoShardedBot,
    bot_has_any_role,
    bot_has_guild_permissions,
    bot_has_permissions,
    bot_has_role,
    command,
    has_any_role,
    has_guild_permissions,
    has_permissions,
    has_role,
    Context,
    CommandOnCooldown,
    CommandError,
)
import jishaku
from asyncpg import (
    create_pool,
    ConnectionFailureError,
)
import os
from modules.client import Authorization, Color
from discord import Embed


class Bot(AutoShardedBot):
    """
    A bot that does invoices
    """

    def __init__(self: "Bot", *args, **kwargs) -> None:
        super().__init__(
            command_prefix=Authorization.prefix,
            intents=discord.Intents.all(),
            help_command=None,
            owner_ids=Authorization.owner_ids,
            activity=discord.Activity(
                type=discord.ActivityType.competing,
                url=Authorization.url,
                name="Fastly ⚡",
            ),
        )

    async def on_ready(self: "Bot") -> None:
        """
        Loads the needed things to debug
        """
        await self.load_features()
        await self.load_extension("jishaku")
        print("Ready.")

    async def on_connect(self: "Bot") -> None:
        """
        Connects to the actual websocket for discord
        And the database (postgres)
        """
        try:
            # self.db = await create_pool(
            #     **{
            #         "host": Authorization.db.host,
            #         "port": Authorization.db.port,
            #         "user": Authorization.db.user,
            #         "database": Authorization.db.database,
            #         "password": Authorization.db.password,
            #     },
            # )
            pass
        except Exception as e:
            raise Exception(f"Error logging into the db -> {e}")

    async def load_features(self: "Bot") -> None:
        """
        Loads all of the cogs
        """
        for root, dirs, files in os.walk("features"):
            for filename in files:
                if filename.endswith(".py"):
                    cog_name = os.path.join(root, filename)[:-3].replace(os.sep, ".")
                    try:
                        await self.load_extension(cog_name)
                        print(f"{cog_name} has been granted")
                    except:
                        pass

    def __run__(self: "Bot") -> None:
        """
        Runs the actual bot
        """
        Bot().run(
            token=Authorization.token,
            reconnect=True,
        )

    async def on_command_error(
        self: "Bot",
        ctx: Context,
        error: CommandError,
    ) -> None:
        if isinstance(error, CommandOnCooldown):
            return await ctx.error(
                "Command is on cooldown!",
            )

    async def get_context(self: "Bot", message: discord.Message, *, cls=None) -> None:
        """
        Custom Context
        """
        return await super().get_context(
            message,
            cls=cls or Bot.context,
        )

    class context(Context):
        """
        Custom Context Class
        """

        async def approve(self: "Bot.context", message: str) -> None:
            await self.send(
                embed=Embed(
                    title="**Woah, Success!**",
                    color=Color.blurple,
                    description=f"{message}",
                )
                .add_field(
                    name="**Did you know?**",
                    value="> You can invite or boost for a free upgrade rank!",
                    inline=False,
                )
                .set_footer(
                    text="⚡ Efficient Services by Fastly ⚡",
                    icon_url=self.author.display_avatar.url,
                )
                .set_author(
                    name="Fastly Members ⚡",
                    icon_url=self.guild.icon.url,
                )
                .set_thumbnail(
                    url=self.bot.user.display_avatar.url,
                )
            )

        async def warn(self: "Bot.context", message: str) -> None:
            await self.send(
                embed=Embed(
                    title="Warning",
                    color=Color.blurple,
                    description=f"{message}",
                )
                .add_field(
                    name="**Did you know?**",
                    value="> You can invite or boost for a free upgrade rank!",
                    inline=False,
                )
                .set_footer(
                    text="⚡ Efficient Services by Fastly ⚡",
                    icon_url=self.author.display_avatar.url,
                )
                .set_author(
                    name="Fastly Members ⚡",
                    icon_url=self.guild.icon.url,
                )
                .set_thumbnail(
                    url=self.bot.user.display_avatar.url,
                )
            )

        async def error(self: "Bot.context", message: str) -> None:
            await self.send(
                embed=Embed(
                    title="**Error Encountered**",
                    color=Color.blurple,
                    description=f"{message}",
                )
                .add_field(
                    name="**Did you know?**",
                    value="> You can invite or boost for a free upgrade rank!",
                    inline=False,
                )
                .set_footer(
                    text="⚡ Efficient Services by Thunder ⚡",
                    icon_url=self.author.display_avatar.url,
                )
                .set_author(
                    name="Thunder Members ⚡",
                    icon_url=self.guild.icon.url,
                )
                .set_thumbnail(
                    url=self.bot.user.display_avatar.url,
                )
            )

        async def normal(self: "Bot.context", message: str) -> None:
            await self.send(
                embed=Embed(
                    title="**Thunder Services**",
                    color=Color.blurple,
                    description=message,
                )
                .set_footer(
                    text="⚡ Efficient Services by Thunder ⚡",
                    icon_url=self.author.display_avatar.url,
                )
                .set_author(
                    name="Thunder Members ⚡",
                    icon_url=self.guild.icon.url,
                )
                .set_thumbnail(
                    url=self.bot.user.display_avatar.url,
                )
            )
