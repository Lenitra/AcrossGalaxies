from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import get
import psutil
import os
import yaml
import across
from reqsql import readsql, reqsql, retbrut


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
    await bot.change_presence(status=discord.Status, activity=discord.Game(f"Across-Galaxies.fr"))
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

    msg.add_field(name="Nombre d'inscrits :", value=len(retbrut(f"SELECT Psd FROM Accounts")))
    msg.add_field(name="Nombre de planètes colonisées :",
                  value=len(retbrut(f"SELECT * FROM Planets WHERE Psd != 'None'")), inline=False)
    await ctx.send(embed=msg)


@bot.command()
async def restart(ctx):
    if ctx.author.id in op:
        await ctx.channel.purge(limit=1)
        await bot.change_presence(activity=discord.Game(name="redémarrer"))
        os.system("sudo reboot")

@bot.command()
async def reload(ctx):
    if ctx.author.id in op:
        await ctx.channel.purge(limit=1)
        await bot.change_presence(activity=discord.Game(name="redémarrer"))
        os.system("sudo reboot")

@bot.command()
async def reboot(ctx):
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
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="Les commandes utilisateur.",
                          description="Vous avez accès à ces commandes",
                          color=discord.Colour.blue())
    embed.add_field(name="$help", value="Affiche les commandes disponibles.", inline=False)
    embed.add_field(name="$serveur", value="Affiche les informations du serveur.", inline=False)
    embed.add_field(name="$infos", value="Affiche les informations du jeu.", inline=False)
    embed.add_field(name="$link <e-mail>",value="Lier votre compte de jeu avec votre compte discord. (supprime automatiquement votre mail du chat)",inline=False)
    embed.set_footer(text="Across-Galaxies.fr")
    await ctx.send(embed=embed)

    with open(f'data/discorddata.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    duser = ctx.author.id
    try:
        player = data[duser]
    except:
        await ctx.send("*Veuillez connecter votre compte Across-Galaxies et votre discord pour avoir accès à plus de commandes*")
        return


    embed = discord.Embed(
        title="Les commandes joueur.",
        description=
        "Vous avez accès à ces commandes car votre compte Across-Galaxies est lié à votre discord.",
        color=discord.Colour.blue())
    embed.add_field(name="$me <'player'-'ress'-'infra'-'flotte'>", value="Affiche les informations de votre compte.", inline=False)
    embed.add_field(name="$unlink", value="Délier votre compte de jeu avec votre compte discord.", inline=False)
    embed.set_footer(text="Across-Galaxies.fr")
    await ctx.send(embed=embed)


    if across.isvip(player) or ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="Les commandes vip.",
            description="Vous avez accès à ces commandes car vous êtes VIP sur le jeu.",
            color=discord.Colour.blue())
        embed.add_field(
            name="$recolte",
            value="Récolte les ressources sur toutes vos planètes.",
            inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)

    else:
        await ctx.send("*Pour avoir accès à plus de commandes, il vous faut être VIP.*")
        return


    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="Les commandes administrateur.",
            description="Vous avez accès à ces commandes car vous êtes administrateur.",
            color=discord.Colour.blue())
        embed.add_field(name="$purge <nombre>", value="Supprime un nombre défini de messages", inline=False)
        embed.add_field(name="$logs", value="Affiche les logs du jeu de la journée.", inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)

    if ctx.author.id in op:
        embed = discord.Embed(
            title="Les commandes fondateur.",
            description=
            "Vous avez accès à ces commandes car vous êtes fondateur.",
            color=discord.Colour.blue())
        embed.add_field(name="$restart | $reboot | $reload", value="Redémarre la machine.", inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)


@commands.has_permissions(administrator=True)
@bot.command()
async def logs(ctx, *args):
    if ctx.author.id in op:
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
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit + 1)


@bot.command()
async def unlink(ctx):
    await ctx.channel.purge(limit=1)
    with open(f'data/discorddata.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    duser = ctx.author.id
    try:
        player = data[duser]
    except:
        embed = discord.Embed(
            title=
            "Votre compte Across Galaxies n'est pas lié à votre compte discord.",
            description="$link <e-mail>",
            color=discord.Colour.blue())
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)
        return
    data.pop(duser)
    with open(f'data/discorddata.yaml', 'w', encoding='utf8') as f:
        yaml.dump(data, f, default_flow_style=False)
    embed = discord.Embed(title="Votre compte Across Galaxies a bien été délié.",
                          description="",
                          color=discord.Colour.blue())
    embed.set_footer(text="Across-Galaxies.fr")
    await ctx.send(embed=embed)


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
            embed = discord.Embed(
                title="Votre compte Across Galaxies est déjà lié à un compte discord.",
                description="",
                color=discord.Colour.blue())
            embed.set_footer(text="Across-Galaxies.fr")
            await ctx.send(embed=embed)
            return

        if discord == iddis :
            embed = discord.Embed(
                title="Votre compte discord est déjà lié à un compte Across Galaxies.",
                description="",
                color=discord.Colour.blue())
            embed.set_footer(text="Across-Galaxies.fr")
            await ctx.send(embed=embed)
            return

    data[discord] = game

    with open(f'data/discorddata.yaml', 'w', encoding='utf8') as f:
        data = yaml.dump(data, f)
    embed = discord.Embed(title="Vos comptes ont bien été liés.",
                          description="",
                          color=discord.Colour.blue())
    embed.set_footer(text="Across-Galaxies.fr")
    await ctx.send(embed=embed)


