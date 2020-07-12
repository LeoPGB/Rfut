import os

import discord
import asyncio
import keep_alive
import textbased
import random as r
import linecache as lc
from dotenv import load_dotenv
from discord.ext import commands
import numpy as np
import wikipedia
import treys

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!poker'): 
    user = bot.user
    user2 = bot.user
    author: discord.Member = message.author
    channel = message.channel
    deck = treys.Deck()
    evaluator = treys.Evaluator()
    board = deck.draw(5)
    p1_hand = deck.draw(0)
    await channel.send(treys.Card.print_pretty_cards(board + p1_hand))
    
    change = await channel.send(str(author.mention) + ', quantas cartas você quer trocar? (Espere todos os emotes aparecerem, você tem 20 segundos)')

    await change.add_reaction('0️⃣')
    await change.add_reaction('1️⃣')
    await change.add_reaction('2️⃣')
    await change.add_reaction('3️⃣')
    await change.add_reaction('4️⃣')
    await change.add_reaction('5️⃣')

    def check(reaction, user):
      if str(reaction.emoji) == '0️⃣':
        return user == message.author and str(reaction.emoji) == '0️⃣'
      if str(reaction.emoji) == '1️⃣':
        return user == message.author and str(reaction.emoji) == '1️⃣'
      elif str(reaction.emoji) == '2️⃣':
        return user == message.author and str(reaction.emoji) == '2️⃣'
      elif str(reaction.emoji) == '3️⃣':
        return user == message.author and str(reaction.emoji) == '3️⃣'
      elif str(reaction.emoji) == '4️⃣':
        return user == message.author and str(reaction.emoji) == '4️⃣'
      elif str(reaction.emoji) == '5️⃣':
        return user == message.author and str(reaction.emoji) == '5️⃣'

    def check2(reaction):
      if str(reaction.emoji) == '0️⃣':
        return -1
      if str(reaction.emoji) == '1️⃣':
        return 0
      elif str(reaction.emoji) == '2️⃣':
        return 1
      elif str(reaction.emoji) == '3️⃣':
        return 2
      elif str(reaction.emoji) == '4️⃣':
        return 3
      elif str(reaction.emoji) == '5️⃣':
        return 4

    try:
      while (user != message.author):
        reaction, user= await bot.wait_for('reaction_add', timeout=20.0, check=check)
      a = check2(reaction) + 1
      x = np.zeros(a)

      if (a != 0):
        change = await channel.send(str(author.mention) + ', quais cartas você quer trocar? (Espere todos os emotes aparecerem, você tem 20 segundos)')
        await change.add_reaction('1️⃣')
        await change.add_reaction('2️⃣')
        await change.add_reaction('3️⃣')
        await change.add_reaction('4️⃣')
        await change.add_reaction('5️⃣')

      for i in range (a):
        while (user2 != message.author): 
          reaction, user2= await bot.wait_for('reaction_add', timeout=20.0, check=check)
        user2 = bot.user
        x[i]= check2(reaction)
      x.sort()
      x = x[::-1]
      for i in range (a):
        board[int(x[i])] = deck.draw(1)

    except asyncio.TimeoutError:
      await channel.send(str(author.mention) + ', demorou demais')
    else:
      await channel.send(treys.Card.print_pretty_cards(board + p1_hand))
      p1_score = evaluator.evaluate(board, p1_hand)
      p1_class = evaluator.get_rank_class(p1_score)
      await channel.send(str(author.mention) + ', você tirou um ' + evaluator.class_to_string(p1_class))

  await bot.process_commands(message)
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Faltam argumentos no comando')
  if isinstance(error, commands.CommandNotFound):
    pass

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
#@commands.is_channel('CHANNEL_ID')
async def createrole(ctx, arg, c1:int, c2:int , c3:int):
  cor = '%02x%02x%02x' % (c1, c2, c3)
  x = int(cor, 16)

  await ctx.guild.create_role(name=arg, color=discord.Colour(x))
  await ctx.send("Role {} criada <:sorrizoronaldo:586752638767464448>".format(arg)) 

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def addrole(ctx, member: discord.Member=None, *, role: discord.Role):
  member = member or ctx.message.author

  await discord.Member.add_roles(member, role)
  await ctx.send("Role {} adicionada ao usuário <:sorrizoronaldo:586752638767464448>".format(role, member)) 

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def removerole(ctx, member: discord.Member=None, *, role: discord.Role):
  member = member or ctx.message.author
  await discord.Member.remove_roles(member, role)
  await ctx.send("Role {} removida do usuário <:sorrizoronaldo:586752638767464448>".format(role)) 

