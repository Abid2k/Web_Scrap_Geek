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

    def add_question_answer(self, number, question, answer):
        question = question.replace('\u2018', "'").replace('\u2019', "'")  # Replace smart quotes
        question = question.replace('\u201c', '"').replace('\u201d', '"')
        question = question.replace('\u2013', '-')# Replace smart double quotes
        answer = answer.replace('\u2018', "'").replace('\u2019', "'")
        answer = answer.replace('\u201c', '"').replace('\u201d', '"')
        answer = answer.replace('\u2013', '-')
        
        # Check if the current position (y-axis) on the page is too close to the bottom
        if self.get_y() > 250:
            self.add_page()  # Create a new page if needed

        # Add both question and answer to the PDF
        self.multi_cell(0, 10, f"{number}. {question}", border=0)
        self.multi_cell(0, 10, f"Answer: {answer}", border=0)
        self.ln(5)

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

        # Step 4: Extract all <h3> tags and their corresponding answers
        questions_answers = []
        while header:
            for sibling in header.find_next_siblings():
                if sibling.name == 'h2':  # If another header (new section) is encountered, stop
                    header = sibling
                    break
                if sibling.name == 'h3':  # Extract question from <h3> tags
                    question_text = sibling.get_text(strip=True)
                    answer_text = ""
                    next_sibling = sibling.find_next_sibling()
                    if next_sibling and next_sibling.name in ['p', 'span']:  # Check for answer
                        answer_text = next_sibling.get_text(strip=True)
                    
                    # Debugging: Print the extracted question and answer
                    if question_text and answer_text:
                        print(f"Question: {question_text}")
                        print(f"Answer: {answer_text}")
                        questions_answers.append((question_text, answer_text))
            
            # After processing the current section, move to the next header
            header = header.find_next_sibling('h2')

        print(f"Total Questions Extracted: {len(questions_answers)}")

        # Step 5: Save questions and answers to PDF
        if questions_answers:
            pdf = PDF()
            pdf.add_title("Python Interview Questions for Freshers")

            for i, (question, answer) in enumerate(questions_answers, 1):
                pdf.add_question_answer(i, question, answer)

            pdf.output(output_pdf, 'F')
            print(f"Saved {len(questions_answers)} questions and answers to {output_pdf}")
        else:
            print("No questions found in the specified section.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
url = "https://www.geeksforgeeks.org/python-interview-questions/"  # Replace with the exact URL
output_res = "./Output_PDF/Python_Interview_Questions_Freshers__1.pdf"
scrape_python_questions(url, output_res)
