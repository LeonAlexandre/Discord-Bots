import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from tinder_interface import TinderBot, Person
from reddit_interface import RedditBot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

## CLASSES
class Vote_Poll:
    def __init__(self, userId, choice):
        self.userId = userId
        self.choice = choice

    def __repr__(self):
        return f'(choice {self.choice}; userId: {self.userId})'

class Poll_Tinder:
    def __init__(self,id):
        self.id = id
        #defaults to a left swipe so we dont run otu when testing
        self.vote_queue = [Vote_Poll(0, 'left')]
    
    def __repr__(self):
        return f'Poll Id: {self.id}'

    def count_votes(self):
        left_choice = 0
        right_choice = 0
        for vote in self.vote_queue:
            if vote.choice == 'left':
                left_choice += 1
            elif vote.choice == 'right':
                right_choice += 1
        return {'left': left_choice, 'right': right_choice}
    
    def clear_poll(self):
        self.vote_queue.clear()

class PollReddit():
    def __init__(self, post):
        self.post = post
        self.vote_queue = [Vote_Poll, 0]
    
    def __repr__(self):
        return f'Poll on post: {self.post.id}'

    def count_votes(self):
        down_choice = 0
        up_choice = 0
        for vote in self.vote_queue:
            if vote.choice == 'upvote':
                up_choice += 1
            elif vote.choice == 'downvote':
                down_choice += 1
        return {'upvote': up_choice, 'downvote': down_choice}
    
    def clear_poll(self):
        self.vote_queue.clear() 


## EVENTS
@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command(name='meme_review')
async def launch_reddit(ctx):
    global reddit_bot
    reddit_bot = RedditBot()

    await ctx.send('Meme Review')

@bot.command(name='next_meme')
async def create_poll_reddit(ctx):
    reddit_bot.get_post_new('meme')
    global current_meme
    current_meme = PollReddit(reddit_bot.current_post)

    response = current_meme.post.url

    await ctx.send(response)

@bot.command(name='upvote')
async def upvote_poll(ctx):
    user_of_poll = ctx.author
    user_vote = Vote_Poll( user_of_poll, 'upvote')
    print(user_vote)
    current_meme.vote_queue.append( user_vote )
    print(current_meme.vote_queue)
    print(f'Vote submitted: { user_vote }')

@bot.command(name='downvote')
async def downvote_poll(ctx):
    user_of_poll = ctx.author
    user_vote = Vote_Poll( user_of_poll, 'downvote')
    current_meme.vote_queue.append( user_vote )
    print(f'Vote submitted: { user_vote }')

@bot.command(name='meme_rate')
async def end_poll_reddit(ctx):
    votes = current_meme.count_votes()
    result = f'Upvotes: { votes["upvote"] } | { votes["downvote"] } : Downvotes'
    response = result
    # if votes["upvote"] > votes["downvote"]:
    #     reddit_bot.send_upvote
    #     print(f'Upvote on post {current_meme.post.id}')
    #     response = 'Upvote!\n' + result
    # else:
    #     reddit_bot.send_downvote
    #     response = 'Downvote!\n' + result
    
    await ctx.send(response)


@bot.command(name='tinder')
async def tinder_create(ctx):
    global tinder_bot
    tinder_bot = TinderBot()
    tinder_bot.login()
    await ctx.send('Tinder is launched!')

@bot.command(name='create_poll_tinder')
async def create_poll(ctx):
    poll_id = random.choice(range(100)) #placeholder till i have IDS and figure out the DB format
    global current_poll 
    current_poll = Poll_Tinder(poll_id)
    print(current_poll)
    print(tinder_bot)
    tinder_bot.new_person()
    res = printInfo(tinder_bot)
    response_create_poll = res
    

    await ctx.send(response_create_poll)

@bot.command(name='end_poll_tinder')
async def end_poll(ctx):
    votes = current_poll.count_votes()
    print(tinder_bot)
    result = f'Right: { votes["right"] } | { votes["left"] } : Left'
    response = result
    tinder_bot.swipe_left()
    # if votes["right"] > votes["left"]:
    #     tinder_bot.swipe_right()
    #     response = 'Swiping Right!\n' + result
    # else:
    #     tinder_bot.swipe_left()
    #     response = 'Swiping Left\n' + result
    
    await ctx.send(response)

@bot.command(name='vote_tinder', help='type "!vote left" or "!vote right" ')
async def vote_poll(ctx, choice: str):
    user_of_poll = ctx.author
    user_vote = Vote_Poll( user_of_poll, choice)
    current_poll.vote_queue.append( user_vote )
    print(f'Vote submitted: { user_vote }')

@bot.command(name='alex', help='Responds with a classic Alex quote')
async def alex_talk(ctx):
    alex_quotes = [
        'PRESS DOWN B',
        'It\'s life',
        'I haven\'t had an erection in three years'
        'Would you rape a pigeon for $5 and a McChicken?'
    ]
    user_to_reply = ctx.author


    response = f'Here you go {user_to_reply}: \n { random.choice(alex_quotes) }'
    #response =  random.choice(alex_quotes)
    await ctx.send(response)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

def printInfo(bot):
    name = bot.current_person.name
    age = bot.current_person.age
    bio = bot.current_person.bio

    response = f'New Poll Created:\nName: {name} \nAge: {age}\nBio: {bio}'
    return(response)


bot.run(TOKEN)