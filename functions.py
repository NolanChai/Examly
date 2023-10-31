# Import necessary libraries and modules
from PyPDF2 import PdfMerger, PdfReader  # Library for PDF operations
import openai                            # Library for OpenAI GPT-3 API
import re                                # Library for regular expression operations

# Function to merge multiple PDF files into a single file
def merge_files(filenames: list, merged_filename: str):
    merger = PdfMerger()  # Create a PDF merger object
    for filename in filenames:
        merger.append(filename)  # Append each PDF file to the merger
    merger.write(merged_filename + '.pdf')  # Write the merged content to a new file
    merger.close()  # Close the merger

# Function to add a prompt before a given text
def add_prompt(text_file: str):
    prompt_intro = 'Generate new questions based on the following questions, in the format of 1., 2. etc. Do not answer them:'
    final_query = prompt_intro + '\n' + text_file
    return final_query

# Function to extract text from a PDF file
def textify(filename: str):
    pdf_file = open(filename, 'rb')  # Open the PDF in binary reading mode
    read_pdf = PdfReader(pdf_file)   # Read the PDF content
    fulltext = ""                    # Initialize an empty string to store the extracted text
    for page in read_pdf.pages:
        part = page.extract_text()   # Extract text from each page
        fulltext += part            # Add the extracted text to the fulltext string
    return fulltext

# Class to generate questions using the OpenAI GPT-3 API
class QuestionGenerator:
    def __init__(self, model_engine, openai_api_key):
        self.model_engine = model_engine       # Set the model engine (e.g., "text-davinci-003")
        self.openai_api_key = openai_api_key   # Set the API key for OpenAI

    # Function to generate questions based on a provided prompt
    def generate_questions(self, prompt, max_tokens, temperature, top_p, frequency_penalty, presence_penalty):
        """
        Generates questions based on the prompt provided.
        """
        openai.api_key = self.openai_api_key  # Set the OpenAI API key
        completion = openai.Completion.create(  # Generate a completion using the OpenAI API
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        response = completion.choices[0].text  # Extract the generated text from the response
        return response

# Function to add newlines between questions for readability
def add_newlines(text):
    # Find all occurrences of patterns like "1. " in the text
    matches = re.finditer(r'\d+\.\s', text)
    indices = [match.start() for match in matches]

    # Split the text based on the indices found
    result = [text[i:j] for i, j in zip([0] + indices, indices + [None])][1:]
    final_list = []
    for elem in result:
        # Remove the numbering (e.g., "1. ") from each question
        final_list.append(re.sub(r'\d+\.\s', '', elem, count=1))

    return final_list
