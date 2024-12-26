from openai import OpenAI
import os
import json
from datetime import datetime
import time
import sys
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()

# Only import readline on non-Windows platforms
try:
    import readline
except ImportError:
    pass  # readline not available on Windows

class TerminalChatbot:
    def __init__(self):
        # Get API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("No API key found. Please set OPENAI_API_KEY in .env file")
            
        self.client = OpenAI(api_key=api_key)
        self.conversation_history: List[Dict] = []
        self.model = "gpt-3.5-turbo"
        self.max_retries = 3
        self.conversation_file = "conversation_history.json"
        self.settings = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "presence_penalty": 0.6,
            "frequency_penalty": 0.5
        }

    # ... [rest of your class code stays the same] ...

def main():
    # Clear screen at startup
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        chatbot = TerminalChatbot()
        
        # Welcome message
        print("\n=== Welcome to Enhanced Terminal Chatbot ===")
        print("Type !help for available commands")
        print("Type !quit or press Ctrl+C to exit")
        print("==========================================\n")

        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle empty input
                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("!"):
                    if not chatbot.handle_command(user_input):
                        print("\nGoodbye!")
                        break
                    continue

                # Get and display response
                print("\nChatbot is thinking...")
                response = chatbot.get_response(user_input)
                print(f"\nChatbot: {response}")
                
                # Update conversation history
                chatbot.update_history(user_input, response)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                
    except Exception as e:
        print(f"Failed to initialize chatbot: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()