from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def rank_resumes(job_description, resume_texts):
    """
    Rank resumes based on similarity to the job description.
    :param job_description: str
    :param resume_texts: list of str (one for each resume)
    :return: list of (index, score) tuples sorted by score
    """
    documents = [job_description] + resume_texts  # First is JD, rest are resumes
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    jd_vector = tfidf_matrix[0]        # Vector for Job Description
    resume_vectors = tfidf_matrix[1:]  # Vectors for resumes

    similarities = cosine_similarity(jd_vector, resume_vectors)[0]  # 1D array of similarity scores
    ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)

    return ranked  # List of tuples: (resume index, similarity score)
