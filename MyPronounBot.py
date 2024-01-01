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
from reactionmenu import ReactionMenu, ReactionButton
from dotenv import load_dotenv

intents = Intents(messages=True, message_content=True, reactions=True, guilds=True, members=True)

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
    'mey/mer',
    'any'
]

def is_pronoun(str):
    for pronoun in pronouns:
        if pronoun.startswith(str.casefold()):
            return True
    return False

@bot.command(name='is', help='Sets your pronouns')
async def mypronoun_is(ctx, *args):
    name = ctx.message.author.name + ' '
    user_pronouns = []
    for pronoun in args:
        added = False
        for p in pronouns:
            if p.startswith(pronoun.casefold()):
                if not added:
                    user_pronouns.append(p)
                    added = True
    if ctx.message.author.nick is not None and ctx.message.author.nick != ctx.message.author.name:
        nick = ctx.message.author.nick
        possible_pronouns = nick.split('(')[1:]
        nick = nick.split('(')[0]
        for s in possible_pronouns:
            if not is_pronoun(s[:-1]) and not is_pronoun(s[:-1].split(',')[0]):
                nick = nick + '(' + s
            else:
                nick = nick.rstrip()
        name = nick + ' '
    if len(user_pronouns) == 1:
        nick_arg = name + '(' + user_pronouns[0] + ')'
        if ctx.message.author == ctx.message.guild.owner:
            await ctx.send('`/nick ' + nick_arg + '`')
        else:
            await ctx.message.author.edit(nick=nick_arg)
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
        nick_arg = name + pronoun_string
        if ctx.message.author == ctx.message.guild.owner:
            await ctx.send('`/nick ' + nick_arg + '`')
        else:
            await ctx.message.author.edit(nick=nick_arg)

@bot.command(name='howto', help='Explains how to use pronouns')
async def howto(ctx, pronoun):
    for p in pronouns:
        if p.startswith(pronoun.casefold()) and pronoun.casefold() != 'any':
            subject = p.split('/')[0]
            object = p.split('/')[1]
            possessive = ''
            if p.split('/')[0] == 'he':
                possessive = 'his'
            elif p.split('/')[0] == 'they':
                possessive = 'their'
            else:
                if len(p.split('/')) < 3:
                    possessive = p.split('/')[1]
                else:
                    possessive = p.split('/')[2]
            await ctx.send(subject.capitalize() + ' ran to the house. I ran to the house with ' + object + '. ' + subject.capitalize() + ' brought ' + possessive + ' book.')
        elif p.startswith(pronoun.casefold()) and pronoun.casefold() == 'any':
            await ctx.send('This person doesn\'t mind which pronouns you use for them. Take a look at our list with `!mypronoun list` if you want a few examples to try!')

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
    menu = ReactionMenu(ctx, menu_type=ReactionMenu.TypeEmbed)
    menu.add_button(ReactionButton.back())
    menu.add_button(ReactionButton.next())
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
