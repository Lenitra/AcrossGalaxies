from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import get
import psutil
import os
import yaml
import across


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
        await ctx.channel.purge(limit=1)
        await bot.change_presence(activity=discord.Game(name="redémarrer"))
        os.system("sudo reboot")


# @bot.command()
# async def mdp(ctx):
#     await ctx.channel.purge(limit=1)
#     python_role = get(bot.get_guild(ctx.guild.id).roles, name="bleu")
#     await ctx.author.add_roles(python_role)


# region Commande help (affiche le message d'aide) (à finir)
@bot.command()
async def help(ctx):
    await ctx.send(
        f"**Les commandes utilisateur** :```"
        f"\n - {prefix}help"
        f"\n     # Affiche ce message."
        f"\n - {prefix}serveur"
        f"\n     # Affiche les donées de la machine."
        f"\n - {prefix}infos"
        f"\n     # Affiche les stats du jeu."
        f"\n - {prefix}link <e-mail>"
        f"\n     # Lier votre compte de jeu avec votre compte discord."
        f"\n - {prefix}me"
        f"\n     # Vous affiche les données (en mp) de votre compte Across Galaxies si il est lié à votre compte discord."
        "\n```"
        f"**Les commandes Admin** :```"
        f"\n - {prefix}msgingame <titre>;<contenu>"
        f"\n     # Permet d'envoyer un message à tout les joueurs en jeu."
        f"\n - {prefix}log [<day>-<month>-<year>]"
        f"\n     # Permet d'envoyer un message à tout les joueurs en jeu."
        f"\n - {prefix}purge <nombre>"
        f"\n     # Permet d'effacer un nombre de message définis."
        "\n```"
        f"**Les commandes Opérateur (TauMah)** :```"
        f"\n - {prefix}restart"
        f"\n     # Redémarre la machine."
        "\n```")



@commands.has_permissions(administrator=True)
@bot.command()
async def logs(ctx, *args):
    pass
    date = datetime.now()
    if args == ():
        with open(f'logs/{date.day}-{date.month}-{date.year}.yaml', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for e in data:
                await ctx.send(e)
    else:
        with open(f'logs/{args[0]}.yaml', encoding='utf8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for e in data:
                await ctx.send(e)



@commands.has_permissions(administrator=True)
@bot.command()
async def msgingame(ctx, *args):
    print(args)
    if not ";" in args:
        await ctx.send(f"Usage : ```{prefix}msgingame <titre> ; <contenu> ```")
        return
    titre = ""
    contenu = ""
    dotcheck = False
    for m in args:
        if m != ";":
            if not dotcheck:
                titre += m
                titre += " "
            else:
                contenu += m
                contenu += " "
        else:
            dotcheck = True

    msg = (titre, contenu)
    li = os.listdir("data/players")
    for e in li:
        player = e.split(".")[0]
        across.sendmsg(player, msg)

@commands.has_permissions(administrator=True)
@bot.command()
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit + 1)

@bot.command()
async def link(ctx, mail:str):
    await ctx.channel.purge(limit=1)

    game = across.getpsd(mail)
    discord = ctx.author.id

    if not game:
        await ctx.send(
            "Mail Across Galaxies introuvable.")
        return

    with open(f'data/discorddata.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    for iddis, psds in data.items():
        if game == psds :
            await ctx.send("Ce compte Across Galaxies est déjà lié à compte discord")
            return
        if discord == iddis :
            await ctx.send("Ce compte discord est déjà lié à compte Across Galaxies")
            return

    data[discord] = game

    with open(f'data/discorddata.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)

    await ctx.send("Vos comptes ont bien été liés")


@bot.command()
async def me(ctx):
    await ctx.channel.purge(limit=1)
    with open(f'data/discorddata.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    user = data[ctx.author.id]
    with open(f'data/players/{user}.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)


    msg = discord.Embed(title=f"Infos de {user}",
                        description="",
                        colour=discord.Colour.blue())
    msg.add_field(name="Messages",
                  value=f"{len(data['pinf']['msgs'])} non lus",
                  inline=False)
    for plaid, dete in data.items():
        if plaid != "pinf":
            msg.add_field(name=f"\x00", value=f"__-----__", inline=False)
            msg.add_field(name=f"Planète #{plaid}", value=f"\x00", inline=False)
            msg.add_field(name=f"Ressources", value=f"{dete['ress']}")
            msg.add_field(name=f"Batiments", value=f"{dete['bat']}")
            msg.add_field(name=f"Flotte", value=f"{dete['flotte']}")


    await ctx.author.send(embed=msg)

    # await ctx.send(data)



@purge.error
async def purge(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"```Usage : {prefix}purge (nombre)```")
    else:
        await ctx.send("Tu n'as pas la permission de faire ça.")


bot.run(jeton)
