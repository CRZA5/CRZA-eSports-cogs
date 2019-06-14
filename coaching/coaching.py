import discord
from discord.ext import commands
import asyncio

BOTCOMMANDER_ROLES = ["Mod", "admin", "Member"]

icon = "https://i.imgur.com/YqLKAzg.png"
credit = "Bot by CRZA eSports"

class coaching:
  
    """CRZAeSports coaching cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def coaching(self, ctx):

        msg_timeout = ("I had to wait too long. "
                       "Start over by typing !coaching again!")
        msg_stop = "Stopped."
        msg_start = "**Hello! I will ask you few questions, let's move to DM!**"
        msg_start_dm = "**Lets start! You can stop anytime by typing \"stop\". Keep in Mind answer the questions properly, donate make funs. or Ban!** "

        user = ctx.message.author
        channel = await self.bot.start_private_message(user)
        channel_req = self.bot.get_channel("588659301833375744")
        server_req = self.bot.get_server("567325025649033236")
        coach_role = discord.utils.get(server_req.roles, name="Coach")

        await self.bot.send_message(ctx.message.channel, msg_start)
        await self.bot.send_message(channel, msg_start_dm)
        await asyncio.sleep(3)
        await self.bot.send_message(channel, "**What's your in-game name in Brawlstars?**")
        reply = (await self.bot.wait_for_message(channel=channel, author=user, timeout=90))
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            ingame_name = reply.content

        await self.bot.send_message(channel, "**How many trophies do you have?**")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=90)
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            trophies = reply.content

        await self.bot.send_message(channel, "**What do you want to learn/tips?**")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=120)
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            info = reply.content

        await self.bot.send_message(channel, "**What time do you prefer (with timezones) for coaching?**")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=120)
        if reply is None:
            await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            time = reply.content

        await self.bot.send_message(channel, "**Do you have anything else you want to add? (Type \"No\" if not)**")
        reply = await self.bot.wait_for_message(channel=channel, author=user, timeout=120)
        if reply is None:
            return await self.bot.send_message(channel, msg_timeout)
        elif reply.content.lower() == "stop":
            return await self.bot.send_message(channel, msg_stop)
        else:
            more_info = reply.content

                # Embed Code
        embed = discord.Embed(colour=0xff0000)
        embed.add_field(name="**Request by:**", value=user)
        embed.add_field(name="**In-game name:**", value=ingame_name)
        embed.add_field(name="**Trophies:**", value=trophies)
        embed.add_field(name="**Wants to Learn:**", value=info)
        embed.add_field(name="**Time:**", value=time)
        embed.add_field(name="**Additional Info:**", value=more_info)
        embed.title = "**New Coaching Request**"
        embed.set_footer(text=credit, icon_url=icon)
        await self.bot.send_message(channel_req, content=coach_role.mention + 'Request By: ' + user.mention, embed=embed)
        
        await self.bot.send_message(channel, "Ok! I sent your request to coaches, "
                                             "someone will get to you as soon as possible. Our coach will talk with you via Modmail Soon!")


def setup(bot):
    bot.add_cog(coaching(bot))
