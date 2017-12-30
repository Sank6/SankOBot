import discord, time, random, asyncio, smtplib, sys, os, requests, praw, sqlite3
from PyDictionary import PyDictionary
from datetime import datetime
from discord import ChannelType
from pyfiglet import figlet_format
from Levels import manage
from Levels import servers_s as servers
from backgrounds.Real import create_img
from googleapiclient.discovery import build

# ENDING:            ```\n\n`*` <-- Add `d` to the end of the command (word starting with `%`) to delete your message\n\nThe link to the help server has been Direct Messaged to you.\n\nMade By Guru Ankrad'


# \n %spam [x]        | Spams a random message [x] number of times
# ADMIN :    message.author.server_permissions.administrator




# TOKEN HERE!
my_token = os.environ.get('TOKEN')  # replace with your token
your_user_id = ""

google_developer_key = ""
google_cx = ""

reddit_client_id = ""
reddit_client_secret = ""
reddit_user_agent = ""


def image_search(query):
    service = build("customsearch", "v1",
                    developerKey=google_developer_key)

    res = service.cse().list(
        q=query,
        cx=google_cx,
        searchType='image',
        rights='cc_publicdomain cc_attribute cc_sharealike cc_noncommercial cc_nonderived',
    ).execute()

    urls = [item['link'] for item in res['items']]
    return urls


client = discord.Client()
dictionary = PyDictionary()
ai = 1
timespeed = 0


