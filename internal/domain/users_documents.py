import pandas as pd

anime_path = 'Recommendation/internal/domain/tables/anime.csv'
rating_path = 'Recommendation/internal/domain/tables/rating.csv'


def get_users_documents(logger, removing_symbols):
    logger.info('read csv')
    anime = pd.read_csv(anime_path)
    anime['name'] = anime['name'].str.lower()
    anime['name'] = anime['name'].str.capitalize()
    anime['name'] = anime['name'].str.translate(str.maketrans('', '', removing_symbols))

    ratings = pd.read_csv(rating_path)
    ratings.drop_duplicates(['anime_id', 'user_id'], inplace=True)
    ratings = ratings[ratings.rating != -1]

    logger.info('pivot operation')
    user_item_matrix = ratings.pivot(index='anime_id', columns='user_id', values='rating')
    user_item_matrix.fillna(0, inplace=True)

    logger.info('cut matrix')
    users_votes = ratings.groupby('user_id')['rating'].agg('count')
    anime_votes = ratings.groupby('anime_id')['rating'].agg('count')

    user_mask = users_votes[users_votes > 50].index
    anime_mask = anime_votes[anime_votes > 10].index

    user_item_matrix = user_item_matrix.loc[anime_mask, :]
    user_item_matrix = user_item_matrix.loc[:, user_mask]

    logger.info('get ids')
    users_anime_ids = [
        user_item_matrix.index[user_item_matrix[int(i)] != 0].tolist()
        for i in user_item_matrix.columns.values
    ]

    logger.info('getting documents')
    documents = [
        [anime[anime['anime_id'] == user_anime_id]['name'].values.tolist()[0] for user_anime_id in user_anime_ids]
        for user_anime_ids in users_anime_ids
    ]

    return documents
