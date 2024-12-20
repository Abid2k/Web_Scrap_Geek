import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("Arial", size=12)

    def add_title(self, title):
        self.set_font("Arial", style="B", size=14)
        self.cell(200, 10, txt=title, ln=True, align='C')
        self.ln(10)  # Add some space

    def add_question(self, number, question):
        question = question.replace('\u2018', "'").replace('\u2019', "'")  # Replace smart quotes
        question = question.replace('\u201c', '"').replace('\u201d', '"')  # Replace smart double quotes
        self.multi_cell(0, 10, f"{number}. {question}", border=0)

def scrape_python_questions(url, output_pdf):
    try:
        # Step 1: Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Step 2: Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 3: Locate the specific section starting from the <h2> header
        header = soup.find('h2', id="python-interview-questions-for-freshers")
        if not header:
            print("Header with the specified ID not found.")
            return

        # Step 4: Extract all <h3> tags after this header
        questions = []
        for sibling in header.find_next_siblings():
            if sibling.name == 'h2':  # Stop when reaching the next <h2> tag
                break
            if sibling.name == 'h3':  # Extract the question from <h3> tags
                text = sibling.get_text(strip=True)
                if text:
                    questions.append(text)

        # Step 5: Save questions to PDF
        if questions:
            pdf = PDF()
            pdf.add_title("Python Interview Questions for Freshers")

            for i, question in enumerate(questions, 1):
                pdf.add_question(i, question)

            pdf.output(output_pdf, 'F')
            print(f"Saved {len(questions)} questions to {output_pdf}")
        else:
            print("No questions found in the specified section.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
url = "https://www.geeksforgeeks.org/python-interview-questions/"  # Replace with the exact URL
output_pdf = "./Output_PDF/Python_Interview_Questions_Freshers.txt"
scrape_python_questions(url, output_pdf)
