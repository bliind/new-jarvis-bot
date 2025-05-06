import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class ForumCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def alliance_post_checker(self, thread: discord.Thread):
        configs = self.bot.config[thread.guild.id]

    async def auto_pin(self, thread: discord.Thread, retries=0):
        configs = self.bot.config[thread.guild.id]
        if thread.parent_id in configs.auto_pin_channels:
            try:
                async for message in thread.history(limit=1, oldest_first=True):
                    await message.pin()
            except Exception as e:
                if retries < 3:
                    await asyncio.sleep(1)
                    await self.auto_pin(thread, retries=retries+1)
                else:
                    print('Failed to auto-pin OP:')
                    print(e, thread, sep='\n')

    ###
    ### Events
    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        if thread.owner_id == self.bot.user.id:
            return

        try: await self.auto_pin(thread)
        except Exception as e:
            print('Failed trying to auto-pin:')
            print(e, thread, sep='\n')

        try: await self.auto_pin(thread)
        except Exception as e:
            print('Failed trying to check alliance post:')
            print(e, thread, sep='\n')
