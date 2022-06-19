import datetime
import json
import random
import conf as cf
import discord
from discord.ext import commands, tasks
import requests
import pythonping
import urllib3

bot = commands.Bot(command_prefix=".", description="Lambda.")

urllib3.disable_warnings()
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
to_check = json.loads(open('to_check.json').read())['data']
timeout = 120


def ping(url):
    try:
        if url.startswith('host://'):
            url = url.replace('host://', '')
            response = pythonping.ping(url, count=1)
            return response.success()
        else:
            response = requests.get(url, verify=False)
            if response.ok or response.status_code in [404]:
                return True
            return False
    except:
        return False


@tasks.loop(seconds=timeout)
async def check_status():
    print('Checking status')
    embed = discord.Embed(title='Status checking', description='checking status of services...', color=discord.Color.light_grey())
    new_message = await s_channel.send(embed=embed)
    embed = discord.Embed(title='Status Bot:', description='Status of all services:')
    is_a_down = False
    for service in to_check:
        response = ping(service['url'])
        emoji = '🟢'
        if not response:
            emoji = '🔴'
            if service['notify']:
                is_a_down = True
                service['url'] = service['url'].replace('host://', 'http://')
                if not '.' in service['url']:
                    service['url'] = 'http://example.com'
                user_embed = discord.Embed(title='Oups...', description=f"It\'s seems like {service['url']} is down ! ({service['nom']} is down !)", color=discord.Color.dark_red())
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


async def start():
   check_status.start()


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
