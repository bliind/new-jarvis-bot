import datetime
import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
import ConfigDB as config

def check_member_age(member: discord.Member, new_account_day_count: int):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - member.created_at

    return diff.days >= new_account_day_count

def check_server_age(member: discord.Member, member_hour_count: int):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - member.joined_at

    return (diff.total_seconds() / 3600) >= member_hour_count

class MemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_member_roles.start()
        # don't run the loops at the same time
        await asyncio.sleep(60)
        self.check_mute_roles.start()

    @tasks.loop(seconds=3600)
    async def check_mute_roles(self):
        for server in self.bot.guilds:
            configs = await config.get_configs(server.id, [
                'new_account_role',
                'new_account_day_count',
            ])

            try:
                role = server.get_role(configs.new_account_role)
                if role:
                    members = [m for m in server.members if role in m.roles]
                    for member in members:
                        if check_member_age(member, configs.new_account_day_count):
                            await member.remove_roles(role)
            except Exception as e:
                print('Failed to check new account roles:')
                print(e, server)
                try: print(member)
                except: pass

    @tasks.loop(seconds=3600)
    async def check_member_roles(self):
        for server in self.bot.guilds:
            configs = await config.get_configs(server.id, [
                'new_account_role',
                'member_role',
                'member_hour_count'
            ])

            try:
                role = server.get_role(configs.member_role)
                new_acct_role = server.get_role(configs.new_account_role)

                if role:
                    members = [m for m in server.members if role not in m.roles]
                    for member in members:
                        if check_server_age(member, configs.member_hour_count) \
                        and new_acct_role not in member.roles:
                            await member.add_roles(role)
            except Exception as e:
                print('Failed to check member roles:')
                print(e, server)
                try: print(member)
                except: pass

    async def check_new_member_age(self, member: discord.Member):
        configs = await config.get_configs(member.guild.id, [
            'new_account_role',
            'new_account_day_count',
        ])

        if not check_member_age(member, configs.new_account_day_count):
            role = member.guild.get_role(configs.new_account_role)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # check for newly joined members with fresh discord accounts
        try: await self.check_new_member_age(member)
        except Exception as e:
            print('Error checking new member age:')
            print(e, member)
