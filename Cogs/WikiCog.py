import os
import re
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
                try:
                    print(old_thread)
                except Exception as e:
                    pass

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

    @app_commands.command(name='scrape_article', description='Save article to .md file')
    async def scape_article_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.channel, discord.Thread):
            embed = discord.Embed(
                color=discord.Color.red(),
                title='Error',
                description='Can only be used inside forum posts'
            )
            await interaction.followup.send(content='', embed=embed)
            return

        # scrape content
        try:
            file_output = ''
            attachments = []
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                file_output += message.content + '\n'
                for attachment in message.attachments:
                    file_output += f'![ ]({attachment.filename})\n'
                    attachments.append(await attachment.to_file())

        except Exception as e:
            print(f'Error scraping article, {e}')
            embed = discord.Embed(
                color=discord.Color.red(),
                title='Error',
                description='Oops, something went scraping the article.'
            )
            await interaction.followup.send(content='', embed=embed)
            return
        # set filename
        try:
            thread_name = interaction.channel.name
            filename = thread_name.replace(' ', '_')
            filename = re.sub(r'[\W_]+', '', filename) + '.md'
        except Exception:
            filename = 'scraped_article.md'

        # save file
        try:
            with open(filename, 'w') as output_file:
                output_file.write(file_output)
        except Exception as e:
            print(f'Error saving article file, {e}')
            embed = discord.Embed(
                color=discord.Color.red(),
                title='Error',
                description='Oops, something went wrong saving the file.'
            )
            await interaction.followup.send(content='', embed=embed)
            return

        # send file
        attachments.append(discord.File(filename))
        embed = discord.Embed(
            color=discord.Color.green(),
            title='Article Saved',
            description=f'You can download the attached file{"s" if len(attachments) > 1 else ""}.'
        )
        await interaction.followup.send(content='', embed=embed, files=attachments)

        try:
            os.remove(filename)
        except Exception as e:
            print(f'Failed to remove output file, {e}')
