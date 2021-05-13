# Copyright 2020-2021 called2voyage
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

from discord import Game, Embed
from discord.ext import commands
from reactionmenu import ReactionMenu
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!mypronoun ')

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
    'fae/flux/faer',
    'fey/fem/feir',
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

@bot.command(name='is', help='Sets your pronouns')
async def mypronoun_is(ctx, pronoun):
    present = False
    for p in pronouns:
        if p.startswith(pronoun):
            pronoun = p
            present = True
    name = ctx.message.author.name + ' '
    if ctx.message.author.nick is not None and ctx.message.author.nick != ctx.message.author.name:
        nick = ctx.message.author.nick
        first = True
        for s in nick.split('(')[1:]:
            if first:
                nick = nick.split('(')[0]
                first = False
            if not is_pronoun(s):
                nick = nick + '(' + s
        name = nick
    if present:
        await ctx.message.author.edit(nick=name + '(' + pronoun + ')')

bot.remove_command('help')
@bot.command(name='help', help='Displays the help message')
async def help(ctx):
    help_message = """To set your pronouns, just message `!mypronoun is [pronoun]` to any channel the bot has access to. For example, `!mypronoun is she/her`.

You can also change your pronouns at any time with the same command.

If you have any trouble, visit the MyPronounBot Discord server: https://discord.gg/GEKq4Ut"""
    await ctx.send(help_message)

@bot.command(name='list', help='Lists recognized pronouns')
async def list(ctx):
    menu = ReactionMenu(ctx, back_button='◀️', next_button='▶️', config=ReactionMenu.STATIC)
    pronoun_details = []
    count = 1
    chunk = ''
    for pronoun in pronouns:
        chunk = chunk + pronoun + '\n'
        if count % 10 == 0 or count == len(pronouns):
            embed = Embed(title='Recognized Pronouns')
            page_number = count // 10
            if count % 10 != 0:
                page_number = page_number + 1
            embed.add_field(name='Page ' + str(page_number), value=chunk)
            pronoun_details.append(embed)
            chunk = ''
        count = count + 1
    for pronoun_embed in pronoun_details:
        menu.add_page(pronoun_embed)
    await menu.start()

@bot.event
async def on_connect():
    await bot.change_presence(activity=Game(name="!mypronoun is it/it/its"))

bot.run(TOKEN)
