import pdftotext

def text_extraction(path):
  with open(path, "rb") as f:
      pdf = pdftotext.PDF(f)
  text = []
  # All pages
  for txt in pdf:
    #   print(txt)
      text.append(txt)
  return text