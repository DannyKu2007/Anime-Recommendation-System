from .users_documents import get_users_documents

from numpy import asarray, save, load
from os.path import exists, dirname
from os import makedirs

users_data_path = 'Recommendation/internal/domain/users_data/documents.npy'


def get_user_data(logger, removing_symbols):
    if not exists(users_data_path):
        documents = get_users_documents(logger, removing_symbols)

        logger.info('save documents')
        makedirs(dirname(users_data_path), exist_ok=True)
        save(users_data_path, asarray(documents, dtype=object))

    else:
        logger.info('load documents')
        documents = load(users_data_path, allow_pickle=True).tolist()

    return documents
