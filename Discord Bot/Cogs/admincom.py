import discord
from discord.ext import commands

class admincogs(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
	    await member.kick(reason=reason)
	    await ctx.send(f'Kicked {member.mention}')

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            print(user)

            if (user.name, user.discriminator) == (member.name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send("{}" .format(msg))


def setup(client):
    client.add_cog(admincogs(client))
