import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB as config
import AutoMod

class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ###
    ### Events
    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        # get all configs to do with new messages
        configs = await config.get_configs(event.guild.id, [
            'automod_links_name',
        ])

        # create a white list from all scheduled events
        events = await event.guild.fetch_scheduled_events()
        white_list = [f'*event={e.url.split("/")[-1]}' for e in events]

        # find the automod rule that blocks links
        rules = AutoMod.get_automod_rules(event.guild.id)
        for rule in rules:
            if rule['name'] == configs.automod_links_name:
                the_rule = rule
                break

        try:
            the_rule['trigger_metadata']['allow_list'] = white_list
            AutoMod.update_automod_rule(event.guild.id, the_rule['id'], the_rule)
        except Exception as e:
            print('Failed to update event whitelist:')
            print(e, event, sep='\n')
