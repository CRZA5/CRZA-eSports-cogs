import discord
from discord.ext import commands
import os
from .utils.dataIO import dataIO, fileIO
from __main__ import send_cmd_help
import asyncio
import random
from random import choice as rand_choice
import string
import time
import brawlstats
from cogs.utils.chat_formatting import pagify
import re


creditIcon = "https://cdn.discordapp.com/attachments/637620236161646592/645638378963861506/PicsArt_11-17-02.18.34.png"
credits = "Bot by Mystic India"
BOTCOMMANDER_ROLES = ["Mod", "Recruitment Manager",
                      "President", "Vice President", "Hub Officer", "Admin"]

rules_text = """Take your roles from #react-role \n **Here are some Mystic India server rules.**\n
• No Hateful, obscene, offensive, racist, sexual or violent words allowed in chat or images.
• Respect others' opinions. If you disagree, please do so in a constructive manner.
• This is an English only server, please use any other languages in a private message.
• Do not spam, and avoid ever using @myclubname without permission from club managers or deputies.
• No advertisement of any kind, e.g. clubs, websites, discord invites.
• Use #bot-spam for bot features, e.g. !deck or !payday
• Obtaining credits or reputations using unethical ways like cheating or trading is strictly forbidden
• Respect and do not subvert moderators and managers.
• A good rule is to talk to people as if you were talking to them face to face.
• There are more rules that vary from club to club. Ask your club leader for the rules of your club.\n
**Club Transfer**\n
• If you are transferring from one Mystic India club to another, please contact your destination club's club leader first, 
and wait for the all clear from that club leader. We are all for members being wherever they want to be, but it helps us keep track of what is going on, and helps us make sure you get accepted.
• If you are leaving the club for another reason, please talk with your leader first when possible. As a club leader it helps to know if you're leaving for good, if you're leaving to do 2v2 with a few friends for a while, or if you're leaving for an eSport event.\n
**Violation of these roles will lead to punishment including temporary guest role reduced access, temporary kick from server, or permanent kick from server, depending on the severity and/or frequency of the offense**"""

commands_text = """Here are some of the Mystic India Bot commands, you can use them in the #bot-spam channel.\n
**!bs profile** - to view your brawl stars stats.
**!payday** - receive your 300 credits every 30 minutes.
**!heist** - Play a heist with a crew in #heist channel.
**!buy** - Take a look at what you can purchase with your credits.
**!balance** - To check your current bank balance.
**!profile** - view your server profile.
**!rep @user** - give reputation points to users.
**!remindme** - Use this command to make the bot remind you of something in the future.
**!trivia** - start a trivia of your choice. Bot will ask you questions, you will get points of answering them.
**!play** - Listen to songs, type with command with the song name inside a voice channel. (!skip, !pause, !resume, !playlist).
**!invite** - Get the invite link for the server to share with your friends.
**!report** - Report a user to the moderators for breaking the rules.\n
**You can type !help here to see the full commands list**"""

info_text = """You will find several channels on our Discord Server\n
**#global-chat**: to discuss about the game.
**profilepic-request**- You can buy or request a profile picture!
**#news**: important info and news about family.
**#react-role**: Easily get your notification and archetype roles.
**#giveaways**: Win Discord credits and game keys every day.
**#bots-spam**: Use bot commands, You can mute the channels you don't need in DISCORD settings.
**#heist**: Play Heist mini game with a crew and get lots of credits.
**#challenges**: Word and number challenge games with other members. Answer all the questions before any one else to win.
"""

credits_info = """WHAT ARE CREDITS? 
**Credits are a virtual currency in discord server, you earn credits by playing  playing mini games in discord. To use your credits, you can buy items from #shop

• Every 25 minutes, you can get free credits by typing !payday in #bot-spam  channel. Rare, Epic,  and Legendary gets More.!!
• You can also win credits by playing  and #race #challenges #heist .
• Last but not least, you can get easy credits by just chatting on discord. The more you chat, the more credits you accumulate.

You can type !shop here to look at different ways you can spend these credits. **
"""

coc_bs = """We Also Do ClashOfClans, and ClashRoyale Tourneys in our server! take your roles from #react-role
"""

social_info = """Stay Social! Come and follow us on these platforms to stay up to date on the latest news and announcements.

https://twitter.com/MysticIndia19
https://invite.gg/MysticIndia
https://discord.me/mysticindia

"""

guest_rules = """Take your roles from #react-role \n Welcome to the **Mystic India** Discord server. At first please take your roles from #react-role in server!  As a guest, you agree to the following rules:

• Respect others' opinions. If you disagree, please do so in a constructive manner.
• This is an English only server, please use any other languages in a private message.
• Do not spam, and avoid ever using @clubname without permission from club managers or deputies.
• No advertisement of any kind, e.g. clubs, websites, discord invites, etc.
• Use #bot-spam for bot features, e.g. !payday.
• Respect and do not subvert moderators or managers.
• A good rule is to talk to people as if you were talking to them face to face.

Failure to follow these rules will get you kicked from the server. Repeat offenders will be banned.

You can chat with family members and guests in `#global-chat`. For games, you can check out `#heist` and `#challenges`.

If you would like to invite your friends to join this server, you may use this Discord invite: <https://invite.gg/MysticIndia>

Thanks + enjoy!
"""

