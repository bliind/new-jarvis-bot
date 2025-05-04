import re
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB as config

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_caps_percent(self, message: discord.Message):
        configs = await config.get_configs([
            'caps_prot_immune_channels',
            'caps_prot_immune_roles',
            'moderator_roles',
            'caps_prot_percent',
            'caps_prot_message'
        ])

        if message.channel.id in configs['caps_prot_immune_channels']:
            return

        immune_roles = configs['caps_prot_immune_roles'] + configs['moderator_roles']
        for role in message.author.roles:
            if role.id in immune_roles:
                return

        # remove emotes
        content = re.sub(r':[\w\d]+:', '', message.content)

        max_percent = configs['caps_prot_percent'][0]
        alph = list(filter(str.isalpha, content))
        if len(alph) >= 5:
            percent = (sum(map(str.isupper, alph)) / len(alph) * 100)
            if percent >= max_percent:
                msg_content = configs['caps_prot_message'][0]
                try: sent = await message.reply(msg_content)
                except Exception as e:
                    print(e, message)

                await message.delete()
                await asyncio.sleep(5)
                try: await sent.delete()
                except: pass

    async def cheeky_me_check(self, message: discord.Message):
        if self.bot.user.mentioned_in(message):
            if message.author.id == 145971157902950401:
                await message.reply('At your service, sir.')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return

        # check if it's me pinging the bot
        try: await self.cheeky_me_check(message)
        except Exception as e:
            print('Failed cheeky me check?')
            print(e, message)

        # check for all caps / mostly caps message
        try: await self.check_caps_percent(message)
        except Exception as e:
            print('Error checking caps percent:')
            print(e, message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.id == self.bot.user.id:
            return

        # check for all caps / mostly caps message
        try: await self.check_caps_percent(after)
        except Exception as e:
            print('Error checking caps percent:')
            print(e, after)
