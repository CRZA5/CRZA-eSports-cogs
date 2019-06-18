import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from datetime import datetime
from copy import deepcopy
from .utils import checks
from collections import namedtuple, defaultdict, deque
from __main__ import send_cmd_help
import logging
import os
import time
import asyncio

icon = "https://cdn3.iconfinder.com/data/icons/avatars-15/64/_Ninja-2-512.png"
credit = "Cog by Weirdo914"


class WalletError(Exception):
    pass


class AccountAlreadyExists(WalletError):
    pass


class NoAccount(WalletError):
    pass


class InsufficientBalance(WalletError):
    pass


class NegativeValue(WalletError):
    pass


class Money:

    def __init__(self, bot, file_path):
        self.accounts = dataIO.load_json(file_path)
        self.bot = bot

    def account_exists(self, user):
        try:
            self._get_account(user)
        except NoAccount:
            return False
        return True

    def deposit_credits(self, user, amount):
        server = user.server
        if amount < 0:
            raise NegativeValue()
        account = self._get_account(user)
        account["balance"] += amount
        self.accounts[server.id][user.id] = account
        self._save_bank()

    def withdraw_credits(self, user, amount):
        server = user.server

        if amount < 0:
            raise NegativeValue()

        account = self._get_account(user)
        if account["balance"] >= amount:
            account["balance"] -= amount
            account["withdrawn"] += amount
            self.accounts[server.id][user.id] = account
            self._save_bank()
        else:
            raise InsufficientBalance()

    def _get_account(self, user):
        server = user.server
        try:
            return deepcopy(self.accounts[server.id][user.id])
        except KeyError:
            raise NoAccount()

    def _save_bank(self):
        dataIO.save_json("data/wallet/wallet.json", self.accounts)

    def get_balance(self, user):
        account = self._get_account(user)
        return account["balance"]


