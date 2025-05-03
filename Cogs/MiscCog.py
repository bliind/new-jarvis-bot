import re
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB as config

async def check_caps_percent(message: discord.Message):
    immune_channels = await config.get_config('caps_prot_immune_channels', make_int=True)
    if message.channel.id in immune_channels:
        return

    immune_roles = await config.get_config('caps_prot_immune_roles', make_int=True)
    immune_roles += await config.get_config('moderator_roles', make_int=True)
    for role in message.author.roles:
        if role.id in immune_roles:
            return

    # remove emotes
    content = re.sub(r':[\w\d]+:', '', message.content)

    max_percent = await config.get_config('caps_prot_percent', make_int=True, single=True)
    alph = list(filter(str.isalpha, content))
    if len(alph) >= 5:
        percent = (sum(map(str.isupper, alph)) / len(alph) * 100)
        if percent >= max_percent:
            msg_content = await config.get_config('caps_prot_message', single=True)
            try: sent = await message.reply(msg_content)
            except Exception as e:
                print(e, message)

            await message.delete()
            await asyncio.sleep(5)
            try: await sent.delete()
            except: pass

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await check_caps_percent(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await check_caps_percent(after)