@bot.command(pass_context=True)
async def addself(ctx, *, role: discord.Role):
  member = ctx.message.author
  x = discord.utils.get(ctx.guild.roles, name='Promessa de Base')
  with open('TextDB/Roles.txt') as myfile:
    if str(role) in myfile.read():
      if (str(role) == 'Grêmio'):
        await ctx.send("Gremista é arrombado <:sorrizoronaldo:586752638767464448>")  
      await ctx.send("Role {} adicionada <:sorrizoronaldo:586752638767464448>".format(role)) 
      await discord.Member.add_roles(member, role)
      await discord.Member.remove_roles(member, x)

@addself.error
async def addself_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send('A role digitada não foi encontrada. Use !allroles para ver as roles disponíveis')

@bot.command(pass_context=True)
async def removeself(ctx, *, role: discord.Role):
  member = ctx.message.author
  with open('TextDB/Roles.txt') as myfile:
    if str(role) in myfile.read():   
      await discord.Member.remove_roles(member, role)
      await ctx.send("Role {} removida <:sorrizoronaldo:586752638767464448>".format(role))

@removeself.error
async def removeself_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send('A role digitada não foi encontrada.')

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def addtable(ctx, *, arg):
  await ctx.send(textbased.addtable(arg))

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def unaddtable(ctx, *, arg):
    await ctx.send(textbased.unaddtable(arg))

@bot.command(pass_context=True)
async def allroles(ctx):
  await ctx.send(textbased.listall())

@bot.command(pass_context=True)
async def ajuda(ctx):
  await ctx.send(textbased.ajuda())

@bot.command(pass_context=True)
async def eightball(ctx, *, arg):
  await ctx.send ('🎱 '+ r.choice(open('TextDB/8ball.txt').readlines()))

@bot.command(pass_context=True)
async def wiki(ctx, lang, *, arg):
  wikipedia.set_lang(lang)  
  #await ctx.send ('Sugestões de busca: \n' + wikipedia.search(arg, results=10))
  await ctx.send (wikipedia.page(arg).url + '\n' + wikipedia.summary(arg, sentences=5))

@bot.command(pass_context=True)
async def jogoshoje(ctx):
  resultados = textbased.jogos_de_hoje()
  for result in resultados:
    if (result['status'] == 'EM BREVE'):
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['start_in'])
    else:
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['Placar'] + ' | ' + result['status'])
	
  await ctx.send('Terminado <:sorrizoronaldo:586752638767464448>')

@bot.command(pass_context=True)
async def jogosaovivo(ctx):
  resultados = textbased.jogos_ao_vivo()
  for result in resultados:
    if (result['status'] == 'EM BREVE'):
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['start_in'])
    else:
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['Placar'] + ' | ' + result['status'])

@bot.command(pass_context=True)
async def jogostime(ctx, arg):
  resultados = textbased.buscar_jogo_por_time(arg)
  for result in resultados:
    if (result['status'] == 'EM BREVE'):
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['start_in'])
    else:
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['Placar'] + ' | ' + result['status'])

@bot.command(pass_context=True)
async def test(ctx):
  resultados = textbased.jogos_ao_vivo()
  for result in resultados:
    await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['Placar'] + ' | ' + result['status'])

@bot.command(pass_context=True)
async def jogosliga(ctx, arg):
  resultados = textbased.buscar_jogo_por_liga(arg)
  for result in resultados:
    if (result['status'] == 'EM BREVE'):
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['start_in'])
    else:
      await ctx.send(result['Liga'] + ' | ' + result['Partida']  + ' | ' + result['Placar'] + ' | ' + result['status'])
    

keep_alive.keep_alive()
bot.run(token)