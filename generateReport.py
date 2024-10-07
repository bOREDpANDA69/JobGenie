import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from crewai import Agent, Task
from crewai import Crew, Process
from langchain_groq import ChatGroq


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

def generateReport(path):
    reader = PdfReader(path)
    resume = ''
    for page in reader.pages:
        resume += page.extract_text()

    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0, groq_api_key=GROQ_API_KEY)

    resume_job_recommender = Agent(
        role = 'Resume Based Job Recommender',
        goal = f'Perform a critical analysis on the Resume and based on the contents of Resume, recommend 5 job profiles along with a few reason why those job profiles are suitable in a JSON report.',
        backstory = 'An expert in hiring so has a great idea on resumes',
        verbose = True,
        llm = llm,
        max_iters = 1,
        allow_delegation = True
    )

    resume_job_recommendation = Task(
        description = f'Resume Content: {resume} \n Analyse the resume provided to create a json resport in which breifly explain why the job profiles are suitable for the given resume. Address the Candidate as You. Format the reasons in a list. Given a list of skills for each job extracted from the text that indicate the proficiency in the field. In each job add a field title the refers to the job title and a list of reason explaining the recommendation of job and a list of skills that are relevant to the job profile. Give a candidate value as well which contains the name of the candidate. Output to strictly a JSON string to the directory provided. no other attributions should be made.',
        expected_output = 'A JSON formatted report as follows: "candidate": candidate, "jobs": [job1, job2, job3, job4, job5]',
        agent = resume_job_recommender,
        output_file = 'resume-report/job_recommendation.json'
    )

    crew = Crew(
        agents=[resume_job_recommender],
        tasks=[resume_job_recommendation],
        verbose=1,
        process=Process.sequential
    )
    return crew.kickoff()
