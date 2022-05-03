__import__("dotenv").load_dotenv()
from aiohttp import ClientSession
from discord.ext import commands
from utils import checks
from os import getenv
import discord

class ConfirmationView(discord.ui.View):
    def __init__(self, userid: int):
        super().__init__(timeout=60)
        self.userid = userid
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✅")
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.userid:
            await interaction.response.send_message("Yep thats not yours stop clicking it you fat prick", ephemeral=True)
            return
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="❌")
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.userid:
            await interaction.response.send_message("Yep thats not yours stop clicking it you fat prick", ephemeral=True)
            return
        self.value = False
        self.stop()

class BadgeTracker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        # sourcery skip: use-fstring-for-concatenation
        self.bot = bot
        self.apikey = getenv("apikey")
        self.base_url = "https://sbc.gacek.wtf"
        self.endpoints = {
            "progress": self.base_url + "/api/progress/{user}",
            "rank": self.base_url + "/api/rank/{user}",
            "quickcount": self.base_url + "/api/quickcount/{user}/",
            "count": self.base_url + "/api/count/{user}/",
            "blacklist": self.base_url + "/api/blacklist/{user}?key=" + self.apikey,
            "unblacklist": self.base_url + "/api/unblacklist/{user}?key=" + self.apikey,
            "clearbadges": self.base_url + "/api/clearbadges/{user}?key=" + self.apikey,
            "lb": self.base_url + "/api/leaderboard/",
            "first": self.base_url + "/api/first/{user}",
            "last": self.base_url + "/api/last/{user}",
            "stats": self.base_url + "/api/stats",
            "cleardb": self.base_url + "/api/cleardb/?key=" + self.apikey
        }

    async def username_to_id(self, username: str) -> int:
        async with ClientSession() as session:
            async with session.get("https://api.roblox.com/users/get-by-username", params={"username": username}) as r:
                resp: dict = await r.json()
                return resp.get("Id", None)

    async def id_to_username(self, uid: int) -> int:
        async with ClientSession() as session:
            async with session.get(f"https://api.roblox.com/users/{uid}") as r:
                resp: dict = await r.json()
                return resp.get("Username", None)

    async def get_progress(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.get(self.endpoints["progress"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("data")
                else: raise RuntimeError(resp.get("message"))

    async def get_leaderboard_rank(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.get(self.endpoints["rank"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("rank")
                else: raise RuntimeError(resp.get("message"))

    async def quickcount_badges(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.post(self.endpoints["quickcount"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("message")
                else: raise RuntimeError(resp.get("message"))
    
    async def count_badges(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.post(self.endpoints["count"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("message")
                else: raise RuntimeError(resp.get("message"))

    async def blacklist_user(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.post(self.endpoints["blacklist"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("message")
                else: raise RuntimeError(resp.get("message"))

    async def unblacklist_user(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.delete(self.endpoints["unblacklist"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("message")
                else: raise RuntimeError(resp.get("message"))

    async def clearbadges_user(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.delete(self.endpoints["clearbadges"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("message")
                else: raise RuntimeError(resp.get("message"))

    async def get_leaderboard(self) -> list:
        async with ClientSession() as session:
            async with session.get(self.endpoints["lb"]) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("data")
                else: raise RuntimeError("Something went wrong whilst fetching the leaderboard")


    async def get_first_badge(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.get(self.endpoints["first"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("data")
                else: raise RuntimeError(resp.get("message"))

    async def get_last_badge(self, uid: int) -> list:
        async with ClientSession() as session:
            async with session.get(self.endpoints["last"].format(user=uid)) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("data")
                else: raise RuntimeError(resp.get("message"))
    
    async def get_stats(self) -> list:
        async with ClientSession() as session:
            async with session.get(self.endpoints["stats"]) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("data")
                else: raise RuntimeError("Something went wrong whilst fetching stats")

    async def clearddb_api(self) -> list:
        async with ClientSession() as session:
            async with session.delete(self.endpoints["cleardb"]) as r:
                resp: dict = await r.json()
                if resp.get("success"): return resp.get("message")
                else: raise RuntimeError("Something went wrong whilst clearing the database")

    @commands.command(aliases=["user", "u"])
    async def userinfo(self, ctx: commands.Context, username: str):
        msg = await ctx.send(embed=discord.Embed(title="Please wait", description="Fetching user info...", color=0xFFFF00))
        uid = await self.username_to_id(username)
        if uid is None: return await msg.edit(embed=discord.Embed(title="Error", description="User not found.", color=0xFF0000))
        try:
            leaderboard_rank = await self.get_leaderboard_rank(uid)
            first_badge = await self.get_first_badge(uid)
            last_badge = await self.get_last_badge(uid)
            progress = await self.get_progress(uid)
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(
            title="User Info",
            description=(f"{username}'s info\n"
                          "\n"
                         f"#{leaderboard_rank} on SBC leaderboards with {progress['count']} badges {'(Still counting!)' if progress['quick_counting'] else ('(Recounting!)' if progress['counting'] else '')}\n"
                         f"First badge: [{first_badge['name']}](https://roblox.com/badges/{first_badge['id']})\n"
                         f"Last badge: [{last_badge['name']}](https://roblox.com/badges/{last_badge['id']})"),
            color=ctx.author.color))
    
    @commands.command(aliases=["c"])
    async def count(self, ctx: commands.Context, username: str):
        msg = await ctx.send(embed=discord.Embed(title="Please wait", description=f"Starting to count {username}'s badges..", color=0xFFFF00))
        uid = await self.username_to_id(username)
        if uid is None: return await msg.edit(embed=discord.Embed(title="Error", description="User not found.", color=0xFF0000))
        try: message = await self.quickcount_badges(uid)
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(title="Badge Count", description=message, color=0x00FF00))

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context):
        msg = await ctx.send(embed=discord.Embed(title="Please wait", description="Getting the leaderboard", color=0xFFFF00))
        try: fetched_leaderboard = await self.get_leaderboard()
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(
            title="SBC Leaderboard",
            description="\n".join([f"#{user['place']} {await self.id_to_username(user['userId'])} - {user['count']} Badges" for user in fetched_leaderboard[:10]]),
            color=ctx.author.color))
    
    @commands.command()
    async def stats(self, ctx: commands.Context):
        msg = await ctx.send(embed=discord.Embed(title="Please wait", description="Getting the counter stats", color=0xFFFF00))
        try: fetched_stats = await self.get_stats()
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(
            title="Statistics",
            description=(f"Users registered: {fetched_stats['users']}\n"
                         f"Badges counted: {fetched_stats['badges']}\n"
                         f"Currently counting {fetched_stats['counting']} users\n"),
            color=ctx.author.color))

    @commands.command()
    @checks.isAdmin()
    async def resetdb(self, ctx: commands.Context):
        view = ConfirmationView(ctx.author.id)
        msg = await ctx.send(embed=discord.Embed(title="Are you sure?", description="Are you sure you want to reset the whole database?", color=0xFFFF00), view=view)
        await view.wait()
        await msg.edit(view=None)
        if view.value is None:
            await msg.edit(embed=discord.Embed(title="Aborted", description="No answer in time, aborted", color=0x00FF00))
            return
        elif not view.value:
            return await msg.edit(embed=discord.Embed(title="Aborted", description="Database reset aborted", color=0xFF0000))
        await msg.edit(embed=discord.Embed(title="Please wait", description="Resetting the database..", color=0xFFFF00))
        try: message = await self.clearddb_api()
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(
            title="Database reset, everyone is currently being recounted.",
            description=message,
            color=ctx.author.color))

    @commands.command()
    @checks.isAdmin()
    async def blacklist(self, ctx: commands.Context, username: str):
        msg = await ctx.send(embed=discord.Embed(title="Please wait", description=f"Blacklisting {username}", color=0xFFFF00))
        uid = await self.username_to_id(username)
        try: message = await self.blacklist_user(uid)
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(title="User blacklisted", description=message, color=0x00FF00))
        
    @commands.command()
    @checks.isAdmin()
    async def unblacklist(self, ctx: commands.Context, username: str):
        msg = await ctx.send(embed=discord.Embed(title="Please wait", description=f"Unblacklisting {username}", color=0xFFFF00))
        uid = await self.username_to_id(username)
        try: message = await self.unblacklist_user(uid)
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(title="User unblacklisted", description=message, color=0x00FF00))
        
    @commands.command()
    @checks.isAdmin()
    async def clearbadges(self, ctx: commands.Context, username: str):
        msg = await ctx.send(embed=discord.Embed(title="Please wait", description=f"Clearing {username}'s badges", color=0xFFFF00))
        uid = await self.username_to_id(username)
        try: message = await self.clearbadges_user(uid)
        except RuntimeError as e: return await msg.edit(embed=discord.Embed(title="Error", description=str(e), color=0xFF0000))
        return await msg.edit(embed=discord.Embed(title="Badges cleared", description=message, color=0x00FF00))

def setup(bot: commands.Bot):
    bot.add_cog(BadgeTracker(bot=bot))
