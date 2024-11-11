# LangChain Learning

This project documents my learning journey with LangChain, featuring incremental updates saved in separate files.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)

## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/dev-arctik/LangChain-Learning.git
    cd LangChain_Learning
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```
      
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Setup

To run the code effectively, create a `.env` file in the root directory to store your API key. This is necessary for using the OpenAI models.

Create a `.env` file and add the following line:

```plaintext
OPENAI_API_KEY='your_openai_api_key_here'
```
Replace 'your_openai_api_key_here' with your actual OpenAI API key.

Note: If you choose to use a different LLM (Language Learning Model), refer to the LangChain documentation and adjust the code as needed.

## Usage

You can run individual files with the following command:
```bash
python [file_name.py]
```
