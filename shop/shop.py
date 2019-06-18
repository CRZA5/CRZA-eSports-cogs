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
import logging


class shop:
    """CRZA Shop for credits"""

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

        payday = await self._is_payday(author)

        if payday:
            return await self.bot.say("You already have Pro Payday.")

        if self.bank_check(author, 30000):
            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 30000)
            await self._add_roles(author, ["Propayday"])
            await self.bot.say("Congratulations, now you can get !payday every 10 minutes.")
            logger.info("{}({}) bought Propayday role.".format(author.name, author.id))
        else:
            await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="2")
    async def buy_2(self, ctx, imgurLink):
        """Buy custom background for your profile, picture must be in JPG and 490x490px
        Example command: !buy 2 https://i.imgur.com/2Oc5E9K.jpg"""
        server = ctx.message.server
        author = ctx.message.author

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
            message.author = discord.utils.get(ctx.message.server.members, id="425991701681930260")

            await self.bot.process_commands(message)
            await self.bot.say("You have successfully bought a custom background image for profile." )

            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 75000)
            logger.info("{}({}) bought background for profile(!buy 2).".format(author.name, author.id))

        else:
            await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="3")
    async def buy_3(self, ctx):

        server = ctx.message.server
        author = ctx.message.author

        await self.bot.say("Where would like the emoji to be in your name?\nReply with-\n**1** for Adding the emoji at start of your name. (Cost- 50000 credits)\n**2** for Adding the emoji at the end of your name. (Cost- 50000 credits)\n**3** for Adding emoji both at start and end of your name. (Cost- 80000 credits)")
        num = await self.bot.wait_for_message(author=author, timeout=120)
        reply = num.content
        if num is None:
            await self.bot.say("You took to long to answer. If you want to buy start over by typing {}buy 3".format(ctx.prefix))
        elif reply == "1":
            await self.bot.say("What would you like the emoji to be?")
            emo = await self.bot.wait_for_message(author=author, timeout=120)
            emoji = emo.content

            if emo is None:
                await self.bot.say(
                    "You took too long to reply. Cancelling the process. If you want to buy run {}buy 3 again.".format(
                        ctx.prefix))
            elif (emoji.startswith("<:") and emoji.endswith(">")) or (emoji.startswith("<a:") and emoji.endswith(">")):
                return await self.bot.say("Error, you can only use default emojis.")

            try:
                await self.bot.add_reaction(ctx.message, emoji)
            except (discord.errors.HTTPException, discord.errors.InvalidArgument):
                return await self.bot.say("Error, That's not an emoji I recognize.")

            if self.bank_check(author, 50000):
                ign = author.display_name
                if ign is None:
                    await self.bot.say("Error, Cannot add emoji.")
                else:
                    try:
                        newname = "{} {}".format(emoji, ign)
                        await self.bot.change_nickname(author, newname)
                    except discord.HTTPException:
                        await self.bot.say("I don’t have permission to change nick for this user.")
                    else:
                        await self.bot.say("Nickname changed to ** {} **\n".format(newname))
                        bank = self.bot.get_cog('Economy').bank
                        bank.withdraw_credits(author, 50000)
                        logger.info( "{}({}) bought emoji at name start(!buy 3 opt- 1).".format( author.name, author.id ) )
            else:
                await self.bot.say("You do not have enough credits to buy this item.")

        elif reply == "2":
            await self.bot.say("What would you like the emoji to be?")
            emo = await self.bot.wait_for_message(author=author, timeout=120)
            emoji = emo.content

            if emo is None:
                await self.bot.say(
                    "You took too long to reply. Cancelling the process. If you want to buy run {}buy 3 again.".format(
                        ctx.prefix))

            if (emoji.startswith("<:") and emoji.endswith(">")) or (emoji.startswith("<a:") and emoji.endswith(">")):
                return await self.bot.say("Error, you can only use default emojis.")

            try:
                await self.bot.add_reaction(ctx.message, emoji)
            except (discord.errors.HTTPException, discord.errors.InvalidArgument):
                return await self.bot.say("Error, That's not an emoji I recognize.")

            if self.bank_check(author, 50000):
                ign = author.display_name
                if ign is None:
                    await self.bot.say("Error, Cannot add emoji.")
                else:
                    try:
                        newname = "{} {}".format(ign, emoji)
                        await self.bot.change_nickname(author, newname)
                    except discord.HTTPException:
                        await self.bot.say("I don’t have permission to change nick for this user.")
                    else:
                        await self.bot.say("Nickname changed to ** {} **\n".format(newname))
                        bank = self.bot.get_cog('Economy').bank
                        bank.withdraw_credits(author, 50000)
                        logger.info( "{}({}) bought emoji at name end(!buy 3 opt- 2).".format( author.name, author.id ) )
            else:
                await self.bot.say("You do not have enough credits to buy this item.")

        elif reply == "3":
            await self.bot.say("What would you like the emoji to be?")
            emo = await self.bot.wait_for_message(author=author, timeout=120)
            emoji = emo.content

            if emo is None:
                await self.bot.say(
                    "You took too long to reply. Cancelling the process. If you want to buy run {}buy 3 again.".format(
                        ctx.prefix))

            if (emoji.startswith("<:") and emoji.endswith(">")) or (emoji.startswith("<a:") and emoji.endswith(">")):
                return await self.bot.say("Error, you can only use default emojis.")

            try:
                await self.bot.add_reaction(ctx.message, emoji)
            except (discord.errors.HTTPException, discord.errors.InvalidArgument):
                return await self.bot.say("Error, That's not an emoji I recognize.")

            if self.bank_check(author, 80000):
                ign = author.display_name
                if ign is None:
                    await self.bot.say("Error, Cannot add emoji.")
                else:
                    try:
                        newname = "{} {} {}".format(emoji, ign, emoji)
                        await self.bot.change_nickname(author, newname)
                    except discord.HTTPException:
                        await self.bot.say("I don’t have permission to change nick for this user.")
                    else:
                        await self.bot.say("Nickname changed to ** {} **\n".format(newname))
                        bank = self.bot.get_cog('Economy').bank
                        bank.withdraw_credits(author, 80000)
                        logger.info( "{}({}) bought emoji at both start and end of name(!buy 3 opt- 2.".format( author.name, author.id ) )
            else:
                await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="4")
    async def buy_4(self, ctx):

        server = ctx.message.server
        author = ctx.message.author

        if self.bank_check(author, 90000):
            await self.bot.say("What do you want the command to be?\n`{}command` Instead of command there will be you name.\nEnter your name or !command in which it will be triggered.\n(Note- It should be a part of your name in server.)".format(ctx.prefix))
            name = await self.bot.wait_for_message(author=author, timeout=60)
            currentname = author.display_name

            if name is None:
                await self.bot.say("You took too long to reply. Cancelling the process. If you want to buy run {}buy 4 again.".format(ctx.prefix))
            elif name.content.lower() in currentname.lower():
                com = name.content
                await self.bot.say("What do you want the bot to say when someone types !'urusername' or !'urcommand'?")
                msg = await self.bot.wait_for_message(author=author, timeout=120)
                if msg is None:
                    await self.bot.say("You took too long to reply. Cancelling the process. If you want to buy run {}buy 4 again.".format(ctx.prefix))
                else:
                    cont = msg.content
                    message = ctx.message
                    message.content = "{}customcom add {} {}".format(ctx.prefix, com, cont)
                    message.author = discord.utils.get(ctx.message.server.members, id="425991701681930260")

                    await self.bot.process_commands(message)

                    bank = self.bot.get_cog('Economy').bank
                    bank.withdraw_credits(author, 75000)
                    logger.info( "{}({}) bought custom command(!buy 4)".format( author.name, author.id ) )
            else:
                await self.bot.say("The name you entered is not a part of your username in the server. If you want something else conatact CRZA™ Modmail")
        else:
            await self.bot.say("You do not have enough credits to buy this item.")

    @buy.command(pass_context=True, name="5")
    async def buy_5(self, ctx):
        """ Buy Rare Role from the shop """
        server = ctx.message.server
        author = ctx.message.author

        rare = await self._is_rare(author)
        epic = await self._is_epic(author)
        legendary = await self._is_legendary(author)

        if rare or epic or legendary:
            return await self.bot.say("You are already Rare™.")

        if self.bank_check(author, 250000):
            bank = self.bot.get_cog('Economy').bank
            bank.withdraw_credits(author, 250000)
            await self._add_roles(author, ["Rare™"])
            await self.bot.say("Congratulations, you are now **Rare™**")
            logger.info("{}({}) bought Rare role(!buy 5).".format(author.name, author.id))
        else:
            await self.bot.say("You do not have enough credits to buy this role.")

    @buy.command(pass_context=True, name="6")
    async def buy_6(self, ctx):
        """ Buy Epic Role from the shop """
        server = ctx.message.server
        author = ctx.message.author

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
            logger.info("{}({}) bought Epic role(!buy 6).".format(author.name, author.id))
        else:
            await self.bot.say("You do not have enough credits to buy this role.")

    @buy.command(pass_context=True, name="7")
    async def buy_7(self, ctx):
        """ Buy Legendary Role from the shop """

        server = ctx.message.server
        author = ctx.message.author

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
            await self.bot.say("Congratulations, you are now **LeGeNDary™**")
            logger.info("{}({}) bought LeGeNDary role(!buy 7).".format(author.name, author.id))
        else:
            await self.bot.say("You do not have enough credits to buy this role.")

    @buy.command(pass_context=True, name="8")
    async def buy_8(self, ctx):

        server = ctx.message.server
        author = ctx.message.author

        if self.bank_check(author, 4000000):
            await self.bot.say("Please contact Crza™ Modmail to purchase it.")
        else:
            await self.bot.say("You do not have enough credits to buy Nitro.")

    @buy.command(pass_context=True, name="9")
    async def buy_9(self, ctx):

        server = ctx.message.server
        author = ctx.message.author
        reqchannel = discord.utils.get(server.channels, name="profilepic-request")

        if self.bank_check(author, 20000):
            await self.bot.say('**If You want to Buy a Avatar please head over to {} and see the pinned message.** Request there and say with your message I want to buy 9.** Thank You!**'.format(reqchannel .mention))
        else:
            await self.bot.say("You do not have enough credits to buy avatar.")


def setup(bot):
    global logger
    logger = logging.getLogger("red.shop")
    if logger.level == 0:
        # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='data/shop/shop.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(shop(bot))
