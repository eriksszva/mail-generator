from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


load_dotenv('/app/docker/.env')

class Chain():
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError('GROQ_API_KEY not set in environment variables!')
        self.llm = ChatGroq(
                    temperature=0.7,
                    groq_api_key=self.api_key,
                    model_name='llama-3.3-70b-versatile'
                )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):
        """
        )
        
        chain_extract = prompt_extract | self.llm 
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException as e:
            raise OutputParserException(
                f'Error parsing the output: {e}'
            ) from e
        return res if isinstance(res, list) else [res]
    
    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are Abi, a Talent Acquisition Specialist at AtliQ Talent Solutions. AtliQ is an AI & Software Consulting company that also provides end-to-end talent sourcing services, with a special focus on placing highly qualified administrative professionals. Over the years, we have partnered with organizations across ASEAN to deliver skilled office administrators, executive assistants, data entry specialists, and other support staff who drive efficiency, accuracy, and seamless day-to-day operations.  

        Your task is to write a concise, no-preamble cold email to the client about the administrative role described above. In your message,  
        1. Emphasize AtliQ’s proven track record in recruiting and onboarding top administrative talent.  
        2. Highlight how our tailored screening process ensures the right fit for their team.  
        3. Include the most relevant portfolio items from these links: {link_list}  

        Remember: you are Abi, Talent Acquisition Specialist at AtliQ. And present the email in a professional manner and good layout.  
        ### EMAIL (NO PREAMBLE):

        """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke(
            {'job_description': str(job),
             'link_list': str(links)}
        )
        return res.content


if __name__ == '__main__':
    pass
    