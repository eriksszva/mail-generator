import streamlit as st
from utils.cleaning import clean_text
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portofolio import Portofolio


def create_streamlit_app(llm, portofolio, clean_text):
    st.title('📧 Cold Mail Generator for Job Post')
    # Description of the app
    st.write("Unlock the potential of personalized cold outreach with ease! This tool helps you craft professional, customized cold emails for reaching out to potential employers or business partners. Whether you're looking for job opportunities, pitching collaborations, or offering your services, this tool streamlines the process of creating compelling, targeted emails. Save time and increase your chances of getting noticed by using email templates that align with your goals, tailored to your audience's needs.")
    url_input = st.text_input('Enter a URL:', value='https://careers.nike.com/3d-footwear-designer-ii/job/R-60083')
    submit_button = st.button('Generate Email')

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portofolio.load_portofolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portofolio.query_links(skills)
                email = llm.write_email(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f'Error loading data: {e}')

if __name__ == "__main__":
    chain = Chain()
    portofolio = Portofolio()
    st.set_page_config(page_title='Cold Mail Generator', page_icon='📧')
    create_streamlit_app(chain, portofolio, clean_text)
            