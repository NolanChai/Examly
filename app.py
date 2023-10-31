# Import necessary libraries
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import openai
from functions import *
from dotenv import dotenv_values

# Initialize Flask app
app = Flask(__name__)

# Load API key from .env file
config = dotenv_values(".env")
openai.api_key = config['API-KEY']

# Define OpenAI model engine
model_engine = "text-davinci-003"

# Define the home route
@app.route('/')
def home():
    """Render the main page."""
    return render_template("index.html")

@app.route('/upload', methods=['post'])
def upload():
    """Handle file uploads and process them."""
    
    # Initialize an empty response
    response_with_endlines = ""
    
    # Check if the request method is POST
    if request.method == 'POST':
        
        # Get the uploaded files
        img = request.files.getlist('file')
        
        # If files are uploaded
        if img:
            filenames = []
            
            # Save each uploaded file and keep track of their names
            for elem in img:
                file_name = secure_filename(elem.filename)
                elem.save(file_name)
                filenames.append(file_name)
            
            # Merge files if necessary
            merged_filename = 'merged'
            merge_files(filenames, merged_filename)
            
            # Convert the merged file to text
            page_content = textify(merged_filename + '.pdf')
            
            # Add a prompt to the content
            page_with_prompt = add_prompt(page_content)
            
            # Use OpenAI to generate questions based on the content
            question_generator = QuestionGenerator(model_engine, openai.api_key)
            response = question_generator.generate_questions(page_with_prompt, 2048, 0.5, 1, 0, 0)
            
            # Format the response for display
            response_with_endlines = add_newlines(response)

    # Render the main page with the generated response
    return render_template("index.html", response=response_with_endlines)

# Entry point for the app
if __name__ == "__main__":
    app.run(debug=True)
