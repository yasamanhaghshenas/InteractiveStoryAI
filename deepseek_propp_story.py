import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os


os.environ['HF_HOME'] = 'D:/huggingface_cache' 
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'  # Disable symlink warning

# Use the smallest CPU-compatible DeepSeek variant
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"

try:
    # Load model directly to CPU with memory optimizations
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map={"": "cpu"},  # Force CPU-only
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
        offload_folder="D:/huggingface_cache/offload"  # Custom offload directory
    )
    print("Model loaded successfully on CPU!")

except Exception as e:
    print(f"Error loading model: {e}")
    print("\nTroubleshooting steps:")
    print("1. Ensure you have at least 8GB of free RAM")
    print("2. Verify drive D: has 5GB+ free space")
    print("3. Close other memory-intensive applications")
    print("4. Try running with --trust-remote-code flag if supported")
    exit()

# Propp's narrative functions
PROPP_FUNCTIONS = [
    "A hero is introduced in their ordinary world.",
    "A villain appears and creates a disturbance.",
    "The hero receives a call to adventure.",
    "The hero meets a mentor or receives magical assistance.",
    "The hero faces tests, allies, and enemies.",
    "The hero confronts the villain in a climactic battle.",
    "The hero achieves their goal and returns home transformed."
]

def generate_story_segment(prompt: str) -> str:
    """Generate story segment with proper attention masking"""
    try:
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            max_length=256,
            truncation=True,
            padding='max_length'  # Add fixed-length padding
        )

        # Explicitly create attention mask
        attention_mask = inputs.attention_mask

        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=attention_mask,  # Pass explicit attention mask
            max_new_tokens=150,
            temperature=0.8,
            top_p=0.85,
            repetition_penalty=1.15,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,  # Ensure proper pad token
            num_return_sequences=1
        )

        # Decode with original prompt cleanup
        full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return full_text.replace(prompt, "").strip()
    
    except Exception as e:
        print(f"Generation error: {e}")
        return None

def generate_propp_based_story(user_prompt: str) -> str:
    """Generate story with memory-safe iterations"""
    story = []
    
    for idx, function in enumerate(PROPP_FUNCTIONS, 1):
        prompt = f"Create a SHORT story part ({idx}/7) containing:\n1. {function}\n2. {user_prompt}\nKeep under 3 paragraphs."
        
        print(f"Generating part {idx}...")
        
        # Clear memory between generations
        with torch.no_grad():
            segment = generate_story_segment(prompt)
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        if segment:
            # Remove duplicate prompts
            clean_segment = segment.replace(prompt, "").strip()
            story.append(f"### Part {idx}: {function}\n{clean_segment}")
        else:
            story.append(f"### Part {idx}: [Segment generation failed]")
    
    return "\n\n".join(story)

if __name__ == "__main__":
    user_theme = input("Enter your story theme (be specific): ")
    
    print("\nStarting generation (this may take 10-15 minutes on CPU)...")
    final_story = generate_propp_based_story(user_theme)
    
    print("\n" + "="*60 + "\nFinal Story\n" + "="*60)
    print(final_story)
    print("\n" + "="*60 + "\nCompleted!")