import re
import openai
from time import time, sleep
from halo import Halo
import textwrap
import yaml


###     file operations


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()


###     API functions


def chatbot(conversation, model="gpt-4-0613", temperature=0, max_tokens=2000):
    max_retry = 7
    retry = 0
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            
            response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
            text = response['choices'][0]['message']['content']

            spinner.stop()
            
            return text, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            exit(5)


def chat_print(text):
    formatted_lines = [textwrap.fill(line, width=120, initial_indent='    ', subsequent_indent='    ') for line in text.split('\n')]
    formatted_text = '\n'.join(formatted_lines)
    print('\n\n\nCHATBOT:\n\n%s' % formatted_text)


if __name__ == '__main__':
    openai.api_key = open_file('key_openai.txt').strip()
    
    prompts = ['Generate an outline of this chapter as it is right now. Make sure to use a numbered and nested list in markdown format. Capture all the main points and details.',
    'Brainstorm a list of topics, concepts, anecdotes, evidence, and examples that could be added to this chapter to flesh it out better.',
    'Create a new and expanded outline by adding in the above brainstormed items. Make sure to preserve the markdown format of a numbered and nested outline. The goal is to create a comprehensive new outline that will result in a fully fleshed out chapter.',
    'Draft a new version of the chapter based upon this new outline. Take as much time and space as needed to fully articulate it. The goal is to greatly expand the word count and get everything on the page.',]
    conversation = list()
    conversation.append({'role': 'system', 'content': open_file('input.txt')})

    for p in prompts:
        conversation.append({'role': 'user', 'content': p})
        print('\n\n\nUSER: %s' % p)
        response, tokens = chatbot(conversation)
        conversation.append({'role': 'assistant', 'content': response})
        print('\n\n\nCHATBOT:\n%s' % response)
    
    save_file('output.txt', response)