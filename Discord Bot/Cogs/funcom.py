import discord
from discord.ext import commands

class funcogs(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.command(aliases=['sup', 'hi', 'yo'])
    async def hello(self, ctx):
        user = ctx.message.author
        await ctx.send(f"Sup {user.mention}, what's poppin?")

def setup(client):
    client.add_cog(funcogs(client))
