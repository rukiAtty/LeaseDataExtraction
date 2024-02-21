from langchain.llms import OpenAI
from pypdf import PdfReader
import pandas as pd
import re
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
import os 
os.environ["OPENAI_API_KEY"] = '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'

from langchain.chat_models import ChatOpenAI
#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_data(pages_data):

    template = '''Extract all following values: Address of the property, Landlord name , Tenant name, 
    period, beginning date, ending date, monthly rent ,late fee, late fee due date , notice period to end the lease from this data: {pages}
    
    Expected output :  {{'Address of the property':'200 9 th road, Seattle','Landlord name':'Carl Thomas', 
    'Tenant name':'Jeffri Bawa','period':' 1 year','beginning date':'1 st March 2023', 
    'ending date':'28 th February 2023', 'monthly rent':'$4000','late fee':'$100','late fee due date':'tenth day','notice period':'twenty days'}}
    '''

    prompt_template = PromptTemplate(input_variables=['pages'], template=template)

    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.4)
    full_response = llm(prompt_template.format(pages=pages_data))

    return full_response

# iterate over files in
# that user uploaded PDF files, one by one

def create_docs(user_pdf_list):
    
    df = pd.DataFrame({ 'Address of the property': pd.Series(dtype='str'),
        'Landlord name': pd.Series(dtype='str'),
                   'Tenant name': pd.Series(dtype='str'),
                   'period': pd.Series(dtype='str'),
                   'beginning date': pd.Series(dtype='str'),
	                'ending date': pd.Series(dtype='str'),
                   'monthly rent': pd.Series(dtype='str'),
                   'late fee': pd.Series(dtype='str'),
                   'late fee due date': pd.Series(dtype='str'),
                   'notice period': pd.Series(dtype='str')
                   
                    })

    for filename in user_pdf_list:
        data_dict=[]
        print(filename)
        raw_data=get_pdf_text(filename)
        #print(raw_data)
        print("extracted raw data")

        llm_extracted_data=extract_data(raw_data)
        print("llm extracted data")
        print(llm_extracted_data)

        lines = llm_extracted_data.strip().split('\n')

        # Initialize an empty list to store the data
        data = []

        # Extract key-value pairs
        for line in lines:
            key, value = line.split(':', 1)
            data.append([key, value])

        # Create a DataFrame
        df = pd.DataFrame(data, columns=['Attribute', 'Value'])
        print(df)
        #Adding items to our list - Adding data & its metadata
    '''
        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)
        print(match)
        if match:
            #data_dict=[]
            extracted_text = match.group(1)
            print(extracted_text)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
        else:
            print("No match found.")

        
        #df=df.append([data_dict], ignore_index=True)
        '''
       # print("********************DONE***************")
        #df=df.append(save_to_dataframe(llm_extracted_data), ignore_index=True)

    df.head(20)
    return df