tags_path = "data/brawlstats/tags.json"
clubs_path = "data/club/clubs.json"


class clubs:
    """BS Club Family Management"""

    def __init__(self):
        self.clubs = dataIO.load_json(clubs_path)

    async def getClubs(self):
        """Return club array"""
        return self.clubs

    async def getClubData(self, clubkey, data):
        """Return club array"""
        return self.clubs[clubkey][data]

    async def getClubMemberData(self, clubkey, memberkey, data):
        """Return club member's dict"""
        return self.clubs[clubkey]['members'][memberkey][data]

    async def numClubs(self):
        """Return the number of clubs"""
        return len(self.clubs.keys())

    def keysClubs(self):
        """Get keys of all the clubs"""
        return self.clubs.keys()

    def keysClubMembers(self, clubkey):
        """Get keys of all the club members"""
        return self.clubs[clubkey]['members'].keys()

    async def namesClubs(self):
        """Get name of all the clubs"""
        return ", ".join(key for key in self.keysClubs())

    async def tagsClubs(self):
        """Get tags of all the clubs"""
        return [self.clubs[club]["tag"] for club in self.clubs]

    async def rolesClubs(self):
        """Get roles of all the clubs"""
        roles = ["Member"]
        for x in self.clubs:
            roles.append(self.clubs[x]['role'])
        return roles

    async def verifyMembership(self, clubtag):
        """Check if a club is part of the family"""
        for clubkey in self.keysClubs():
            if self.clubs[clubkey]['tag'] == clubtag:
                return True
        return False

    async def getClubKey(self, clubtag):
        """Get a club key from a club tag."""
        for clubkey in self.keysClubs():
            if self.clubs[clubkey]['tag'] == clubtag:
                return clubkey
        return None

    async def numWaiting(self, clubkey):
        """Get a club's wating list length from a club key."""
        return len(self.clubs[clubkey]['waiting'])

    async def addWaitingMember(self, clubkey, memberID):
        """Add a user to a club's waiting list"""
        if memberID not in self.clubs[clubkey]['waiting']:
            self.clubs[clubkey]['waiting'].append(memberID)
            dataIO.save_json(clubs_path, self.clubs)
            return True
        else:
            return False

    async def delWaitingMember(self, clubkey, memberID):
        """Remove a user to a club's waiting list"""
        if memberID in self.clubs[clubkey]['waiting']:
            self.clubs[clubkey]['waiting'].remove(memberID)
            dataIO.save_json(clubs_path, self.clubs)

            return True
        else:
            return False

    async def checkWaitingMember(self, clubkey, memberID):
        """check if a user is in a waiting list"""
        return memberID in self.clubs[clubkey]['waiting']

    async def getWaitingIndex(self, clubkey, memberID):
        """Get the waiting position from a club's waiting list"""
        return self.clubs[clubkey]['waiting'].index(memberID)

    async def delClub(self, clubkey):
        """delete a club from the family"""
        if self.clubs.pop(clubkey, None):
            dataIO.save_json(clubs_path, self.clubs)
            return True
        return False

    async def setPBTrophies(self, clubkey, trophies):
        """Set a club's PB Trohies"""
        self.clubs[clubkey]['personalbest'] = trophies
        dataIO.save_json(clubs_path, self.clubs)

    async def setBonus(self, clubkey, bonus):
        """Set a club's Bonus Statement"""
        self.clubs[clubkey]['bonustitle'] = bonus
        dataIO.save_json(clubs_path, self.clubs)

    async def setLogChannel(self, clubkey, channel):
        """Set a club's log channel"""
        self.clubs[clubkey]['log_channel'] = channel
        dataIO.save_json(clubs_path, self.clubs)

    async def addMember(self, clubkey, name, tag):
        """Add a member to the club"""
        self.clubs[clubkey]['members'][tag] = {}
        self.clubs[clubkey]['members'][tag]["tag"] = tag
        self.clubs[clubkey]['members'][tag]["name"] = name
        dataIO.save_json(clubs_path, self.clubs)

    async def delMember(self, clubkey, tag):
        """Remove a member to the club"""
        self.clubs[clubkey]['members'].pop(tag, None)
        dataIO.save_json(clubs_path, self.clubs)

    async def togglePrivate(self, clubkey):
        """oggle Private approval of new recruits"""
        self.clubs[clubkey]['approval'] = not self.clubs[clubkey]['approval']
        dataIO.save_json(clubs_path, self.clubs)

        return self.clubs[clubkey]['approval']


