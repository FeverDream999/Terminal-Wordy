alphabet = "abcdefghijklmnopqrstuvwxyz"

# - Filter only 5 letter words from a list of words of varying lenghts
def raw_filter():

    with open(f"data/20k.txt", "r") as file:
        data = file.readlines()
        data = [line.strip() for line in data if line.strip()]

    with open("data/5k.txt", "w") as file:
        new_data = []
        for line in data:
            if len(line) == 5:
                new_data.append(line)
                file.write(line + "\n")

# - Compute letter frequency by position and store in a matrix
def letter_frequency():
    # - Load all words
    with open("data/wordle-data/wordle-words.txt", "r") as file:
        words = [line.strip() for line in file]

    # - Find max word length
    max_length = max(len(width) for width in words)

    # - Create matrix: 26 rows × max_length cols
    matrix = [[0 for _ in range(max_length)] for _ in range(len(alphabet))]

    # - Fill matrix
    for word in words:
        for index, letter in enumerate(word):
            if letter in alphabet:
                row = alphabet.index(letter)
                matrix[row][index] += 1

    return matrix

# - Save results 
# ===========================================
#   TRANSFORM INTO .TXT AGAIN LOL (not useful though)
# ===========================================
def save_results():
    matrix = letter_frequency()
    with open("data/wordle-data/frequency.json", "w") as file:
        #json.dump(matrix, file, indent=4)
        pass

# - ransforms words letters to numbers based on alphabetic positioning
def words_to_numbers():
    # - Load words
    with open("data/wordle-data/wordle-words.txt", "r") as file:
        words = [line.strip() for line in file]

    with open("data/wordle-data/wordle-words-numbers.txt", "w") as file:
        for word in words:
            words = []
            number = [alphabet.index(letter) for letter in word]
            words.append(number)
            file.write(f"{words[0]}\n")




    


            
        
        
        



