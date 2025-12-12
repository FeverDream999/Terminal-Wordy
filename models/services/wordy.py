from colorama import Fore, Style
import random

alphabet:str = "abcdefghijklmnopqrstuvwxyz"

class game():
    def __init__(self, MaxGuesses:int = 6, WordsLenght:int = 5):

        self.__PermitedWords: list[str] = []
        self.__TriedWords: list[str] = []
        self.__FeedbackList: list[str] = []

        self.__GreenLetters:dict[str,list[int]] = {}
        self.__YellowLetters:dict[str,list[int]] = {}
        self.__RedLetters:dict[str,list[int]] = {}

        self.__MaxGuesses:int = MaxGuesses
        self.__WordsLength:int = WordsLenght

    @staticmethod   
    def menu_converter(menu_text:str = "- Enter an interger:"):
        ExitTry = False
        
        while not ExitTry:
            try:
                NumberInput = input(menu_text)
                menu_number = int(NumberInput)
                return menu_number
            except ValueError:
                print(f"{Fore.RED}{Style.BRIGHT}(Error){Style.NORMAL} --- Enter a whole number{Style.RESET_ALL}")

    def menu(self):
        MenuInput = 0
        ExitInput = None
        while (MenuInput != ExitInput):
            print(Fore.CYAN + "=======================================" +  Style.BRIGHT)
            print(r" _    _                      _         ")
            print(r"| |  | |                    | |        ")
            print(r"| |  | |   ___    _ __    __| |  _   _ ")
            print(r"| |/\| |  / _ \  | '__|  / _` | | | | |")
            print(r"\  /\  / | (_) | | |    | (_| | | |_| |          ／l、 ")
            print(r" \/  \/   \___/  |_|     \__,_|  \__, |        （ﾟ､ ｡ 7")
            print(r"                                  __/ |          l  ~ヽ")
            print(r"                                 |___/           じしf_,)ノ")
            print(Style.NORMAL + "=========================================================" + Style.RESET_ALL)
        
            print()
            print ("1- Play against Bunny!")
            print ("2- Make Wordy guess!")
            print ("3- Add custom word to dictionary")
            print ("4- Reset Custom words")
            print ("5- Reset match history")
            print ("6- Is Wordy the cat?")
            print ("7- Who is Bunny?")
            print ("0- Close program")
            print ("--------------------------------------")
            print()
            MenuInput = self.menu_converter("- Menu Input: ")
            print()
            match MenuInput:
                case 0:
                    print("- Closing program... Goodnight! ᓚ₍ ^. ̫ .^₎  ")
                    print()
                    MenuInput = ExitInput
                case 1:
                    self.bunny_solo()
                case 2:
                    self.wordy_guess()
                case 3:
                    self.add_CustomWord()
                case 4:
                    self.reset_CustomWords()
                case 5:
                    self.reset_matches()
                case 6:
                    print(Fore.LIGHTMAGENTA_EX +"- Yes!!!!!!!!!   ")
                    print("              ,_     _")
                    print("              |\\\\_,-~/")
                    print("              / _  _ |    ,--.")
                    print("             (  @  @ )   / ,-'")
                    print("              \\  _T_/-._( (")
                    print("              /         `. \\")
                    print("             |         _  \\ |")
                    print("              \\ \\ ,  /      |")
                    print("               || |-_\\__   /")
                    print("              ((_/`(____,-'" + Style.RESET_ALL)
                case 7:
                    print(f"- Bunny is a friend that you can rival against or ask to be a neutral ally when playing against wordy. " \
                          f"{Fore.YELLOW}Be wary of her{Style.RESET_ALL} as she will not hold your hand if you decide to challenge her. " \
                          f"She will {Fore.RED}will punish you{Style.RESET_ALL} " \
                          f"if you decide to not use a lenght-appropiate word, symbols she may not recognize or if your word is not in her list")
        
    def letter_frequency(self) -> list[list[int]]:

        # - Create Matrix
        max_length = max(len(width) for width in self.__PermitedWords)
        FrequencyMatrix = [[0 for _ in range(max_length)] for _ in range(len(alphabet))]

        # - Fill matrix
        for word in self.__PermitedWords:
            for index, letter in enumerate(word):
                if letter in alphabet:
                    row = alphabet.index(letter)
                    FrequencyMatrix[row][index] += 1

        return FrequencyMatrix
    
    def compute_BestWord(self, FrequencyMatrix) -> str:
        PotentialBestWords:dict[str, int] = {}
        
        for word in self.__PermitedWords:
            value:int = 0

            for index, letter in enumerate(word):
                if letter in alphabet:
                    value += FrequencyMatrix[alphabet.index(letter)][index]
            PotentialBestWords[word] = value

        PotentialBestWords = dict(sorted(PotentialBestWords.items(), key=lambda item: item[1]))
        BestWord = list(PotentialBestWords.keys())[-1]

        self.__TriedWords.append(BestWord)

        return BestWord
    
    def assign_colors(self, Feedback:str):

        word:str = self.__TriedWords[-1]

        # - Green
        for index, mark in enumerate(Feedback.lower()):
            if mark == "a":
                letter = word[index].lower()
                if letter not in self.__GreenLetters:
                    self.__GreenLetters[letter] = []
                self.__GreenLetters[letter].append(index)
        # - Yellow
        for index, mark in enumerate(Feedback.lower()):
            if mark == "b":
                letter = word[index].lower()
                if letter not in self.__YellowLetters:
                    self.__YellowLetters[letter] = []
                self.__YellowLetters[letter].append(index)
        # - Red
        for index, mark in enumerate(Feedback.lower()):
            if mark == "x":
                letter = word[index].lower()

                if letter not in self.__RedLetters:
                    self.__RedLetters[letter] = []
                self.__RedLetters[letter].append(index)

        # - After processing all letters, check for letters that are X everywhere
        for letter in set(word):
            marks = [Feedback[i].lower() for i, ch in enumerate(word) if ch.lower() == letter]
            if all(m == "x" for m in marks):
                # True absent letter => forbid all positions
                self.__RedLetters[letter] = list(range(self.__WordsLength))

    def get_possibleWords(self):
        self.__PermitedWords = [line.strip() for line in open("data/wordy-data/wordy-words.txt")]
        try:
            self.__PermitedWords += [line.strip() for line in open("data/wordy-data/custom-words.txt")]
            with open ("data/wordy-data/games.txt", "r") as file:
                data = file.readlines()
                data = [line.strip() for line in data if line.strip()]
                for word in data:
                    if word in self.__PermitedWords:
                        self.__PermitedWords.remove(word)
        except FileNotFoundError:
            pass

    def compute_viability(self) -> str | None:
        """Filters words from self.__PermitedWords"""

        # =First Try=======================================================
        if len(self.__TriedWords) == 0:
            self.get_possibleWords()
            FrequencyMatrix = self.letter_frequency()
            BestWord = self.compute_BestWord(FrequencyMatrix)
            return BestWord
        # =================================================================

        for word in list(self.__PermitedWords):   # (iterate over a COPY)
            ValidWord = True

            if word in self.__TriedWords:
                self.__PermitedWords.remove(word)
                continue
            
            
            # =Green filter============================================
            # ONLY RULE: Word must match green positioning (if not, it switches ValidWord to False)
            for g_letter, positions in self.__GreenLetters.items():
                for pos in positions:
                    if pos >= len(word) or word[pos] != g_letter:
                        ValidWord = False
                        break
                if not ValidWord:
                    break
            # (Remove word from self.__PermitedWords if ONLY RULE is broken)
            if not ValidWord:
                self.__PermitedWords.remove(word)
                continue

            # =Yellow filter===========================================
            # RULE 1: Letter must NOT be in forbidden_position (If so, it switches ValidWord to False)
            for y_letter, forbidden_positions in self.__YellowLetters.items():
                for pos in forbidden_positions:
                    if pos >= len(word) or word[pos] == y_letter:
                        ValidWord = False
                        break
                if not ValidWord:
                    break
            # RULE 2: Letter must appear at least once in allowed positions (If so, it switches ValidWord to False)
                found_allowed = False
                for idx, ch in enumerate(word):
                    if ch == y_letter and idx not in forbidden_positions:
                        found_allowed = True
                        break

                if not found_allowed:
                    ValidWord = False
                    break
            # (Remove word from self.__PermitedWords if RULE 1 or RULE 2 is broken)
            if not ValidWord:
                self.__PermitedWords.remove(word)
                continue

            # =Red filter============================================
            # ONLY RULE: Word must NOT match red positioning (if so, it switches ValidWord to False)
            for r_letter, positions in self.__RedLetters.items():
                for pos in positions:
                    if pos >= len(word) or word[pos] == r_letter:
                        ValidWord = False
                        break
                if not ValidWord:
                    break
            # (Remove word from self.__PermitedWords if ONLY RULE is broken)
            if not ValidWord:
                self.__PermitedWords.remove(word)
                continue
            # =========================================================

            # - If no valid words remain, return None (FAIL)
        if not self.__PermitedWords:
            return None
        
        # Otherwise: compute & return a real best word
        FrequencyMatrix = self.letter_frequency()
        return self.compute_BestWord(FrequencyMatrix)
    
    def input_constrainer(self, guess: str, feedback: str) -> bool:

        # =Universal Constraints==========================================
        
        # - Length check
        if len(feedback) != len(guess):
            print(f"{Fore.RED}- Invalid input: must be {len(guess)} characters long.{Style.RESET_ALL}")
            return False
        # - Character check
        for character in feedback.lower():
            if character not in ("a", "b", "x"):
                print(f"{Fore.RED}- Invalid character: only A, B, X allowed.{Style.RESET_ALL}")
                return False
            
        # ================================================================

        PreviousWord = self.__TriedWords[-1]

        # =Green contradictions============================================
        for index, mark in enumerate(feedback.lower()):
            if mark == "a":

                letter = PreviousWord[index].lower()
                
                
                # ONLY CONTRADICTION: Check if this position was already marked green with a different letter
                for g_letter, positions in self.__GreenLetters.items():
                    if index in positions and g_letter != letter:
                        print(f"{Fore.RED}- Logical error: Position {index} was already green for '{g_letter}', cannot now be '{letter}'.{Style.RESET_ALL}")
                        return False
                    
        # ==Yellow contradictions==========================================
        for index, mark in enumerate(feedback.lower()):
            if mark == "b":  # User says this letter is YELLOW

                allowed_positions = []
                letter = guess[index].lower()

                # CONTRADICTION 1: Cannot mark yellow a letter previously marked RED everywhere
                if letter in self.__RedLetters and len(self.__RedLetters[letter]) == self.__WordsLength:
                    print(f"{Fore.RED}- Contradiction: '{letter}' was confirmed absent before (X everywhere).{Style.RESET_ALL}")
                    return False
                # CONTRADICTION 2: Cannot mark yellow a letter that is GREEN in this same position
                if letter in self.__GreenLetters and index in self.__GreenLetters[letter]:
                    print(f"{Fore.RED}- Contradiction: '{letter}' is already green at position {index}.{Style.RESET_ALL}")
                    return False
                # CONTRADICTION 3: If this letter was previously yellow but forbidden in ALL other positions, marking it yellow here again becomes impossible → contradiction
                if letter in self.__YellowLetters:
                    forbidden = self.__YellowLetters[letter]
                    allowed_positions = [i for i in range(self.__WordsLength) if i not in forbidden]

                    # CONTRADICTION 3.1: All allowed positions must remain ≥1
                    if len(allowed_positions) == 0:
                            print(f"{Fore.RED}- Contradiction: '{letter}' cannot appear anywhere except forbidden positions.{Style.RESET_ALL}")
                            return False
        
        for index, mark in enumerate(feedback):
            if mark.lower() == "x":
                letter = guess[index]

                # CONTRADICTION 1: Cannot mark red a position that is green
                if letter in self.__GreenLetters and index in self.__GreenLetters[letter]:
                    print(f"{Fore.RED}- Contradiction: '{letter}' is green at {index}, cannot be X.{Style.RESET_ALL}")
                    return False

                # CONTRADICTION 2: If letter must appear (Green or Yellow exist), then marking this X cannot eliminate all possible positions
                must_appear = letter in self.__GreenLetters or letter in self.__YellowLetters

                if must_appear:
                    forbidden = self.__RedLetters.get(letter, [])
                    new_forbidden = forbidden + [index]

                    allowed = [i for i in range(self.__WordsLength) if i not in new_forbidden]

                    if len(allowed) == 0:
                        print(f"{Fore.RED}- Contradiction: '{letter}' must appear but X forbids all positions.{Style.RESET_ALL}")
                        return False

        return True

    def wordy_guess(self):
        answers_input = []

        for round in range(self.__MaxGuesses):

            if round == 0:
                print("============================")
                print(f"{Fore.GREEN}- Correct guess:   {Style.BRIGHT}'A'{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}- Yellow guess:    {Style.BRIGHT}'B'{Style.RESET_ALL}")
                print(f"{Fore.RED}- Wrong guess:     {Style.BRIGHT}'X'{Style.RESET_ALL}")
                print(f"- Format example: {Fore.CYAN}{Style.BRIGHT}XXABX{Style.RESET_ALL}")
                print("============================")
            else:
                print("============================")
                for past_word, past_answer in zip(self.__TriedWords, answers_input):
                    print(f"- {past_word}: {past_answer}")
                print("============================")

            print()

            # - Compute next best guess
            best_word = self.compute_viability()
            if best_word is None:
                print(f"{Fore.RED}{Style.BRIGHT}- No valid guesses remain with current constraints.{Style.RESET_ALL}")
                return None

            print(f"- My guess ({round + 1}/{self.__MaxGuesses}) is {Fore.CYAN}{Style.BRIGHT}{best_word.upper()}{Style.RESET_ALL}! How did I do?")

            # - Checks if answer makes sense
            answer_input = []
            answer = input("-Your answer: ")
            while not self.input_constrainer(best_word, answer):
                answer = input("-Your answer: ")
                print()
            self.__FeedbackList.append(answer)
            self.assign_colors(answer.lower())
            
            #  - EARLY WIN CHECK: all greens
            if answer.lower() == "a" * len(answer):
                print(f"{Fore.GREEN}{Style.BRIGHT}- Wordy wins again!{Style.NORMAL}")
                print("                   _ |\\_")
                print("                   \\` ..\\")
                print("              __,.-\" =__Y=")
                print("            .\"        )")
                print("      _    /   ,    \\/\\_")
                print("     ((____|    )_-\\ \\_-`")
                print("      `-----'`-----` `--`" + Style.RESET_ALL)
                self.reset_variables()
                self.save_game(best_word)
                return
            
            styled_word = self.answer_styling(answer)
            answers_input.append(styled_word)

    def answer_styling(self, answer: str) -> str:
        styled = []

        for mark in answer:
            if mark.lower() == "a":
                styled.append(f"{Fore.GREEN}{Style.BRIGHT}{mark.upper()}{Style.RESET_ALL}")
            elif mark.lower() == "b":
                styled.append(f"{Fore.YELLOW}{Style.BRIGHT}{mark.upper()}{Style.RESET_ALL}")
            else:
                styled.append(f"{Fore.RED}{Style.BRIGHT}{mark.upper()}{Style.RESET_ALL}")

        return "".join(styled)

    def bunny_solo(self):
        victoryWord = self.bunny_word()
        print(f"{Fore.CYAN}- Bunny chose a word with {self.__WordsLength} letters!{Style.RESET_ALL}")

        for round in range(self.__MaxGuesses):

            # - Show history after the first round
            if round > 0:
                print("============================")
                for past_word, past_feedback in zip(self.__TriedWords, self.__FeedbackList):
                    print(f"- {past_word.upper()}: {self.answer_styling(past_feedback)}")
                print("============================")

            user_input = input(f"- Your guess ({round + 1}/{self.__MaxGuesses}) is: ")

            # = Punishment =========================================================================
            # - Incorrect guess length 
            if len(user_input) != self.__WordsLength:
                print(f"{Fore.RED}- PUNISHED! your guess must be {self.__WordsLength} letters. SILLY!")
                print(r"""
            ,\
            \\\,_
            \` ,\
        __,.-" =__)
    ."        )
    ,_/   ,    \/\_
    \_|    )_-\ \_-`
    `-----` `--`
            """ + Style.RESET_ALL)
                continue
            # - Alphabet-only input
            if any(ch not in alphabet for ch in user_input.lower()):
                print(f"{Fore.RED}- PUNISHED! you can only use letters from the english alphabet (a-z).")
                print(r"""
            ((`\
            ___ \\ '--._
        .'`   `'    o  )
        /    \   '. __.'
    _|    /_  \ \_\_
      {_\______\-'\__\_\
            """ + Style.RESET_ALL)
                
                continue
            # - Word must exist in dictionary
            if user_input.lower() not in self.__PermitedWords:
                print(f"{Fore.RED}- PUNISHED! '{user_input}' is not in Bunny's list of valid words.")
                print(r"""
(\(\
( -.-)
o_(")(")
            """ + Style.RESET_ALL)
                
                continue
            # =======================================================================================

            feedback = self.bunny_feedback(victoryWord, user_input)

            if round == self.__MaxGuesses -1 and feedback != "A" * len(victoryWord):
                print(f"- BLEH! You lost! Bunny's word was: {victoryWord}")
                return
            
            print(f"- Bunny says: {feedback}")
            self.__FeedbackList.append(feedback)

            self.__TriedWords.append(user_input.lower())

            # - Validate bunny feedback only AFTER the first guess
            if len(self.__TriedWords) > 1:
                if not self.input_constrainer(user_input, feedback):
                    print(f"{Style.BRIGHT}{Fore.RED}Bunny produced invalid feedback — this should never happen. o_o {Style.RESET_ALL}")
                    self.reset_variables()
                    return

            self.assign_colors(feedback)

            if feedback == "A" * len(victoryWord):
                print(f"- ARGH!!! You win this time!...")
                return
   
    def bunny_feedback(self, answer:str, guess:str):
        # - Normalize
        answer = answer.lower()
        guess = guess.lower()

        # - Default all to X
        feedback = ["X"] * len(answer)

        # - Count how many times each letter appears in the answer
        letter_counts = {}
        for ch in answer:
            letter_counts[ch] = letter_counts.get(ch, 0) + 1

        # - FIRST PASS: Assign A (correct position)
        for i in range(len(answer)):
            if guess[i] == answer[i]:
                feedback[i] = "A"
                letter_counts[guess[i]] -= 1  # Use one occurrence

        # - SECOND PASS: Assign B (wrong position but exists)
        for i in range(len(answer)):
            if feedback[i] == "A":
                continue  # Already processed

            if guess[i] in letter_counts and letter_counts[guess[i]] > 0:
                feedback[i] = "B"
                letter_counts[guess[i]] -= 1
            else:
                feedback[i] = "X"

        return "".join(feedback)  
    def bunny_word(self):
        self.get_possibleWords()
        random_word = random.choice(self.__PermitedWords)
        return random_word  

    def reset_variables(self):
        self.__PermitedWords.clear()
        self.__TriedWords.clear()
        self.__FeedbackList.clear()

        self.__GreenLetters.clear()
        self.__YellowLetters.clear()
        self.__RedLetters.clear()

    def add_CustomWord(self):
        with open("data/wordy-data/custom-words.txt", "a") as file:
            while True:
                word = input("- Load new custom word: ").strip().lower()
                if all(letter in alphabet for letter in word) and len(word) == self.__WordsLength:
                    file.writelines(word + "\n")
                    print(f"{Fore.GREEN}- Word '{word}' saved!{Style.RESET_ALL}")
                    break
                print(f"{Fore.RED}{Style.BRIGHT}(Error){Style.NORMAL} - Enter a valid word ({self.__WordsLength} letters, English alphabet only){Style.RESET_ALL}") 
 
    @staticmethod
    def save_game(victory_word:str):
        with open("data/wordy-data/wordy-games.txt", "a") as file:
            file.writelines(victory_word + "\n")
    @staticmethod
    def reset_CustomWords():
        with open("data/wordy-data/custom-words.txt", "w"):
            pass
    @staticmethod
    def reset_matches():
        with open("data/wordy-data/wordy-games.txt", "w"):
            pass