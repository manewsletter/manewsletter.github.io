from PyPDF2 import PdfWriter
import pdfkit
import re
import os
from PyPDF2 import PdfReader
from PIL import Image


def convert_html_to_pdf(html_file, pdf_file):
    try:
        # Convertir les images .webp en .png
        convert_webp_to_png(html_file)

        # Convertir le fichier HTML en PDF avec pdfkit
        pdfkit.from_file(html_file, 'temp.pdf')

        # Fusionner les fichiers PDF avec PyPDF2
        merger = PdfWriter()
        merger.add_pages(PdfReader(pdf_file).pages)
        merger.add_pages(PdfReader('temp.pdf').pages)
        with open(pdf_file, 'wb') as output_pdf:
            merger.write(output_pdf)

        # Supprimer le fichier temporaire
        os.remove('temp.pdf')

        print("Conversion réussie !")
    except Exception as e:
        print("Erreur lors de la conversion :", str(e))


def convert_webp_to_png(html_file):
    with open(html_file, 'r') as f:
        html_content = f.read()

    # Rechercher les balises <img> avec src se terminant par .webp
    webp_images = re.findall(r'<img[^>]+src="([^"]+\.webp)"', html_content)

    # Convertir chaque image .webp en .png
    for webp_image in webp_images:
        png_image = webp_image.replace('.webp', '.png')
        Image.open(webp_image).save(png_image, 'PNG')

        # Mettre à jour le chemin de l'image dans le fichier HTML
        html_content = html_content.replace(webp_image, png_image)

    # Écrire le contenu HTML mis à jour dans le fichier
    with open(html_file, 'w') as f:
        f.write(html_content)


html_file = "Artists.html"
pdf_file = "Artists.pdf"

convert_html_to_pdf(html_file, pdf_file)
