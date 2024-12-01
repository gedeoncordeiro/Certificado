import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from io import BytesIO
from datetime import datetime

def create_certificate_overlay(student_name, courses, completion_date):
    """
    Cria um PDF temporário com as informações do certificado para sobrepor no PDF principal.
    O conteúdo é centralizado em uma página A4 no modo paisagem.
    
    :param student_name: Nome do aluno.
    :param courses: Lista de tuplas com (nome do curso, carga horária).
    :param completion_date: Data de conclusão do curso.
    :return: Um objeto BytesIO contendo o PDF do certificado.
    """
    buffer = BytesIO()
    page_width, page_height = landscape(A4)  # A4 no modo paisagem
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    
    # Coordenadas de início (centraliza o texto)
    center_x = page_width / 2

    # Adiciona título e detalhes do certificado
    #c.setFont("Helvetica-Bold", 24)
   # c.drawCentredString(center_x, page_height - 150, "Certificado de Conclusão")
    
    c.setFont("Helvetica", 16)
    c.drawCentredString(center_x, page_height - 200, f"Aluno: {student_name}")
    c.drawCentredString(center_x, page_height - 230, f"Data de Conclusão: {completion_date}")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(center_x, page_height - 280, "Cursos Concluídos:")
    
    # Lista os cursos centralizados
    y_position = page_height - 310
    c.setFont("Helvetica", 14)
    for course_name, hours in courses:
        c.drawCentredString(center_x, y_position, f"{course_name} - {hours} horas")
        y_position -= 20

    c.save()
    buffer.seek(0)
    return buffer

def merge_pdfs(base_pdf_path, overlay_buffer, output_pdf_path):
    """
    Mescla o conteúdo do certificado com a primeira página do PDF principal.
    
    :param base_pdf_path: Caminho do PDF principal.
    :param overlay_buffer: Buffer contendo o PDF do certificado.
    :param output_pdf_path: Caminho do arquivo PDF final gerado.
    """
    base_pdf = PdfReader(base_pdf_path)
    overlay_pdf = PdfReader(overlay_buffer)
    writer = PdfWriter()

    # Mescla a sobreposição apenas na primeira página do PDF principal
    first_page = base_pdf.pages[0]
    first_page.merge_page(overlay_pdf.pages[0])  # Mescla com a página de overlay
    writer.add_page(first_page)

    # Adiciona as demais páginas sem alterações
    for page in base_pdf.pages[1:]:
        writer.add_page(page)
    
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

# Exemplo de uso
def main():
    student_name = "Gedeon da Conceição Cordeiro"
    courses = [("Introdução à Informática", 40), ("Redes de Computadores", 60), ("Programação em Python", 30)]
    completion_date = datetime.now().strftime("%d/%m/%Y")

    # Defina o diretório de saída
    output_dir = "certificados"
    os.makedirs(output_dir, exist_ok=True)

    # Caminhos dos arquivos
    base_pdf_path = r"D:\GEDEON\DESENVOLVIMENTO WEB\Certificado\modelo.pdf"
    output_pdf_path = os.path.join(output_dir, "certificado_final.pdf")

    # Gera o overlay e mescla no PDF principal
    overlay_buffer = create_certificate_overlay(student_name, courses, completion_date)
    merge_pdfs(base_pdf_path, overlay_buffer, output_pdf_path)

    print(f"Certificado gerado e mesclado na primeira página: {output_pdf_path}")

if __name__ == "__main__":
    main()