@bot.command()
async def recolte(ctx):
    await ctx.channel.purge(limit=1)

    with open(f'data/discorddata.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    duser = ctx.author.id
    try:
        player = data[duser]
    except:
        embed = discord.Embed(
            title=
            "Votre compte Across Galaxies n'est pas lié à votre compte discord.",
            description="$link <e-mail>",
            color=discord.Colour.blue())
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)
        return

    if across.isvip(player):
        across.updateressource(player)
        await ctx.send(f"Vous avez récolté vos ressources.")
        return
    else:
        embed = discord.Embed(
            title="Vous devez avoir un compte vip pour effectuer cette action.",
            description="Plus d'informations directement en jeu.",
            color=discord.Colour.blue())
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)
        return


@bot.command()
async def me(ctx, *args):
    await ctx.channel.purge(limit=1)

    with open(f'data/discorddata.yaml', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    duser = ctx.author.id
    try:
        player = data[duser]
    except:
        embed = discord.Embed(
            title=
            "Votre compte Across Galaxies n'est pas lié à votre compte discord.",
            description="$link <e-mail>",
            color=discord.Colour.blue())
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)
        return

    if args == ():
        embed = discord.Embed(title="Commande mal utilisée",
                              description="$me <donnée>",
                              color=discord.Colour.blue())
        embed.add_field(name="$me player", value="Envoie les information générale du joueur", inline=False)
        embed.add_field(name="$me ress", value="Envoie les information relatives aux __ressources__ de toutes vos planètes", inline=False)
        embed.add_field(name="$me infra", value="Envoie les information relatives aux __infrastructures__ de toutes vos planètes", inline=False)
        embed.add_field(name="$me flotte", value="Envoie les information relatives aux __flottes__ de toutes vos planètes", inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)
        return

    if args[0] == "player":
        embed = discord.Embed(title=f"Informations de {player}",
                              description="",
                              color=discord.Colour.blue())

        data = readsql(f"SELECT * FROM PInf WHERE Psd='{player}'")
        embed.add_field(name=f"Vos planètes", value=f"{across.getallplaid(player)}", inline=False)
        embed.add_field(name="Date de dernière récolte : ", value=f"{data[1]}", inline=False)
        if datetime.now() > data[2]:
            embed.add_field(name="Date d'expiration du vip : ", value="Exipiré", inline=False)
        else:
            embed.add_field(name="Date d'expiration du vip : ", value=f"{data[1]}", inline=False)
        embed.add_field(name="Statut : ", value=f"{data[3]}", inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.author.send(embed=embed)
        return

    if args[0] == "ress":
        count = 0
        embed = discord.Embed(title="Ressource de toutes vos planètes",
                              description="",
                              color=discord.Colour.blue())
        data = retbrut(f"SELECT Plaid, Ress1, Ress2, Ress3 FROM Planets WHERE Psd='{player}'")
        for e in range(len(data)):
            count += 1
            if count < 7:
                embed.add_field(name=f"---", value=f"**Planète #{data[e][0]}**", inline=False)
                embed.add_field(name="Carbone : ", value=f"{data[e][1]}", inline=True)
                embed.add_field(name="Puces : ", value=f"{data[e][2]}", inline=True)
                embed.add_field(name="Hydrogène :", value=f"{data[e][3]}", inline=True)
            else:
                embed.add_field(name=f"---", value=f"*Désolé je ne peux pas afficher plus d'informations*", inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.author.send(embed=embed)
        return

    if args[0] == "infra":
        count = 0
        embed = discord.Embed(title="Infrastructures de vos planètes",
                              description="",
                              color=discord.Colour.blue())
        data = retbrut(f"SELECT Plaid, Carbone, Puces, Hydro, Sp, Rad FROM Planets WHERE Psd='{player}'")
        for e in range(len(data)):
            count += 1
            if count < 5:
                embed.add_field(name=f"---", value=f"**Planète #{data[e][0]}**", inline=False)
                embed.add_field(name="Mine de carbone : ", value=f"{data[e][1]}", inline=True)
                embed.add_field(name="Raffinerie de puces : ", value=f"{data[e][2]}", inline=True)
                embed.add_field(name="Centrale d'hydrogène :", value=f"{data[e][3]}", inline=True)
                embed.add_field(name="Spatioport :", value=f"{data[e][4]}", inline=True)
                embed.add_field(name="Radar :", value=f"{data[e][5]}", inline=True)
            else:
                embed.add_field(name=f"---", value=f"*Désolé je ne peux pas afficher plus d'informations*", inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.author.send(embed=embed)
        return

    if args[0] == "flotte":
        count = 0
        embed = discord.Embed(title="Infrastructures de vos planètes",
                              description="",
                              color=discord.Colour.blue())
        data = retbrut(f"SELECT Plaid, Croiseur, Nanosonde, Cargo, Victoire, Colonisateur FROM Planets WHERE Psd='{player}'")
        for e in range(len(data)):
            count += 1
            if count < 5:
                embed.add_field(name=f"---", value=f"**Planète #{data[e][0]}**", inline=False)
                embed.add_field(name="Croiseurs : ", value=f"{data[e][1]}", inline=True)
                embed.add_field(name="Nanosondes : ", value=f"{data[e][2]}", inline=True)
                embed.add_field(name="Cargos :", value=f"{data[e][3]}", inline=True)
                embed.add_field(name="Victoires :", value=f"{data[e][4]}", inline=True)
                embed.add_field(name="Colonisateurs :", value=f"{data[e][5]}", inline=True)
            else:
                embed.add_field(name=f"---", value=f"*Désolé je ne peux pas afficher plus d'informations*", inline=False)
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.author.send(embed=embed)
        return






@purge.error
async def purge(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Usage : {prefix}purge (nombre)", description="", color=discord.Colour.blue())
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title=f"Erreur : Tu n'as pas la permission de faire ça.",
            description="",
            color=discord.Colour.blue())
        embed.set_footer(text="Across-Galaxies.fr")
        await ctx.send(embed=embed)


bot.run(jeton)
