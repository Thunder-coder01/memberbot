from discord.ext.commands import (
    command,
    Cog,
    group,
    Context,
    is_owner,
)
from discord import Embed
from modules.bot import Bot
from modules.client import Color


class Other(Cog):
    """
    Other stuff
    """

    def __init__(self: "Other", bot: Bot, *args, **kwargs) -> None:
        self.bot: Bot = bot

    @command()
    async def stock(self: "Other", ctx: Context) -> None:
        """
        Checks stock
        """
        stock = len(open("tokens.txt", "r").readlines())
        mstock = len(open("modules/managers/spammers.txt").readlines())
        return await ctx.send(
            embed=Embed(
                title="Fastly Member's Stock",
                color=Color.blurple,
            )
            .add_field(
                name="**Member's Stock**",
                value=f"{stock:,}",
                inline=False,
            )
            .add_field(
                name="**Member Messages**",
                value=f"{mstock:,}",
                inline=True,
            )
            .set_author(
                name=ctx.author.name,
                icon_url=ctx.author.display_avatar.url,
            )
            .set_thumbnail(
                url=self.bot.user.display_avatar.url,
            )
        )

    @command()
    @is_owner()
    async def restock(self: "Other", ctx: Context) -> None:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment:
                attachment_data = await attachment.read()
                attachment_content = attachment_data.decode("utf-8")

                with open("tokens.txt", "a") as tokens_file:
                    tokens_file.write(attachment_content)

                await ctx.approve("Successfully restocked.")
        else:
            await ctx.error("No attachment found in the message.")


async def setup(bot):
    """
    Runs the other cog
    """
    await bot.add_cog(Other(bot))
