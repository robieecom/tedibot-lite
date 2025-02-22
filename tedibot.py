import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# to generate a token visit https://discord.com/developers/applications/
DISCORD_TOKEN='TOKEN'
GUILD = 000000000000000

# message for controlling user roles
MESSAGE_ID = 000000000000000

# mapping from emoji to role
# (emoji, role id)
EMOJI_ROLE_MAPPING = {
    '🤙': 000000000000000,
    'custom_role_name': 000000000000000,
    'custom_role_name_1': 000000000000000,
    'custom_role_name_2': 000000000000000
}

# when the bot is ready. Can be used for initialization
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# when a message is sent to the bot or guild channel
@client.event
async def on_message(message : discord.Message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.TextChannel) and message.author != client.user:
        print(f'{message.channel} - {message.author}: {message.content}')
        if message.attachments:
            for attachment in message.attachments:
                print(attachment)

# when someone joins or leaves a voice channel
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        print(f'{member} joined {after.channel}')
    if before.channel is not None and after.channel is None:
        print(f'{member} left {before.channel}')

# when a reaction is added to a specific message
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    emoji = EMOJI_ROLE_MAPPING.get(payload.emoji.name, None)
    guid:discord.Guild = client.get_guild(GUILD)
    member = await guid.fetch_member(payload.user_id)
    role = guid.get_role(emoji)
    if emoji and role and payload.message_id == MESSAGE_ID:
        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    emoji = EMOJI_ROLE_MAPPING.get(payload.emoji.name, None)
    guid:discord.Guild = client.get_guild(GUILD)
    member = await guid.fetch_member(payload.user_id)
    role = guid.get_role(emoji)
    if emoji and role and payload.message_id == MESSAGE_ID:
        await member.remove_roles(role)

# runs the bot
client.run(DISCORD_TOKEN)