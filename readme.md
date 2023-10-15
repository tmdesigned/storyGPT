# Story Generator with GPT-3.5 Turbo

## Overview

This project utilizes OpenAI's GPT-3.5 Turbo to generate a collaborative story with multiple characters and a narrator. The characters, each with a unique backstory, and narrators propose lines of dialogue or action, which are evaluated for emotional or contextual impact and then integrated into the evolving story based on priority. The highest priority proposal is chosen each round to create a coherent and engaging narrative.

## Prerequisites

- Python 3.x
- [OpenAI Python package](https://beta.openai.com/docs/api-reference/introduction)

Ensure you have OpenAI API credentials:
- Visit [OpenAI](https://beta.openai.com/signup/) to create an account and obtain API keys.

## Installation

1. **Clone the Repository**
2. **Install Dependencies**

    ```bash
    pip install openai
    ```
3. **Configure API Key**

    Add your OpenAI API key to main.py
    WARNING -- this uses a lot of API messages (1 per character and narrator per line of the story)

## Usage

### Create Story Setup File

Create a JSON file containing the initial story setup including characters and the first line of the story.

Example `cheese.json`:

```json
{
    "story_prompt": "Taylor the robot is alone on a derelict spaceship. One day, he hears a noise from under his charging station.",
    "characters": [
        {"name": "Taylor", "backstory": "Taylor is a lonely, rusty old robot. He carries on out of a sense of duty. Taylor only talks in very short sentences."},
        {"name": "Cheese", "backstory": "Cheese is a frightened mouse. Cheese cannot talk. Cheese is hungry."},
        {"name": "Ship", "backstory": "Ship is a spaceship AI. Ship can talk and is sarcastic. Ship has no body. Ship is bitter about being a ship."}
    ],
    "num_lines": 10
}
```

### Run the Generator

`python main.py cheese.json`

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
