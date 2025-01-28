from transformers import pipeline

# Load the GPT-2 model for text generation
story_generator = pipeline("text-generation", model="gpt2")

# Define Propp's narrative functions (simplified for demonstration)
propp_functions = [
    "A hero is introduced in their ordinary world.",
    "A villain appears and creates a disturbance.",
    "The hero receives a call to adventure.",
    "The hero meets a mentor or receives magical assistance.",
    "The hero faces tests, allies, and enemies.",
    "The hero confronts the villain in a climactic battle.",
    "The hero achieves their goal and returns home transformed."
]

def generate_propp_based_story(user_prompt):
    """
    Generates a story based on Propp's narrative functions and user input.

    Args:
        user_prompt (str): The initial idea or prompt provided by the user.

    Returns:
        str: The complete generated story.
    """
    story = ""  # Initialize the story as an empty string

    for function in propp_functions:
        try:
            # Combine Propp's function with the user's prompt
            prompt = f"{function} {user_prompt}"
            
            # Generate a story segment using GPT-2
            generated = story_generator(
                prompt,
                max_length=100,
                truncation=True,  # Ensure the output doesn't exceed max length
                num_return_sequences=1
            )[0]["generated_text"]
            
            # Add the generated segment to the story
            story += generated.strip() + "\n\n"
        except Exception as e:
            print(f"Error generating text for '{function}': {e}")

    return story

if __name__ == "__main__":
    # Prompt the user for an initial story idea
    user_prompt = input("Enter a starting idea for your story (e.g., 'Once upon a time, there was a brave knight...'): ")

    # Generate the story
    print("\nGenerating your story...\n")
    story = generate_propp_based_story(user_prompt)

    # Output the full story
    print("Your Generated Story:\n")
    print(story)
