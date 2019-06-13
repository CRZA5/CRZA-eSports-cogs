import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from cogs.utils import checks
import asyncio
import math
from PIL import Image
import re
import os
import aiohttp


class shop:
    """Legend Family Shop for credits"""

    def __init__(self, bot):
        self.bot = bot
        self.banks = dataIO.load_json('data/economy/bank.json')
        self.session = aiohttp.ClientSession()

    async def updateBank(self):
        self.banks = dataIO.load_json('data/economy/bank.json')

    async def _add_roles(self, member, role_names):
        """Add roles"""
        server = member.server
        roles = [discord.utils.get(server.roles, name=role_name) for role_name in role_names]
        try:
            await self.bot.add_roles(member, *roles)
        except discord.Forbidden:
            raise
        except discord.HTTPException:
            raise

    async def _remove_roles(self, member, role_names):
        """Remove roles"""
        server = member.server
        roles = [discord.utils.get(server.roles, name=role_name) for role_name in role_names]
        try:
            await self.bot.remove_roles(member, *roles)
        except:
            pass

    async def _is_rare(self, member):
        server = member.server
        botcommander_roles = [discord.utils.get(server.roles, name=r) for r in ["Rare™"]]
        botcommander_roles = set(botcommander_roles)
        author_roles = set(member.roles)
        if len(author_roles.intersection(botcommander_roles)):
            return True
        else:
            return False

    async def _is_epic(self, member):
        server = member.server
        botcommander_roles = [discord.utils.get(server.roles, name=r) for r in ["Epic™"]]
        botcommander_roles = set(botcommander_roles)
        author_roles = set(member.roles)
        if len(author_roles.intersection(botcommander_roles)):
            return True
        else:
            return False

    async def _is_legendary(self, member):
        server = member.server
        botcommander_roles = [discord.utils.get(server.roles, name=r) for r in ["LeGeNDary™"]]
        botcommander_roles = set(botcommander_roles)
        author_roles = set(member.roles)
        if len(author_roles.intersection(botcommander_roles)):
            return True
        else:
            return False

    async def _is_payday(self, member):
        server = member.server
        botcommander_roles = [discord.utils.get(server.roles, name=r) for r in ["Propayday"]]
        botcommander_roles = set(botcommander_roles)
        author_roles = set(member.roles)
        if len(author_roles.intersection(botcommander_roles)):
            return True
        else:
            return False

    def bank_check(self, user, amount):
        bank = self.bot.get_cog('Economy').bank
        if bank.account_exists(user):
            if bank.can_spend(user, amount):
                return True
            else:
                return False
        else:
            return False

    async def _valid_image_url(self, url):

        try:
            async with self.session.get(url) as r:
                image = await r.content.read()

            with open('data/leveler/test.jpg', 'wb') as f:
                f.write(image)

            image = Image.open('data/leveler/test.jpg').convert('RGBA')

            size = os.path.getsize('data/leveler/test.jpg')
            if size > 50000:
                return "Image file size is too big."

            width, height = image.size
            if width != height:
                return "Image is not a square"

            os.remove('data/leveler/test.jpg')

            return None
        except:
            return "Image is not valid"


    @commands.group(pass_context=True)
    async def buy(self, ctx):
        """Buy different items from the CRZAeSports shop"""

        await self.bot.type()

        if ctx.invoked_subcommand is None:
            await self.bot.send_file(ctx.message.channel, 'data/shop/shop.png')

    @buy.command(pass_context=True, name="1")
    async def buy_1(self, ctx):
        """ Buy Payday Pro from the shop """
        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the CRZAeSports Server")

        payday = await self._is_payday(author)

        if payday:
            return await self.bot.say("You already have Pro Payday.")

        if self.bank_check(author, 30000):
            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 30000)
            await self._add_roles(author, ["Propayday"])
            await self.bot.say("Congratulations, now you can get !payday every 10 minutes.")
        else:
            await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="2")
    async def buy_2(self, ctx, imgurLink):
        """Buy custom background for your profile, picture must be in JPG and 490x490px
        Example command: !buy 2 https://i.imgur.com/2Oc5E9K.jpg"""
        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the CRZAeSports Server")

        if self.bank_check(author, 75000):
            pattern = re.compile(r"<?(https?:\/\/)?(www\.)?([i.]*)?(imgur\.com)\b([-a-zA-Z0-9/]*)>?(\.jpg)?")

            if not pattern.match(imgurLink):
                return await self.bot.say("The URL does not end in **.jpg** or is not from **i.imgur.com**. "
                                          "Please upload a JPG image to imgur.com and get a direct link.")

            validate = await self._valid_image_url(imgurLink)
            if validate is not None:
                return await self.bot.say(validate)

            message = ctx.message
            message.content = "{}lvladmin bg setcustombg profile {} {}".format(ctx.prefix, author.id, imgurLink)
            message.author = discord.utils.get(ctx.message.server.members, id="112356193820758016")

            await self.bot.process_commands(message)

            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 75000)

        else:
            await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="3")
    async def buy_3(self, ctx, emoji):

        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the CRZAeSports Server")

        if (emoji.startswith("<:") and emoji.endswith(">")) or (emoji.startswith("<a:") and emoji.endswith(">")):
            return await self.bot.say("Error, you can only use default emojis.")

        try:
            await self.bot.add_reaction(ctx.message, emoji)
        except (discord.errors.HTTPException, discord.errors.InvalidArgument):
            return await self.bot.say("Error, That's not an emoji I recognize.")

        if self.bank_check(author, 80000):
            ign = profiledata.name
            if ign is None:
                await self.bot.say("Error, Cannot add emoji.")
            else:
                try:
                    newname = "{} {} | Guest".format(ign, emoji)
                    await self.bot.change_nickname(author, newname)
                except discord.HTTPException:
                    await self.bot.say("I don’t have permission to change nick for this user.")
                else:
                    await self.bot.say("Nickname changed to ** {} **\n".format(newname))

                    bank = self.bot.get_cog('Economy').bank
                    bank.withdraw_credits(author, 80000)
        else:
            await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="4")
    async def buy_4(self, ctx):

        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the CRZAeSports Server")

        if self.bank_check(author, 90000):
            await self.bot.say("Please contact @★Cpt_Dark™★#6019 to purchase it for you.")
        else:
            await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="5")
    async def buy_5(self, ctx):
        """ Buy Rare Role from the shop """
        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the CRZAeSports Server")

        rare = await self._is_rare(author)
        epic = await self._is_epic(author)
        legendary = await self._is_legendary(author)

        if rare or epic or legendary:
            return await self.bot.say("You are already Rare™.")

        if self.bank_check(author, 250000):
            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 250000)
            await self._add_roles(author, ["Rare™"])
            await self.bot.say("Congratulations, you are now a **Rare™**")
        else:
            await self.bot.say("You do not have enough credits to buy this role.")

    @buy.command(pass_context=True, name="6")
    async def buy_6(self, ctx):
        """ Buy Epic Role from the shop """
        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the LeGeND Family Server")

        rare = await self._is_rare(author)
        epic = await self._is_epic(author)
        legendary = await self._is_legendary(author)

        if epic or legendary:
            return await self.bot.say("You are already Epic™.")

        if not rare:
            return await self.bot.say("You need to have **Rare™** to buy this role.")

        if self.bank_check(author, 750000):
            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 750000)
            await self._remove_roles(author, ["Rare™"])
            await asyncio.sleep(3)
            await self._add_roles(author, ["Epic™"])
            await self.bot.say("Congratulations, you are now a **Epic™**")
        else:
            await self.bot.say("You do not have enough credits to buy this role.")

    @buy.command(pass_context=True, name="7")
    async def buy_7(self, ctx):
        """ Buy Legendary Role from the shop """

        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the LeGeND Family Server")

        epic = await self._is_epic(author)
        legendary = await self._is_legendary(author)

        if legendary:
            return await self.bot.say("You are already LeGeNDary™.")

        if not epic:
            return await self.bot.say("You need to have **Epic™** to buy this role.")

        if self.bank_check(author, 1000000):
            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 1000000)
            await self._remove_roles(author, ["Epic™"])
            await asyncio.sleep(3)
            await self._add_roles(author, ["LeGeNDary™"])
            await self.bot.say("Congratulations, you are now a **LeGeNDary™**")
        else:
            await self.bot.say("You do not have enough credits to buy this role.")

    @buy.command(pass_context=True, name="8")
    async def buy_8(self, ctx):

        server = ctx.message.server
        author = ctx.message.author
        legendServer = ["567325025649033236"]

        if server.id not in legendServer:
            return await self.bot.say("This command can only be executed in the LeGeND Family Server")

        if self.bank_check(author, 4000000):
            await self.bot.say("please contact Crza™ Modmail to purchase it for you.")
        else:
            await self.bot.say("You do not have enough credits to buy Nitro.")


def setup(bot):
    bot.add_cog(shop(bot))
