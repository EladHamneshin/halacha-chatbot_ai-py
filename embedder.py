import pickle
import pandas as pd


def calc_file_embeddings(file_path, model):
    """Create the embeddings file from the data file.
    :param file_path: The path to the data file
    """
    # Load the data
    df = pd.read_csv(file_path)
    quetions = df["Question"].tolist()
    answers = df["Answer"].tolist()

    # Start the multi-process pool on all available CUDA devices
    pool = model.start_multi_process_pool()

    # Compute the embeddings using the multi-process pool
    embeddings = model.encode_multi_process(quetions, pool)

    # Stop the multi-process pool
    model.stop_multi_process_pool(pool)

    # Get the file's name
    file_name = file_path.split("/")[-1].split(".")[0]

    # Save the embeddings and the answers to disk in pickel format
    with open("embeddings/{}_embeddings.pickle".format(file_name),
              "wb") as fOut:
        pickle.dump(
            {
                'answers': answers,
                'questions': quetions,
                'embeddings': embeddings
            },
            fOut,
            protocol=pickle.HIGHEST_PROTOCOL)
