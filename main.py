from telethon import TelegramClient, events
import requests
import pyshorteners
import re



# create a TelegramClient object with your API ID, hash, and phone number
client = TelegramClient('send_message_bot', api_id, api_hash)
client.connect()

# log in to your account with the phone number and code
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Enter the code: '))

# create a PyShorteners object for URL shortening
s = pyshorteners.Shortener()
#(chats=source_group_ids)

# define a function to handle incoming messages in the source group
@client.on(events.NewMessage(chats=source_group_ids))
async def handle_message(event):
    try: 
        # check if the source chat ID matches the expected 
        #print(event.chat.title)
        
        if event.chat.title.lower() in event.message.message.lower():
            return
        # get the incoming message text
        message_text = event.message.message
        # find all URLs in the message text
         # find all URLs in the message text
        urls = re.findall(r'(https?://\S+)', message_text)
        
        # loop through each URL and process it
        shortened_urls = []
        for url in urls:
            # decode the URL
            decoded_url = requests.get(url).url
            
            # check if the URL is from Amazon.in
            if 'amazon.in' in decoded_url:
                # extract the existing affiliate tag from the URL
                start_index = decoded_url.find('tag=') + len('tag=')
                end_index = decoded_url.find('&', start_index)
                if end_index == -1:
                    end_index = len(decoded_url)
                existing_affiliate_tag = decoded_url[start_index:end_index]
                
                # replace the existing affiliate tag with the new one
                new_url = decoded_url.replace(existing_affiliate_tag, affiliate_tag)
                short_url = s.tinyurl.short(new_url)
                
            else:
                short_url = s.tinyurl.short(decoded_url)
                

            shortened_urls.append(short_url)

        for i in range(len(urls)):
            message_text = message_text.replace(urls[i], shortened_urls[i]) # send the modified message to the destination group
       
        for destination_group_id in destination_group_ids:
            message = await client.send_message(destination_group_id, message_text)
           # pin the message in the destination group
            await client.pin_message(destination_group_id, message.id) 
            

    except Exception as e:
        print(f"Exception occurred: {e}")

# start the client
client.start()

# run the client until you stop it manually
client.run_until_disconnected()
