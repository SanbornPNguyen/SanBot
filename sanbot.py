import discord, time

def calc_time(measurement, units):
    if units == "seconds" or units == "second":
        return measurement
    elif units == "minutes" or units == "minute":
        return measurement * 60
    elif units == "hours" or units == "hour":
        return measurement * 60 * 60

token = open("token.txt" , "r")
token = token.readlines()[0]

admins = open("admin.txt", "r")
admins = admins.readlines()
admins = [int(admin.strip("\n")) for admin in admins]

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

censored_individuals = dict()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id in admins:
        if "!censor" in message.content:
            censor_id = message.mentions[0].id # User ID of the person who is to be censored
            censor_time = int(message.content.split()[2]) # Time (minutes) user is to be censored
            censor_units = message.content.split()[3] # Units of time the user is to be censored
            calculated_censor_time = calc_time(censor_time, censor_units) + time.time() # Time when user is allowed to speak freely again

            censored_individuals[censor_id] = calculated_censor_time

            await message.channel.send("User {} has been censored for {} {}.".format(message.mentions[0], censor_time, censor_units))

        elif "!uncensor" in message.content:
            uncensored_user = message.mentions[0].id
            if uncensored_user in censored_individuals.keys():
                censored_individuals.pop(uncensored_user)
                await message.channel.send("User {} has been uncensored.".format(message.mentions[0]))

    if message.author.id in censored_individuals.keys():
        if time.time() <= censored_individuals[message.author.id]:
            await message.delete()
        else:
            censored_individuals.pop(message.author.id)

client.run(token)
