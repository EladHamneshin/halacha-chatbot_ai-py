# imports
from sentence_transformers import SentenceTransformer, LoggingHandler, util
import halacha_chatbotDL
import logging
import torch

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])

# Load the model
model = SentenceTransformer('imvladikon/alephbertgimmel-base-512')

# Load the data
halacha_chatbotDL.init_data()

# top results of the last query
top_results = []
current_question_embedding = None


def update_shabbat():
    """
    change the embeddings and the answers to shabbat
    """
    halacha_chatbotDL.update_shabbat()


def update_brachot():
    """
    change the embeddings and the answers to brachot
    """
    halacha_chatbotDL.update_brachot()


def append_question(question, answer, question_embedding):
    """
    Append a question and its answer to the data
    :param question: The question
    :param answer: The answer
    :param question_embedding: The question embedding
    """
    halacha_chatbotDL.append_question(question, answer, question_embedding)


def find_k_nearest_neighbors(query_emb, embeddings, k=1):
    """Find the k nearest neighbors for a query embedding in a corpus of embeddings.
    :param query_emb: The query embedding
    :param embeddings: The questions embeddings
    :param k: The number of nearest neighbors to find
    :return: The indices of the k nearest neighbors
    """
    # Compute cosine-similarits
    cos_scores = util.pytorch_cos_sim(query_emb, embeddings)[0]

    # Sort the results in decreasing order
    top_results_tuples = torch.topk(cos_scores,
                                    k=k)  # taple of (values, indices)

    return top_results_tuples[1]


def find_closest_answer(query):
    """
    Find the closest sentences of the corpus for each query sentence based on cosine similarity
    :param query: The query sentence
    :return: The closest question and its answer
    """
    global top_results
    global current_question_embedding
    current_question_embedding = model.encode(query)
    top_results = find_k_nearest_neighbors(current_question_embedding,
                                           halacha_chatbotDL.embeddings,
                                           k=4)
    index = top_results[0].item()
    answer = halacha_chatbotDL.answers[index]
    question = halacha_chatbotDL.questions[index]
    return question, answer


def get_answer_by_index(result_index):
    """
    Get a answer from the top results by index
    :param result_index: The index of the result
    :return: The question and its answer in the index
    """
    if result_index >= len(top_results):
        return None, None
    index = top_results[result_index].item()
    answer = halacha_chatbotDL.answers[index]
    question = halacha_chatbotDL.questions[index]
    return question, answer
