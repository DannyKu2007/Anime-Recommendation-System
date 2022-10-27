from internal.adapters.db.sqlite import get_watched_document, get_undesired_document

from internal.model.lda_model import get_lda_model
from internal.domain.user_data import users_data_path

from gensim.corpora.dictionary import Dictionary

from numpy import load


def get_recommendation(logger, user_id, removing_symbols):
    user_document = get_watched_document(logger, user_id)
    hate_list = get_undesired_document(logger, user_id)

    logger.debug(f'user_document: {user_document}')
    lda_model = get_lda_model(logger, removing_symbols)

    documents = load(users_data_path, allow_pickle=True).tolist()
    dictionary = Dictionary(documents)

    logger.info('get user vector')
    user_corpus = dictionary.doc2bow(user_document)

    vector = lda_model[user_corpus]
    logger.debug(f'{len(vector)} vectors: {vector}')

    if len(vector) == 0:
        return 'for a recommendation, you need at least one watched anime'

    logger.info('getting probability')
    probability = [vector[i][1] for i in range(len(vector))]

    while len(probability) > 0:
        cont = False

        logger.debug(f'probability {probability}')

        logger.info('getting index')
        index = vector[probability.index(max(probability))][0]

        logger.info('get topic')
        topic = lda_model.print_topic(index)

        logger.info('get titles and probabilities')
        titles = [t[t.index('*') + 1:][1:-2] for t in topic.split('+')]
        probs = [float(t[:t.index('*')]) for t in topic.split('+')]

        logger.debug(f'titles for these topics: {titles}')

        logger.info('search recommendation')
        idx = probs.index(max(probs))

        logger.info('transform titles')
        for i in range(len(titles)):
            titles[i] = titles[i].split(': ')[0].split('. ')[0].split(' movie')[0].split(' tv')[0]

            if len(titles[i].split('season')) > 1:
                titles[i] = ' '.join(titles[i].split('season')[0].split()[:-1])

        logger.debug(f'titles for these topics: {titles}')

        while any(titles[idx] in title for title in user_document) or any(titles[idx] in title for title in hate_list):
            logger.info('search recommendation index')
            probs.pop(idx)
            titles.pop(idx)

            if len(probs) == 0:
                probability.pop(probability.index(max(probability)))

                cont = True
                break

            idx = probs.index(max(probs))

        if cont:
            continue

        logger.info('getting recommendations')
        recommendation = titles[idx]

        return recommendation

    return "sorry, i can't recommend anything to you"
