import random
import re
from collections import Counter
import time

class SmartWordGuessingGame:
    """
    An AI-powered word guessing game that learns from player patterns
    and adapts difficulty based on performance
    """
    
    def __init__(self):
        # Word database categorized by difficulty
        self.word_categories = {
            'easy': ['cat', 'dog', 'sun', 'car', 'book', 'tree', 'fish', 'bird', 'moon', 'star'],
            'medium': ['python', 'computer', 'rainbow', 'elephant', 'butterfly', 'mountain', 'ocean', 'galaxy'],
            'hard': ['algorithm', 'artificial', 'intelligence', 'programming', 'technology', 'creativity', 'philosophy']
        }
        
        # AI learning components
        self.player_stats = {
            'games_played': 0,
            'total_guesses': 0,
            'correct_letters': 0,
            'wrong_letters': 0,
            'average_time': 0,
            'preferred_letters': Counter(),
            'difficulty_success': {'easy': 0, 'medium': 0, 'hard': 0}
        }
        
        # Current game state
        self.current_word = ""
        self.guessed_letters = set()
        self.wrong_guesses = []
        self.max_wrong = 6
        self.difficulty = 'easy'
        self.start_time = 0
        
    def analyze_player_performance(self):
        """AI function to analyze player performance and adapt difficulty"""
        if self.player_stats['games_played'] == 0:
            return 'easy'
        
        # Calculate success rate
        avg_guesses = self.player_stats['total_guesses'] / self.player_stats['games_played']
        success_rate = self.player_stats['correct_letters'] / max(1, self.player_stats['total_guesses'])
        
        # AI decision making for difficulty adjustment
        if success_rate > 0.8 and avg_guesses < 8:
            if self.difficulty == 'easy':
                return 'medium'
            elif self.difficulty == 'medium':
                return 'hard'
        elif success_rate < 0.4:
            if self.difficulty == 'hard':
                return 'medium'
            elif self.difficulty == 'medium':
                return 'easy'
        
        return self.difficulty
    
    def ai_hint_generator(self):
        """AI-powered hint system based on word analysis"""
        if not self.current_word:
            return "No word selected yet!"
        
        # Analyze word patterns
        vowels = set('aeiou')
        consonants = set('bcdfghjklmnpqrstvwxyz')
        
        word_vowels = [c for c in self.current_word.lower() if c in vowels]
        word_consonants = [c for c in self.current_word.lower() if c in consonants]
        
        hints = []
        
        # Pattern-based hints
        if len(self.current_word) <= 4:
            hints.append(f"This is a short word with {len(self.current_word)} letters")
        elif len(self.current_word) >= 8:
            hints.append(f"This is a long word with {len(self.current_word)} letters")
        else:
            hints.append(f"This word has {len(self.current_word)} letters")
        
        # Letter frequency hints
        if len(word_vowels) > len(word_consonants):
            hints.append("This word has more vowels than consonants")
        else:
            hints.append("This word has more consonants than vowels")
        
        # Common letter hints based on player history
        if self.player_stats['preferred_letters']:
            common_player_letters = set(self.player_stats['preferred_letters'].most_common(5))
            word_letters = set(self.current_word.lower())
            overlap = common_player_letters.intersection(word_letters)
            
            if overlap:
                hints.append(f"This word contains some letters you often guess: {', '.join(list(overlap)[:2])}")
        
        return random.choice(hints) if hints else "Try guessing common letters like 'e', 'a', 'r', 's', 't'"
    
    def smart_word_selection(self):
        """AI selects words based on player performance and learning"""
        difficulty = self.analyze_player_performance()
        self.difficulty = difficulty
        
        available_words = self.word_categories[difficulty].copy()
        
        # Remove recently played words to avoid repetition
        if hasattr(self, 'recent_words'):
            available_words = [w for w in available_words if w not in self.recent_words]
        
        if not available_words:
            available_words = self.word_categories[difficulty]
        
        # AI word selection based on player's letter preferences
        if self.player_stats['preferred_letters'] and len(available_words) > 1:
            # Score words based on player's preferred letters
            word_scores = {}
            for word in available_words:
                score = sum(self.player_stats['preferred_letters'][letter] for letter in word.lower())
                word_scores[word] = score
            
            # Select from top-scored words with some randomness
            top_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            selected_word = random.choice([word for word, _ in top_words])
        else:
            selected_word = random.choice(available_words)
        
        self.current_word = selected_word.upper()
        
        # Track recent words
        if not hasattr(self, 'recent_words'):
            self.recent_words = []
        self.recent_words.append(selected_word)
        if len(self.recent_words) > 5:
            self.recent_words.pop(0)
    
    def display_word_progress(self):
        """Display current progress of word guessing"""
        display = ""
        for letter in self.current_word:
            if letter.upper() in self.guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        return display.strip()
    
    def display_hangman(self):
        """Visual representation of wrong guesses"""
        stages = [
            "  +---+\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n  |   |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|   |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n========="
        ]
        return stages[len(self.wrong_guesses)]
    
    def update_ai_learning(self, letter, is_correct):
        """Update AI learning based on player's guesses"""
        self.player_stats['preferred_letters'][letter.lower()] += 1
        
        if is_correct:
            self.player_stats['correct_letters'] += 1
        else:
            self.player_stats['wrong_letters'] += 1
    
    def play_game(self):
        """Main game loop"""
        print("🎮 Welcome to the AI Smart Word Guessing Game! 🎮")
        print("The AI learns from your playing style and adapts!")
        print("-" * 50)
        
        while True:
            # Initialize new game
            self.smart_word_selection()
            self.guessed_letters = set()
            self.wrong_guesses = []
            self.start_time = time.time()
            
            print(f"\n🎯 New Game! Difficulty: {self.difficulty.upper()}")
            print(f"Word: {self.display_word_progress()}")
            print(f"Category: {len(self.current_word)} letters")
            
            game_won = False
            
            # Game loop
            while len(self.wrong_guesses) < self.max_wrong and not game_won:
                print(f"\n{self.display_hangman()}")
                print(f"Word: {self.display_word_progress()}")
                print(f"Wrong guesses: {', '.join(self.wrong_guesses) if self.wrong_guesses else 'None'}")
                print(f"Guesses remaining: {self.max_wrong - len(self.wrong_guesses)}")
                
                # AI hint system
                if len(self.wrong_guesses) >= 3:
                    print(f"💡 AI Hint: {self.ai_hint_generator()}")
                
                # Get player input
                guess = input("\nGuess a letter (or 'hint' for help, 'quit' to exit): ").upper().strip()
                
                if guess == 'QUIT':
                    print("Thanks for playing! 👋")
                    return
                elif guess == 'HINT':
                    print(f"💡 AI Hint: {self.ai_hint_generator()}")
                    continue
                elif len(guess) != 1 or not guess.isalpha():
                    print("❌ Please enter a single letter!")
                    continue
                elif guess in self.guessed_letters:
                    print("❌ You already guessed that letter!")
                    continue
                
                # Process guess
                self.guessed_letters.add(guess)
                
                if guess in self.current_word.upper():
                    print(f"✅ Great! '{guess}' is in the word!")
                    self.update_ai_learning(guess, True)
                    
                    # Check if word is complete
                    if all(letter.upper() in self.guessed_letters for letter in self.current_word):
                        game_won = True
                else:
                    print(f"❌ Sorry, '{guess}' is not in the word.")
                    self.wrong_guesses.append(guess)
                    self.update_ai_learning(guess, False)
            
            # Game end
            game_time = time.time() - self.start_time
            self.player_stats['games_played'] += 1
            self.player_stats['total_guesses'] += len(self.guessed_letters)
            self.player_stats['average_time'] = (self.player_stats['average_time'] + game_time) / 2
            
            if game_won:
                print(f"\n🎉 Congratulations! You guessed '{self.current_word}' correctly!")
                self.player_stats['difficulty_success'][self.difficulty] += 1
            else:
                print(f"\n💀 Game Over! The word was '{self.current_word}'")
                print(self.display_hangman())
            
            # Display AI insights
            print(f"\n📊 AI Performance Analysis:")
            print(f"Games played: {self.player_stats['games_played']}")
            print(f"Average guesses per game: {self.player_stats['total_guesses'] / self.player_stats['games_played']:.1f}")
            print(f"Success rate: {(self.player_stats['correct_letters'] / max(1, self.player_stats['total_guesses']) * 100):.1f}%")
            print(f"Your most used letters: {', '.join([letter for letter, _ in self.player_stats['preferred_letters'].most_common(5)])}")
            
            # Play again?
            play_again = input("\nPlay again? (y/n): ").lower().strip()
            if play_again != 'y':
                print("\n🤖 AI Learning Summary:")
                print(f"Total games: {self.player_stats['games_played']}")
                print(f"Preferred difficulty based on performance: {self.analyze_player_performance()}")
                print("Thanks for helping me learn! 🧠✨")
                break

# Run the game
if __name__ == "__main__":
    game = SmartWordGuessingGame()
    game.play_game()