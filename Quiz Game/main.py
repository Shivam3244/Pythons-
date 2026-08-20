import json
import random
from pathlib import Path

QUESTIONS_FILE = Path("questions.json")

def load_questions():
    with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_questions(questions):
    with QUESTIONS_FILE.open("w", encoding="utf-8") as file:
        json.dump(questions, file, indent=4, ensure_ascii=False)

def generate_questions():
    return [
        {
            "question": "Which language is used to create this project?",
            "options": ["Python", "Java", "C++", "HTML"],
            "answer": "Python"
        },
        {
            "question": "Which data structure stores key-value pairs in Python?",
            "options": ["List", "Tuple", "Dictionary", "Set"],
            "answer": "Dictionary"
        },
        {
            "question": "What is the extension of a Python file?",
            "options": [".java", ".py", ".cpp", ".html"],
            "answer": ".py"
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "func", "define"],
            "answer": "def"
        },
        {
            "question": "Which module is commonly used for generating random choices in Python?",
            "options": ["random", "math", "os", "time"],
            "answer": "random"
        }
    ]

def play_quiz():
    questions = load_questions()
    random.shuffle(questions)
    score = 0

    print("\n===== PYTHON QUIZ GAME =====")
    print(f"Total Questions: {len(questions)}\n")

    for number, item in enumerate(questions, 1):
        print(f"Q{number}. {item['question']}")
        for index, option in enumerate(item["options"], 1):
            print(f"  {index}. {option}")

        while True:
            try:
                choice = int(input("Your answer: "))
                if 1 <= choice <= len(item["options"]):
                    break
                print("Please choose a valid option.")
            except ValueError:
                print("Please enter a number.")

        selected = item["options"][choice - 1]
        if selected == item["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. Correct answer: {item['answer']}\n")

    percentage = (score / len(questions)) * 100 if questions else 0
    print("===== QUIZ RESULT =====")
    print(f"Score: {score}/{len(questions)}")
    print(f"Percentage: {percentage:.2f}%")

    if percentage >= 80:
        print("Excellent performance!")
    elif percentage >= 50:
        print("Good effort! Keep practicing.")
    else:
        print("Keep learning and try again.")

def main():
    if not QUESTIONS_FILE.exists():
        save_questions(generate_questions())

    while True:
        print("\n1. Start Quiz")
        print("2. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            play_quiz()
        elif choice == "2":
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