class club:
    """Brawl Stars Club Management Cog"""
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/club/settings.json')
        self.auth = self.bot.get_cog('BrawlStats').auth
        self.tags = self.bot.get_cog('BrawlStats').tags
        self.clubs = clubs()
        self.brawl = brawlstats.BrawlAPI(self.auth.getToken(), is_async=False)
        self.welcome = dataIO.load_json('data/club/welcome.json')
        self.bank = dataIO.load_json('data/economy/bank.json')
        self.seen = dataIO.load_json('data/seen/seen.json')

    async def updateSeen(self):
        self.seen = dataIO.load_json('data/seen/seen.json')

    def save_settings(self):
        """Saves the json"""
        dataIO.save_json('data/club/settings.json', self.settings)

    async def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

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

    async def _is_commander(self, member):
        server = member.server
        botcommander_roles = [discord.utils.get(server.roles, name=r) for r in BOTCOMMANDER_ROLES]
        botcommander_roles = set(botcommander_roles)
        author_roles = set(member.roles)
        if len(author_roles.intersection(botcommander_roles)):
            return True
        else:
            return False

    async def _is_member(self, member):
        server = member.server
        botcommander_roles = [discord.utils.get(server.roles, name=r) for r in ["Member",
                                                                                "Vice President",
                                                                                "Hub Officer",
                                                                                "Club Deputy",
                                                                                "Club Manager"]]
        botcommander_roles = set(botcommander_roles)
        author_roles = set(member.roles)
        if len(author_roles.intersection(botcommander_roles)):
            return True
        else:
            return False

    def emoji(self, name):
        """Emoji by name."""
        for emoji in self.bot.get_all_emojis():
            if emoji.name == name.replace(" ", "").replace("-", "").replace(".", ""):
                return '<:{}:{}>'.format(emoji.name, emoji.id)
        return ''

    def getLeagueEmoji(self, trophies):
        """Get clan war League Emoji"""
        mapLeagues = {
            "starLeague": [10000, 100000],
            "masterLeague": [8000, 9999],
            "crystalLeague": [6000, 7999],
            "diamondLeague": [4000, 5999],
            "goldLeague": [3000, 3999],
            "silverLeague": [2000, 2999],
            "bronzeLeague": [1000, 1999],
            "woodLeague": [0, 999]
        }
        for league in mapLeagues.keys():
            if mapLeagues[league][0] <= trophies <= mapLeagues[league][1]:
                return self.emoji(league)

    @commands.group(pass_context=True, no_pm=True, name="brawl")
    async def _brawl(self, ctx):
        """Legend BS cog's group command"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_brawl.command(pass_context=True)
    async def legend(self, ctx, member: discord.Member=None):
        """ Show BrawlStars India clubs, can also show clubs based on a member's trophies"""

        await self.bot.type()
        if member is None:
            trophies = 9999
            maxtrophies = 9999
        else:
            try:
                await self.bot.type()
                profiletag = await self.tags.getTag(member.id)
                profiledata = self.brawl.get_player(profiletag)
                trophies = profiledata.trophies
                maxtrophies = profiledata.highest_trophies

                if profiledata.club is None:
                    clubname = "*None*"
                else:
                    clubname = profiledata.club.name

                ign = await self.tags.formatName(profiledata.name)
            except brawlstats.RequestError as e:
                return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))
            except KeyError:
                return await self.bot.say("You must associate a tag with this member first using ``{}bsave #tag @member``".format(ctx.prefix))

        clubdata = []
        for clubkey in self.clubs.keysClubs():
            try:
                club = self.brawl.get_club(await self.clubs.getClubData(clubkey, 'tag'))
                clubdata.append(club)
            except brawlstats.RequestError as e:
                return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))

        clubdata = sorted(clubdata, key=lambda x: (x.required_trophies, x.trophies), reverse=True)

        embed = discord.Embed(color=0xFAA61A)
        if "url" in self.settings and "family" in self.settings:
            embed.set_author(name=self.settings['family'], url=self.settings['url'],
                             icon_url="https://cdn.discordapp.com/attachments/637620236161646592/645638378963861506/PicsArt_11-17-02.18.34.png")
        else:
            embed.set_author(name="Mystic India Clubs",
                             url="https://discord.me/bsindia",
                             icon_url="https://cdn.discordapp.com/attachments/637620236161646592/645638378963861506/PicsArt_11-17-02.18.34.png")

        embed.set_footer(text=credits, icon_url=creditIcon)

        foundClub = False
        totalMembers = 0
        totalWaiting = 0
        for club in clubdata:
            numWaiting = 0
            personalbest = 0
            bonustitle = None

            clubkey = await self.clubs.getClubKey(club.tag)
            numWaiting = await self.clubs.numWaiting(clubkey)
            personalbest = await self.clubs.getClubData(clubkey, 'personalbest')
            bonustitle = await self.clubs.getClubData(clubkey, 'bonustitle')
            emojiName = await self.clubs.getClubData(clubkey, 'emoji1')
            emoji = self.emoji(emojiName or "gameroom")
            totalWaiting += numWaiting

            if numWaiting > 0:
                title = "["+str(numWaiting)+" Waiting] "
            else:
                title = ""

            totalMembers += club.members_count
            if club.members_count < 100:
                showMembers = str(club.members_count) + "/100"
            else:
                showMembers = "**FULL**  "

            if str(club.status) != 'Invite Only':
                title += "["+str(club.status)+"] "

            title += club.name + " (#" + club.tag + ") "

            if personalbest > 0:
                title += "PB: "+str(personalbest)+"+  "

            if bonustitle is not None:
                title += bonustitle

            desc = ("{} {}  {} "
                    "{}+  {} {}".format(emoji,
                                        showMembers,
                                        self.getLeagueEmoji(int(club.required_trophies)),
                                        club.required_trophies,
                                        self.emoji("bstrophy"),
                                        club.trophies))

            if (member is None) or ((club.required_trophies <= trophies) and
                                    (club.members_count != 100) and
                                    (club.status != 'Closed')):
                foundClub = True
                embed.add_field(name=title, value=desc, inline=False)

        if not foundClub:
            embed.add_field(name="uh oh!",
                            value="There are no clubs available for you at the moment, "
                            "please type !legend to see all clubs.",
                            inline=False)

        embed.description = ("Our Family is made up of {} "
                             "clubs with a total of {} "
                             "members. We have {} spots left "
                             "and {} members in waiting lists.".format(await self.clubs.numClubs(),
                                                                       totalMembers,
                                                                       (await self.clubs.numClubs()*100)-totalMembers,
                                                                       totalWaiting))
        await self.bot.say(embed=embed)

        if member is not None:
            await self.bot.say(("Hello **{}**, above are all the clubs "
                                "you are allowed to join, based on your statistics. "
                                "Which club would you like to join? \n\n"
                                "**Name:** {} (#{})\n**Trophies:** {}/{}\n"
                                "**Club:** {}\n\n"
                                ":warning: **YOU WILL BE REJECTED "
                                "IF YOU JOIN ANY CLUB WITHOUT "
                                "APPROVAL**".format(ign,
                                                    ign,
                                                    profiletag,
                                                    trophies,
                                                    maxtrophies,
                                                    clubname)))

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def approve(self, ctx, member: discord.Member, clubkey):
        """Send instructions to people joining a club"""
        server = ctx.message.server

        clubkey = clubkey.lower()

        try:
            club_tag = await self.clubs.getClubData(clubkey, 'tag')
            club_name = await self.clubs.getClubData(clubkey, 'name')
            club_role = await self.clubs.getClubData(clubkey, 'role')
            club_pb = await self.clubs.getClubData(clubkey, 'personalbest')
            club_approval = await self.clubs.getClubData(clubkey, 'approval')
        except KeyError:
            return await self.bot.say("Please use a valid clubname: {}".format(await self.clubs.namesClubs()))

        leftClub = False
        try:
            await self.bot.type()
            profiletag = await self.tags.getTag(member.id)
            profiledata = self.brawl.get_player(profiletag)
            clubdata = self.brawl.get_club(club_tag)

            ign = await self.tags.formatName(profiledata.name)
            if profiledata.club is None:
                leftClub = True
                clubtag = ""
            else:
                clubtag = profiledata.club.tag
        except brawlstats.RequestError as e:
            return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))
        except KeyError:
            return await self.bot.say("You must associate a tag with this member first using ``{}bsave #tag @member``".format(ctx.prefix))

        membership = not await self.clubs.verifyMembership(clubtag)

        if membership:

            trophies = profiledata.trophies
            maxtrophies = profiledata.highest_trophies

            if (clubdata.get("members") == 100):
                return await self.bot.say("Approval failed, the club is Full.")

            if ((trophies < clubdata.required_trophies) or (maxtrophies < club_pb)):
                return await self.bot.say("Approval failed, you don't meet the trophy requirements.")

            if (clubdata.type == "Closed"):
                return await self.bot.say("Approval failed, the club is currently Closed.")

            if club_approval:
                if club_role not in [y.name for y in ctx.message.author.roles]:
                    return await self.bot.say("Approval failed, only {} staff can approve new recruits for this club.".format(club_name))

            if await self.clubs.numWaiting(clubkey) > 0:
                if await self.clubs.checkWaitingMember(clubkey, member.id):
                    canWait = (100 - clubdata.get("members")) - 1

                    if await self.clubs.getWaitingIndex(clubkey, member.id) > canWait:
                        return await self.bot.say("Approval failed, you are not first in queue for the waiting list on this server.")

                    await self.clubs.delWaitingMember(clubkey, member.id)

                    role = discord.utils.get(server.roles, name="Waiting")
                    try:
                        await self.bot.remove_roles(member, role)
                    except discord.Forbidden:
                        raise
                    except discord.HTTPException:
                        raise
                else:
                    return await self.bot.say("Approval failed, there is a waiting queue for this club. Please first join the waiting list.")

            if not leftClub:
                warning = ("\n\n:warning: **YOU WILL BE REJECTED "
                           "IF YOU JOIN ANY CLUB WITHOUT "
                           "APPROVAL**")
                await self.bot.say(("{} Please leave your current club now. "
                                    "Your recruit code will arrive in 3 minutes.{}".format(member.mention, warning)))
                await asyncio.sleep(180)

            try:
                recruitCode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

                await self.bot.send_message(member, "Congratulations, You have been approved to join **" + club_name +
                                                    " (#" + club_tag + ")**.\n\n\n" +
                                                    "Your **RECRUIT CODE** is: ``" + recruitCode + "`` \n" +
                                                    "Send this code in the join request message.\n\n" +
                                                    # "Click this link to join the club: https://legendclubs.com/clubInfo/" +
                                                    # club_tag + "\n\n" +
                                                    "That's it! Now wait for your club leadership to accept you. " +
                                                    "It usually takes a few minutes to get accepted, but it may take up to a few hours. \n\n" +
                                                    "**IMPORTANT**: Once your club leadership has accepted your request, " +
                                                    "let a staff member in discord know that you have been accepted. " +
                                                    "They will then unlock all the member channels for you.")
                await self.bot.say(member.mention + " has been approved for **" + club_name + "**. Please check your DM for instructions on how to join.")

                try:
                    newname = ign + " (Approved)"
                    await self.bot.change_nickname(member, newname)
                except discord.HTTPException:
                    await self.bot.say("I don’t have permission to change nick for this user.")

                roleName = discord.utils.get(server.roles, name=club_role)

                embed = discord.Embed(color=0x0080ff)
                embed.set_author(name="New Recruit", icon_url="https://cdn.discordapp.com/attachments/637620236161646592/645638378963861506/PicsArt_11-17-02.18.34.png")
                embed.add_field(name="Name", value=ign, inline=True)
                embed.add_field(name="Recruit Code", value=recruitCode, inline=True)
                embed.add_field(name="Club", value=club_name, inline=True)
                embed.set_footer(text=credits, icon_url=creditIcon)

                await self.bot.send_message(discord.Object(id='613064679538950144'), content=roleName.mention, embed=embed)
            except discord.errors.Forbidden:
                await self.bot.say("Approval failed, {} please fix your privacy settings, we are unable to send you Direct Messages.".format(member.mention))
        else:
            await self.bot.say("Approval failed, You are already a part of a club in the family.")

    @_brawl.command(pass_context=True, no_pm=True)
    async def newmember(self, ctx, member: discord.Member):
        """Setup nickname, roles and invite links for a new member"""

        server = ctx.message.server
        author = ctx.message.author

        isMember = await self._is_member(member)
        if isMember:
            return await self.bot.say("Error, " + member.mention + " is not a new member.")

        try:
            await self.bot.type()
            profiletag = await self.tags.getTag(member.id)
            profiledata = self.brawl.get_player(profiletag)
            if profiledata.club is None:
                clubtag = ""
                clubname = ""
            else:
                clubtag = profiledata.club.tag
                clubname = profiledata.club.name

            ign = await self.tags.formatName(profiledata.name)
        except brawlstats.RequestError as e:
            return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))
        except KeyError:
            return await self.bot.say("You must associate a tag with this member first using ``{}bs save #tag @member``".format(ctx.prefix))

        allowed = False
        if member is None:
            allowed = True
        elif member.id == author.id:
            allowed = True
        else:
            allowed = await self._is_commander(author)

        if not allowed:
            return await self.bot.say("You dont have enough permissions to use this command on others.")

        membership = await self.clubs.verifyMembership(clubtag)

        if membership:

            try:
                savekey = await self.clubs.getClubKey(clubtag)
                invite = await self.clubs.getClubData(savekey, 'discord')
                if invite is not None:
                    joinLink = "https://discord.gg/" + str(invite)
                    await self.bot.send_message(member, "Hi There! Congratulations on getting accepted into our family. " +
                                                        "We have unlocked all the member channels for you in Legend Brawl Stars Discord Server. " +
                                                        "Now you have to carefuly read this message and follow the steps mentioned below: \n\n" +
                                                        "Please click on the link below to join your club Discord server. \n\n" +
                                                        clubname + ": " + joinLink + "\n\n" +
                                                        "Please do not leave our main or club servers while you are in the club. Thank you.")
                else:

                    await self.bot.send_message(member, "Hi There! Congratulations on getting accepted into our family. "
                                                        "We have unlocked all the member channels for you in Legend Brawl Stars Discord Server. \n\n" +
                                                        "Please do not leave our Discord server while you are in the club. Thank you.")
            except discord.errors.Forbidden:
                return await self.bot.say(("Membership failed, {} please fix your privacy settings, "
                                           "we are unable to send you Direct Messages.".format(member.mention)))

            await self.clubs.delWaitingMember(savekey, member.id)

            mymessage = ""
            if ign is None:
                await self.bot.say("Cannot find IGN.")
            else:
                try:
                    newclubname = await self.clubs.getClubData(savekey, 'nickname')
                    newname = ign + " | " + newclubname
                    await self.bot.change_nickname(member, newname)
                except discord.HTTPException:
                    await self.bot.say("I don’t have permission to change nick for this user.")
                else:
                    mymessage += "Nickname changed to **{}**\n".format(newname)

            role_names = [await self.clubs.getClubData(savekey, 'role'), 'Member']
            try:
                await self._add_roles(member, role_names)
                mymessage += "**" + await self.clubs.getClubData(savekey, 'role') + "** and **Member** roles added."
            except discord.Forbidden:
                await self.bot.say(
                    "{} does not have permission to edit {}’s roles.".format(
                        author.display_name, member.display_name))
            except discord.HTTPException:
                await self.bot.say("failed to add {}.".format(', '.join(role_names)))

            await self.bot.say(mymessage)

            welcomeMsg = rand_choice(self.welcome["GREETING"])
            await self.bot.send_message(discord.Object(id='599816861789716522'), welcomeMsg.format(member, server))

            await self._remove_roles(member, ['Guest'])

            await self.bot.send_message(discord.Object(id='613064679538950144'),
                                        "**{}** recruited **{} (#{})** to {}".format(ctx.message.author.display_name,
                                                                                     ign,
                                                                                     profiletag,
                                                                                     role_names[0]))
            await asyncio.sleep(300)
            await self.bot.send_message(member, rules_text)

            await asyncio.sleep(300)
            await self.bot.send_message(member, commands_text)

            await asyncio.sleep(300)
            await self.bot.send_message(member, info_text)

            await asyncio.sleep(300)
            await self.bot.send_message(member, credits_info)

            await asyncio.sleep(300)
            await self.bot.send_message(member, coc_bs)

            await asyncio.sleep(300)
            await self.bot.send_message(member, social_info)
        else:
            await self.bot.say("You must be accepted into a club before I can give you club roles. "
                               "Would you like me to check again in 2 minutes? (Yes/No)")

            answer = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)

            if answer is None:
                return
            elif "yes" not in answer.content.lower():
                return

            await self.bot.say("Okay, I will retry this command in 2 minutes.")
            await asyncio.sleep(120)
            message = ctx.message
            message.content = ctx.prefix + "brawl newmember {}".format(member.mention)
            await self.bot.process_commands(message)

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def waiting(self, ctx, member: discord.Member, clubkey):
        """Add people to the waiting list for a club"""
        server = ctx.message.server

        clubkey = clubkey.lower()

        try:
            club_tag = await self.clubs.getClubData(clubkey, 'tag')
            club_name = await self.clubs.getClubData(clubkey, 'name')
            club_pb = await self.clubs.getClubData(clubkey, 'personalbest')
        except KeyError:
            return await self.bot.say("Please use a valid clubname: {}".format(await self.clubs.namesClubs()))

        try:
            await self.bot.type()
            profiletag = await self.tags.getTag(member.id)
            profiledata = self.brawl.get_player(profiletag)
            clubdata = self.brawl.get_club(club_tag)

            ign = await self.tags.formatName(profiledata.name)
            trophies = profiledata.trophies
            maxtrophies = profiledata.highest_trophies

        except brawlstats.RequestError as e:
            return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))
        except KeyError:
            return await self.bot.say("You must associate a tag with this member first using ``{}bsave #tag @member``".format(ctx.prefix))

        if ((trophies < clubdata.required_trophies) and (maxtrophies < club_pb)):
            return await self.bot.say("Cannot add you to the waiting list, you don't meet the trophy requirements.")

        if not await self.clubs.addWaitingMember(clubkey, member.id):
            return await self.bot.say("You are already in a waiting list for this club.")

        role = discord.utils.get(server.roles, name="Waiting")
        try:
            await self.bot.add_roles(member, role)
        except discord.Forbidden:
            raise
        except discord.HTTPException:
            raise
        await self.bot.say(member.mention + " You have been added to the waiting list for **" +
                           club_name +
                           "**. We will mention you when a spot is available.")

        roleName = discord.utils.get(server.roles, name=await self.clubs.getClubData(clubkey, 'role'))
        await self.bot.send_message(discord.Object(id='599824035391602688'), "**{} (#{})** added to the waiting list for {}".format(ign, profiletag, roleName.mention))

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def remove(self, ctx, member: discord.Member, clubkey):
        """Delete people from the waiting list for a club"""
        server = ctx.message.server


        clubkey = clubkey.lower()

        try:
            club_name = await self.clubs.getClubData(clubkey, 'name')
        except KeyError:
            return await self.bot.say("Please use a valid clubname: {}".format(await self.clubs.namesClubs()))

        try:
            await self.clubs.delWaitingMember(clubkey, member.id)

            role = discord.utils.get(server.roles, name="Waiting")
            try:
                await self.bot.remove_roles(member, role)
            except discord.Forbidden:
                raise
            except discord.HTTPException:
                raise
            await self.bot.say(member.mention + " has been removed from the waiting list for **" + club_name + "**.")
        except ValueError:
            await self.bot.say("Recruit not found in the waiting list.")

    @_brawl.command(pass_context=True, no_pm=True, aliases=["waitlist", "wait"])
    async def waitinglist(self, ctx):
        """Show status of the waiting list."""

        message = ""
        counterClubs = 0
        counterPlayers = 0


        await self.bot.type()

        embed = discord.Embed(color=0xFAA61A)

        for club in self.clubs.keysClubs():
            if await self.clubs.numWaiting(club) > 0:
                counterClubs += 1
                message = ""
                for index, userID in enumerate(await self.clubs.getClubData(club, 'waiting')):
                    user = discord.utils.get(ctx.message.server.members, id=userID)
                    try:
                        message += str(index+1) + ". " + user.display_name + "\n"
                        counterPlayers += 1
                    except AttributeError:
                        await self.clubs.delWaitingMember(club, userID)
                        message += str(index+1) + ". " + "*user not found*" + "\n"
                embed.add_field(name=await self.clubs.getClubData(club, 'name'), value=message, inline=False)

        if not message:
            await self.bot.say("The waiting list is empty")
        else:
            embed.description = "We have " + str(counterPlayers) + " people waiting for " + str(counterClubs) + " clubs."
            embed.set_author(name="Blazing Family Waiting List", icon_url="https://i.imgur.com/5GfHj5o.png")
            embed.set_footer(text=credits, icon_url=creditIcon)
            await self.bot.say(embed=embed)

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def changenick(self, ctx, member: discord.Member=None):
        """ Change nickname of a user of their IGN + Club"""

        member = member or ctx.message.author

        try:
            await self.bot.type()
            profiletag = await self.tags.getTag(member.id)
            profiledata = self.brawl.get_player(profiletag)
            if profiledata.club is None:
                clubtag = "none"
            else:
                clubtag = profiledata.club.tag
            ign = await self.tags.formatName(profiledata.name)
        except brawlstats.RequestError as e:
            return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))
        except KeyError:
            return await self.bot.say("You must associate a tag with this member first using ``{}bsave #tag @member``".format(ctx.prefix))

        membership = await self.clubs.verifyMembership(clubtag)

        if membership:
            if ign is None:
                await self.bot.say("Cannot find IGN.")
            else:
                try:
                    savekey = await self.clubs.getClubKey(clubtag)
                    newclubname = await self.clubs.getClubData(savekey, 'nickname')
                    newname = ign + " | " + newclubname
                    await self.bot.change_nickname(member, newname)
                except discord.HTTPException:
                    await self.bot.say("I don’t have permission to change nick for this user.")
                else:
                    await self.bot.say("Nickname changed to ** {} **\n".format(newname))
        else:
            await self.bot.say("This command is only available for family members.")

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def changeclub(self, ctx, member: discord.Member=None):
        """ Change club of a user of their IGN + Club"""

        member = member or ctx.message.author

        try:
            await self.bot.type()
            profiletag = await self.tags.getTag(member.id)
            profiledata = self.brawl.get_player(profiletag)
            if profiledata.club is None:
                clubtag = "none"
            else:
                clubtag = profiledata.club.tag
            ign = await self.tags.formatName(profiledata.name)
        except brawlstats.RequestError as e:
            return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))
        except KeyError:
            return await self.bot.say("You must associate a tag with this member first using ``{}bsave #tag @member``".format(ctx.prefix))

        membership = await self.clubs.verifyMembership(clubtag)

        if membership:
            mymessage = ""
            savekey = await self.clubs.getClubKey(clubtag)

            rolesToRemove = await self.clubs.rolesClubs()
            await self._remove_roles(member, rolesToRemove)

            if ign is None:
                await self.bot.say("Cannot find IGN.")
            else:
                try:
                    newclubname = await self.clubs.getClubData(savekey, 'nickname')
                    newname = ign + " | " + newclubname
                    await self.bot.change_nickname(member, newname)
                except discord.HTTPException:
                    await self.bot.say("I don’t have permission to change nick for this user.")
                else:
                    mymessage += "Nickname changed to **{}**\n".format(newname)

            role_names = [await self.clubs.getClubData(savekey, 'role'), 'Member']
            try:
                await self._add_roles(member, role_names)
                mymessage += "**" + await self.clubs.getClubData(savekey, 'role') + "** and **Member** roles added."
            except discord.Forbidden:
                await self.bot.say(
                    "{} does not have permission to edit {}’s roles.".format(
                        member.display_name, member.display_name))
            except discord.HTTPException:
                await self.bot.say("failed to add {}.".format(', '.join(role_names)))

            await self.bot.say(mymessage)
        else:
            await self.bot.say("This command is only available for family members.")

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def audit(self, ctx, clubkey):
        """ Check to see if your club members are setup properly in discord."""
        server = ctx.message.server

        clubkey = clubkey.lower()

        try:
            club_tag = await self.clubs.getClubData(clubkey, 'tag')
            club_role = await self.clubs.getClubData(clubkey, 'role')
            club_name = await self.clubs.getClubData(clubkey, 'name')
            club_nickname = await self.clubs.getClubData(clubkey, 'nickname')
        except KeyError:
            return await self.bot.say("Please use a valid clubname: {}".format(await self.clubs.namesClubs()))

        await self.bot.type()

        try:
            clubdata = self.brawl.get_club(club_tag)
        except brawlstats.RequestError as e:
            return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))

        await self.updateSeen()

        bs_members_name = []
        bs_members_tag = []
        bs_members_trophy = []
        for member in clubdata.members:
            bs_members_name.append(await self.tags.formatName(member.name))
            bs_members_tag.append(member.tag)
            bs_members_trophy.append(member.trophies)

        role = discord.utils.get(server.roles, name=club_role)
        d_members = [m for m in server.members if role in m.roles]
        d_members = sorted(d_members, key=lambda x: x.display_name.lower())

        bs_members_with_no_player_tag = []
        bs_members_with_less_trophies = []
        d_members_with_no_player_tag = []
        d_members_not_in_club = []
        d_members_without_role = []
        d_members_without_name = []
        d_members_inactive = []
        bs_clubSettings = []

        for d_member in d_members:
            try:
                player_tag = await self.tags.getTag(d_member.id)

                if player_tag not in bs_members_tag:
                    d_members_not_in_club.append(d_member.display_name)

                try:
                    if self.seen[server][d_member.id]['TIMESTAMP'] < time.time() - 691200:
                        d_members_inactive.append(d_member.display_name)
                except:
                    pass
            except KeyError:
                d_members_with_no_player_tag.append(d_member.display_name)
                continue

        for index, player_tag in enumerate(bs_members_tag):
            try:
                dc_member = await self.tags.getUser(server.members, player_tag)

                if role not in dc_member.roles:
                    d_members_without_role.append(dc_member.display_name)

                if (bs_members_name[index] not in dc_member.display_name) or (club_nickname not in dc_member.display_name):
                    d_members_without_name.append(dc_member.display_name)
            except AttributeError:
                bs_members_with_no_player_tag.append(bs_members_name[index])
                continue

        clubReq = clubdata.required_trophies
        for index, player_trophy in enumerate(bs_members_trophy):
            if player_trophy < clubReq:
                bs_members_with_less_trophies.append(bs_members_name[index])

        bs_clubSettings.append(clubdata.badge_id == 4)
        bs_clubSettings.append("<c7>Legend Family</c> :fire: <c5>discord.gg/5ww5D3q</c> :fire: <c3>2 Clubs</c> :fire: <c8>Discord is mandatory</c> :fire:" in clubdata.description)
        bs_clubSettings.append(clubdata.type != "Closed")

        message = ""

        if False in bs_clubSettings:
            message += "\n\n:warning: Problems in club settings for **" + club_name + "**:```"

            if not bs_clubSettings[0]: message += "\n• Club Badge is incorrect."
            if not bs_clubSettings[1]: message += "\n• Club description is incorrect."
            if not bs_clubSettings[2]: message += "\n• Club is Closed."

            message += "```\n\n"

        if bs_members_with_no_player_tag:
            message += ":warning: **({})** Players in **{}**, but have **NOT** joined discord: ```• ".format(len(bs_members_with_no_player_tag), club_name)
            message += "\n• ".join(bs_members_with_no_player_tag)
            message += "```\n\n"

        if d_members_with_no_player_tag:
            message += ":warning: **({})** Players with **{}** role, but have **NO** tags saved: ```• ".format(len(d_members_with_no_player_tag), club_name)
            message += "\n• ".join(d_members_with_no_player_tag)
            message += "```\n\n"

        if d_members_not_in_club:
            message += ":warning: **({})** Players with **{}** role, but have **NOT** joined the club: ```• ".format(len(d_members_not_in_club), club_name)
            message += "\n• ".join(d_members_not_in_club)
            message += "```\n\n"

        if d_members_without_role:
            message += ":warning: **({})** Players in **{}**, but **DO NOT** have the club role: ```• ".format(len(d_members_without_role), club_name)
            message += "\n• ".join(d_members_without_role)
            message += "```\n\n"

        if d_members_without_name:
            message += ":warning: **({})** Players in **{}**, but have an **INCORRECT** nickname: ```• ".format(len(d_members_without_name), club_name)
            message += "\n• ".join(d_members_without_name)
            message += "```\n\n"

        if bs_members_with_less_trophies:
            message += ":warning: **({})** Players in **{}**, but **DO NOT** meet the trophy requirements: ```• ".format(len(bs_members_with_less_trophies), club_name)
            message += "\n• ".join(bs_members_with_less_trophies)
            message += "```\n\n"

        if d_members_inactive:
            message += ":warning: **({})** Players in **{}**, but **NOT** active on Discord: ```• ".format(len(d_members_inactive), club_name)
            message += "\n• ".join(d_members_inactive)
            message += "```"

        if message == "":
            message += "Congratulations, your club has no problems found so far. Kudos!"

        for page in pagify(message):
            await self.bot.say(page)

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def guest(self, ctx, member: discord.Member):
        """Add guest role and change nickname to CR"""
        server = ctx.message.server

        try:
            await self.bot.type()
            profiletag = await self.tags.getTag(member.id)
            profiledata = self.brawl.get_player(profiletag)
            ign = await self.tags.formatName(profiledata.name)
        except brawlstats.RequestError as e:
            return await self.bot.say('```\n{}: {}\n```'.format(e.code, e.error))
        except KeyError:
            return await self.bot.say("You must associate a tag with this member first using ``{}bsave #tag @member``".format(ctx.prefix))

        try:
            newname = ign + " | Guest"
            await self.bot.change_nickname(member, newname)
        except discord.HTTPException:
            return await self.bot.say("I don’t have permission to change nick for this user.")

        role = discord.utils.get(server.roles, name="Guest")
        channel = await self.bot.start_private_message(member)
        try:
            message = guest_rules + "\n" + credits_info
            await self.bot.send_message(channel, message)
            await self.bot.send_message(channel, commands_text)
            await self.bot.say("{} Role Added to {}".format(role.name, member.display_name))
        except discord.errors.Forbidden:
            return await self.bot.say("Command failed, {} please fix your privacy settings, we are unable to send you Guest Rules.".format(member.mention))
        try:
            await self.bot.add_roles(member, role)
        except discord.Forbidden:
            raise
        except discord.HTTPException:
            raise

    @_brawl.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLES)
    async def inactive(self, ctx, member: discord.Member):
        """Use this command after kicking people from club"""

        rolesToRemove = await self.clubs.rolesClubs()

        await self._remove_roles(member, rolesToRemove)
        await self.bot.change_nickname(member, None)

        await self.bot.say("Member and club roles removed.\nNickname has been reset.")


def check_folders():
    if not os.path.exists("data/club"):
        print("Creating data/club folder...")
        os.makedirs("data/club")

    if not os.path.exists("data/seen"):
        print("Creating data/seen folder...")
        os.makedirs("data/seen")


def check_files():
    f = "data/club/clubs.json"
    if not fileIO(f, "check"):
        print("Creating empty clubs.json...")
        fileIO(f, "save", {})

    f = "data/club/welcome.json"
    if not fileIO(f, "check"):
        print("Creating empty welcome.json...")
        fileIO(f, "save", {})

    f = "data/club/settings.json"
    if not fileIO(f, "check"):
        print("Creating empty settings.json...")
        fileIO(f, "save", {})

    f = "data/seen/seen.json"
    if not fileIO(f, "check"):
        print("Creating empty seen.json...")
        fileIO(f, "save", {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(club(bot))
