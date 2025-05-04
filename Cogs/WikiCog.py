import discord
from discord import app_commands
from discord.ext import commands, tasks

class WikiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        pass
        # self.loop_func.start()

    @tasks.loop(seconds=30)
    async def loop_func(self):
        print('Looping')

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        pass
