import json

class DatasetManager:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.sections = ["introduction", "challenge", "resolution"]

    def process_text(self):
        """Reads a text file and converts it into a structured dataset."""
        dataset = []
        with open(self.input_file, "r") as file:
            lines = file.readlines()

        for line in lines:
            if len(line.strip()) > 0:  # Ignore empty lines
                story_parts = line.strip().split(".")
                if len(story_parts) >= len(self.sections):
                    story = {self.sections[i]: story_parts[i].strip() for i in range(len(self.sections))}
                    dataset.append(story)

        return dataset

    def save_to_json(self, dataset):
        """Saves the processed dataset to a JSON file."""
        with open(self.output_file, "w") as file:
            json.dump(dataset, file, indent=4)

        print(f"Dataset saved to {self.output_file}")

# Example usage:
if __name__ == "__main__":
    manager = DatasetManager("story.txt", "dataset.json")
    dataset = manager.process_text()
    manager.save_to_json(dataset)
