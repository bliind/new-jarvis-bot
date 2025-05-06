import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB

class ConfigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def refresh_config(self, guild = None):
        all_configs = await ConfigDB.get_all_configs(guild)

        if guild:
            self.bot.config[guild] = all_configs[guild]
        else:
            self.bot.config = all_configs

    @app_commands.command(name='refresh_config', description='Reload the bot configs')
    async def refresh_config_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            await self.refresh_config(guild=interaction.guild_id)
            await interaction.edit_original_response(content='Config updated')
        except Exception as e:
            await interaction.edit_original_response(content='Something went wrong, sorry!')
            print(f'Failed to manually refresh config for {interaction.guild_id}:')
            print(e)

    @app_commands.command(name='show_config_keys', description='Shows config keys')
    async def show_keys_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        keys = await ConfigDB.get_distinct_keys(interaction.guild_id)

        message = '- ' + '\n- '.join([f'`{k}`' for k in keys])
        embed = discord.Embed(
            color=discord.Color.greyple(),
            title='Config Items',
            description=message
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='list_config', description='Lists existing config item')
    async def list_config_command(self, interaction: discord.Interaction, key: str):
        await interaction.response.defer(ephemeral=True)
        configs = await ConfigDB.get_config(interaction.guild_id, key)

        message = ''
        for value in configs:
            message += f'`{key}` = `{value}`\n'

        embed = discord.Embed(
            color=discord.Color.greyple(),
            title='Config Items',
            description=message
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='add_config', description='Add a new config')
    async def add_config_command(self, interaction: discord.Interaction, key: str, value: str):
        await interaction.response.defer(ephemeral=True)

        if key.endswith('s'):
            success = await ConfigDB.add_config(interaction.guild_id, key, value)

            if success:
                # add to live config
                try: self.bot.config[interaction.guild_id][key].append(int(value))
                except: self.bot.config[interaction.guild_id][key].append(value)

                color = discord.Color.brand_green()
                description = f'Added `{key}` with value of `{value}`'
            else:
                color = discord.Color.red()
                description = 'Something went wrong'
        else:
            color = discord.Color.yellow()
            description = 'This is a single entry config, use /update_config'

        embed = discord.Embed(
            color=color,
            title='Add Config',
            description=description
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='update_config', description='Update an existing config')
    async def update_config_command(self, interaction: discord.Interaction, key: str, value: str):
        await interaction.response.defer(ephemeral=True)

        if not key.endswith('s'):
            success = await ConfigDB.update_config(interaction.guild_id, key, value)

            if success:
                # update live config
                try: self.bot.config[interaction.guild_id][key] = int(value)
                except: self.bot.config[interaction.guild_id][key] = value

                color = discord.Color.brand_green()
                description = f'Updated `{key}` with new value of `{value}`'
            else:
                color = discord.Color.red()
                description = 'Something went wrong'
        else:
            color = discord.Color.yellow()
            description = 'This is a multiple entry config, use /add_config and/or /delete_config'

        embed = discord.Embed(
            color=color,
            title='Add Config',
            description=description
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='delete_config', description='Delete an existing config')
    async def delete_config_command(self, interaction: discord.Interaction, key: str, value: str):
        await interaction.response.defer(ephemeral=True)
        if key.endswith('s'):
            success = await ConfigDB.delete_config(interaction.guild_id, key, value)

            if success:
                # update live config
                self.bot.config[interaction.guild_id][key].remove(value)

                color = discord.Color.brand_green()
                description = f'Deleted `{key}` with value of `{value}`'
            else:
                color = discord.Color.red()
                description = 'Something went wrong'
        else:
            color = discord.Color.yellow()
            description = 'This is a single entry config, cannot delete.'

        embed = discord.Embed(
            color=color,
            title='Delete Config',
            description=description
        )

        await interaction.followup.send(embed=embed)
