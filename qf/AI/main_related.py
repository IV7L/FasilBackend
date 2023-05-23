



def test_similar(source_sentance, sentance_list):
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    sentences1 = [source_sentance]
    embedded_sen2 = []
    cosine_scores = []
    
    embeddings1 = model.encode(sentences1, convert_to_tensor=True)

    for i in sentance_list:
        embeddings2 = model.encode(i, convert_to_tensor=True)
        embedded_sen2.append(embeddings2)
        cosine_scores.append(util.cos_sim(embeddings1, embeddings2))
    
    for i in range(len(cosine_scores)):
        # print(sentences1[0])
        # print(sentance_list[i])
        # print(cosine_scores[i][0][0].item())
        return cosine_scores[i][0][0].item()

