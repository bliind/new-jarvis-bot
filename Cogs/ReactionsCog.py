import re
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB as config

class ReactionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def remove_emotes(self, payload: discord.RawReactionActionEvent):
        # handles removing certain emotes
        configs = await config.get_configs(payload.guild_id, [
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

    async def add_emotes(self, thread: discord.Thread):
        # handle adding certain emotes to new threads
        configs = await config.get_configs(thread.guild.id, [
            'full_react_channel',
            'half_react_channel',
            'full_react_emote',
            'half_react_emote'
        ])

        if thread.parent.id in configs['full_react_channel']:
            async for message in thread.history(limit=1, oldest_first=True):
                for emote in configs['full_react_emote']:
                    await message.add_reaction(emote)
                    await asyncio.sleep(0.5)

        if thread.parent.id in configs['half_react_channel']:
            async for message in thread.history(limit=1, oldest_first=True):
                for emote in configs['half_react_emote']:
                    await message.add_reaction(emote)
                    await asyncio.sleep(0.5)

    async def reaction_role(self, payload: discord.RawReactionActionEvent):
        # handles adding roles with reactions
        configs = await config.get_configs(payload.guild_id, [
            'reaction_role_users',
            'reaction_role_reaction',
            'reaction_role_role'
        ])

        if payload.member.id in configs['reaction_role_users'] \
        and payload.emoji.name == configs['reaction_role_reaction']:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await self.bot.fetch_user(payload.user_id)
            # remove the reaction role reaction
            await message.remove_reaction(payload.emoji, user)
            # give the author of the message the role
            await message.author.add_roles(discord.Object(id=configs['reaction_role_role']))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.member.id == self.bot.user.id:
            return

        # handle removing certain emotes
        try: await self.remove_emotes(payload)
        except Exception as e:
            print('Error while removing emotes:')
            print(e, payload)

        # check for ReactionRole
        try: await self.reaction_role(payload)
        except Exception as e:
            print('Error while checking reaction role:')
            print(e, payload)

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        if thread.owner_id == self.bot.user.id:
            return

        # handle adding certain emotes to certain threads
        try: await self.add_emotes(thread)
        except Exception as e:
            print('Error while adding emotes:')
            print(e, thread)
