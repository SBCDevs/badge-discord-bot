print('Booting up..')
# Import
__import__("dotenv").load_dotenv()
from discord.ext import commands
from utils import prefixList
import nest_asyncio
import discord
import logging
import time
import os


start = time.time()

# Fix asyncio
nest_asyncio.apply()

# Subclasses
# Help Command
class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(title="Help",description=page)
            embed.set_footer(text="Made by SBC")
            await destination.send(embed=embed)

# Variables
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix = prefixList.get_prefix, owner_ids = [795651331721265153], case_insensitive = True, intents = discord.Intents(
    guild_reactions=False,  # reaction add/remove/clear
    guild_messages=True,    # message create/update/delete
    guilds=True,            # guild/channel join/remove/update
    integrations=False,     # integrations update
    voice_states=False,     # voice state update
    dm_reactions=False,     # reaction add/remove/clear
    guild_typing=False,     # on typing
    dm_messages=True,       # message create/update/delete
    presences=False,        # member/user update for games/activities
    dm_typing=False,        # on typing
    webhooks=False,         # webhook update
    members=False,          # member join/remove/update
    invites=False,          # invite create/delete
    emojis=False,           # emoji update
    bans=False              # member ban/unban
))
client.help_command = CustomHelp()

# Extensions
print('Loading extensions..')
for filename in os.listdir('./ext'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'ext.{filename[:-3]}')
        except Exception as e:
            print(f'Failed to load {filename[:-3]} extension')
            print("Error: ", e)
        else:
            continue
try:
    client.load_extension('jishaku')
except Exception as e:
    print('Failed to load Jishaku.')
    print("Error: ", e)
print('Loaded extensions!')

# Login
runtime = time.time() - start
print(f'Bot loaded in {str(runtime)[:3]} seconds.')
client.run(os.getenv('token'))
