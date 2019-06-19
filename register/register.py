import discord
from discord.ext import commands
import asyncio

BOTCOMMANDER_ROLES = ["Family Representative", "Clan Manager", "Clan Deputy",
                      "TournamentManager", "Hub Officer", "admin", "Member"]


class academy:
    """Crza Esports Tournament Register Command"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def register(self, ctx):

        msg_req = ("**Request by:** {}\n"
                   "**In-game name:** {}\n"
                   "**Trophies:** {}\n"
                   "**Attend at time:** {}\n"
                   "**Additional Request:** {}\n"
                   "**Additional info/suggestion:** {}\n{}")
        msg_timeout = ("**I had to wait too long. "
                       "Start over by typing `!register` again!**")
        msg_stop = "Stopped."
        msg_start = "**Hello! I will ask you few questions to you to keep record of this touenament, let's move to DM!**"
        msg_start_dm = "**Lets start! You can stop anytime by typing \"stop\". **"

        user = ctx.message.author
        channel = await self.bot.start_private_message(user)
        channel_req = self.bot.get_channel("590920114225020975")
        server_req = self.bot.get_server("567325025649033236")
        coach_role = discord.utils.get(server_req.roles, name="TournamentManager")

        await self.bot.send_message(ctx.message.channel, msg_start)
        await self.bot.send_message(channel, msg_start_dm)
        await asyncio.sleep(3)
        await self.bot.send_message(channel, "**What's your in-game name**?")
        reply = (await self.bot.wait_for_message(channel=channel, author=user, timeout=90))
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            ingame_name = reply.content

        await self.bot.send_message(channel, "How many trophies do you have?")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=90)
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            trophies = reply.content

        await self.bot.send_message(channel, "**Can you attend at right time of tournament? type `yes` or `no`**")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=120)
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            info = reply.content

        await self.bot.send_message(channel, "**Do you have any other requests to us? type `Yes` or `No`**")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=120)
        if reply is None:
            await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            time = reply.content

        await self.bot.send_message(channel, "**Do you have anything else you want to add or any tournament suggestion? (Type \"No\" if not)**")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=120)
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            more_info = reply.content

        await self.bot.send_message(channel_req,
                                    msg_req.format(
                                        user.mention,
                                        ingame_name,
                                        trophies,
                                        info,
                                        time,
                                        more_info,
                                        coach_role.mention)
                                    )

        await self.bot.send_message(channel, "**Ok! I sent your details to Managers!,** "
                                             "**Thank you!**.")


def setup(bot):
    bot.add_cog(academy(bot))
