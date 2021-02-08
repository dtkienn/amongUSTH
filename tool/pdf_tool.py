from PyPDF2 import PdfFileReader

class PDF():
    def __init__(self, file_path):
        self.file_path = file_path
        file = PdfFileReader(file_path)
        self.page_count = file.getNumPages()

    def get_page_count(self):
        return self.page_count