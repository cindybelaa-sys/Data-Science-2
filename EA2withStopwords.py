import os
import math
import string

# === 1. Load and Clean Texts ===
def load_texts(folder_path):
    texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='latin1') as file:
                texts[filename] = clean_text(file.read())
    return texts

def clean_text(text):

    
    # Remove stopwords
    stopwords = {
        "a", "an", "the", "and", "or", "in", "on", "at", "of", "for", "with", "to", "from",
       "by", "is", "it", "this", "that", "was", "as", "be", "are", "were", "has", "had",
      "have", "but", "not", "no", "yes", "you", "i", "he", "she", "they", "them", "we", "our", "his", "her"
    }
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Split into words (tokenize)
    tokens = text.split()
    filtered = [word for word in tokens if word not in stopwords]
    return filtered

# === 2. Build Vocabulary ===
def build_vocabulary(texts):
    vocab = set()
    for tokens in texts.values():
        vocab.update(tokens)
    return sorted(list(vocab))  # Sort to ensure consistent vector positions

# === 3. Create BoW Vectors ===
def text_to_bow(tokens, vocab):
    vector = [0] * len(vocab)
    for word in tokens:
        if word in vocab:
            index = vocab.index(word)
            vector[index] += 1
    return vector

# === 4. Euclidean Distance ===
def euclidean_distance(vec1, vec2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))

# === 5. Main Workflow ===
folder = "bbc/sport"  # adjust path as needed
texts = load_texts(folder)
vocab = build_vocabulary(texts)

#print(f"-------- ergebnis fuer text ----------{texts}")

#print(f"-------- ergebnis fuer vocab ----------{vocab}")

bow_vectors = {}
for filename, tokens in texts.items():
    bow_vectors[filename] = text_to_bow(tokens, vocab)

print(f"--------- ergebnis fuer bow ---------{bow_vectors}")

# Compare 497.txt to all others
target = bow_vectors["497.txt"]
distances = []

for filename, vector in bow_vectors.items():
    if filename != "497.txt":
        dist = euclidean_distance(target, vector)
        distances.append((filename, dist))

# Sort and get top 3 closest
distances.sort(key=lambda x: x[1])
top_3 = distances[:3]

#print("---------- Top 3 closest texts to 497.txt:----------")
for fname, dist in top_3:
   print(f"{fname} - Distance: {dist}")

