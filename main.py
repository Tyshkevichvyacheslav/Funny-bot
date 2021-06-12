import discord
import asyncpraw
import asyncio
import config

bot = discord.Client()
reddit = asyncpraw.Reddit(client_id=config.settings['client id'],
                          client_secret=config.settings['secret'],
                          user_agent='Brat') # это все берется из файла config для взаимодействия с reddit

Fun = [] # список в котором  сохранены все загруженные картинки, чтобы не было повторений при загрузке в канал
Time = 5 # один раз в 5 секунд бот будет обращатся в редит и искать смешные картинки
IdChannel = 853274225733271592 # айди канала в дискорде куда загружаются смешные картинки
Subname = 'funny'# название сабредита, откуда бот будет брать смешные картинки
Limit = 1 # кол-во картинок


@bot.event
async def on_ready():
    channel = bot.get_channel(IdChannel) # передаю боту айди канал куда загружать
    while True:
        await asyncio.sleep(Time)
        funny_submissions = await reddit.subreddit(Subname) #передаю боту куда я хочу получить доступ
        funny_submissions = funny_submissions.new(limit=Limit) # бот берет один самый последний пост
        item = await funny_submissions.__anext__()  # в item находится информация о самом свежем посте
        if item.title not in Fun: # проверка на дубликаты,чтобы не было повторений
            Fun.append(item.title) # идет запись заголовка в список , если его еще не добавляли
            await channel.send(item.url) # отправляет ссылку на картинку в канал дискорда


bot.run(config.settings['token'])