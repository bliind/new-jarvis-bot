import re
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def check_caps_percent(self, message: discord.Message):
        configs = self.bot.config[message.guild.id]

        if message.channel.id in configs.caps_prot_immune_channels:
            return

        immune_roles = configs.caps_prot_immune_roles + configs.moderator_roles
        for role in message.author.roles:
            if role.id in immune_roles:
                return

        # remove emotes
        content = re.sub(r':[\w\d]+:', '', message.content)

        max_percent = configs.caps_prot_percent
        alph = list(filter(str.isalpha, content))
        if len(alph) >= 5:
            percent = (sum(map(str.isupper, alph)) / len(alph) * 100)
            if percent >= max_percent:
                msg_content = configs.caps_prot_message
                try: sent = await message.reply(msg_content)
                except Exception as e:
                    print(e, message, sep='\n')

                await message.delete()
                await asyncio.sleep(5)
                try: await sent.delete()
                except: pass

    async def cheeky_me_check(self, message: discord.Message):
        if self.bot.user.mentioned_in(message):
            if message.author.id == 145971157902950401:
                await message.reply('At your service, sir.')

    async def auto_publish(self, message: discord.Message):
        configs = self.bot.config[message.guild.id]
        if message.channel.id in configs.auto_publish_channels:
            await message.publish()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        try: await self.cheeky_me_check(message)
        except Exception as e:
            print(f'Failed doing cheeky me check:')
            print(e, message, sep='\n')

        try: await self.check_caps_percent(message)
        except Exception as e:
            print(f'Failed checking caps percent:')
            print(e, message, sep='\n')

        try: await self.auto_publish(message)
        except Exception as e:
            print(f'Failed doing auto publish:')
            print(e, message, sep='\n')

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.bot:
            return

        try: await self.check_caps_percent(after)
        except Exception as e:
            print(f'Failed checking caps percent:')
            print(e, after, sep='\n')
