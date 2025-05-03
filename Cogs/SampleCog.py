import discord
from discord import app_commands
from discord.ext import commands

class SampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.user.mention in message.content:
            await message.reply('no ping')

    @app_commands.command(name='slash_command', description='A Slash Command')
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def slash_command(self, interaction: discord.Interaction):
        await interaction.response.send_message('Boom')
