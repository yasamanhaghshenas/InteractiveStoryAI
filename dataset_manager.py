import json

class DatasetManager:
    def init(self, input_file, output_file):
        """
        Initializes the DatasetManager.

        Args:
            input_file (str): Path to the input text file.
            output_file (str): Path to the output JSON file.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.sections = ["introduction", "challenge", "resolution"]

    def process_text(self):
        """
        Reads a text file and converts it into a structured dataset.

        Returns:
            list: A list of dictionaries, where each dictionary represents a story.
        """
        dataset = []
        try:
            with open(self.input_file, "r") as file:
                lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line:  # Ignore empty lines
                    story_parts = line.split(".")
                    story_parts = [part.strip() for part in story_parts if part.strip()]  # Remove empty parts
                    
                    # Ensure the story has enough parts for all sections
                    if len(story_parts) >= len(self.sections):
                        story = {self.sections[i]: story_parts[i] for i in range(len(self.sections))}
                        dataset.append(story)
                    else:
                        print(f"Warning: Skipping incomplete story: {line}")

        except FileNotFoundError:
            print(f"Error: Input file '{self.input_file}' not found.")
        except Exception as e:
            print(f"Error processing text: {e}")

        return dataset

    def save_to_json(self, dataset):
        """
        Saves the processed dataset to a JSON file.

        Args:
            dataset (list): The dataset to save.
        """
        try:
            with open(self.output_file, "w") as file:
                json.dump(dataset, file, indent=4)
            print(f"Dataset saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving dataset to JSON: {e}")

# Example usage:
if name == "main":
    manager = DatasetManager("story.txt", "dataset.json")
    dataset = manager.process_text()
    manager.save_to_json(dataset)