@client.event
async def on_message(message):
    try:
        global ai, timespeed, SpamNo, status_option
        # num_var_rand = 10
        # if message.author == client.user:
        #    return

        '''if not message.author.bot:
            try:
                change = manage.add_messages(message.author.id)
            except UnboundLocalError:
                manage.add_user((message.author.name + '#' + message.author.discriminator), message.author.id)
                change = manage.add_messages(message.author.id)
            except sqlite3.OperationalError:
                print("Message Adding Failed for " + message.author.name + " in the server " + message.server.name)
                change = False
            if change is False:
                pass
            else:
                try:
                    await client.send_message(message.channel, message.author.mention + ' is now level ' + str(change) + '!')
                except discord.errors.Forbidden:
                    pass'''

        if message.content.startswith('%credits') and not message.author.bot:
            if not manage.check_time_for_credits(message.author.id) is True:
                msg = message.author.mention + " You have already collected today's daily credits. Come back in " + str(
                    manage.time_till_credits(message.author.id)) + " for more. You have " + str(
                    manage.check_time_for_credits(
                        message.author.id)) + ' credits!  :credit_card: :money_with_wings: :money_with_wings: '
                await client.send_message(message.channel, msg)
                return
            credits = manage.add_credits(message.author.id, 100)
            await client.send_message(message.channel,
                                      message.author.mention + ' You recieved 100 Credits! You have ' + str(
                                          credits) + ' credits!  :credit_card: :money_with_wings: :money_with_wings: ')

        if message.content.startswith('%credits') and message.author.bot:
            await client.send_message(message.channel, 'Good try, but bots cannot collect credits!')

        if message.content.startswith('%daily') and not message.author.bot:
            if not manage.check_time_for_credits(message.author.id) is True:
                msg = message.author.mention + " You have already collected today's daily credits. Come back in " + str(
                    manage.time_till_credits(message.author.id)) + " for more. You have " + str(
                    manage.check_time_for_credits(
                        message.author.id)) + ' credits!  :credit_card: :money_with_wings: :money_with_wings: '
                await client.send_message(message.channel, msg)
                return
            credits = manage.add_credits(message.author.id, 100)
            await client.send_message(message.channel,
                                      message.author.mention + ' You recieved 100 Credits! You have ' + str(
                                          credits) + ' credits!  :credit_card: :money_with_wings: :money_with_wings: ')

        if message.content.startswith('%daily') and message.author.bot:
            await client.send_message(message.channel, 'Good try, but bots cannot collect credits!')

            # ping with "d"

        if message.content.startswith('%ping'):
            pingtime = time.time()
            pingms = await client.send_message(message.channel, "Pinging...")
            ping = time.time() - pingtime
            await client.edit_message(pingms, "Pong! `%.01f seconds`" % ping)
        if message.content.startswith('%pingd'):
            pingtime = time.time()
            pingms = await client.send_message(message.channel, "Pinging...")
            ping = time.time() - pingtime
            await client.edit_message(pingms, "Pong! `%.01f seconds`" % ping)
            await client.delete_message(message)


            # spam the channel, with d

        error = 0

        if message.content.startswith('%spamd'):
            await client.delete_message(message)
            #        spamms = await client.send_message(message.channel, "Loading...")
            try:
                value = message.content.split(" ")
                SpamNo = int(value[1])
            except:
                error = 1
                await client.send_message(message.channel,
                                          "Check your syntax. It should be like this:`%spam [number]`, where [number] is he amount of messages to send")
                #    await client.delete_message(spamms)

            # if admin and more than 100, continue
            if SpamNo >= 10 and error == 0 and message.author.server_permissions.administrator:
                while 1 <= SpamNo:
                    abArr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                             's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                    RandomString = abArr[random.randint(0, 25)]
                    for x in range(random.randint(7, 25)):
                        ltr = abArr[random.randint(0, 25)]
                        RandomString = RandomString + ltr
                    await client.send_message(message.channel, RandomString)
                    SpamNo = SpamNo - 1
                    time.sleep(timespeed)

                    # if less than 100 continue
            elif SpamNo <= 10 and error == 0:
                while 1 <= SpamNo:
                    abArr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                             's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                    RandomString = abArr[random.randint(0, 25)]
                    for x in range(random.randint(7, 25)):
                        ltr = abArr[random.randint(0, 25)]
                        RandomString = RandomString + ltr
                    await client.send_message(message.channel, RandomString)
                    SpamNo = SpamNo - 1
                    time.sleep(timespeed)

                    # if more than 100 and not admin, STOP
            elif not message.author.server_permissions.administrator and SpamNo >= 10 and error == 0:
                await client.send_message(message.channel, "Cannot send more than 100 messages if you are not admin!")






        elif message.content.startswith('%spam'):
            #        spamms = await client.send_message(message.channel, "Loading...")
            try:
                value = message.content.split(" ")
                SpamNo = int(value[1])
            except:
                error = 1
                await client.send_message(message.channel,
                                          "Check your syntax. It should be like this:`%spam [number]`, where [number] is he amount of messages to send")
                #    await client.delete_message(spamms)

            # if admin and more than 100, continue
            if SpamNo >= 10 and error == 0 and message.author.server_permissions.administrator:
                while 1 <= SpamNo:
                    abArr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                             's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                    RandomString = abArr[random.randint(0, 25)]
                    for x in range(random.randint(7, 25)):
                        ltr = abArr[random.randint(0, 25)]
                        RandomString = RandomString + ltr
                    await client.send_message(message.channel, RandomString)
                    SpamNo = SpamNo - 1
                    time.sleep(timespeed)

                    # if less than 100 continue
            elif SpamNo <= 10 and error == 0:
                while 1 <= SpamNo:
                    abArr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                             's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                    RandomString = abArr[random.randint(0, 25)]
                    for x in range(random.randint(7, 25)):
                        ltr = abArr[random.randint(0, 25)]
                        RandomString = RandomString + ltr
                    await client.send_message(message.channel, RandomString)
                    SpamNo = SpamNo - 1
                    time.sleep(timespeed)

                    # if more than 100 and not admin, STOP
            elif not message.author.server_permissions.administrator and SpamNo >= 10 and error == 0:
                await client.send_message(message.channel, "Cannot send more than 100 messages if you are not admin!")















                # ASCII ART
        if message.content.startswith('%ascii'):
            if len(message.mentions) >= 1:
                await client.send_message(message.channel, 'Cannot tag in ascii art.')
                return
            # init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
            parts = message.content.split(' ')
            text = str(parts[1:])
            text = text.replace(text[:2], '')
            text = text[:-2]
            text = text.replace("', '", ' ')
            font = 'big'
            ascii_text = figlet_format(text, font=font)
            await client.send_message(message.channel, '```' + ascii_text + '```')

        if message.content.startswith('%info'):
            await client.send_typing(message.channel)
            parts_of_msg = message.content.split(' ')
            if len(parts_of_msg) >= 2:
                list_of_mentions = message.mentions
                if len(list_of_mentions) >= 2:
                    await client.send_message(message.channel, 'Please tag only one person!')
                    return
                else:
                    if len(list_of_mentions) == 0:
                        info = message.author
                    else:
                        info = list_of_mentions[0]
            else:
                info = message.author

            if info.bot:
                await client.send_message(message.channel, 'You cannot get info about a bot.')
                return
            if str(info.game) != 'None':
                playing = str(info.game)
            else:
                playing = 'Nothing'
            level = str(manage.get_level(info.id))
            _credits = str(manage.get_credits(info.id))
            time_left = manage.time_till_credits(info.id)
            if time_left is True:
                _time = '0 minutes left! Collect Now!'
            else:
                _time = 'Collect more in ' + str(time_left)
            messages = str(manage.get_messages(info.id))
            status = str(info.status).capitalize()
            date = str(datetime.utcnow().strftime("Sent on %d/%m/%Y at %H:%M"))
            joined = str(info.joined_at.strftime("%d/%m/%Y at\n                  %H:%M"))
            manage.add_user(info.name + '#' + str(info.discriminator), info.id)
            choice = manage.get_choice(info.id)
            xp = manage.get_xp(info.id)
            total_xp = str(manage.get_total_xp(info.id))
            total_xp = total_xp.split('.')
            total_xp = total_xp[0]
            if info.avatar_url == '':
                url = info.default_avatar_url
            else:
                url = info.avatar_url
            em = discord.Embed(title=title, description=content, colour=0x1cffe2)
            if info.avatar_url == '':
                picture_of_user = info.default_avatar_url
            else:
                picture_of_user = info.avatar_url
            em.set_author(name=info, icon_url=picture_of_user)
            em.set_thumbnail(url=picture_of_user)
            server_details = '__Server: ' + str(info.server) + '__'
            content2 = 'Joined on: ' + str(info.joined_at.strftime("%d/%m/%Y at %H:%M"))
            em.add_field(name="__User's Bot Related Info__", value=content3)
            em.add_field(name=server_details, value=content2)
            date = str(datetime.utcnow().strftime("Sent on %d/%m/%Y at %H:%M"))
            em.set_footer(text=date, icon_url=client.user.avatar_url)
            await client.send_message(message.channel, embed=em)


        # AI mode NO "d"

        if message.content.startswith('%activate'):
            await client.send_message(message.channel, "Activated the AI replies")
            ai = 1
        if message.content.startswith('%deactivate'):
            await client.send_message(message.channel, "De-activated the AI replies")
            ai = 0
        if message.content.startswith('%aicheck'):
            if ai == 1:
                await client.send_message(message.channel, "AI is active!")
            elif ai == 0:
                await client.send_message(message.channel, "AI is NOT active!")
            else:
                await client.send_message(message.channel, "AI is confused!")




















                # random number with "d"

        if message.content.startswith('%randd '):
            try:
                vals = message.content.split(" ")
                NumberX = int(vals[1])
                NumberY = int(vals[2])
                msg = 'Your Random Number Is: __**' + str(random.randint(NumberX, NumberY)) + "**__!!!!"
                await client.send_message(message.channel, msg)
            except ValueError:
                await client.send_message(message.channel,
                                          "Make sure you entered 2 numbers (with a space in between) and the first number is smaller than the second.")
            await client.delete_message(message)

        elif message.content.startswith('%rand '):
            try:
                vals = message.content.split(" ")
                NumberX = int(vals[1])
                NumberY = int(vals[2])
                msg = 'Your Random Number Is: __**' + str(random.randint(NumberX, NumberY)) + "**__!!!!"
                await client.send_message(message.channel, msg)
            except ValueError:
                await client.send_message(message.channel,
                                          "Make sure you entered 2 numbers (with a space in between) and the first number is smaller than the second.")

        if message.content.startswith("%reply") and message.author.id == int(your_user_id):
            parts = message.content.split(" ")
            messg = str(parts[2:])
            b = {'[': '', ']': '', "'": '', ",": ''}
            for x, y in b.items():
                messg = messg.replace(x, y)
            message2 = "Thanks For Asking Frazer the question. Here is your answer: \n\n" + messg
            name = message.server.get_member(parts[1])
            replying = await client.send_message(message.channel, "Sending answer to " + str(name))
            await client.send_message(name, message2)
            await client.edit_message(replying, "Sent to " + str(name))



            # Say what you want. with "d"

        if message.content.startswith('%sayd'):
            txt = message.content
            word, space, rest = txt.partition(' ')
            await client.delete_message(message)
            await client.send_message(message.channel, rest)
        elif message.content.startswith('%say'):
            txt = message.content
            word, space, rest = txt.partition(' ')
            await client.send_message(message.channel, rest)

        # clear messages simple

        if message.content.startswith('%cleard'):
            await client.delete_message(message)
            try:
                vals = message.content.split(" ")
                clrnumber = int(vals[1])
                clrnumber = clrnumber + 1
                counter = 0
                async for x in client.logs_from(message.channel, limit=clrnumber):
                    if counter < clrnumber and x.pinned == False:
                        await client.delete_message(x)
                        counter += 1
                        await asyncio.sleep(timespeed)  # 1.2 second timer so the deleting process can be even

            except discord.DiscordException:
                await client.send_message(message.channel,
                                          "Discord Error!!! I may not have the right permissions.:frowning: ")

            except:
                if message.content.startswith('%clear all'):
                    aRandomVariable = 1
                else:
                    await client.send_message(message.channel,
                                              "Make Sure You Used the Right Syntax! ```%clear [number]```")


        elif message.content.startswith('%clear'):
            try:
                vals = message.content.split(" ")
                clrnumber = int(vals[1])
                clrnumber = clrnumber + 1
                counter = 0
                async for x in client.logs_from(message.channel, limit=clrnumber):
                    if counter < clrnumber and x.pinned == False:
                        await client.delete_message(x)
                        counter += 1
                        await asyncio.sleep(timespeed)  # 1.2 second timer so the deleting process can be even
            except discord.DiscordException:
                try:
                    await client.send_message(message.channel,
                                              "Discord Error!!! I may not have the right permissions.:frowning: ")
                except discord.Forbidden:
                    await  client.send_message(message.author,
                                               "Discord Error!!! I may not have the right permissions in the server (" + str(
                                                   message.server.name) + ") :frowning: ")
            except:
                if message.content.startswith('%clear all'):
                    aRandomVariable = 1
                else:
                    await client.send_message(message.channel,
                                              "Make Sure You Used the Right Syntax! ```%clear [number]```")



























                    # even the time

        if message.content.startswith('%timed'):
            await client.delete_message(message)
            try:
                value3 = message.content.split(" ")
                optionChoice = int(value3[1])
            except:
                await client.send_message(message.channel,
                                          "**Make Sure You Entered A Number After  `%time`**\nCheck Your syntax. It should be `%time 1` or `%time 0`")
            if optionChoice == 1:
                await client.send_message(message.channel, "Time mode is set to `Quick, with stops in between`")
                timespeed = 0
            elif optionChoice == 0:
                await client.send_message(message.channel, "Time mode is set to `Slow, but consistent`")
                timespeed = 1.2
            else:
                await client.send_message(message.channel, "Check Your syntax. It should be `%time 1` or `%time 0`")

        elif message.content.startswith('%time'):
            try:
                value3 = message.content.split(" ")
                optionChoice = int(value3[1])
            except:
                await client.send_message(message.channel,
                                          "**Make Sure You Entered A Number After  `%time`**\nCheck Your syntax. It should be `%time 1` or `%time 0`")
            if optionChoice == 1:
                await client.send_message(message.channel, "Time mode is set to `Quick, with stops in between`")
                timespeed = 0
            elif optionChoice == 0:
                await client.send_message(message.channel, "Time mode is set to `Slow, but consistent`")
                timespeed = 1.2
            else:
                await client.send_message(message.channel, "Check Your syntax. It should be `%time 1` or `%time 0`")




















                # clear all
        try:
            if message.author.server_permissions.administrator:
                pass
        except AttributeError:
            pass
            return
        if message.content.startswith('%clear all') & message.author.server_permissions.administrator:
            async for x in client.logs_from(message.channel,
                                            limit=99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999):
                if x.pinned == False:
                    await client.delete_message(x)
                    await asyncio.sleep(timespeed)  # 1.2 second timer so the deleting process can be even
        elif message.content.startswith('%clear all') and not message.author.server_permissions.administrator:
            await client.send_message(message.channel, "You need admin to clear all!")





















            # ENDLESS SPAM
        if message.content.startswith('%infinite-spam'):
            if message.author.server_permissions.administrator:
                await client.send_message(message.channel, "%infinite-spam")
            else:
                await client.send_message(message.channel, "Cannot spam endlessly if you are not admin!")

            '''

# ENDLESS SPAM
        if message.content.startswith('bleigh'):
            if message.author == client.user:
                return
            else:
                MsG = message.content.split(" ")
                try:
                    wNumber = int(MsG[1])
                    while wNumber > 0:
                       await client.send_message(message.channel, "bleigh")
                       wNumber = wNumber - 1
                except ValueError:
                    await client.send_message(message.channel, "Check syntax: ``` bleigh [x] ``` ^^^ [x] must be a number")
                except IndexError:
                    await client.send_message(message.channel, "Check syntax: ``` bleigh [x] ``` ^^^ [x] make sure you added the number [x]!")
'''

        if message.content.startswith('%stfu'):
            await client.delete_message(message)
            RnC = random.randint(1, 4)
            if RnC == 1:
                await client.send_message(message.channel,
                                          'http://i0.kym-cdn.com/photos/images/facebook/000/471/143/020.jpg')
            elif RnC == 2:
                await client.send_message(message.channel, 'https://www.youtube.com/watch?v=OLpeX4RRo28')
            elif RnC == 3:
                await client.send_message(message.channel, 'https://media.giphy.com/media/sveHxTt4ARcVG/source.gif')
            elif RnC == 4:
                await client.send_message(message.channel,
                                          'http://s2.quickmeme.com/img/cb/cbaba0d9392bd964ff9c4b5296cbe06312a8539f976d28cf66b48289d18adbec.jpg')

        if message.content.startswith('%status'):
            stm = message.content.split(" ")
            if stm[1] == '1':
                await client.send_message(message.channel, 'Successfully enabled status messages')
                status_option = True
            elif stm[1] == '0':
                status_option = True
                await client.send_message(message.channel, 'Successfully disabled status messages')
            else:
                status_option = True
                await client.send_message(message.channel, 'Check syntax: `%status [1/0]`...')









            # help
        HelpMsg1 = '```fix\n Command           : What It Does                                               \n-------------------:------------------------------------------------------------\n %ping *           : pong                                                       \n %help *           : Shows Help Page                                            \n %rand [x] [y] *   : Finds a random number between [x] and [y]                  \n %invite *         : Invite Link                                                \n %say *            : Control Me! Tell me what to say!                           \n %clear [number] * : clear [number] of messages from that channel!              \n %clear all        : Clears all messages in channel!                            \n %ask[question] *  : Asks Frazer a Question!                                    \n %spam [x] *       : Spams a random message [x] number of times                 \n %time [ 0 or 1 ]  : Changes time mode for `%spam` and `%clear`. (Fast or Even) \n %aicheck          : Checks if AI is activated                                  \n %activate         : Activates AI bot                                           \n %deactivate       : De-activates AI                                            \n %clear [x]        : Clears [x] messages from that channel                      \n %clear all        : Clears all messages in the channel                         \n %stop             : Restarts SankOBot                                          \n %reddit [x]       : Shows a reddit post (one of top 10) from the subreddit [x] \n %meme             : Shows a meme                                               \n %cmeme            : Shows a constantly changing meme                           \n %prequelmeme      : Shows a prequelmeme                                        \n %cprequelmeme     : Shows a constantly changing prequelmeme ```'

        HelpMsg3 = '''```fix
 Command             : What It Does                                    
---------------------:-------------------------------------------------
 %newgame            : Starts a new chessgame                          
 %endgame            : Resign the current game                         
 %move [x] [y]       : Move the piece at [x] to [y]                    
 %movelist           : Suggests a move to you, if it is your turn      
 %data               : Checks whether either player is in check        
 %ascii [x]          : Prints [x] in ASCII Art                         
 %info [tag someone] : Retrieves information about the user you tagged 
 %update             : Shows newly added and upcoming features    
 %pun                : Shows a pun
 %define [x]         : Defines the WORD (Not Phrase) [x]      
 %img [x]            : Searches for [x] in google images
 %email [x] [y]      : Emails [x], [y] number of times 

 %credits             : Collect daily credits
 %buy                : Shows a list of backgrounds to buy
 %buy [x]            : Buy background [x]
 %choose [x]         : Choose background [x] for yuor info page```'''

        HelpMsg2 = '\n\n`*` <-- Add `d` to the end of the command (word starting with `%`) to delete your message\n\nThe link to the help server has been Direct Messaged to you.\n\nAdd SankOBot Music now: https://discordapp.com/oauth2/authorize?client_id=370274598559678467&scope=bot&permissions=267471873\n\nMade By Guru Ankrad'
        if message.content.startswith('%helpd'):
            await client.send_message(message.channel, HelpMsg1)
            await client.send_message(message.channel, HelpMsg3)
            await client.send_message(message.channel, HelpMsg2)
            await client.delete_message(message)
        elif message.content.startswith('%help'):
            await client.send_message(message.channel, HelpMsg1)
            await client.send_message(message.channel, HelpMsg3)
            await client.send_message(message.channel, HelpMsg2)

        if client.user in message.mentions:
            if 'help' in message.content:
                await client.send_message(message.channel, HelpMsg1)
                await client.send_message(message.channel, HelpMsg3)
                await client.send_message(message.channel, HelpMsg2)
        if message.content.startswith('%reddit'):
            url_list = []
            await client.send_typing(message.channel)
            try:
                split_msg = message.content.split(' ')
            except:
                await client.send_message(message.channel, 'Unkown Error!')
            reddit = praw.Reddit(client_id=reddit_client_secret,
                                 client_secret=reddit_client_secret,
                                 redirect_uri='http://localhost:8080',
                                 user_agent=reddit_user_agent)
            try:
                for submission in reddit.subreddit(split_msg[1]).hot(limit=10):
                    url = submission.url
                    url_list.append(url)
                ran_num = random.randint(0, len(url_list))
                msg = url_list[ran_num]
                await client.send_message(message.channel, msg)

            except:
                await client.send_message(message.channel, 'Unkown Error!')

        if message.content.startswith('%meme'):
            url_list = []
            await client.send_typing(message.channel)
            reddit = praw.Reddit(client_id=reddit_client_secret,
                                 client_secret=reddit_client_secret,
                                 redirect_uri='http://localhost:8080',
                                 user_agent=reddit_user_agent)
            try:
                for submission in reddit.subreddit('dankmemes').hot(limit=100):
                    url = submission.url
                    url_list.append(url)

                ran_num = random.randint(0, len(url_list))
                await client.send_message(message.channel, msg)

            except:
                await client.send_message(message.channel, 'Unkown Error!')

        if message.content.startswith('%cmeme'):
            url_list = []
            await client.send_typing(message.channel)
            reddit = praw.Reddit(client_id=reddit_client_id,
                                 client_secret=reddit_client_secret,
                                 redirect_uri='http://localhost:8080',
                                 user_agent=reddit_user_agent)
            try:
                while True:
                    for submission in reddit.subreddit('dankmemes').hot(limit=10000):
                        url = submission.url
                        time.sleep(2)
                        await client.send_message(message.channel, url)

            except:
                try:
                    await client.send_message(message.channel, 'Unkown Error!')
                except:
                    pass

        if message.content.startswith('%prequelmeme'):
            url_list = []
            await client.send_typing(message.channel)
            reddit = praw.Reddit(client_id=reddit_client_id,
                                 client_secret=reddit_client_secret,
                                 redirect_uri='http://localhost:8080',
                                 user_agent=reddit_user_agent)
            try:
                for submission in reddit.subreddit('prequelmemes').hot(limit=100):
                    url = submission.url
                    url_list.append(url)
                ran_num = random.randint(0, len(url_list))
                msg = url_list[ran_num]
                await client.send_message(message.channel, msg)

            except:
                await client.send_message(message.channel, 'Unkown Error!')

        if message.content.startswith('%cprequelmeme'):
            url_list = []
            await client.send_typing(message.channel)
            reddit = praw.Reddit(client_id=reddit_client_id,
                                 client_secret=reddit_client_secret,
                                 redirect_uri='http://localhost:8080',
                                 user_agent=reddit_user_agent)
            try:
                while True:
                    for submission in reddit.subreddit('prequelmemes').hot(limit=10000):
                        url = submission.url
                        time.sleep(2)
                        await client.send_message(message.channel, url)
            except:
                await client.send_message(message.channel, 'Unkown Error!')

                # PUNS!!!!

        if message.content.startswith('%puns') or message.content.startswith('%pun'):
            try:
                puns = ["How do you throw a space party? You planet.",
                        "How was Rome split in two? With a pair of Ceasars.", "Nope. Unintended.",
                        "The shovel was a ground breaking invention, but everyone was blow away by the leaf blower.",
                        "A scarecrow says, 'This job isn't for everyone, but hay, it's in my jeans.''",
                        "A Buddhist walks up to a hot dog stand and says 'Make me one with everything.'",
                        "Did you hear about the guy who lost the left side of his body? He's alright now.",
                        "What do you call a girl with one leg that's shorter than the other? Ilene.",
                        "The broom swept the nation away.",
                        "I did a theatrical performance on puns. It was a play on words.",
                        "What does a clock do when it's hungry? It goes back for seconds.",
                        "What do you do with a dead chemist? You barium.",
                        "I bet the person who created the door knocker won a Nobel prize.",
                        "Towels can’t tell jokes. They have a dry sense of humor.",
                        "Two birds are sitting on a perch and one says “Do you smell fish?”",
                        "Did you hear about the cheese factory that exploded in france? There was nothing but des brie.",
                        "Do you know sign language? You should learn it, it’s pretty handy.",
                        "What do you call a beautiful pumpkin? GOURDgeous.",
                        "Why did one banana spy on the other? Because she was appealing.",
                        "What do you call a cow with no legs? Ground beef.",
                        "What do you call a cow with two legs? Lean beef.",
                        "What do you call a cow with all of its legs? High steaks.",
                        "A cross eyed teacher couldn’t control his pupils.",
                        "After the accident, the juggler didn’t have the balls to do it.",
                        "I used to be afraid of hurdles, but I got over it.",
                        "To write with a broken pencil is pointless.",
                        "I read a book on anti-gravity. I couldn’t put it down.",
                        "I couldn’t remember how to throw a boomerang but it came back to me.",
                        "What did the buffalo say to his son? Bison.",
                        "What should you do if you’re cold? Stand in the corner. It’s 90 degrees.",
                        "How does Moses make coffee? Hebrews it.",
                        "The energizer bunny went to jail. He was charged with battery.",
                        "What did the alien say to the pitcher of water? Take me to your liter.",
                        "What happens when you eat too many spaghettiOs? You have a vowel movement.",
                        "The soldier who survived mustard gas and pepper spray was a seasoned veteran.",
                        "Sausage puns are the wurst.", "What do you call a bear with no teeth? A gummy bear.",
                        "How did Darth Vader know what luke was getting him for his birthday? He could sense his presence.",
                        "Why shouldn’t you trust atoms? They make up everything.",
                        "What’s the difference between a bench, a fish, and a bucket of glue? You can’t tune a bench but you can tuna fish. I bet you got stuck on the bucket of glue part.",
                        "What’s it called when you have too many aliens? Extraterrestrials.",
                        "Want to hear a pizza joke? Nevermind, it’s too cheesy.",
                        "What do you call a fake noodle? An impasta.",
                        "What do cows tell each other at bedtime? Dairy tales.",
                        "Why can’t you take inventory in Afghanistan? Because of the tally ban.",
                        "Why didn’t the lion win the race? Because he was racing a cheetah.",
                        "Why did the man dig a hole in his neighbor’s backyard and fill it with water? Because he meant well.",
                        "What happens to nitrogen when the sun comes up? It becomes daytrogen.",
                        "What’s it called when you put a cow in an elevator? Raising the steaks.",
                        "What’s america’s favorite soda? Mini soda.",
                        "Why did the tomato turn red? Because it saw the salad dressing.",
                        "What kind of car does a sheep drive? A lamborghini, but if that breaks down they drive their SuBAHHru.",
                        "What do you call a spanish pig? Porque.",
                        "What do you call a line of rabbits marching backwards? A receding hairline.",
                        "Why don’t vampires go to barbecues? They don’t like steak.",
                        "A cabbage and celery walk into a bar and the cabbage gets served first because he was a head.",
                        "How do trees access the internet? They log on.",
                        "Why should you never trust a train? They have loco motives."]
                puns2 = ["Time flies like an arrow. Fruit flies like a banana.",
                         "Show me a piano falling down a mineshaft and I'll show you A-flat minor.",
                         "To write with a broken pencil is pointless.",
                         "A bicycle can't stand on its own because it is two-tired.",
                         "Those who get too big for their britches will be exposed in the end.",
                         "When a clock is hungry it goes back four seconds.",
                         "A chicken crossing the road is poultry in motion.",
                         "If you don't pay your exorcist you get repossessed.",
                         "What's the definition of a will? It's a dead giveaway.",
                         "The man who fell into an upholstery machine is fully recovered.",
                         "Every calendar's days are numbered.", "Bakers trade bread recipes on a knead to know basis.",
                         "When the electricity went off during a storm at a school the students were de-lighted.",
                         "I used to be a tap dancer until I fell in the sink.",
                         "He wears glasses during math because it improves division.",
                         "She was only a whisky maker but he loved her still.",
                         "She had a boyfriend with a wooden leg, but broke it off.",
                         "Those who jump off a Paris bridge are in Seine.",
                         "It wasn't school John disliked it was just the principal of it.",
                         "It's better to love a short girl than not a tall.",
                         "There was once a cross-eyed teacher who couldn't control his  pupils.",
                         "A grenade thrown into a kitchen in France would result in Linoleum Blownapart.",
                         "A boiled egg in the morning is hard to beat.",
                         "The one who invented the door knocker got a No-bell prize.",
                         "Old power plant workers never die they just de-generate.",
                         "There was a ghost at the hotel, so they called for an inn spectre.",
                         "With her marriage she got a new name and a dress.",
                         "The short fortune-teller who escaped from prison was a small medium at large",
                         "Some Spanish government employees are Seville servants.",
                         "He drove his expensive car into a tree and found out how the Mercedes bends.",
                         "Show me someone in denial and I'll show you a person in Egypt up to their ankles.",
                         "Two peanuts were walking in a tough neighborhood and one of them was a-salted.",
                         "When cannibals ate a missionary they got a taste of religion.",
                         "When an actress saw her first strands of gray hair she thought she'd dye.",
                         "He often broke into song because he couldn't find the key.",
                         "Marathon runners with bad footwear suffer the agony of defeat.",
                         "Driving on so many turnpikes was taking its toll.",
                         "To some - marriage is a word ... to others - a sentence.",
                         "Old lawyers never die they just lose their appeal.",
                         "In democracy its your vote that counts. In feudalism its your count that votes.",
                         "Atheism is a non-prophet organization",
                         "It was an emotional wedding. Even the cake was in tiers.",
                         "Old skiers never die -- they just go down hill.",
                         "A cardboard belt would be a waist of paper.",
                         "Local Area Network in Australia: the LAN down under.",
                         "When the TV repairman got married the reception was excellent.",
                         "An office with many people and few electrical outlets could be in for a power struggle.",
                         "How do you make antifreeze? Steal her blanket.",
                         "A small boy swallowed some coins and was taken to a hospital. When his grandmother telephoned to ask how he was a nurse said 'No change yet'.",
                         "A pediatrician is a doctor of little patients.", "Nylons give women a run for their money.",
                         "Talking to her about computer hardware I make my mother board.",
                         "Ancient orators tended to Babylon.",
                         "The best way to stop a charging bull is to take away his credit card.",
                         "If you give some managers an inch they think they're a ruler.",
                         "Two silk worms had a race. They ended up in a tie.",
                         "He had a photographic memory that was never developed.",
                         "Old burglars never die they just steal away.",
                         "A lawyer for a church did some cross-examining.",
                         "Chronic illegal parkers suffer from parking zones disease.",
                         "Some people don't like food going to waist..",
                         "A cannibal's favourite game is 'swallow the leader'.",
                         "You feel stuck with your debt if you can't budge it.",
                         "Girls who don't get asked out as often as their friends could feel out-dated.",
                         "We were so poor when I was growing up we couldn't even afford to pay attention. ",
                         "A pet store had a bird contest with no perches necessary.",
                         "A backwards poet writes inverse.",
                         "If a lawyer can be disbarred can a musician be denoted or a model deposed?",
                         "Once you've seen one shopping center you've seen a mall.",
                         "When the smog lifts in Los Angeles, U C L A.", "A plateau is a high form of flattery.",
                         "When chemists die, we barium.",
                         "A long knife has been invented that cuts four loaves of bread at a time called a four loaf cleaver.",
                         "When the wheel was invented, it caused a revolution.",
                         "Two robbers with clubs went golfing, but they didn't play the fairway.",
                         "Seven days without a pun makes one weak.",
                         "A circus lion won't eat clowns because they taste funny.",
                         "A toothless termite walked into a tavern and said, 'Is the bar tender here?'",
                         "Did you hear about the fire at the circus? The heat was intense.",
                         "A tattoo artist has designs on his clients.", "Santa's helpers are subordinate clauses.",
                         "A lot of money is tainted. It taint yours and it taint mine.",
                         "When they bought a water bed, the couple started to drift apart.",
                         "What you seize is what you get.", "Gardeners always know the ground rules.",
                         "Some people's noses and feet are build backwards: their feet smell and their noses run.",
                         "Two banks with different rates have a conflict of interest.",
                         "A successful diet is the triumph of mind over platter.",
                         "What do you call cheese that is not yours? Nacho Cheese.",
                         "When a new hive is done bees have a house swarming party.",
                         "Looting a drugstore is called Pillaging",
                         "Never lie to an x-ray technician. They can see right through you.",
                         "Old programmers never die, they just can't C as well.",
                         "A music store had a small sign which read: Bach in a Minuet.",
                         "Long fairy tales have a tendency to dragon.",
                         "Visitors to Cuba are usually Havana good time.",
                         "A bachelor is a guy who is footloose and fiancée-free.",
                         "A ditch digger was entrenched in his career.",
                         "A girl and her boyfriend went to a party as a barcode. They were an item.",
                         "A criminal's best asset is his lie ability."]
                puns3 = [
                    "A vulture boards a plane, carrying two dead possums. The attendant looks at him and says, 'I'm sorry, sir, only one carry on allowed per passenger.'",
                    "Santa’s helpers are known as subordinate Clauses.",
                    "She had a photographic memory but never developed it.",
                    "The two pianists had a good marriage. They always were in a chord.",
                    "I was struggling to figure out how lightning works then it struck me.",
                    "I really wanted a camouflage shirt, but I couldn't find one.",
                    "The grammarian was very logical. He had a lot of comma sense.",
                    "A chicken farmer's favorite car is a coupe.",
                    "What do you call a person rabid with wordplay? An energizer punny.",
                    "I've been to the dentist many times so I know the drill. ",
                    "What did one plant say to another? What's stomata?",
                    "The other day I held the door open for a clown. I thought it was a nice jester.",
                    "A chicken crossing the road is truly poultry in motion.",
                    "The politician is not one for Indian food. But he's good at currying favors.",
                    "How do construction workers party? They raise the roof.",
                    "A boiled egg every morning is hard to beat.",
                    "When a woman returns new clothing, that's post traumatic dress syndrome.",
                    "After hours of waiting for the bowling alley to open, we finally got the ball rolling.",
                    "Two antennas met on a roof, fell in love and got married. The ceremony wasn't much, but the reception was brilliant!",
                    "Always trust a glue salesman. They tend to stick to their word.",
                    "Where do you find giant snails? On the ends of giants’ fingers.",
                    "Guerrilla warfare is more than just throwing a banana.",
                    "The cartoon animator felt imprisoned by his job. He could not free himself from his cel.",
                    "I thought Santa was going to be late, but he arrived in the Nick of time.",
                    "With her marriage, she got a new name and a dress", "Every calendar's days are numbered.",
                    "A bicycle can't stand on its own because it is two-tired.",
                    "No matter how much you push the envelope, it will still be stationery.",
                    "A dog gave birth to puppies near the road and was cited for littering.",
                    "If you don't pay your exorcist, you will get repossessed.",
                    "Being struck by lightning is really a shocking experience!",
                    "A pessimist's blood type is always B-negative.", "Dockyard: A physician's garden.",
                    "I went to a seafood disco last week... and pulled a mussel.",
                    "Two peanuts walk into a bar, and one was a-salted.",
                    "Reading while sunbathing makes you well red.",
                    "The lights were too bright at the Chinese restaurant so the manager decided to dim sum."]
                ran_number = random.randint(1, 3)
                if ran_number == 1:
                    ran_number = random.randint(0, len(puns))
                    await client.send_message(message.channel, puns[ran_number] + '\n-1.' + str(ran_number))
                elif ran_number == 2:
                    ran_number = random.randint(0, len(puns2))
                    await client.send_message(message.channel, puns2[ran_number] + '\n-2.' + str(ran_number))
                elif ran_number == 3:
                    ran_number = random.randint(0, len(puns3))
                    await client.send_message(message.channel, puns3[ran_number] + '\n-3.' + str(ran_number))
                else:
                    await client.send_message(message.channel, 'Error')
            except:
                print('Failed punning...')

        if message.content.startswith('%define'):
            try:
                await client.send_typing(message.channel)
                split = message.content.split(' ')
                input_word = split[1]
                original_meaning = str(dictionary.meaning(input_word))

                final = original_meaning.replace('{', '')
                final = final.replace("'", '')
                final = final.replace("[", '')
                final = final.replace("], ", '\n\n')
                final = final.replace("; ", '\n    - ')
                final = final.replace("]}", '')
                final = final.replace(": ", ':\n    - ')
                final = final.replace(",", '\n        - ')
                final = final.replace("None", 'Error getting definition (Check spelling)')
                if final is None or final == '':
                    final = 'Error getting definition (Check spelling)'
                msg = str('```' + final + '```')

                await client.send_message(message.channel, msg)
            except IOError:
                await client.send_message(message.channel, 'Error...')

        if message.content.startswith('%img'):
            term = message.content.split(' ')
            img_urls = image_search(str(term[1:]))
            img_data = requests.get(img_urls[1]).content
            with open('image.jpg', 'wb') as handler:
                handler.write(img_data)
            em = discord.Embed(title='', description='', colour=0x00ff00)
            em.set_image(url=img_urls[1])
            await client.send_message(message.channel, embed=em)

        if message.content.startswith('%url'):
            search_term = message.content.split(' ')
            search_term = str(search_term[1:])
            img_url = 'http://www.robothumb.com/src/?url=' + search_term + '&size=800x600'

        if message.content.startswith('%buy'):
            await client.send_typing(message.channel)
            code = message.content.split(' ')
            if len(code) >= 2:
                code = int(code[1])
                if code > 5 or code < 1:
                    await client.send_message(message.channel,
                                              "There are only 5 backgrounds. In `%buy [x]`, [x] needs to be between 1 and 5.")
                    return
                bought = manage.bought_(message.author.id, code)
                if bought is True:
                    await client.send_message(message.channel, "You already own this item.")
                else:
                    result = manage.buy_background(message.author.id, code)
                    if result is False:
                        await client.send_message(message.channel, "You don't have enough credits.")
                    else:
                        await client.send_message(message.channel,
                                                  message.author.mention + " successfully bought the background!!")
            else:
                await client.send_message(message.channel,
                                          'Get the image code below and use `%buy [x]`, where [x] is the code to buy that background for your informatin profile.')
                await client.send_file(message.channel, 'all_2.jpg')

        if message.content.startswith('%choose'):
            await client.send_typing(message.channel)
            choice = message.content.split(' ')
            try:
                choice = int(choice[1])
            except IndexError:
                await client.send_message(message.channel, 'Specify which background to choose. `%choose [x]`')
                return
            if manage.bought_(user_id=message.author.id, choice=choice):
                result = manage.set_choice(user_id=message.author.id, choice=choice)
                if result is True:
                    await client.send_message(message.channel, 'Changed choice to ' + str(choice))
                else:
                    await client.send_message(message.channel, 'Error changing choice.')
            else:
                if choice > 5:
                    await client.send_message(message.channel,
                                              "There are only 5 backgrounds. In `%choose [x]`, [x] needs to be between 1 and 5.")
                else:
                    await client.send_message(message.channel,
                                              'You do not own this background. Buy it with `%buy ' + str(choice) + '`.')
    except discord.Forbidden:
        print('ERROR    Forbidden')
    except discord.NotFound:
        print('ERROR    NotFound')
    except sqlite3.OperationalError:
        print('ERROR    SqliteOperational')


