from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_texts, jd_text):

    # combine resumes + job description
    documents = resume_texts + [jd_text]

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    # last vector is job description
    jd_vector = tfidf_matrix[-1]

    # resume vectors
    resume_vectors = tfidf_matrix[:-1]

    # cosine similarity
    similarity_scores = cosine_similarity(resume_vectors, jd_vector)

    return similarity_scores.flatten()