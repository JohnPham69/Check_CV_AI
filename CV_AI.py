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

def GeminiChat(prompt, pCV, pCrit):
    def upload_to_gemini(path, mime_type=None):
        """Uploads the given file to Gemini.
        See https://ai.google.dev/gemini-api/docs/prompting_with_media
        """
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    
    def wait_for_files_active(files):
        """Waits for the given files to be active.

        Some files uploaded to the Gemini API need to be processed before they can be
        used as prompt inputs. The status can be seen by querying the file's "state"
        field.

        This implementation uses a simple blocking polling loop. Production code
        should probably employ a more sophisticated approach.
        """
        print("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        print("...all files ready")
        print()

    """ Use for getting own API
    userAPI = ""
    filename = "C:\\LibreHelper\\userAPI.txt"
    with open(filename, 'r', encoding='utf-8') as file:
        userAPI = file.read()
        file.close()
    """
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
    
    model = genai.GenerativeModel(
      model_name="gemini-2.0-flash-lite-preview-02-05",
      generation_config=generation_config,
      # safety_settings = Adjust safety settings
      # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    chat_session = model.start_chat(
      history=[
            {
            "role": "user",
            "parts": [
                "hi",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Hi there! I'm here to check CVs based on provided criteria\n",
            ],
            },
        ]
    )
    
    # TODO Make these files available on the local file system
    # You may need to update the file path
    b = upload_to_gemini(pCrit, mime_type="application/pdf")
    a = upload_to_gemini(pCV, mime_type="application/pdf")
    files = [
    b,
    a,
    ]

    # Some files have a processing delay. Wait for them to be ready.
    wait_for_files_active(files)
    
    #response = chat_session.send_message(prompt)
    #base^^^^^origin up here

    response = model.generate_content([prompt, b, a])
    x = {"role":"user","parts": [prompt]}
    y = {"role": "model", "parts": [response.text]}
    #write_json(x, y)
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

def thebot(foShoCrit, foShoCV, user_prompt=""):
    '''Test prompt idea - next up
    if missing a criteria, a smol one, not that super important, or not that necessary
    then accept.
    '''
    prompt = f"""  
    You are the CV123456TEST bot.
    You may read from an attached file and strictly decide whether it fits as criterias or a CV (CVs), will be sent as PDF files.
    If it strictly matches the criterias. You may agree of accepting the applicant.
    You must give one's CV a score, such as 9/10 or 3/4. Dependings on user's prompt.
    If the score is equal to or exceed the passing rate, which will be provide as 'the mininum score to pass must be', applicant shall pass.
    The score must be shown first than the reasons or its break-down.
    Your respond will be: "I [agree or disagree] of accepting the applicant [number #? if there are many CVs at a time]."
    Give us a list of why you agree or disagree. Start each point with a '-'. If agree, tell us what criteria one has met and the other way around if one failed.
    Create at least 3 questions for the afterwards interview if the applicant's CV met the criterias.
    
    Read the attached criteria and CV, tried to sastify all user's requests in the prompt below:
    {user_prompt}
    """
    if (os.path.exists(foShoCrit) != True) or (os.path.exists(foShoCV) != True):
        return "ERROR 404: NOT FOUND\nWe couldn't find the file. Please browse the file again."
    arr = GeminiChat(prompt, foShoCV, foShoCrit)
    return arr.replace("\n\n", "\n").strip()

def start_up(path_to_crit, path_to_CVs, user_prompt=""):
    print("CV AI setting up...")
    path_to_crit = path_to_crit.replace("\\", "\\\\")
    path_to_CVs = path_to_CVs.replace("\\", "\\\\")
    print("Uploading...")
    a = thebot(path_to_crit, path_to_CVs, user_prompt)
    return a