@client.event
async def on_member_update(before, after):
    if not before.avatar == after.avatar:
        pass
    if not before.name == after.name:
        manage.update_user_name(after.id, str(str(after.name) + '#' + str(after.discriminator)))


@client.event
async def on_server_join(server):
    print("+1: " + server.name)
    channel_list = []
    for channel in server.channels:
        if channel.type is ChannelType.text:
            channel_list.append(server.get_channel(channel.id))
    ran_num = random.randint(0, (len(channel_list) - 1))
    try:
        inv_link = await client.create_invite(destination=channel_list[ran_num], max_age=0)
        text_to_send = inv_link.url
    except discord.Forbidden:
        ran_num = random.randint(0, (len(channel_list) - 1))
        try:
            inv_link = await client.create_invite(destination=channel_list[ran_num], max_age=0)
            text_to_send = inv_link.url
        except discord.Forbidden:
            text_to_send = 'Cannot create invite link (Forbidden)'
    servers.add_server(server.name, server.id, text_to_send, server.member_count)


@client.event
async def on_server_remove(server):
    print("-1: " + server.name)
    servers.removed_from_server(server.id)


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Use %help'))
    global ai, timespeed, status_option
    print('--------------------')
    print('Logged In!')
    print('Name: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('Number of Servers: ' + str(len(client.servers)))
    print([s.name for s in client.servers])
    bot_list = []
    human_list = []
    owner_list = []
    for server in client.servers:
        for member in server.members:
            if not member.bot:
                if member == server.owner:
                    owner_list.extend(member.name)
                elif not member == server.owner:
                    human_list.extend(member.name)
            elif member.bot:
                bot_list.extend(member.name)

    for server in client.servers:
        if len(server.members) > 500:
            print(str(server.name) + ' has ' + str(len(server.members)) + ' users!')
    humans = []
    bots = []
    admins = []
    for i in human_list:
        if i not in humans:
            humans.append(str(i))
    for i in owner_list:
        if i not in admins:
            admins.append(str(i))
    for i in bot_list:
        if i not in bots:
            bots.append(str(i))
    ai = 1
    timespeed = 0
    status_option = False
    print('--------------------')
    print('I can see: ' + str(len(humans)) + ' humans!')
    print('I can see: ' + str(len(admins)) + ' admins!')
    print('I can see: ' + str(len(bots)) + ' bots!')
    print('--------------------')

client.run(my_token)
