import discord
from discord.ext import commands
from discord.utils import get
import psutil
import os
import pyscreenshot as ImageGrab
import yaml
import speedtest


prefix = "$"
# region Jeton
jeton = "NzExOTQzNDExNjU3MDgwODUy.XsKW-A.H4DQnB9GWrWKiv81PzWNWBu1Nk4"
# endregion

bot = commands.Bot(command_prefix=prefix)

bot.remove_command("help")
client = discord.Client()

op = [304868399492759553]

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status, activity=discord.Game(f"Développé par ToMa#0504"))
    print("-------------------------------")
    print("-------- BOT SYSTEM -----------")
    print("-------------------------------")


# @commands.has_permissions(administrator=True)
@bot.command()
async def serveur(ctx):
    a = await ctx.send("Calcul en cours..")
    msg = discord.Embed(
        title=f"**SYSTEM INFO**",
        description="",
        colour=discord.Colour.blue()
    )
    msg.add_field(name="Mémoire",
                  value=f"{psutil.virtual_memory().percent}%")
    msg.add_field(name="Processeur",
                  value=f"{psutil.cpu_percent(5)}%")
    #msg.add_field(name="Température", inline=False,value=f"{int(GPUtil.getGPUs()[0].temperature)} °C")

    msg.add_field(name="Latence du bot", inline= False,
                  value=f"{round(bot.latency * 1000)} ms")

    await ctx.send(embed=msg)
    await a.delete()


@bot.command()
async def infos(ctx):
    msg = discord.Embed(
        title=f"**Stats du jeu**",
        description="",
        colour=discord.Colour.blue()
    )
    inscrits = 0
    for _ in os.listdir("data/players"):
        inscrits += 1
    nb_pla_col = 0
    with open(f'data/planets.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for e in data.values():
        if e != None:
            nb_pla_col +=1

    msg.add_field(name="Nombre d'inscrits :", value=f"{inscrits}")
    msg.add_field(name="Nombre de planètes colonisées :",
                  value=f"{nb_pla_col}", inline=False)
    await ctx.send(embed=msg)


@bot.command()
async def restart(ctx):
    if ctx.author.id in op:
        await bot.change_presence(activity=discord.Game(name="redémarrer"))
        await ctx.channel.purge(limit=1)
        os.system("sudo reboot")


# @bot.command()
# async def mdp(ctx):
#     await ctx.channel.purge(limit=1)
#     python_role = get(bot.get_guild(ctx.guild.id).roles, name="bleu")
#     await ctx.author.add_roles(python_role)


# region Commande help (affiche le message d'aide) (à finir)
@bot.command()
async def help(ctx):
    await ctx.send(f"**Les commandes utilisateur** :```"
                                  f"\n - {prefix}help"
                                  f"\n     # Affiche ce message."
                                  f"\n - {prefix}serveur"
                                  f"\n     # Affiche les donées de la machine."
                                  f"\n - {prefix}infos"
                                  f"\n     # Affiche les stats du jeu."
                                  f"\n - {prefix}myid"
                                  f"\n     # Affiche votre id discord."
                                  "\n```"
                   f"**Les commandes Admin** :```"
                                  f"\n - {prefix}purge <nombre>"
                                  f"\n     # Permet d'effacer un nombre de message définis."
                                  "\n```"
                   f"**Les commandes Opérateur (TauMah)** :```"
                                  f"\n - {prefix}restart"
                                  f"\n     # Redémarre la machine."
                                  "\n```"

                   )



@commands.has_permissions(administrator=True)
@bot.command()
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit + 1)

@bot.command()
async def myid(ctx):
    await ctx.send(f"L'id de {ctx.author} est : {ctx.author.name}")



@bot.command()
async def screen(ctx):
    im = ImageGrab.grab()
    im.save("cache_full.png")
    await ctx.send(file=discord.File('cache_full.png'))


@purge.error
async def purge(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"```Usage : {prefix}purge (nombre)```")
    else:
        await ctx.send("Tu n'as pas la permission de faire ça.")


bot.run(jeton)
