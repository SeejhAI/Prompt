import google.generativeai as palm
from dotenv import load_dotenv
import os
from fpdf import FPDF
from google.api_core import retry

load_dotenv()
API_KEY: str = os.getenv("API_KEY")
palm.configure(api_key=API_KEY)
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

@retry.Retry()
def prompt_generetor(intro, university, proff, researchtitle):
    prompt = f"""
    suppose you are research student and your are {intro}.
    you are applying for university name is {university}, name of the professsor is {proff} and 
    you research title is {researchtitle}.
    Write email to the professsor for accpetance letter also write greate email subject, in which you have to introduce yourself and tell
    and you want to acceptance letter from
    him or her and tell him or her that you will send him your CV and Abstract so add something 
    above so add something about it. 
     
    
    
    """

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.7,
        # The maximum length of the response
        max_output_tokens=800,
    )
    return completion.result


if __name__ == "__main__":
    text = prompt_generetor(intro=" name Muhammad Ishaque from Pakistan Hyderabad done BE in computer system engneering for Mehran university of Engineering and technology",
                            university="Chiba University",
                            proff="Takahiko Horiuchi", 
                            researchtitle="AI-driven noise reduction system to address environmental noise pollution in urban and industrialized areas" )
    print(text)
    # Create a PDF class instance
    pdf = FPDF()

    # Add a page (optional, if you don't add a page, it'll create one by default)
    pdf.add_page()

    # Set font and size
    pdf.set_font("Arial", size=11)

    # Your email-formatted text
    email_text =text

    # Split the email text into lines
    email_lines = email_text.split('\n')

    # Add each line to the PDF
    for line in email_lines:
        pdf.multi_cell(0, 10, line)

    # Specify the name of the output PDF file
    pdf_file = "email.pdf"

    # Output the PDF to the file
    pdf.output(pdf_file)

    print(f"PDF saved to {pdf_file}")