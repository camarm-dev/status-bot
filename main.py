import asyncio
import datetime
import random

import conf as cf
import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix=".", description="Lambda.")

conf = cf.asdict()
token = conf['Bot']['token']
invite = conf['Bot']['invite']
userId = int(conf['Bot']['user'])
statusChannelId = int(conf['Bot']['statuschannel'])
logsChannelId = int(conf['Bot']['logschannel'])
s_channel = discord.TextChannel
l_channel = discord.TextChannel
message = discord.Message
gifs = ['https://c.tenor.com/iu2d2HPdtzIAAAAC/tenor.gif', 'https://i.giphy.com/media/uVPv3hrAa4ehQeRHvk/giphy.gif', 'https://media0.giphy.com/media/MNfZSteJU94qc/giphy.gif?cid=790b76110d54693cc3b083a128883ed6c27be505f46fb491&rid=giphy.gif&ct=g', 'https://c.tenor.com/HHwDrmgUMw0AAAAC/vilebrequin-vilebrequin-sylvain-levy.gif', 'https://c.tenor.com/SXM68LEzlTYAAAAM/vilebrequin-vilebrequin-tellement-pt.gif', 'https://c.tenor.com/V8VPN6vsPqoAAAAC/vilebrequin-vilebrequin-sylvain-levy.gif', 'https://c.tenor.com/sx5M-bGDt1oAAAAd/vilebrequin-vilebrequin-cpt.gif']
sample_embed = discord.Embed(title='Status bot is starting...', description='Please wait, this message will be edited.', color=discord.Color.blue())
user = discord.User
to_check = [
    {'url': 'http://blaugue.camponovo.xyz', 'nom': 'Blaugue (personal blog)', 'desc': 'Blaugue, LE blog des cocoyoyos !', 'notify': True},
    {'url': 'https://www.camarm.dev', 'nom': 'CAMARM Website (personal website)', 'desc': 'Site officiel de CAMARM-DEV.', 'notify': True},
    {'url': 'http://192.168.1.32', 'nom': 'Nas OMV Local (storage)', 'desc': 'Local NAS', 'notify': True},
    {'url': 'http://server.camarm.fr', 'nom': 'Tunnels / Redirections (urls)', 'desc': 'Very important, if this server is down, it\'s impossible to reach other services', 'notify': True},
    {'url': 'http://ondine.camponovo.art', 'nom': 'Ondine Camponovo Portfolio (ondine website)', 'desc': 'Ondine Camponovo Portfolio', 'notify': True},
    {'url': 'https://192.168.1.103:8006', 'nom': 'Odirion (hosting services)', 'desc': 'PVE node (all hosting services)', 'notify': True},
    {'url': 'https://meteo.camarm.dev', 'nom': 'Meteo Station', 'desc': 'Station meteo Etalans website', 'notify': True},
    {'url': 'http://vps1.camarm.fr:9090', 'nom': 'CAMARM Vps 1', 'desc': 'VPS 1', 'notify': False},
    {'url': 'http://vps2.camarm.fr:9090', 'nom': 'CAMARM Vps 2', 'desc': 'VPS 2', 'notify': True},
    {'url': 'http://152.228.131.152:40075', 'nom': 'Campo Vps 1', 'desc': 'VPS 3', 'notify': True},
    {'url': 'https://cocoyoyo-librairie.camponovo.space', 'nom': 'Cocoyoyolibrairie (personal babelio)', 'desc': 'La cocoyoyoLibrairie est une bibliothèque virtuelle pour toute la famille.', 'notify': True},
]
timeout = 120


def ping(url):
    try:
        response = requests.get(url, verify=False)
        if response.ok or response.status_code in [404]:
            return True
        return False
    except:
        # raise e
        return False


async def check_status():
    while True:
        print('Checking status')
        embed = discord.Embed(title='Status checking', description='checking status of services...', color=discord.Color.light_grey())
        new_message = await s_channel.send(embed=embed)
        embed = discord.Embed(title='Status Bot:', description='Status of all services:')
        is_a_down = False
        for service in to_check:
            response = ping(service['url'])
            print(response)
            emoji = '🟢'
            if not response:
                emoji = '🔴'
                if service['notify']:
                    is_a_down = True
                    user_embed = discord.Embed(title='Oups...', description=f"It\'s seems like {service['url']} ({service['nom']} is down !)", color=discord.Color.dark_red())
                    user_embed.set_image(url=random.choice(gifs))
                    user_embed.set_author(name='Down service link here', url=service['url'], icon_url='https://cdn.discordapp.com/app-icons/987993226701058079/7236c41d6da22576a69f969d9c5397a9.png?size=256')
                    await user.send(embed=user_embed)
            name = f"{service['nom']} {emoji}"
            embed.add_field(name=name, value=service['desc'], inline=False)
        embed.set_author(name='Status Bot by CAMARM', url='https://www.camarm.dev', icon_url='https://cdn.discordapp.com/app-icons/987993226701058079/7236c41d6da22576a69f969d9c5397a9.png?size=256')
        date = datetime.datetime.now().strftime('%c')
        embed.set_footer(text=f'Last check {date}', icon_url='https://images.emojiterra.com/twitter/v12.1.5/512px/1f556.png')
        if is_a_down:
            embed.set_image(url=random.choice(gifs))
            embed.color = discord.Color.red()
        else:
            embed.color = discord.Color.green()
        await message.edit(embed=embed)
        await new_message.delete()
        await asyncio.sleep(timeout)


async def start():
    bot.loop.create_task(check_status())


@bot.command()
async def dstart(ctx):
    message_to_delete_id = ctx.message.id
    to_delete = await ctx.channel.fetch_message(message_to_delete_id)
    await to_delete.delete()
    await l_channel.send('Starting bot status !')


@bot.event
async def on_ready():
    global s_channel, l_channel, message, user
    user = await bot.fetch_user(userId)
    s_channel = await bot.fetch_channel(statusChannelId)
    l_channel = await bot.fetch_channel(logsChannelId)
    await s_channel.purge(limit=50)
    message = await s_channel.send(embed=sample_embed)
    print(f'Connected has {bot.user} to discord !')
    print(f'Channels: #{s_channel.name} for status, #{l_channel.name} for logs')
    watching = discord.Activity(type=discord.ActivityType.watching, name='si les services sont up')
    await bot.change_presence(status=discord.Status.dnd, activity=watching)
    await start()


if __name__ == '__main__':
    print('Connecting to discord...')
    print(f'Token: {token}')
    print(f'Invite: {invite}')
    bot.run(token)
