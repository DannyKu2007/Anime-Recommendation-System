from internal.domain.user_data import get_user_data

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from os.path import exists, dirname
from os import makedirs

models_path = './../internal/model/models/lda_model'


def get_lda_model(logger, removing_symbols):
    if not exists(models_path):
        logger.info('make models')
        makedirs(dirname(models_path), exist_ok=True)

        documents = get_user_data(logger, removing_symbols)

        logger.info('preparing corpus')
        dictionary = Dictionary(documents)
        corpus = [dictionary.doc2bow(document) for document in documents]

        logger.info('make model')
        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=100,
            passes=5,
        )

        logger.info('save model')
        lda_model.save(models_path)

    else:
        logger.info('load model')
        lda_model = LdaModel.load(models_path)

    return lda_model
