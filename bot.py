import os
import discord
from discord import app_commands
from discord.ext import commands

from Cogs.SampleCog import SampleCog
from Cogs.WikiCog import WikiCog
from Cogs.MiscCog import MiscCog

# extend bot class
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='¤', intents=intents)
        self.synced = False

    async def setup_hook(self):
        await self.add_cog(SampleCog(self))
        await self.add_cog(WikiCog(self))
        await self.add_cog(MiscCog(self))

    async def on_ready(self):
        if self.synced:
            return

        await self.tree.sync()
        self.synced = True

        print('Bot ready to go!')

bot = MyBot()
bot.run(os.getenv('BOT_TOKEN'))

