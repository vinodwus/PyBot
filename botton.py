
from telethon import TelegramClient, events


api_id = 27989413
api_hash = 'bf7f2540d24231e3b8e4854683d6bb9a'
destination_group_ids = -1001349913249
client = TelegramClient('session', api_id, api_hash)
client.connect()

@client.on(events.NewMessage())
async def handle_message(event):
    print(event.message.message)

# start the client
client.start()

# send a sample message to yourself
client.send_message('me', 'Hello, world!')

# run the client until you stop it manually

