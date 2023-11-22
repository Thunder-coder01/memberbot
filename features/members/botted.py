import aiohttp
import discord
from aiohttp import ClientError, ClientSession
from discord import Embed, Interaction
from discord.ext.commands import Cog, Context, command, cooldown
from discord.ui import View

from modules.bot import Bot
from modules.client import Authorization
from modules.managers.instagram.models import InstagramModel
from modules.managers.spammer import Spammerworker
from modules.managers.worker import Worker


class MemberBoost(Cog):
    """
    Member booster for joinify
    """

    def __init__(self: "MemberBoost", bot: Bot) -> None:
        self.bot: Bot = bot

    @command(
        name="ifollow",
    )
    async def ifollow(
        self: "MemberBoost",
        ctx: Context,
        username: str = None,
    ) -> None:
        channel = ctx.channel.id
        if not channel == Authorization.channels.farm:
            return await ctx.error("You cannot execute commands here!")
        if not username:
            return await ctx.error(
                "You must provide a valid instagram **username**!",
            )
        try:
            Model = InstagramModel(
                username=username,
            )
            r = await Model.__follow__()
            await ctx.approve(
                f"Now following `{username}` with `35` followers!",
            )

        except Exception as e:
            return await ctx.warn(e)

    @command(
        name="spam",
    )
    @cooldown(10, 15)
    async def mspam(
        self: "MemberBoost",
        ctx: Context,
        guildid: int,
        channelid: int,
        *,
        message: str = None,
    ) -> None:
        # return await ctx.error(
        #     "This command is currently paused!",
        # )
        guild = self.bot.get_guild(guildid)
        channel = ctx.channel.id
        if not channel == Authorization.channels.farm:
            return await ctx.error("You cannot execute commands here!")

        if guildid == 1161964377977663538:
            return await ctx.error(
                "This server is blacklisted from our bot.",
            )

        try:
            if not guild.owner.id == ctx.author.id:
                return await ctx.warn("You don't own this server! **Check pinned**")
        except:
            pass

        await ctx.approve(
            f"Now spamming `31` of `31` to {guild}!",
        )

        worker = Spammerworker(
            Amount=31,
            Channel=channelid,
            Guild=guild.id,
            Message=message if message else None,
        )
        await worker.__spammer__()

    @command(
        name="join",
    )
    @cooldown(10, 15)
    async def Join(
        self: "MemberBoost",
        ctx: Context,
        guildid: int,
    ) -> None:
        guild = self.bot.get_guild(guildid)
        channel = ctx.channel.id
        if not channel == Authorization.channels.farm:
            return await ctx.error("You cannot execute commands here!")

        if guildid == 1161964377977663538:
            return await ctx.error(
                "This server is blacklisted from our bot.",
            )

        try:
            if not guild.owner.id == ctx.author.id:
                return await ctx.warn("You don't own this server! **Check pinned**")
        except:
            pass

        if not guild:
            return await ctx.error(
                f"You must add me to `{guildid}`! **Check pinned**",
            )

        user_roles = ctx.author.roles
        role_to_members = {
            Authorization.roles.premium: 60,
            Authorization.roles.plat: 50,
            Authorization.roles.gold: 45,
            Authorization.roles.silver: 35,
            Authorization.roles.bronze: 20,
            Authorization.roles.member: 15,
        }

        max_members = 3

        for role_id, num_members in role_to_members.items():
            if role_id in [r.id for r in user_roles]:
                max_members = max(max_members, num_members)

        await ctx.approve(
            f"Now adding `{max_members}` of `{max_members}` to {guild}!",
        )

        worker = Worker(
            Amount=max_members,
            Guild=guild.id,
        )
        await worker.start()


async def setup(bot):
    """
    Sets up the cog
    """
    await bot.add_cog(MemberBoost(bot))
