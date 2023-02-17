from collections import defaultdict
import random
import discord
from dotenv import load_dotenv
from os import getenv
import pickle

load_dotenv()
BOT_KEY = getenv("BOT_KEY")
SAVE_FILE = getenv("SAVE_FILE")
CHANNEL = getenv("CHANNEL")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try:
            with open(SAVE_FILE, 'rb') as f:
                self.data = pickle.load(f)
        except:
            print("no save")
        print("ready")

    async def on_message(self, message: discord.Message):
        if message.author == client.user:
            return
        if message.content.startswith("!getsentence"):
            try:
                author_id = message.content.split(" ")[1]
                # build_sentence
                await message.channel.send(self.build_sentence(int(author_id)))
            except:
                print("incorrect format")
                return
        if message.content.startswith("!train"):
            await self.get_data(client.get_channel(CHANNEL).history(limit=10000))


            
    async def get_data(self, history):
        self.data = defaultdict(lambda: defaultdict(list))
        epoch = 0
        async for message in history:
            epoch += 1
            if epoch % 100 == 0:
                print(epoch)
            split_string = message.content.split(" ")
            for i, word in enumerate(split_string[:-1]):
                self.data[message.author.id][word].append(split_string[i + 1])
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump(dict(self.data), f)

    def build_sentence(self, author_id):
        # get seed_word
        seed = random.choice(list(self.data[author_id].keys())) 
        length = random.randint(7, 25)
        sentence = seed
        curr_word = seed
        for _ in range(length):
            if curr_word not in self.data[author_id]:
                return sentence
            curr_word = random.choice(self.data[author_id][curr_word])
            sentence += " " + curr_word
        return sentence

            



intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False


client = MyClient(intents=intents)
client.run(BOT_KEY)
