import os
import time
import google.generativeai as genai

#To improve
#PROMPT: TELL AI to list

#File -> Read & add to prompt
#No history should be save
#Session start need 2 files, criteria and CV
#1st time, required criteria
#2nd on, if there is criteria file, then overwrite the current.

def get_curr_crit():
    path_to_save = "C:\\CV_BOT_AI\\ccrit.docx"
    with open(path_to_save, "r+", encoding='utf-8') as file:
        a = file.read()
        file.close()
        return a
    
def save_curr_crit(criterias):
    path_to_save = "C:\\CV_BOT_AI\\ccrit.docx"
    with open(path_to_save, "w+", encoding='utf-8') as file:
        file.write(criterias)
        file.close()

def createFolder(FolderName):
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(FolderName):
            os.makedirs(FolderName)
    except OSError as e:
        print(f"An error occurred while creating the folder: {str(e)}")

def get_inp_cv(pathToCV):
    if os.path.exists(pathToCV):
        with open(pathToCV, "r+", encoding='utf-8') as file:
            a = file.read()
            file.close()
            return a
    else:
        return "404: CV Not Found"

def get_inp_criteria(pathToCrit):
    if os.path.exists(pathToCrit):
        with open(pathToCrit, "r+", encoding='utf-8') as file:
            a = file.read()
            file.close()
            return a
    else:
        return "404: Criteria Not Found"


def GeminiChat(prompt, pCVs, pCrit):
    def upload_to_gemini(path, mime_type=None):
        """Uploads the given file to Gemini.
        See https://ai.google.dev/gemini-api/docs/prompting_with_media
        """
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    #My API
    genai.configure(api_key="AIzaSyCxacO9TqPYM1Dsq56ms_oZvze1fwvZcxU")
    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    # Upload the criteria file first
    if not os.path.exists(pCrit):
        return "ERROR 404: Criteria Not Found"
    criteria_file = upload_to_gemini(pCrit, mime_type="application/pdf")

    # Upload all CVs
    cv_files = []
    for cv in pCVs.split(";"):  # Split by ";" in case multiple CVs are provided
        if not os.path.exists(cv):
            return f"ERROR 404: CV Not Found ({cv})"
        cv_files.append(upload_to_gemini(cv, mime_type="application/pdf"))

    # Ensure all CV files are used in the prompt
    files = [criteria_file] + cv_files

    model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
    chat_session = model.start_chat(history=[
        {"role": "user", "parts": ["hi"]},
        {"role": "model", "parts": ["Hi! I'm here to check CVs based on provided criteria."]},
    ])

    # Send all CVs and the criteria file as input
    response = model.generate_content([prompt] + files)
    return response.text


"""
def write_json(new_data, sec_data):
    filename = 'C:\\LibreHelper\\history.json'
    if not os.path.exists(filename):
        first_add = json.load(new_data)
        sec_add = json.load(sec_data)
        createJsonFile(filename, first_add, "history", "C:\\LibreHelper")
        appendContentJson(filename, sec_add, "history")
    with open(filename,'r+', encoding='utf-8') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["history"].append(new_data)
        file_data["history"].append(sec_data)
        if (len(file_data["history"]) == 20):
            file_data["history"].pop(0)
            file_data["history"].pop(0)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
        file.truncate()

def getHistory():
    filename = 'C:\\LibreHelper\\history.json'
    with open(filename, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        return file_data['history']
"""

def thebot(foShoCrit, foShoCVs, user_prompt=""):
    prompt = f"""  
    You are the CV123456TEST bot.
    Analyze **all** CVs based on the provided criteria.
    - Each CV is a separate PDF file.
    - Provide a score for **each** CV (e.g., 9/10 or 3/4).
    - If the score meets or exceeds the passing rate, the applicant **passes**.
    - State: "I [agree/disagree] on accepting the applicant [# if multiple CVs]."
    - List reasons using "- " bullet points.
    - If the CV **passes**, suggest at least 3 interview questions.
    - Count and display the **total number of CVs**.

    User prompt:
    {user_prompt}
    """

    if not os.path.exists(foShoCrit):
        return "ERROR 404: Criteria File Not Found"

    # Send ALL CVs to GeminiChat at once
    return GeminiChat(prompt, ";".join(foShoCVs), foShoCrit)

def start_up(path_to_crit, path_to_CVs, user_prompt=""):
    if isinstance(path_to_CVs, list):
        path_to_CVs = [cv.replace("\\", "\\\\") for cv in path_to_CVs]
    else:
        path_to_CVs = [path_to_CVs.replace("\\", "\\\\")]
    print("Uploading files...")
    a = thebot(path_to_crit, path_to_CVs, user_prompt)  # Pass list of CVs

    return a
