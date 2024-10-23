import openai
import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAIError

# Load environment variables from the .env file
load_dotenv()

# Get the OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the JSON schema without the 'creator' field
json_schema = {
    "type": "object",
    "properties": {
        "columns": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "List of column names for the data"
        },
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Perfume brand name"
                    },
                    "perfume_name": {
                        "type": "string",
                        "description": "Name of the perfume"
                    },
                    "descriptors": {
                        "type": "string",
                        "description": "Key descriptive phrases"
                    }
                },
                "required": ["brand", "perfume_name", "descriptors"],
                "additionalProperties": False
            },
            "description": "List of perfume data extracted"
        }
    },
    "required": ["columns", "data"],
    "additionalProperties": False
}

def extract_entities_and_phrases(text):
    """
    Use OpenAI's ChatGPT API to extract entities (perfume brands, product names) 
    and descriptive phrases from text, formatted according to the provided schema.
    """
    prompt = f"Extract perfume brand names, perfume product names, and key descriptive phrases from the following text. Format the descriptors as a list of comma-separated values:\n\n{text}"
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You're an expert in perfume descriptions."},
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "perfume_data",
                    "schema": json_schema,
                    "strict": True
                }
            }
        )

        # Correct response handling
        return response.choices[0].message.content

    except OpenAIError as e:
        print(f"An error occurred: {e}")
        return None

def process_files(input_folder, output_folder):
    """
    Process JSON files in a folder, extracting perfume brands, products, and phrases 
    using ChatGPT, and save the results.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing {file_path}...")

            # Load the JSON data
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Extract entities and key phrases using ChatGPT
            result = extract_entities_and_phrases(data.get("combined_text", ""))

            if result:
                # Save the extracted information directly in JSON format
                output_file_path = os.path.join(output_folder, file_name)
                with open(output_file_path, 'w') as output_file:
                    # Assuming `result` is already a valid JSON structure (dictionary or list)
                    output_file.write(result)
                print(f"Saved results to {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Extract perfume brands, product names, and descriptive phrases using OpenAI GPT")
    parser.add_argument("input_folder", type=str, help="Path to folder containing the combined JSON files")
    parser.add_argument("output_folder", type=str, help="Path to folder to save the results")

    args = parser.parse_args()
    
    # Process all files
    process_files(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()