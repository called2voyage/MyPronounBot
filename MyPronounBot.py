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

# pronouns = [
#     'she/her',
#     'he/him',
#     'they/them',
#     'ze/hir',
#     'ze/zir',
#     'xey/xem/xyr',
#     'ae/aer',
#     'e/em/eir',
#     'ey/em/eir',
#     'fae/faer',
#     'fey/fem/feir'
#     'hu/hum/hus',
#     'it/it/its',
#     'jee/jem/jeir',
#     'kit/kit/kits',
#     'ne/nem/nir',
#     'peh/pehm/peh\'s',
#     'per/per',
#     'sie/hir',
#     'se/sim/ser',
#     'shi/hir',
#     'si/hyr',
#     'thon/thon/thons',
#     've/ver/vis',
# ve/vem
# vi/ver
# vi/vim/vir
# vi/vim/vim
# xie
# xe
# xey/xem/xeir
# yo
# ze/zem
# ze/mer
# zee
# zie/zir
# zie/zem
# zie/hir
# zme
# ]

@client.event
async def on_message(message):
    if message.content.startswith('!mypronoun is '):
        pronoun = message.content.split('!mypronoun is ')[1]
        name = message.author.name
        if message.author.nick is not None:
            name = message.author.nick
        await message.author.edit(nick=name + ' ' + pronoun)

client.run(TOKEN)
