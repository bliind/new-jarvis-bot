import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB as config

class ConfigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='show_config_keys', description='Shows config keys')
    async def show_keys_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        keys = await config.get_distinct_keys(interaction.guild_id)

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
        configs = await config.get_config(interaction.guild_id, key)

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
            success = await config.add_config(interaction.guild_id, key, value)

            if success:
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
            success = await config.update_config(interaction.guild_id, key, value)

            if success:
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
            success = await config.delete_config(interaction.guild_id, key, value)

            if success:
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
