import os
import re
from PyPDF2 import PdfReader
from settings import PDFExtractorSettings


class PDFExtractor:
    def __init__(self):
        pass

    @staticmethod
    def check_pdf_in_directory(directory):
        files = os.listdir(directory)
        for file in files:
            if file.endswith('.pdf'):
                return True
        return False

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def extract_correct_order_from_text(text_to_search):
        # Pattern for the number sequence
        # number_pattern = r'\b\d{10,18}\b'

        # Extract all number sequences
        number_matches = re.findall(PDFExtractorSettings.Patterns.number_sequence, text_to_search)

        paired_matches = []
        current_pos = 0
        for i, num in enumerate(number_matches):
            # Find the position of this number in the text
            num_pos = text_to_search.find(num, current_pos)
            end_num_pos = num_pos + len(num)

            # If this is not the last number, find the position of the next number
            if i < len(number_matches) - 1:
                next_num_pos = text_to_search.find(number_matches[i + 1], end_num_pos)
                # Extract the "complex" sequence as everything from the end of the current number
                # to the start of the next number
                complex_seq = text_to_search[end_num_pos:next_num_pos].strip()
            else:
                # If this is the last number, the "complex" sequence is everything after it
                complex_seq = text_to_search[end_num_pos:].strip()

            # We'll look for a sequence that starts with alphanumeric or special characters and
            # ends with a desired set of characters, ensuring we don't capture unwanted content after it
            match = re.match(PDFExtractorSettings.Patterns.complex_sequence, complex_seq)
            if match:
                paired_matches.append(num + match.group())

            current_pos = end_num_pos

        return paired_matches

    def process_pdfs_in_directory(self, directory_path, output_file_path, progress_callback=None):
        total_pages = self.get_total_pages(directory_path)
        processed_pages = 0

        open(output_file_path, 'w').close()  # Это очистит содержимое файла

        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(directory_path, filename)
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        text = page.extract_text()
                        sequences = self.extract_correct_order_from_text(text)

                        with open(output_file_path, 'a') as f:  # 'w' was changed to 'a' to append results
                            for seq in sequences:
                                f.write(seq + '\n\n')

                        processed_pages += 1
                        if progress_callback:  # обновляем прогресс-бар
                            progress_callback(processed_pages, total_pages)

    @staticmethod
    def get_total_pages(directory_path):
        """Возвращает общее количество страниц во всех PDF-файлах в указанной директории."""
        total_pages = 0
        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(directory_path, filename)
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    total_pages += len(reader.pages)
        return total_pages
