import discord
from discord.ext import commands

from util import configuration, select_one

class UserJoinEvent(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  """
  This event is triggered when a user joins the server,
  and will assign the user their Maaldar role if they are
  an old Maaldar
  """  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    guild: discord.Guild = member.guild

    maaldar_role = select_one(f"SELECT * FROM MaaldarRoles WHERE user_id = '{member.id}'")
    if maaldar_role is None:
      return
    
    # Create the role according to user data and position it
    role = await guild.create_role(
      name=maaldar_role[1], 
      color=discord.Color(int(maaldar_role[2]))
    )
    
    await role.edit(
      position=(guild.get_role(configuration["custom_role_id"]).position - 1)
    )
    await member.add_roles(role)
  

async def setup(bot: commands.Bot):
  await bot.add_cog(UserJoinEvent(bot), guilds=[discord.Object(id=configuration["guild_id"])])
