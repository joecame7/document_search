import numpy as np

inverted_index = {}
number_of_appearences = {}
document_vector = {}
query_vector = {}
angles = {}

id = 1

def calculate_angle(x, y):
    x_dot_y = np.dot(x, y) # Dot product
    x_norm = np.linalg.norm(x)
    y_norm = np.linalg.norm(y)

    return np.degrees(np.arccos(x_dot_y / (x_norm * y_norm)))

with open('docs.txt') as documents:
    for line in documents:
        document = line.strip() # Remove blankline
        words = document.split() # Split document into individual words
        sorted_words = sorted(words)

        # Create inverted index
        for word in sorted_words:
            inverted_index_documents = []
            if word not in inverted_index:
                inverted_index_documents.append(id)
                inverted_index[word] = inverted_index_documents
            elif (word in inverted_index) and (id not in inverted_index[word]):
                temp = inverted_index[word]
                temp.append(id)

        # Number of times a word appears in each document
        document_list = {}
        for word in sorted_words:
            if word not in document_list:
                document_list[word] = 1
            elif word in document_list:
                number = document_list[word]
                document_list[word] = number + 1
                sorted(document_list)
        number_of_appearences[id] = document_list

        id += 1
print(f"Words in dictionary:  {len(inverted_index)}")

with open('queries.txt') as queries:

    for line in queries:
        documents = set()
        query = line.strip()
        words = query.split()

        # Print words in query
        query_words = ""
        for i in words:
            query_words += " " + i
        print(f"Query: {query_words}")

        # Find relevant documents
        for word in words:
            if word in inverted_index:
                if not documents:
                    for i in inverted_index[word]:
                        documents.add(i)
                elif documents:
                    temp = inverted_index[word]
                    intersection = set(documents).intersection(set(temp))
                    documents = set()
                    documents.update(intersection)
            else:
                print(f"The query '{word}' is not in the inverted index.")

        # Print relevant documents
        relevant_documents = ""
        if documents:
            for i in documents:
                relevant_documents += str(i) + " "
            print(f"Relevant documents: {relevant_documents}")
        else:
            print("Relevant documents: None")
            
        for word in words:

            for document_id in documents:
                list_of_words = number_of_appearences[document_id]
                
                # Document vector
                if document_id not in document_vector:
                    document_vec = list(list_of_words.values())
                    document_vector[document_id] = document_vec

                # Query vector
                query_vec = list(list_of_words.keys())
                if document_id not in query_vector:
                    query_list = []
                    for i in range(len(query_vec)):
                        if query_vec[i] == word:
                            query_list.append(1)
                        else:
                            query_list.append(0)   
                    query_vector[document_id] = query_list
                elif document_id in query_vector:
                    for i in range(len(query_vector[document_id])):
                        if query_vec[i] == word:
                            query_vector[document_id][i] = 1

        document_id = list(query_vector.keys())
        for i in document_id:
            document_vec = document_vector[i]
            query_vec = query_vector[i]
            angle = calculate_angle(document_vec, query_vec)
            angles[i] = angle
        
        sorted_angles = sorted(angles.items(), key=lambda x:x[1])
        for i in sorted_angles:
            print(f"{i[0]} {i[1]:.2f}")

        query_vector = {}
        angles = {}