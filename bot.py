import os
import discord
from discord import app_commands
from discord.ext import commands

from Cogs.MiscCog import MiscCog
from Cogs.WikiCog import WikiCog
from Cogs.EventCog import EventCog
from Cogs.ForumCog import ForumCog
from Cogs.ConfigCog import ConfigCog
from Cogs.MemberCog import MemberCog
from Cogs.ReactionsCog import ReactionsCog
from Cogs.TeamAnswersCog import TeamAnswersCog

import ConfigDB

# extend bot class
class MyBot(commands.Bot):
    def __init__(self, use_cogs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='¤', intents=intents)
        self.synced = False
        self.use_cogs = use_cogs
        self.config = {}

    async def setup_hook(self):
        self.config = await ConfigDB.get_all_configs()
        for use_cog in self.use_cogs:
            await self.add_cog(use_cog(self))

    async def on_ready(self):
        if self.synced:
            return

        await self.tree.sync()
        self.synced = True

        print('Bot ready to go!')

use_cogs = [
    MiscCog,
    WikiCog,
    EventCog,
    ForumCog,
    ConfigCog,
    MemberCog,
    ReactionsCog,
    TeamAnswersCog,
]
bot = MyBot(use_cogs)
bot.run(os.getenv('BOT_TOKEN'))

