import discord
import asyncio
from discord.utils import get
import time
from colorama import Fore

# create client object.
client = discord.Client()


# Main decorator for search user and give parameters to wraper function
def find_member(func):
	async def wrap(*args, **kwargs):
		print(client.user)
		user_id = args[0]
		server_name = args[1]
		servers = client.guilds
		target = []

		for server in servers:
			if server.name == server_name:
				target.append(server)
				afk_room = server.afk_channel

				for voice in server.voice_channels:
					for member in voice.members:
						if member.id == user_id:
							target.append(member)
							break

		return await func(*args, target[0], target[1])
	return wrap


# When client.run() ready to use this function called.
@client.event
async def on_ready():
	print("""
					Hi And welcome to MoveBot
		To start input user id and choose move mode. Try)))
			""".center(25))

	user_id = int(input("Target user id: "))
	server_name = str(input("Server name: "))

	print("""
			1. Always move to afk.
			2. Carousel(Move to each room fast).
			""")
	action = int(input("Choose action id (For example: 1) : "))

	if action == 1:
		await afk_always(user_id, server_name)
	elif action == 2:
		await carousel(user_id, server_name)
	else:
		print(Fore.RED + "Bad choose! Try again.")
		await on_ready()


# Function can always move user to afk but you need Permissions.move_members.
@find_member
async def afk_always(user_id, server_name):
	servers = client.guilds
	target_member = None

	for server in servers:
		if server.name == server_name:
			afk_room = server.afk_channel

			for voice in server.voice_channels:
				for member in voice.members:
					if member.id == user_id:
						target_member = member
						break
					else:
						print(f"{member.name} - not found. Do you wanna try again? Y/N")
						return await try_again()

		else:
			print(f"{server_name} - not found. Do you wanna try again? Y/N")
			return await try_again()

	amount_of_repeat = 0
	print("Start: Afk Always to target: ", target_member)
	try:
		while True:
			await target_member.edit(voice_channel=None)
			# Move delay
			time.sleep(0.3)
			amount_of_repeat += 1
	except:
		print(Fore.RED + "You have not permission to do this!")
		exit()


# Function can move user to each channel on server but you need Permissions.move_members.
@find_member
async def carousel(user_id, server_name, server_target, target_member):
	print(f"Сarousel is activated for user: {target_member.name}, in server: {server_name}.")
	for voice in server_target.voice_channels:

		try:
			await target_member.edit(voice_channel=voice)
			print('Move to: ', str(voice.name))
		except:
			print(Fore.RED + "You have not permission to do this!")

		# Move delay
		time.sleep(0.3)


async def try_again():
	choose = input()

	if choose.lower() == 'y' or choose.lower() == 'yes':
		await on_ready()
	elif choose.lower() == 'n' or choose.lower() == 'no':
		exit()
	else:
		print("I don't understand :(")
		await try_again()

if __name__ == '__main__':
	print("Wait a little while I prepare your account!")

	token_file = open("token.txt", "r")
	token = token_file.readline()

	try:
		client.run(token, bot=False)
	except:
		print("Token error token! Check your token to validity.")
