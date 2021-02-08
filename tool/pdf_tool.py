import fitz # PyMuPDF
import io
from PIL import Image
# from fitz import Document
import os

class PDF():
    def __init__(self, pdf_file_path, file_id):
        pdf_file = fitz.open(pdf_file_path)
        self.pdf_file = pdf_file
        self.page_count = pdf_file.pageCount
        self.file_id = file_id

    def get_page_count(self):
        return self.page_count

    def get_front(self):
        pdf_file = self.pdf_file
        file_id = self.file_id
        front = ''
        page = pdf_file[0]
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            image.save(open(('temp/image_' + file_id + '.' + image_ext), "wb"))
            front = 'temp/image_' + file_id + '.' + image_ext
        return front

# file = PDF('User_file\Fundamental_of_Physics_10th_edition_questions.pdf', '123')
# print(file.get_page_count())