class Wallet:
    """Economy

    Get rich and have fun with imaginary currency!"""

    def __init__(self, bot):
        self.bot = bot
        self.money = Money(bot, "data/wallet/wallet.json")

    @commands.group(name="wallet", pass_context=True)
    async def wallet(self, ctx):
        """Bank operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @wallet.command(pass_context=True, no_pm=True)
    async def register(self, ctx):
        """Register for a wallet"""
        user = ctx.message.author
        server = user.server
        channel = await self.bot.start_private_message(user)
        reg_msg = "**Hello! I will ask you few questions, let's move to DM!**"
        reg_stop = "OK, cancelling Wallet creation. If you still want to create wallet type `!register` in <#569026201419644929>"
        reg_timeout = "You took too long to respond. Cancelling Wallet creation. If you still want to create wallet type `!register` in <#569026201419644929>"
        reg_start = "**Lets start! You can stop anytime by typing \"stop\". Keep in Mind answer the questions properly, do not make funs. or Ban!** "

        if not self.money.account_exists(user):
            if server.id not in self.money.accounts:
                self.money.accounts[server.id] = {}
            if user.id in self.money.accounts:  # Legacy account
                balance = self.money.accounts[user.id]["balance"]
            else:
                balance = 0
            await self.bot.send_message(channel, reg_start)
            await self.bot.send_message(ctx.message.channel, reg_msg)
            await asyncio.sleep(3)
            await self.bot.send_message(channel, "What is your Brawl Stars in-game name?(Reply within 2 minutes)")
            reply = (await self.bot.wait_for_message(channel=channel, author=user, timeout=120))
            if reply is None:
                return await self.bot.send_message(channel, reg_timeout)
            elif reply.content.lower() == "stop":
                return await self.bot.send_message(channel, reg_stop)
            else:
                ingame_name = reply.content

            await self.bot.send_message(channel, "What is your Brawl Stars in-game tag?(Reply within 2 minutes)")
            reply = (await self.bot.wait_for_message(channel=channel, author=user, timeout=120))
            if reply is None:
                return await self.bot.send_message(channel, reg_timeout)
            elif not reply.content.startswith("#")":
                return await self.bot.send_message(channel, "Please enter your Tag starting with #. Run the command again to register for wallet")
            else:
                ingame_tag = reply.content
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            account = {"name": user.display_name,
                       "balance": balance,
                       "created_at": timestamp,
                       "game_name": ingame_name,
                       "game_tag": ingame_tag,
                       "dis_name_tag": str(user),
                       "dis_id": user.id,
                       "withdrawn": 0
                       }
            self.money.accounts[server.id][user.id] = account
            self.money._save_bank()
            await self.bot.send_message(channel, "Created a wallet for you in CRZA eSports.")
            return
        else:
            return await self.bot.send_message(ctx.message.channel, "You already have a wallet in CRZA eSports.")

    @wallet.command(pass_context=True, no_pm=True)
    async def claim(self, ctx):
        """Register for a wallet"""
        user = ctx.message.author
        settings = self.check_server_settings(ctx.message.server)
        channel = self.bot.get_channel("590563426753839109")
        server_req = self.bot.get_server("581666499907813425")
        manage_role = discord.utils.get(server_req.roles, name="Wallet Claim Manager")
        req = 30
        if self.money.account_exists(user):
            bal = settings[user.id]["balance"]
            if bal >= req:
                await self.bot.send_message(ctx.message.channel, "How much money do you wish to claim/withdraw from your wallet?(Reply within 1 minute)")
                reply = (await self.bot.wait_for_message(channel=ctx.message.channel, author=user, timeout=60))
                value = reply.content
                if reply is None:
                    return await self.bot.send_message(ctx.message.channel, "You took too long to answer. Cancelling claiming process.")
                elif not value.isdigit():
                    return await self.bot.send_message(ctx.message.channel, "You need to enter a number.")
                else:
                    rs = int(value)
                    if rs < req:
                        return await self.bot.send_message(ctx.message.channel, "You need to enter a number greater or equal to {}.".format(req))
                    else:
                        await self.bot.send_message(ctx.message.channel, "Your claim request has been sent to our team. We will get back to you as soon as possible.\nLook out for messages by <@574970208481968168>")
                        return await self.bot.send_message(channel, "{}\n{}({}) has requested to claim Rs {} from wallet.".format(manage_role.mention, user, user.id, value))
            else:
                return await self.bot.send_message(ctx.message.channel, "You need at least Rs {} to claim money from wallet.".format(req))
        else:
            return await self.bot.send_message(ctx.message.channel, "You need to make a wallet before claiming money")

    @wallet.command(pass_context=True)
    async def balance(self, ctx, user: discord.Member=None):
        """Shows balance of user.

        Defaults to yours."""
        settings = self.check_server_settings(ctx.message.server)
        if not user:
            user = ctx.message.author
            bal = settings[user.id]["balance"]
            try:
                await self.bot.say("{} Your wallet balance is: Rs {}".format(user.mention, bal))
            except NoAccount:
                await self.bot.say("{} You don't have a wallet in"
                                   " CRZA eSports. Type `{}wallet register`"
                                   " to create one.".format(user.mention, ctx.prefix))
        else:
            if self.money.account_exists(user):
                bal = settings[user.id]["balance"]
                await self.bot.say("{}'s wallet's balance is Rs {}".format(user.display_name, bal))
            else:
                await self.bot.say("That user has no wallet.")

    @wallet.command(pass_context=True)
    async def info(self, ctx, user: discord.Member=None):
        """Shows info of wallet of user.

        Defaults to yours."""
        settings = self.check_server_settings(ctx.message.server)
        if not user:
            user = ctx.message.author
            withdraw = settings[user.id]["withdrawn"]
            gamename = settings[user.id]["game_name"]
            gametag = settings[user.id]["game_tag"]
            bal = settings[user.id]["balance"]
            wltime = settings[user.id]["created_at"]
            embed = discord.Embed(colour=0xff0000)
            embed.add_field(name="**Name:**", value=user.display_name)
            embed.add_field(name="**Money in Wallet:**", value="Rs " + str(bal))
            embed.add_field(name="**Withdrawn Money:**", value="Rs " + str(withdraw))
            embed.add_field(name="**Discord Username & Tag:**", value=user)
            embed.add_field(name="**Brawl Stars in-game name:**", value=gamename)
            embed.add_field(name="**Brawl Stars Tag:**", value=gametag)
            embed.add_field(name="**Wallet created at:**", value=wltime)
            embed.title = "**CRZA eSports Wallet**"
            embed.set_footer(text=credit, icon_url=icon)
            try:
                await self.bot.say(embed=embed)
            except NoAccount:
                await self.bot.say("{} You don't have a wallet in"
                                   " CRZA eSports. Type `{}wallet register`"
                                   " to create one.".format(user.mention, ctx.prefix))
        else:
            if self.money.account_exists(user):
                withdraw = settings[user.id]["withdrawn"]
                gamename = settings[user.id]["game_name"]
                gametag = settings[user.id]["game_tag"]
                bal = settings[user.id]["balance"]
                wltime = settings[user.id]["created_at"]
                embed = discord.Embed( colour=0xff0000 )
                embed.add_field(name="**Name:**", value=user.display_name)
                embed.add_field(name="**Money in Wallet:**", value="Rs " + str(bal))
                embed.add_field(name="**Withdrawn Money:**", value="Rs " + str(withdraw))
                embed.add_field(name="**Discord Username & Tag:**", value=user)
                embed.add_field(name="**Brawl Stars in-game name:**", value=gamename)
                embed.add_field(name="**Brawl Stars Tag:**", value=gametag)
                embed.add_field(name="**Wallet created at:**", value=wltime)
                embed.title = "**CRZA eSports Wallet**"
                embed.set_footer(text=credit, icon_url=icon)
                await self.bot.say(embed=embed)
            else:
                await self.bot.say("That user has no wallet.")

    @wallet.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def addmoney(self, ctx, user: discord.Member, sum: int):
        author = ctx.message.author
        try:
            self.money.deposit_credits(user, sum)
            logger.info("{}({}) added {} rupees to {}({})'s wallet.".format(author.name, author.id, sum, user.name, user.id))
            await self.bot.say("Rs {} have been added to {}'s account.".format(sum, user.name))
        except NegativeValue:
            await self.bot.say("You cannot transfer Rs 0 of if you want to remove money from someone's wallet, Use {}wallet withdraw.".format(ctx.prefix))
        except NoAccount:
            await self.bot.say("That user has no wallet. First ask him to register using {}wallet register.".format(ctx.prefix))

    @wallet.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def withdraw(self, ctx, user: discord.Member, sum: int):
        author = ctx.message.author
        try:
            self.money.withdraw_credits(user, sum)
            logger.info("{}({}) withdrew {} rupees from {}({})'s wallet.".format(author.name, author.id, sum, user.name, user.id))
            await self.bot.say("Rs {} have been withdrawn from {}'s account.".format(sum, user.name))

        except NegativeValue:
            await self.bot.say("You cannot transfer Rs 0 of if you want to add money from someone's wallet, Use {}wallet addmoney.".format(ctx.prefix))
        except NoAccount:
            await self.bot.say("That user has no wallet. First ask him to register using {}wallet register.".format(ctx.prefix))
        except InsufficientBalance:
            await self.bot.say("User doesn't have enough money in wallet.")

    def check_server_settings(self, server):
        if server.id not in self.money.accounts:
            default = {}
            self.money.accounts[server.id] = default
            self.money._save_bank()
            path = self.money.accounts[server.id]
            return path
        else:
            path = self.money.accounts[server.id]
            return path



def check_folders():
    if not os.path.exists("data/wallet"):
        print("Creating data/wallet folder...")
        os.makedirs("data/wallet")


def check_files():

    f = "data/wallet/wallet.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty wallet.json...")
        dataIO.save_json(f, {})


def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("red.wallet")
    if logger.level == 0:
        # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='data/wallet/wallet.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(Wallet(bot))
