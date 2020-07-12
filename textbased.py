import random as r
import discord
from discord.ext import commands
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import re
from dicttoxml import dicttoxml

_page = None

def listall():
  f = open('TextDB/Roles.txt', 'r')
  lines = f.readlines()
  response = 'Roles: \n'

  for line in lines:
    response += line
  return(response)

def addtable(arg):
  f = open('TextDB/Roles.txt', 'a')
  f.write(str(arg)+'\n')
  f.close()
  return('👍')

def unaddtable(arg):
  with open('TextDB/Roles.txt', "r") as f:
    lines = f.readlines()
  with open('TextDB/Roles.txt', "w") as f:
    for line in lines:
        if line.strip("\n") != arg:
            f.write(line)
  return('👍')
  
def ajuda():
  f = open('TextDB/Comandos.txt', 'r')
  lines = f.readlines()
  response = ''
  total = sum(1 for line in open('TextDB/Comandos.txt'))

  with open('TextDB/Comandos.txt') as temp_file:
    test = [line.rstrip('\n') for line in temp_file]

  for line in lines:
    response += line

  return(response)
def get_html_page(cache):
    global _page
    
    if cache is False:
        _page = None
    if _page is None:
        html = urlopen('https://www.placardefutebol.com.br/')
        _page = BeautifulSoup(html, 'lxml')
        
    res = _page
    
    return res
    

def jogos_de_hoje(cache=False):
    page = get_html_page(cache)
    titles = page.find_all('h3', class_='match-list_league-name')
    championships = page.find_all('div', class_='container content')
    
    results = []
    
    for id, championship in enumerate(championships):
        matchs = championship.find_all('div', class_='row align-items-center content')
        
        for match in matchs:
            status = match.find('span', class_='status-name').text
            teams = match.find_all('div', class_='team-name')
            status = match.find('span', class_='status-name').text
            scoreboard = match.find_all('span', class_='badge badge-default')
            
            team_home = teams[0].text.strip()
            team_visitor = teams[1].text.strip()
            
            info = {
                'Liga': titles[id + 1].text,
                'Partida': '{} x {}'.format(team_home, team_visitor),
                'status': status,
                
            }
            
            score = {}
            
            # Se o jogo já começou então existe placar.
            try:
#                score['scoreboard'] = {
#                    team_home: scoreboard[0].text,
#                    team_visitor: scoreboard[1].text
#                }
                score['Placar'] = '{} x {}'.format(scoreboard[0].text, scoreboard[1].text)
            # Caso não tenha começado, armazena o horário de início
            except:
                score['start_in'] = status
                score['status'] = 'EM BREVE'
            
            info.update(score)
            
            results.append(info)
        
    return results

  
def jogos_ao_vivo():
    matchs = jogos_de_hoje(cache=False)
    results = list(filter(lambda match: re.findall(r'INTERVALO|AO VIVO|MIN', match['status']), matchs))
    return results
        
def buscar_jogo_por_time(arg):
    matchs = jogos_de_hoje(cache=False)
    return list(filter(lambda match: arg.lower() in match['Partida'].lower(), matchs))
    
def buscar_jogo_por_liga(arg):
    matchs = jogos_de_hoje(cache=False)
    return list(filter(lambda match: arg.lower() in match['Liga'].lower(), matchs))
