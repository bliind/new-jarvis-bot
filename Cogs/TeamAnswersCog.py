import discord
from discord import app_commands
from discord.ext import commands

from Views.ConfirmView import ConfirmView
from Modals.AskDevsModal import AskDevsModal
import ConfigDB

class TeamAnswersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # silly way to do context menus if you ask me but hey
        devreply_contextmenu = app_commands.ContextMenu(
            name='Post Dev Reply',
            callback=self.post_devreply_contextmenu
        )
        self.bot.tree.add_command(devreply_contextmenu)

    def is_message_devreply(self, message: discord.Message):
        configs = self.bot.config[message.guild.id]

        # make sure is our forum and developer is replying
        if message.channel.type != discord.ChannelType.public_thread:
            return False
        if message.channel.parent.type != discord.ChannelType.forum:
            return False
        if message.channel.parent.id not in configs.team_question_channels:
            return False

        return self.check_member_role(message.author, configs.developer_roles)

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

    def create_devreply_embed(self, message: discord.Message, thread_open: str):
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

    async def send_devreply_embed(self, message: discord.Message, thread_open: str):
        configs = self.bot.config[message.guild.id]

        # get the output channel
        output_channel = await self.bot.fetch_channel(configs.team_answer_channel)

        # create and send the embed
        embed = self.create_devreply_embed(message, thread_open)
        sent = await output_channel.send(embed=embed)
        await sent.publish()

        return sent

    async def get_thread_open(self, message):
        # get the original message in the thread the dev is posting on
        forum = self.bot.get_channel(message.channel.parent.id)
        thread = forum.get_thread(message.channel.id)
        async for message in thread.history(limit=1, oldest_first=True):
            return (thread, message.content)

    async def find_posted_reply(self, message: discord.Message, thread_open: str):
        configs = self.bot.config[message.guild.id]

        # loop through reply channel to find the answer post
        team_answer_channel = self.bot.get_channel(configs.team_answer_channel)
        async for posted in team_answer_channel.history(limit=50):
            try:
                # create an embed from the message and ensure we find the same Q/A
                embed = self.create_devreply_embed(message, thread_open)
                if embed.title == posted.embeds[0].title \
                and embed.description == posted.embeds[0].description:
                    return posted
            except: pass

    ###
    ### The actual actions

    async def post_new_devreply(self, message: discord.Message):
        configs = self.bot.config[message.guild.id]

        # ensure is dev replying
        if not self.is_message_devreply(message):
            return

        # get thread and opening message
        thread, thread_open = await self.get_thread_open(message)

        # send dev reply post
        await self.send_devreply_embed(message, thread_open)

        # add tag to post
        await thread.add_tags(discord.Object(id=configs.team_response_tag))

    async def check_modreply(self, message: discord.Message):
        configs = self.bot.config[message.guild.id]

        if message.channel.type != discord.ChannelType.public_thread: return
        if message.channel.parent.type != discord.ChannelType.forum: return
        if message.channel.parent.id not in configs.team_question_channels: return
        if not self.check_member_role(message.author, configs.moderator_roles): return

        # get the thread and add the tag
        forum = self.bot.get_channel(message.channel.parent.id)
        thread = forum.get_thread(message.channel.id)
        await thread.add_tags(discord.Object(id=configs.moderator_response_tag))

    async def delete_devreply(self, message: discord.Message):
        if not self.is_message_devreply(message):
            return

        _, thread_open = await self.get_thread_open(message)
        posted = await self.find_posted_reply(message, thread_open)
        if posted:
            await posted.delete()

    async def edit_devreply(self, before: discord.Message, after: discord.Message):
        if not self.is_message_devreply(after):
            return

        _, thread_open = await self.get_thread_open(after)
        posted = await self.find_posted_reply(before, thread_open)
        if posted:
            new_embed = self.create_devreply_embed(after, thread_open)
            await posted.edit(embed=new_embed)

    ###
    ### Events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return

        # check for dev replies to watched forums
        try: await self.post_new_devreply(message)
        except Exception as e:
            print('Failed during post_new_devreply:')
            print(e, message, sep='\n')

        # check for mod replies to watched forums
        try: await self.check_modreply(message)
        except Exception as e:
            print('Failed during check_modreply:')
            print(e, message, sep='\n')

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.bot: return

        # check for dev reply edit
        try: await self.edit_devreply(before, after)
        except Exception as e:
            print(f'Failed during edit_devreply:')
            print(e, before, after, sep='\n')

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot: return

        # check for dev reply deletion
        try: await self.delete_devreply(message)
        except Exception as e:
            print(f'Failed during delete_devreply:')
            print(e, message, sep='\n')

    ###
    ### Slash Command
    @app_commands.command(name='askdevs', description='Post the ask-the-team guidelines')
    async def askdevs_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        configs = self.bot.config[interaction.guild.id]
        embed = discord.Embed(
            colour=discord.Color.yellow(),
            description=configs.askdevs_message
        )
        await interaction.channel.send(embed=embed)
        await interaction.delete_original_response()

    @app_commands.command(name='update_askdevs', description='Update the ask-the-team guidelines')
    async def update_askdevs_command(self, interaction: discord.Interaction):
        configs = self.bot.config[interaction.guild.id]

        modal = AskDevsModal(configs.askdevs_message)
        await interaction.response.send_modal(modal)
        await modal.wait()
        if await ConfigDB.update_config(interaction.guild.id, 'askdevs_message', modal.new_message.value):
            await interaction.followup.send('ask-the-team Guidelines Updated', ephemeral=True)

    ###
    ### Context Menu
    async def post_devreply_contextmenu(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)
        # ensure message is in a forum
        if not (message.channel.type == discord.ChannelType.public_thread and \
                message.channel.parent.type == discord.ChannelType.forum):
            await interaction.edit_original_response(content='Message is not in a forum thread')
            return

        try:
            if not self.is_message_devreply(message):
                await interaction.edit_original_response(content='Message is not from a dev')
                return

            _, thread_open = await self.get_thread_open(message)
            # post confirm message then do the thing
            confirm_view = ConfirmView(timeout=10)
            confirm_embed = discord.Embed(title='Post Reply?', description=message.content)
            await interaction.edit_original_response(embed=confirm_embed, view=confirm_view)
            await confirm_view.wait()
            if confirm_view.value:
                # yes was picked
                sent = await self.send_devreply_embed(message, thread_open)
                await interaction.edit_original_response(content=f'## Posted: {sent.jump_url}', view=None)
            elif confirm_view.value == None:
                # timeout
                await interaction.edit_original_response(content='## Timed out.', view=None)
            else:
                # no chosen
                await interaction.edit_original_response(content='## Cancelled!', view=None)
        except Exception as e:
            print('Failed doing Post Dev Reply context menu:')
            print(e, message, sep='\n')
