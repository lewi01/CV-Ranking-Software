from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial import distance

def cosine_distance_countvectorizer_method(job_requirements, applicant_requirements):
    
    # sentences to list
    allsentences = [job_requirements , applicant_requirements]
    
    # text to vector
    vectorizer = CountVectorizer()
    all_sentences_to_vector = vectorizer.fit_transform(allsentences)
    text_to_vector_v1 = all_sentences_to_vector.toarray()[0].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[1].tolist()
    
    # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    print('Candidate skills matching to requirements',round((1-cosine)*100,2),'%')
    return round((1-cosine)*100,2)

def personality_matching_percentage(job_personality_type, predicted_type):
    total_percentage = 0;
    for x in range (4):
        if (job_personality_type[x] == predicted_type[x]):
            total_percentage += 25
    return total_percentage