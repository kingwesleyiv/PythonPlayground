import random

options = [1, 2, 3]
score = 0
runs = 0

def get_user_input():
    print("Choose a door between 1 and 3: ")
    try:
        user_input = int(random.randint(1,3))
        if 1 <= user_input <= 3:
            print(f"{user_input}")
            return user_input
        else:
            print("Please enter a number between 1 and 3:")
    except ValueError:
        print("Please enter a valid number.")

def reveal_incorrect_answer(correct_number, user_choice):
    incorrect_answer = 0
    if user_choice == correct_number:
        options.remove(user_choice)
        incorrect_answer = random.choice(options)
        options.append(user_choice)
    else:
        options.remove(user_choice)
        options.remove(correct_number)
        incorrect_answer = random.choice(options)
        options.append(user_choice)
        options.append(correct_number)
    print(f"Door number {incorrect_answer} was incorrect.")
    return incorrect_answer

def switch_answer(user_choice, incorrect_answer):
    print("Would you like to switch your answer? (y/n): ")

    choice = 1 #random.randint(0,1)

    if choice == 1:
        options.remove(user_choice)
        options.remove(incorrect_answer)
        new_answer = options[0]
        options.append(user_choice)
        options.append(incorrect_answer)
        print(f"You switched your answer to {new_answer}.")
        return new_answer
    else:
        print("You did NOT switch.")
        return user_choice

def check_answer(correct_number, final_choice):
    if final_choice == correct_number:
        print("Congratulations! Your answer is correct.")
        return 1
    else:
        print("Sorry, your answer is incorrect.")
        return 0

def main():
    correct_number = random.randint(1,3)
    user_choice = get_user_input()
    incorrect_answer = reveal_incorrect_answer(correct_number, user_choice)
    final_choice = switch_answer(user_choice, incorrect_answer)
    return check_answer(correct_number, final_choice)

for i in range(10000):
    score += main()
    runs += 1
    print(f"Test number {i+1}. Choices; {options}. Beginning Next Test.")

input(f"The test has completed. The Score is: {score} Correct Answers out of {runs} Tests ({(score/runs)*100}%)")