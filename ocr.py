# import fitz
# import os  # import the bindings
# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai

# def pdf2images(file):
#     images = []
#     # print(file.filename)
#     fname = file.filename
#     fname = fname.rsplit('.', 1)[0]
#     # print(fname)
#     folder = f"static/images/{fname}/"
#     # print(os.path.exists(folder))
#     if os.path.exists(folder) is True:
#         pass
#     else:
#         os.makedirs(folder)
#     doc = fitz.open(f"static/documents/{fname}.pdf")  # open document
#     for page in doc:  # iterate through the pages
#         pix = page.get_pixmap()  # render page to an image
#         pgn = page.number+1
#         pix.save(f"{folder}page-%i.png" % pgn)  # store image as a PNG
#         images.append(f"{folder}page-{pgn}.png")
#     return images


# PROJECT_ID = "numeric-chassis-395210"
# LOCATION = "eu"
# PROCESSOR_ID = "2f9085feb2522929"
# def mal_ocr(fp):
#     FILE_PATH = fp
#     MIME_TYPE = "image/png"

#     docai_client = documentai.DocumentProcessorServiceClient(
#         client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
#     )

#     RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

#     with open(FILE_PATH, "rb") as image:
#         image_content = image.read()

#     raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

#     request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

#     result = docai_client.process_document(request=request)

#     document_object = result.document
#     print("Document processing complete.")
#     return document_object.text