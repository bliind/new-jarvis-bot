import discord
from discord import app_commands
from discord.ext import commands, tasks

class WikiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bump_archived_wiki_posts.start()

    @tasks.loop(seconds=3600)
    async def bump_archived_wiki_posts(self):
        for server in self.bot.guilds:
            configs = self.bot.config[server.id]

            try:
                forum = self.bot.get_channel(configs.wiki_channel)
                async for old_thread in forum.archived_threads(limit=None):
                    await old_thread.edit(archived=False)
            except Exception as e:
                print('Error bumping archived wiki posts:')
                print(e, server)
                try: print(old_thread)
                except: pass

    @app_commands.command(name='wiki', description='Links to common wiki pages')
    async def wiki_command(self, interaction: discord.Interaction, page: str, ping: discord.User = None):
        await interaction.response.defer(ephemeral=False)
        configs = self.bot.config[interaction.guild.id]

        wiki_links = {}
        for link in configs.wiki_links:
            title, url = link.split('|')
            wiki_links[title] = url
        message = f'{ping.mention if ping else ""} {wiki_links[page]}'
        await interaction.followup.send(message)

    @wiki_command.autocomplete('page')
    async def auto_complete_wiki_page(self, interaction: discord.Interaction, current: str):
        configs = self.bot.config[interaction.guild.id]

        out = []
        for link in configs.wiki_links:
            title, _ = link.split('|')
            if current.lower() in title.lower():
                out.append(app_commands.Choice(name=title, value=title))
        return out
