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

Example `story_setup.json`:

```json
{
    "story_prompt": "Once upon a time...",
    "characters": [
        {"name": "Alice", "backstory": "A curious adventurer."},
        {"name": "Bob", "backstory": "A skeptical scientist."}
    ],
    "num_lines": 5
}

### Run the Generator

`python story_generator.py story_setup.json`

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
