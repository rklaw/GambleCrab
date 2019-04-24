# The betting and payout logic has to be changed to fit the game more accurately.
# It will be changed soon.
import discord
import random
import constants
import time

inGame = []
userArr = []

class MyClient(discord.Client):


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):

        # So the bot doesnt reply to itself
        if message.author.id == self.user.id:
            return

        #Splitting the user message into a list so we can see the different commands
        msgArr = message.content.split(" ")

        if message.content.startswith('!gc'):

            #Display all animals that you can pick for your dice rolls
            if msgArr[1] == "choices":
                await message.channel.send(constants.ANIMAL_STR)

            #Starts a new game and randomly picks 3 different dice roll results and sends results to the chat
            #Then displays what everybody won
            if msgArr[1] == "play":
                temp = random.randint(0, 5)
                temp2 = random.randint(0, 5)
                temp3 = random.randint(0, 5)

                rollArr = [str(constants.ANIMAL_ARR[temp]), str(constants.ANIMAL_ARR[temp2]), str(constants.ANIMAL_ARR[temp3])]
                
                # Countdown loop
                t = 3
                while t > 0:
                    await message.channel.send(str(t))
                    time.sleep(.5)
                    t -= 1


                await message.channel.send(rollArr[0] + "  " + rollArr[1] + "  " + rollArr[2])

                #Checks to see if the values each player picked are in the array containing the rolled values
                #And if they are it removes one instance from the array
                for x in inGame:
                    count = 0
                    if x[2] in rollArr:
                        rollArr.remove(x[2])
                        count = count + 1
                    if x[3] in rollArr:
                        rollArr.remove(x[3])
                        count = count + 1
                    if x[4] in rollArr:
                        rollArr.remove(x[4])
                        count = count + 1
                    x[1] = x[1] + (x[5] * count - 100)
                    if count == 0:
                        await message.channel.send(str(x[0]) + " lost " + str(x[5]))
                    else:
                        await message.channel.send(str(x[0]) + " won " + str(x[5] * count))


            #Displays a list of possible commands and what they do
            if msgArr[1] == "commands":
                await message.channel.send("play : !gc play\n" + "choices : !gc choices\n" + "about : !gc about\n" + "join : !gc join\n" + "pick : !gc pick 'X' 'Y' 'Z'")

            #Adds the discord user to the game to be able to have access to the other commands
            if msgArr[1] == "join":
                if message.author in userArr:
                    await message.channel.send("You are already in the game!")
                else:
                    inGame.append([message.author, 1000, ":question: ", ":question: ", ":question: ", 0])
                    userArr.append(message.author)
                    await message.channel.send("You are entered into the game")

            #Displays the the current balance of the user
            if msgArr[1] == "balance":
                if any(message.author in sublist for sublist in inGame):
                    for x in inGame:
                        if x[0] == message.author:
                            await message.channel.send(x[1])                   
                else:
                    await message.channel.send("You aren't in the game yet. do '!gc join' to join the game")

            #Adds 1000 more to the balance of the user
            if msgArr[1] == "buy":
                if any(message.author in sublist for sublist in inGame):
                    for x in inGame:
                        if x[0] == message.author:
                            x[1] = x[1] + 1000
                            await message.channel.send(x[1])                   
                else:
                    await message.channel.send("You aren't in the game yet. do '!gc join' to join the game")

            #This sets the dice prediction for the player. The command starts with pick followed by their choices
            #For example !gc pick snake shrimp crab
            if msgArr[1] == "pick":
                if any(message.author in sublist for sublist in inGame):
                    for x in inGame:
                        if x[0] == message.author:
                            x[2] = str(":" + msgArr[2] + ":")
                            x[3] = str(":" + msgArr[3] + ":")
                            x[4] = str(":" + msgArr[4] + ":")
                            await message.channel.send("Good luck!!")
                else:
                    await message.channel.send("You aren't in the game yet. do '!gc join' to join the game")

            #Sets the users bet amount. This value stays until changed by the user.
            if msgArr[1] == "bet":
                tempBet = float(msgArr[2])
                if tempBet >= 0:
                    if any(message.author in sublist for sublist in inGame):
                        for x in inGame:
                            if x[0] == message.author:
                                    if x[1] - tempBet >= 0:
                                        x[1] += x[5]
                                        x[5] = tempBet
                                        x[1] = x[1] - tempBet
                                        await message.channel.send("You changed your bet to " + msgArr[2] + ", good luck!!")
                                    else:
                                        await message.channel.send("You only have " + str(x[1]) + " in your balance :cry:")
                    else:
                        await message.channel.send("You aren't in the game yet. do '!gc join' to join the game")
                else:
                    await message.channel.send("Don't be Brandon. Make a real bet!")

            #Displays all the infor of a user including name, balance, picks, bet amount
            if msgArr[1] == "myinfo":
                if any(message.author in sublist for sublist in inGame):
                    for x in inGame:
                        if x[0] == message.author:
                           await message.channel.send("Your balance is: " + str(x[1]) + "\nYour first pick is: " + str(x[2]) + "\nYour second pick is: " + str(x[3]) + "\nYour third pick is: " + str(x[4]) + "\nYour current bet is: " + str(x[5]) )
                else:
                    await message.channel.send("You aren't in the game yet. do '!gc join' to join the game")

            if msgArr[1] == "about":
                await message.channel.send("This game is inspired by a Vietnamese gambling game called Bầu Cua Tôm Cá. It rolls three 'dice' and displays the outcome of each dice.")


            



client = MyClient()
client.run('PUT YOUR BOTS TOKEN HERE')
