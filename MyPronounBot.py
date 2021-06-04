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

from discord import Game, Embed, Intents
from discord.ext import commands
from reactionmenu import ReactionMenu
from dotenv import load_dotenv

intents = Intents(messages=True, reactions=True, guilds=True, members=True)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!mypronoun ', intents=intents)

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
    'zme/zmyr',
    'any'
]

def is_pronoun(str):
    for pronoun in pronouns:
        if pronoun.startswith(str):
            return True
    return False

@bot.command(name='is', help='Sets your pronouns')
async def mypronoun_is(ctx, *args):
    name = ctx.message.author.name + ' '
    user_pronouns = []
    for pronoun in args:
        added = False
        for p in pronouns:
            if p.startswith(pronoun):
                if not added:
                    user_pronouns.append(p)
                    added = True
    if ctx.message.author.nick is not None and ctx.message.author.nick != ctx.message.author.name:
        nick = ctx.message.author.nick
        possible_pronouns = nick.split('(')[1:]
        nick = nick.split('(')[0]
        add_space = False
        for s in possible_pronouns:
            if not is_pronoun(s[:-1]) and not is_pronoun(s[:-1].split(',')[0]):
                nick = nick + '(' + s
                add_space = True
        name = nick
        if add_space:
            name = name + ' '
    if len(user_pronouns) == 1:
        await ctx.message.author.edit(nick=name + '(' + user_pronouns[0] + ')')
    elif len(user_pronouns) > 1:
        pronoun_string = '('
        first = True
        for pronoun in user_pronouns:
            if first:
                pronoun_string = pronoun_string + pronoun.split('/')[0]
                first = False
            else:
                pronoun_string = pronoun_string + ', ' + pronoun.split('/')[0]
        pronoun_string = pronoun_string + ')'
        await ctx.message.author.edit(nick=name + pronoun_string)

bot.remove_command('help')
@bot.command(name='help', help='Displays the help message')
async def help(ctx):
    help_message = """To set your pronouns, just message `!mypronoun is [pronoun]` to any channel the bot has access to. For example, `!mypronoun is she/her`.

You can also change your pronouns at any time with the same command.

If you'd like to include multiple pronouns, you can by separating them with spaces, like this `!mypronoun is she they`. The pronouns will be displayed shortened with commas: `[nickname] (she, they)`.

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
