import PyPDF2
import sys
import os

def create_password_protected_pdf(input_pdf, output_pdf, password):
    try:
        # Open the input PDF
        with open(input_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            # Add all pages to writer
            for page in reader.pages:
                writer.add_page(page)

            # Set the password
            writer.encrypt(user_password=password, owner_password=None, use_128bit=True)

            # Write the output
            with open(output_pdf, 'wb') as output:
                writer.write(output)

            print(f"✅ Password-protected PDF saved as: {output_pdf}")
    
    except FileNotFoundError:
        print(f"❌ File not found: {input_pdf}")
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")

def main():
    # If script is run with arguments
    if len(sys.argv) == 4:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        password = sys.argv[3]
    else:
        # Ask user interactively if no arguments
        print("Usage: python pdf_password_protect.py <input.pdf> <output.pdf> <password>")
        input_pdf = input("Enter input PDF filename: ")
        output_pdf = input("Enter output PDF filename: ")
        password = input("Enter password to protect PDF: ")

    if not os.path.exists(input_pdf):
        print(f"❌ File '{input_pdf}' does not exist.")
        return

    create_password_protected_pdf(input_pdf, output_pdf, password)

if __name__ == "__main__":
    main()
