# Copyright 2020 called2voyage
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

pronouns = [
    'she/her',
    'he/him',
    'they/them',
    'ze/hir',
    'ze/zir',
    'xey/xem/xyr',
    'ae/aer',
    'e/em/eir',
    'ey/em/eir',
    'fae/faer',
    'fey/fem/feir'
    'hu/hum/hus',
    'it/it/its',
    'jee/jem/jeir',
    'kit/kit/kits',
    'ne/nem/nir',
    'peh/pehm/peh\'s',
    'per/per',
    'sie/hir',
    'se/sim/ser',
    'shi/hir',
    'si/hyr',
    'thon/thon/thons',
    've/ver/vis',
    've/vem/vir',
    'vi/ver',
    'vi/vim/vir',
    'vi/vim/vim',
    'xie/xer',
    'xe/xem/xyr',
    'xey/xem/xeir',
    'yo/yo/yos',
    'ze/zem/zes',
    'ze/mer/zer',
    'zee/zed/zeta',
    'zie/zir',
    'zie/zem/zes',
    'zie/hir',
    'zme/zmyr'
]

def is_pronoun(str):
    for pronoun in pronouns:
        if str.startswith(pronoun):
            return True
    return False

@client.event
async def on_message(message):
    if message.content.startswith('!mypronoun is '):
        pronoun = message.content.split('!mypronoun is ')[1]
        present = False
        for p in pronouns:
            if p.startswith(pronoun):
                pronoun = p
                present = True
        name = message.author.name
        if message.author.nick is not None and message.author.nick != message.author.name:
            nick = message.author.nick
            first = True
            for s in nick.split('(')[1:]:
                if first:
                    nick = nick.split('(')[0]
                    first = False
                if not is_pronoun(s):
                    nick = nick + '(' + s
            name = nick
        if present:
            await message.author.edit(nick=name + ' (' + pronoun + ')')
    if message.content.startswith('!mypronoun help'):
        await message.channel.send('To set your pronouns, just message "!mypronoun is *pronoun*" to any channel the bot has access to. For example, "!mypronoun is she/her". You can also change your pronouns at any time with the same command.')

@client.event
async def on_connect():
    await client.change_presence(activity=discord.Game(name="!mypronoun is it/it/its"))

client.run(TOKEN)
