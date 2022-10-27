from peewee import SqliteDatabase, Model, CharField

db_path = './../internal/adapters/db/users.db '
db = SqliteDatabase(db_path)


class WatchedAnime(Model):
    user_id = CharField()
    anime_title = CharField()

    class Meta:
        database = db


class UndesirableAnime(Model):
    user_id = CharField()
    anime_title = CharField()

    class Meta:
        database = db


def create_table(logger):
    logger.info('creating table')
    logger.info(f'connected to table: {db.connect()}')

    logger.info('creating table models')
    db.create_tables([WatchedAnime, UndesirableAnime])


def get_watched_document(logger, user_id):
    logger.info('get watched user document')
    user_watched_document = list(set([row.anime_title for row in WatchedAnime.select().where(WatchedAnime.user_id == user_id)]))

    return user_watched_document


def get_undesired_document(logger, user_id):
    logger.info('get watched user document')
    user_undesired_document = list(set([row.anime_title for row in UndesirableAnime.select().where(UndesirableAnime.user_id == user_id)]))

    return user_undesired_document


def watch_anime(logger, user_id, anime_title):
    logger.info(f'adding anime: {anime_title}')
    WatchedAnime.create(user_id=user_id, anime_title=anime_title)

    allow_anime(logger, user_id, anime_title)


def allow_anime(logger, user_id, anime_title):
    logger.info(f'allowing anime to watch: {anime_title}')
    query = UndesirableAnime.delete().\
        where(UndesirableAnime.user_id == user_id, UndesirableAnime.anime_title == anime_title)
    query.execute()


def hate_anime(logger, user_id, anime_title):
    logger.info(f'undesired anime: {anime_title}')
    UndesirableAnime.create(user_id=user_id, anime_title=anime_title)

    query = WatchedAnime.delete().\
        where(WatchedAnime.user_id == user_id, WatchedAnime.anime_title == anime_title)
    query.execute()
