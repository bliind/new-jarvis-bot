import discord
from discord import app_commands
from discord.ext import commands
import ConfigDB as config

class TeamAnswersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.configs = {}

    def make_embed(self, title, description, color='blue'):
        try: dcolor = getattr(discord.Color, color)
        except: dcolor = discord.Color.blue()

        return discord.Embed(
            color=dcolor(),
            title=title,
            description=description
        )

    def check_member_role(self, member: discord.Member, roles: list):
        for role in member.roles:
            if role.id in roles:
                return True
        return False

    def create_devreply_embed(self, message: discord.Message, thread_open: str, configs: config.dotdict):
        # set up the embed message
        description = f'{thread_open}\n\n'
        description += '------\n\n'
        description += f'***Replied to by {message.author.mention}:***\n'
        description += f'{message.content}\n\n'
        description += f'[See reply here]({message.jump_url})'

        # create the embed
        embed = self.make_embed(message.channel.name, description)
        embed.set_thumbnail(url=message.author.display_avatar.url)

        return embed

    async def send_devreply_embed(self, message: discord.Message, thread_open: str, configs: config.dotdict):
        # get the output channel
        output_channel = await self.bot.fetch_channel(configs.team_answer_channel)

        # create and send the embed
        embed = self.create_devreply_embed(message, thread_open, configs)
        sent = await output_channel.send(embed=embed)
        await sent.publish()

    async def check_devreply(self, message: discord.Message, configs: config.dotdict):
        # make sure is our forum and developer is replying
        if message.channel.type != discord.ChannelType.public_thread: return
        if message.channel.parent.type != discord.ChannelType.forum: return
        if message.channel.parent.id not in configs.team_question_channels: return
        if not self.check_member_role(message.author, configs.developer_roles): return

        # get the original message in the thread the dev is posting on
        forum = self.bot.get_channel(message.channel.parent.id)
        thread = forum.get_thread(message.channel.id)
        async for m in thread.history(limit=1, oldest_first=True):
            thread_open = m.content

        # send dev reply post
        await self.send_devreply_embed(message, thread_open, configs)

        # add tag to post
        await thread.add_tags(discord.Object(id=configs.team_response_tag))

    async def check_modreply(self, message: discord.Message, configs: config.dotdict):
        if message.channel.type != discord.ChannelType.public_thread: return
        if message.channel.parent.type != discord.ChannelType.forum: return
        if message.channel.parent.id not in configs.team_question_channels: return
        if not self.check_member_role(message.author, configs.moderator_roles): return

        # get the thread and add the tag
        forum = self.bot.get_channel(message.channel.parent.id)
        thread = forum.get_thread(message.channel.id)
        await thread.add_tags(discord.Object(id=configs.moderator_response_tag))

    ###
    ### Events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return

        # get all configs to do with new messages
        configs = await config.get_configs(message.guild.id, [
            'developer_roles',
            'moderator_roles',
            'team_response_tag',
            'moderator_response_tag',
            'team_answer_channel',
            'team_question_channels',
        ])

        actions = [
            'check_devreply',
            'check_modreply',
        ]

        for action in actions:
            method = getattr(self, action)
            try: await method(message, configs)
            except Exception as e:
                print(f'Failed during {action}:')
                print(e, message, sep='\n')

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.bot: return

        # get all configs to do with edited messages
        configs = await config.get_configs(after.guild.id, [
            'moderator_roles',
            'team_answer_channel',
            'team_question_channels',
        ])

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot: return

        configs = await self.load_configs(message.guild.id)
