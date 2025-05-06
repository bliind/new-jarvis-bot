import discord
from discord import app_commands
from discord.ext import commands
import AutoMod

class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ###
    ### Events
    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        # get all configs to do with new messages
        configs = self.bot.config[event.guild.id]

        # create a white list from all scheduled events
        events = await event.guild.fetch_scheduled_events()
        white_list = [f'*event={e.url.split("/")[-1]}' for e in events]
        event_string = f'*event={event.url.split("/")[-1]}'
        if event_string not in white_list:
            white_list.append(event_string)

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
