import re
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB as config



class ReactionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def remove_emotes(self, payload):
        # handle removing certain emotes
        configs = await config.get_configs([
            'country_flag',
            'no_flag_channel',
            'banned_emote',
        ])

        if (payload.channel_id in configs['no_flag_channel'] \
        and payload.emoji.name in configs['country_flag']) \
        or payload.emoji.name in configs['banned_emote']:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.clear_reaction(payload.emoji.name)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.member.id == self.bot.user.id:
            return

        await self.remove_emotes(payload)
