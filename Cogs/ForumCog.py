import re
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from Modals.ConfigParagraphModal import ConfigParagraphModal
import ConfigDB

class ForumCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def alliance_post_checker(self, thread: discord.Thread, retries=0):
        configs = self.bot.config[thread.guild.id]

        if thread.parent.id not in configs.alliance_channels:
            return

        try:
            thread_open = [m async for m in thread.history(limit=1, oldest_first=True)][0]
        except Exception as e:
            if retries < 3:
                await asyncio.sleep(1)
                await self.alliance_post_checker(thread, retries=retries+1)
            else:
                print('Failed trying to check alliance post:')
                print(e, thread)
                return

        matches = [re.search(r, thread_open.content, re.MULTILINE | re.IGNORECASE) for r in configs.alliance_post_regexes]
        # if any patterns fail, send message
        if None in matches:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=configs.alliance_post_message
            )
            await thread.send(content=thread.owner.mention, embed=embed)
            await thread.edit(archived=True, locked=True)

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

        try: await self.alliance_post_checker(thread)
        except Exception as e:
            print('Failed trying to check alliance post:')
            print(e, thread, sep='\n')

    ###
    ### Slash commands
    @app_commands.command(name='update_alliance_message', description='Update the Alliance post message')
    async def update_alliancemsg_command(self, interaction: discord.Interaction):
        configs = self.bot.config[interaction.guild.id]

        modal = ConfigParagraphModal(configs.alliance_post_message)
        await interaction.response.send_modal(modal)
        await modal.wait()
        if await ConfigDB.update_config(interaction.guild.id, 'alliance_post_message', modal.new_message.value):
            # update live config
            self.bot.config[interaction.guild.id]['alliance_post_message'] = modal.new_message.value
            await interaction.followup.send('Alliance post message updated', ephemeral=True)
