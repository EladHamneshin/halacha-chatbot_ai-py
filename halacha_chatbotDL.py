import pickle

data_path = "embeddings/faq_brachot3000_embeddings.pickle"
questions = []
answers = []
embeddings = []


def init_data():
    """
    Load the default embeddings and the answers from disk
    """
    global answers
    global embeddings
    global questions
    # Load the default embeddings and the answers from disk
    with open("embeddings/faq_brachot3000_embeddings.pickle", "rb") as fIn:
        data = pickle.load(fIn)
        answers = data['answers']
        embeddings = list(data['embeddings'])
        questions = data["questions"]


def update_brachot():
    """
    change the embeddings and the answers to brachot
    """
    global answers
    global embeddings
    global questions
    global data_path
    data_path = "embeddings/faq_brachot3000_embeddings.pickle"
    with open("embeddings/faq_brachot3000_embeddings.pickle", "rb") as fIn:
        data = pickle.load(fIn)
        answers = data['answers']
        embeddings = list(data['embeddings'])
        questions = data["questions"]


def update_shabbat():
    """
    change the embeddings and the answers to brachot
    """
    global answers
    global embeddings
    global questions
    global data_path
    data_path = "embeddings/faq_shabbat1500_embeddings.pickle"
    with open("embeddings/faq_shabbat1500_embeddings.pickle", "rb") as fIn:
        data = pickle.load(fIn)
        answers = data['answers']
        embeddings = list(data['embeddings'])
        questions = data["questions"]


def append_question(question, answer, question_embedding):
    """
    Append a question and its answer to the data
    :param question: The question
    :param answer: The answer
    :param question_embedding: The question embedding
    """
    global answers
    global embeddings
    global questions
    answers.append(answer)
    embeddings.append(question_embedding)
    questions.append(question)
    with open(data_path, 'a+') as fp:
        pickle.dump(
            {
                'questions': question,
                'answers': answer,
                'embeddings': question_embedding
            }, fp)
