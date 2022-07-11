import discord
from decouple import config
import pandas as pd
from detoxify import Detoxify

token = config('token')
def most_toxic(dicc):
    max = 0
    legend = ''
    for i in dicc['Toxicity']:
        if(i > max):
            max = i
            legend = dicc["Comment"][dicc['Toxicity'].index(i)]
    return [max, legend]
def toxicity_analysis(lista):
    dicti = {'Comment':[], 'Toxicity':[]}
    i = 1
    
    for msg in lista:
        tox = Detoxify('original').predict(msg)
        dicti['Comment'].append(msg)
        dicti['Toxicity'].append(round(tox['toxicity']*100, 2))
        print("++Comment {} done!".format(i))
        i += 1
   
    
    
    return dicti

client = discord.Client()
@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel == 'general':
            await client.send(f'''Welcome to the server {member.mention}! Don't be a naughty toxic boy otherwise you get the hammer.''')
@client.event
async def on_message(message):
    serverr = client.get_guild(994978550182576198)
    msg =  message.content
    lisst = []
    if(msg == '!users'):
        await message.channel.send(f'''There are currently: {serverr.member_count} members!''')
    elif(msg == '!amitoxic'):
        await message.channel.send(f"""Computing... don't go anywhere!""")
        messages = await message.channel.history(limit=300).flatten()
        for mess in messages:
            if(mess.author == message.author) and (mess.content[0] != '!'):
                lisst.append(mess.content)
        dic = toxicity_analysis(lisst)
        df = pd.DataFrame(dic).sort_values(by='Toxicity', ascending=False)
        
        peak = most_toxic(dic)
        await message.channel.send(f'''{message.author.mention}\nYour most toxic comment is: \n'{peak[1]}' with a whopping {peak[0]}% toxicity! Chill out man..\nYour comments and their corresponding toxicity levels: \n{df}''')            
    elif('!istoxic' in msg) and (msg[0] == '!'):
        if(str(msg[msg.find('@')+1::].replace('>','')) == '994977171846217798'):
            await message.channel.send(f'''Hehehe.. well everybody knows I can't be toxic! There's no need to check me.''')
        else:
            await message.channel.send(f"""Computing... don't go anywhere!""")
            messages = await message.channel.history(limit=300).flatten()
            for mess in messages:
                if(str(mess.author.id) == msg[msg.find('@')+1::].replace('>','')) and (mess.content[0] != '!'):
                    lisst.append(mess.content)
            dic = toxicity_analysis(lisst)
            df = pd.DataFrame(dic).sort_values(by='Toxicity', ascending=False)
            peak = most_toxic(dic)
            await message.channel.send(f"""{message.author.mention}\n\n<@{msg[msg.find('@')+1::].replace('>','')}> 's most toxic comment is: \n'{peak[1]}' with a whopping {peak[0]}% toxicity! Chill out man..\nA list of their comments and their corresponding toxicity levels: \n{df}""")
    elif(msg == '!help'):
        await message.channel.send(f'''\n+++ In order to see your own toxic comments: \n!amitoxic\n+++ In order to see a user's toxic comments: \n!istoxic @user_tag\n+++ In order to see the number of present users: \n!users''')
client.run(token)


