import json

class DatasetManager:
    def __init__(self, input_file, output_file):
        """
        Initializes the DatasetManager.

        Args:
            input_file (str): Path to the input text file.
            output_file (str): Path to the output JSON file.
        """
        self.input_file = input_file
        self.output_file = output_file
        
        # Expanded sections based on Propp’s functions
        self.sections = [
            "introduction", "hero_departure", "first_challenge", 
            "mentor_appearance", "main_conflict", "climax", "resolution"
        ]

    def process_text(self):
        """
        Reads a text file and converts it into a structured dataset.

        Returns:
            list: A list of dictionaries, where each dictionary represents a structured story.
        """
        dataset = []
        try:
            with open(self.input_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line:  # Ignore empty lines
                    story_parts = line.split(". ")
                    story_parts = [part.strip() for part in story_parts if part.strip()]  # Remove empty parts
                    
                    # Ensure the story has enough parts for all sections
                    story = {self.sections[i]: story_parts[i] if i < len(story_parts) else "" for i in range(len(self.sections))}
                    dataset.append(story)

        except FileNotFoundError:
            print(f"❌ Error: Input file '{self.input_file}' not found.")
        except Exception as e:
            print(f"❌ Error processing text: {e}")

        return dataset

    def save_to_json(self, dataset):
        """
        Saves the processed dataset to a JSONL file.

        Args:
            dataset (list): The dataset to save.
        """
        try:
            with open(self.output_file, "w", encoding="utf-8") as file:
                for entry in dataset:
                    file.write(json.dumps(entry, ensure_ascii=False) + "\n")  # JSONL format (one JSON per line)
            print(f"✅ Dataset saved to {self.output_file}")
        except Exception as e:
            print(f"❌ Error saving dataset: {e}")

# Example usage:
if __name__ == "__main__":
    manager = DatasetManager("story.txt", "dataset.jsonl")
    dataset = manager.process_text()
    manager.save_to_json(dataset)
