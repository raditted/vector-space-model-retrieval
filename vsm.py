import sys
import os
import math
import string
from collections import defaultdict

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# handling buat cek res nltk
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")



# untuk preprocessing
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


def preprocess(text):
    text = text.lower()

    tokens = word_tokenize(text)

    result = []

    for token in tokens:
        # untuk hapus tanda baca
        if token in string.punctuation:
            continue

        # untuk hapus stopwords
        if token in stop_words:
            continue

        # cuma huruf
        if not token.isalpha():
            continue

        # untuk stemming
        token = stemmer.stem(token)

        result.append(token)

    return result


# untuk load dokumen
def loadDocuments(base_file):
    documents = {}

    with open(base_file, "r") as f:
        filenames = [line.strip() for line in f]

    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as file:
            documents[filename] = file.read()

    return documents


# untuk menghitung TF (Term Frequency)
def calculateTf(tokens):
    tf = {}

    for token in tokens:
        tf[token] = tf.get(token, 0) + 1

    for token in tf:
        tf[token] = 1 + math.log10(tf[token])

    return tf


# untuk menghitung DF (Document Frequency)
def calculateDf(processed_docs):
    df = {}

    for doc in processed_docs.values():
        unique_terms = set(doc)

        for term in unique_terms:
            df[term] = df.get(term, 0) + 1

    return df


# untuk menghitung IDF (Inverse Document Frequency)
def calculateIdf(df, total_docs):
    idf = {}

    for term in df:
        idf[term] = math.log10(total_docs / df[term])

    return idf


# untuk menghitung TF-IDF
def calculateTfIdf(tf, idf):
    tfidf = {}

    for term in tf:
        tfidf[term] = tf[term] * idf.get(term, 0)

    return tfidf


# untuk menghitung cosine similarity
def cosSim(doc_vector, query_vector):
    dot_product = 0

    for term in query_vector:
        if term in doc_vector:
            dot_product += doc_vector[term] * query_vector[term]

    doc_norm = math.sqrt(sum(value ** 2 for value in doc_vector.values()))
    query_norm = math.sqrt(sum(value ** 2 for value in query_vector.values()))

    if doc_norm == 0 or query_norm == 0:
        return 0

    return dot_product / (doc_norm * query_norm)


# untuk menulis index
def wrtIndex(tfidf_docs, prefix="query"):
    inverted_index = defaultdict(list)

    for doc_id, vector in tfidf_docs.items():
        for term, weight in vector.items():
            inverted_index[term].append((doc_id, weight))

    os.makedirs("index", exist_ok=True)
    file_path = os.path.join("index", f"index_{prefix}.txt")

    with open(file_path, "w") as f:
        for term in sorted(inverted_index.keys()):
            f.write(f"{term}: ")

            postings = []

            for doc, weight in inverted_index[term]:
                postings.append(f"{doc},{weight:.4f}")

            f.write(" ".join(postings))
            f.write("\n")


# untuk menulis berat
def wrtWeights(tfidf_docs, prefix="query"):
    os.makedirs("weights", exist_ok=True)
    file_path = os.path.join("weights", f"weights_{prefix}.txt")

    with open(file_path, "w") as f:
        for doc, vector in tfidf_docs.items():
            f.write(f"{doc}: ")

            terms = []

            for term, weight in vector.items():
                terms.append(f"{term},{weight:.4f}")

            f.write(" ".join(terms))
            f.write("\n")


# untuk menulis response
def wrtResponse(results, prefix="query"):
    filtered = []

    for doc, score in results:
        if score > 0.001:
            filtered.append((doc, score))

    os.makedirs("response", exist_ok=True)
    file_path = os.path.join("response", f"response_{prefix}.txt")

    with open(file_path, "w") as f:
        f.write(str(len(filtered)))
        f.write("\n")

        for doc, score in filtered:
            f.write(f"{doc} {score:.4f}\n")


# main function
def main():
    if len(sys.argv) != 3:
        print("python vsm.py base.txt query.txt")
        return

    base_file = sys.argv[1]
    query_file = sys.argv[2]

    documents = loadDocuments(base_file)

    # preprocessing dokumen
    processed_docs = {}

    for filename, text in documents.items():
        processed_docs[filename] = preprocess(text)

    # menghitung TF
    tf_docs = {}

    for filename, tokens in processed_docs.items():
        tf_docs[filename] = calculateTf(tokens)

    # menghitung DF
    df = calculateDf(processed_docs)

    # menghitung IDF
    idf = calculateIdf(df, len(documents))

    # menghitung TF-IDF
    tfidf_docs = {}

    for filename, tf in tf_docs.items():
        tfidf_docs[filename] = calculateTfIdf(tf, idf)

    # baca query
    with open(query_file, "r") as f:
        query_text = f.read()

    query_name = query_file.replace(".txt", "")

    wrtWeights(tfidf_docs, query_name)

    # preprocessing query
    query_tokens = preprocess(query_text)

    # TF query
    query_tf = calculateTf(query_tokens)

    # TF-IDF query
    query_vector = calculateTfIdf(query_tf, idf)

    # similarity
    results = []

    for filename, vector in tfidf_docs.items():
        score = cosSim(vector, query_vector)
        results.append((filename, score))

    # ranking
    results.sort(key=lambda x: x[1], reverse=True)

    # save
    wrtResponse(results, query_name)

    print("done.... check folder for results")

if __name__ == "__main__":
    main()