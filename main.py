import random
import openai
import json
import argparse

# dont worry, this key is disabled :) put your own here
openai.api_key = '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' 

def get_input():
    num_characters = int(input("Enter number of characters (up to 4): "))
    characters = []
    for _ in range(min(num_characters, 4)):
        name = input("Enter character name: ")
        backstory = input(f"Enter backstory for {name}: ")
        characters.append({"name": name, "backstory": backstory})
    story_prompt = input("Enter starting prompt for the story: ")
    num_lines = int(input("Enter number of lines the story should produce: "))
    return characters, story_prompt, num_lines

def get_messages(character, context):

    # Compose the prompt to GPT API.
    prompt = f"Story so far: {context}\n"\
             "Suggest a next line of dialogue or action for your character."
    
    instructions = f"You are the character  {character['name']}. You should respond with an action or line of dialogue as this character."\
                    f"This character should act like this: {character['backstory']}"\
                    f"Return a JSON string with 2 properties, 'priority' and 'line'"\
                    f"'line' should be 1 sentence of 30 words or less, telling what {character['name']} says or does next."\
                    f"It is okay to just be a line of dialogue, but it must be written as dialogue in quotes and say who is speaking to whom."\
                    f"For instance, '\"Who are you?\" he asked her.'"\
                    f"'priority' should be a number 1-100 with how important this would be to the scene emotionally."\
                    f"Respond with only the JSON string and no explanation text."
    
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt}
    ]

    return messages

def get_narrator_messages(context):

    # Compose the prompt to GPT API.
    prompt = f"Story so far: {context}\n"\
             "Suggest a next event or action for the story."
    
    instructions = f"Return a JSON string with 2 properties, 'priority' and 'line'"\
             f"'line' should be 1 sentence of 30 words or less, telling what the narrator says next."\
             f"It should be events that happen in the scene or that affect multiple characters."\
             f"It should not just be an action taken by a single charater, and should not be dialogue."\
             f"'priority' should be a number 1-100 with how important this would be to the scene."\
             f"Respond with only the JSON string and no explanation text."
    
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt}
    ]

    return messages

def get_line(messages, defaultLine="The character did nothing"):

    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages,
          max_tokens=100,
          temperature=0.5,
          stop=None
        )
    
        output_text = response.choices[0].message.content.strip()
        
        # Attempt to load the string as JSON and extract the expected keys
        output_data = json.loads(output_text)
        line = output_data['line']
        priority = output_data['priority']
        
        return {"priority": priority, "line": line}
    
   
    except json.JSONDecodeError:
        print("Received malformed JSON.")
    except KeyError:
        print("Expected keys not found in JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    

    return {"priority": 0, "line": defaultLine}

def main():
    parser = argparse.ArgumentParser(description='Generate a story based on input characters and prompt.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file containing the story setup.')
    
    args = parser.parse_args()
    if not args.file_path:
        characters, story_prompt, num_lines = get_input()
    else:
        with open(args.file_path, 'r') as file:
            setup_data = json.load(file)
        
        story_prompt = setup_data["story_prompt"]
        characters = setup_data["characters"]
        num_lines = setup_data["num_lines"]

    story = [story_prompt]

    # give bonuses for characters who haven't talked in a while
    speaker_priority_bonuses = { c['name']:0 for c in characters }
    speaker_priority_bonuses['narrator'] = 0

    for _ in range(num_lines):
        candidate_lines = []

        # Limit the context to the initial prompt and the last 100 lines to prevent exceeding max token limit.
        context = [story_prompt] + story[-50:]
        context_str = " ".join(context)

        for char in characters:
            prompt = get_messages(char, context_str)
            candidate_line = get_line(prompt)
            candidate_line['priority'] += speaker_priority_bonuses[char['name']]
            candidate_line['speaker'] = char['name']

            print(f"CANDIDATE: {char['name']}: {candidate_line['line']} (Priority: {candidate_line['priority']})")
            candidate_lines.append(candidate_line)

        # Additional entry for the narrator
        narrator_prompt = get_narrator_messages(context_str)
        narrator_line = get_line(narrator_prompt)
        narrator_line['priority'] += speaker_priority_bonuses['narrator']
        narrator_line['speaker'] = 'narrator'

        print(f"CANDIDATE: Narrator: {narrator_line['line']} (Priority: {narrator_line['priority']})")

        candidate_lines.append(narrator_line)

        # Choose highest priority line
        highest_priority = max(candidate_lines, key=lambda x: x['priority'])
        high_priority_lines = [line for line in candidate_lines if line['priority'] == highest_priority['priority']]

        chosen_line = random.choice(high_priority_lines)

        # increment each value in speaker_priority_bonuses by 10
        for speaker in speaker_priority_bonuses:
            speaker_priority_bonuses[speaker] += 10
        
        speaker_priority_bonuses[ chosen_line['speaker'] ] = 0 # reset this speaker

        print(f"-----\nCHOSEN LINE: {chosen_line}")
        print(f"=======================")
        story.append(chosen_line['line'])



    # Save to output file
    with open("output_story.txt", "w") as f:
        f.write("CHARACTERS\n")
        for character in characters:
            f.write(f"{character['name']}: {character['backstory']}\n")
        f.write("\n\nSTORY\n")
        for line in story:
            f.write(line + "\n")

if __name__ == "__main__":
    main()
