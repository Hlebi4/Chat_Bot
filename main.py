from aiogram import Bot, Dispatcher
from aiogram.types import Message
from core.handlers.basic import get_start
import asyncio
import logging
from aiogram.filters import Command
from core.settings import settings
from core.untils.commands import set_commands
from core.handlers import recommendation
from core.untils.statesform import StepsForm

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id,  text = 'Бот остановлен!')
async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(recommendation.get_recommendatrion, Command(commands='get_recommendation'))
    dp.message.register(recommendation.expectation_rec, StepsForm.GET_FILM)
    dp.message.register(recommendation.get_rating, StepsForm.GET_RATING)

    dp.message.register(get_start)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

# Content Based Filtering

df1 = pd.read_csv('core/tmdb_5000_credits.csv')
df2 = pd.read_csv('core/tmdb_5000_movies.csv')

df1.columns = ['id','tittle','cast','crew']
df2 = df2.merge(df1,on='id')

C = df2['vote_average'].mean()
m = df2['vote_count'].quantile(0.9)
q_movies = df2.copy().loc[df2['vote_count'] >= m]
def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

# Определим новую функцию "оценка" и вычислите ее значение с помощью `weighted_rating()`
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

# Сортировка фильмов на основе оценки, рассчитанной выше
q_movies = q_movies.sort_values('score', ascending=False)

# Определим объект векторизатора TF-IDF. Удалим все английские стоп-слова, такие как "the", "a"
tfidf = TfidfVectorizer(stop_words='english')

# Заменим значения NaN пустой строкой
df2['overview'] = df2['overview'].fillna('')

# Построим требуемую матрицу TF-IDF путем подгонки и преобразования данных
tfidf_matrix = tfidf.fit_transform(df2['overview'])

# Вычислим матрицу косинусного подобия
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Построим обратную карту индексов и названий фильмов
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

# Функция, которая принимает название фильма в качестве входных данных и выводит большинство похожих фильмов
# Функция, которая принимает название фильма в качестве входных данных и выводит большинство похожих фильмов
# Функция, которая принимает название фильма в качестве входных данных и выводит большинство похожих фильмов
def get_recommendations(title, cosine_sim=cosine_sim):
    # Получаем индекс фильма, который соответствует названию
    idx = indices[title]

    # Получаем оценки парного сходства всех фильмов с этим фильмом
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Отсортируем фильмы по показателям сходства
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Получаем оценки 10 самых похожих фильмов
    sim_scores = sim_scores[1:11]

    # Получаем индексы фильмов
    movie_indices = [i[0] for i in sim_scores]
    recom = df2['title'].iloc[movie_indices]
    recom = recom.to_string(index=False, dtype=False)
    recom = recom.replace(' ', '')
    # Возвращаем топ-10 самых похожих фильмов
    return recom

# Collaborative Filtering

ratings = pd.read_csv('core/movies.csv')
movies = pd.read_csv('core/ratings.csv')

ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1)
# Не рассматривайте фильмы с количеством оценок пользователей менее 10 и заполните остальные nan значением 0
userRatings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')

# Алгоритм поиска сходства элементов, используемый для корреляции, с поправкой на средние значения
corrMatrix = userRatings.corr(method='pearson')

# Функция сходства для поиска похожих фильмов
def get_similar(movie_name, rating):
    similar_ratings = corrMatrix[movie_name] * (rating - 2.5)
    # Получаем индексы фильмов
    similar_ratings = similar_ratings.sort_values(ascending=False)
    similar_ratings = pd.DataFrame(data=similar_ratings)
    return '\n'.join(similar_ratings[1:11].index)

if __name__ == "__main__":
    asyncio.run(start())