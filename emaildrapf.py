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
def prompt_generetor(intro, university, proff, researchtitle, about):
    prompt = f"""
    suppose you are research student and your are {intro}.
    you are applying for university name is {university}, name of the professsor is {proff} and 
    you read the professsor research paper and it's title is  {researchtitle}.
    Write email to the professsor for accpetance letter also write greate email subject, 
    Write that you are applying for scholeship {about}
    Make sure your from address and subject lines are useful
    
    Greeting: its safest to be a bit formal here
    Briefly introduce yourself in at most two sentences. Don’t tell your whole life story. Be direct and clear about applying to grad school.
     
    Explain specifically what you read and where you found it (people sometimes publish several papers with similar names and forget which is which). A touch of flattery never hurts, but don’t go overboard. If appropriate, relate it to your background and interests and briefly plug your work.
    Concisely describe your insight or why you are interested in the work.
    End with a clear, simple question. Offer a suggestion on how to proceed.
    Closing — make sure to include your name and email address.
    
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
    text = prompt_generetor(intro=" name Muhammad Ishaque from Pakistan Hyderabad done BE in computer system engneering for Mehran university of Engineering and technology and I am applying for master also add my profolo link https://muhammadishaquedev.vercel.app/ in email but it should be plan text",
                            university="Ritsumeikan University Japan",
                            proff="Yen-Wei Chen", 
                            researchtitle="Ladder Fine-tuning approach for SAM integrating complementary networkAuthors",
                            about="MEXT university track")
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