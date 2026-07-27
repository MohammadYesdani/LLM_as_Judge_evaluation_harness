# 40 test questions with deliberate variety:
# easy facts, reasoning, math, writing, and a few hard ones
# where a weaker model is likely to stumble.

PROMPTS = [
    "What is the capital of Japan?",
    "How many continents are there on Earth?",
    "What gas do plants absorb from the air for photosynthesis?",
    "Who wrote the play Romeo and Juliet?",
    "What is the boiling point of water at sea level in Celsius?",
    "Explain why the sky appears blue, in two sentences.",
    "Explain the difference between weather and climate.",
    "In simple terms, what is compound interest?",
    "Why does ice float on water?",
    "What causes the seasons to change on Earth?",
    "A shirt costs $40 and is discounted by 25%. What is the final price?",
    "If a train travels 60 km in 45 minutes, what is its speed in km/h?",
    r"What is 15% of 240?",
    "I have 3 apples and buy 2 more bags with 4 apples each. How many apples total?",
    "A rectangle is 8 cm long and 5 cm wide. What is its area and perimeter?",
    "If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?",
    "Sarah is twice as old as Tom. In 5 years their ages sum to 40. How old is each now?",
    "Write a 4-line poem about the ocean at night.",
    "Write a short, polite email declining a meeting invitation.",
    "Suggest three creative names for a coffee shop aimed at students.",
    "Write a two-sentence product description for a reusable water bottle.",
    "Rewrite this sentence to be more formal: 'Hey, can you send me that file real quick?'",
    "Summarize the water cycle in three sentences.",
    "Explain what an API is to someone who has never coded.",
    "What are the main differences between a list and a dictionary in Python?",
    "Write a Python function that returns whether a number is even.",
    "What does the word 'ubiquitous' mean, and use it in a sentence.",
    "List three pros and three cons of remote work.",
    "Explain the concept of supply and demand with a simple example.",
    "What is the difference between a virus and bacteria?",
    "A farmer has chickens and cows totaling 20 animals and 56 legs. How many of each?",
    "Explain recursion in programming using a real-world analogy.",
    "What are three practical tips for improving sleep quality?",
    "Translate 'Good morning, how are you?' into French.",
    "Explain the difference between correlation and causation with an example.",
    "If today is Wednesday, what day will it be 100 days from now?",
    "Write a haiku about autumn leaves.",
    "What is the greenhouse effect, and why does it matter?",
    "Give step-by-step instructions to make a basic peanut butter sandwich.",
    "Explain why dividing by zero is undefined in mathematics.",
]

# A quick sanity check you can run: python prompts.py
if __name__ == "__main__":
    print(f"Loaded {len(PROMPTS)} prompts.")
    print("First one:", PROMPTS[0])