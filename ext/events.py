import discord
import typing as t
from discord.ext import commands
from utils import checks, exceptions
from dotenv import load_dotenv; load_dotenv()

class Events(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as: {self.bot.user.name}')
        await self.bot.change_presence(activity=discord.Game(name='with badges'))
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):  # sourcery no-metrics
        if isinstance(error, commands.CommandNotFound): return
        elif isinstance(error, commands.MissingPermissions): return
        elif isinstance(error, commands.NotOwner): return
        elif isinstance(error, checks.NoAdmin): return
        elif isinstance(error, commands.errors.CheckFailure): return
        elif isinstance(error, commands.errors.CheckAnyFailure): return
        elif isinstance(error, commands.errors.DisabledCommand): return
        elif isinstance(error, commands.errors.MissingRole): return
        elif isinstance(error, commands.errors.MissingAnyRole): return
        elif isinstance(error, commands.errors.NoEntryPointError): print(f'{error.name} does not have the "setup" entry point function')
        elif isinstance(error, commands.errors.ExtensionFailed): print(f'{error.name} extension failed to load during execution of the module or setup entry point.\nException: {error.original}')
        elif isinstance(error, commands.errors.CommandRegistrationError): print(f"The {error.name} command can't be added because the name is already taken by a different command")
        elif isinstance(error, commands.NoPrivateMessage): await ctx.send('This command can be only used in a guild!')
        elif isinstance(error, commands.CommandOnCooldown): embed = discord.Embed(title="Chill out!", description=f"Chill out, you are on cooldown\nYou have `{error.retry_after:.2f} seconds left!`"); await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MissingRequiredArgument): embed = discord.Embed(title="Missing arguments!",description=f'You are missing the {error.param} argument!'); await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.PrivateMessageOnly): embed = discord.Embed(title="Error!", description='This command can only be used in private messages'); await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.NSFWChannelRequired): embed = discord.Embed(title="NSFW Only!", description='This command can only be used in a NSFW channel!'); await ctx.send(embed=embed)
        else: await exceptions.log_error(error=error)
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        if not payload.guild_id: return
        try:
            message: t.Optional[discord.Message] = payload.cached_message
            if message and message.author.id not in self.bot.owner_ids: return
            if message is None:
                guild: t.Optional[discord.Guild] = self.bot.get_guild(payload.guild_id) or await self.bot.fetch_guild(payload.guild_id)
                channel: t.Optional[discord.TextChannel] = guild.get_channel(payload.channel_id) or await self.bot.fetch_channel(payload.channel_id)
                message: discord.Message = await channel.fetch_message(payload.message_id)
                if message and message.author.id not in self.bot.owner_ids: return
            await self.bot.process_commands(message)
        except Exception as e: await exceptions.log_error(e)

def setup(bot: commands.Bot): bot.add_cog(Events(bot=bot))
