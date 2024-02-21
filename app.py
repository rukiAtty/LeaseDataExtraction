import streamlit as st
import os
from dotenv import load_dotenv
from utils import *

def main():
    load_dotenv()

    st.set_page_config(page_title="Agreement Information Extraction Bot")
    st.title("Agreement Information Extraction Bot")
    #st.subheader("I can help you in extracting invoice data")


    # Upload the Invoices (pdf files)
    pdf = st.file_uploader("Upload Lease Agreement here, only PDF files allowed",
    type=["pdf"],accept_multiple_files=True)

    submit=st.button("Extract Data")

    if submit:
        with st.spinner('Wait for it...'):
            df=create_docs(pdf)
            st.write(df)

            data_as_csv= df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download data as CSV", 
                data_as_csv, 
                "output.csv",
                "text/csv",
                key="download-output-csv",
            )
        st.success("Done")


#Invoking main function
if __name__ == '__main__':
    main()