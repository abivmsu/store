from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden,JsonResponse , HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed 
from django.urls import reverse
from .forms import StoreForm, BookForm, ItemForm, StoreForm, OrderForm, ProductForm, ProductGivenForm, ProductGivenDetailForm, StaffOrderForm
from django.contrib import messages
from .models import *
from cart.cart import Cart
from django.db import transaction
from django.db.models import Q , F
import datetime , json
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError, ObjectDoesNotExist
# Create your views here.

    

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def books_report(request):
    # Register the font
    # pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('Nyala', 'static/fonts/Nyala.ttf'))
    # Sample data from your models
    books = Store.objects.filter(is_book = True)
    # Create a PDF document
    doc = SimpleDocTemplate("Books_in_store.pdf", pagesize=letter)
    elements = []
    # Define styles
    styles = getSampleStyleSheet()
    style_heading = styles["Title"]
    style_normal = styles["Normal"]
    style_heading1 = styles["Heading1"]

   # Create a style using the registered font
    style_normal.fontName = 'Nyala'
    style_heading.fontName = 'Nyala'

    elements.append(Spacer(1, -50))  # Remove some space
    # Define the title text
    title_text = "አንደሉስ ት/ቤት"
    styles = getSampleStyleSheet()
    title = Paragraph("<b>{}</b>".format(title_text), style_heading)
    # Define the title text
    Entitle_text = "ANDELUS SCHOOL"
    styles = getSampleStyleSheet()
    Entitle = Paragraph("<b>{}</b>".format(Entitle_text), style_heading)

    # Load the image
    image_path = "static/img/login.png"
    logo = Image(image_path, width=65, height=60)

    # Create a table for layout
    data = [[title, logo, Entitle]]
    table = Table(data, colWidths=[200, 100 , 200], hAlign="CENTER")
    table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table)
    elements.append(Spacer(1, 10))  # Add some space

    #Add todays date
    today = [
            ["Date:", str(datetime.now().strftime('%d-%m-%Y'))],
            ["Ref.No:", "AND-Adama-00"],
        ]
    report_date = Table(today, colWidths=[60, 75] ,hAlign="RIGHT")
    report_date.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
        ]))
    elements.append(report_date)
    elements.append(Spacer(1, 12))  # Add some space

    
        # Add title
    title = Paragraph("<b>Books In Store</b>", style_heading)
    title_table = Table([[title]], colWidths=[500], hAlign="CENTER")
    elements.append(title_table)
    elements.append(Spacer(1, 12))  # Add some space

    # Add Orders Table
    data = [["Book Name", "Description", "Subjects","Grade", "Pages", "Quantity"]]
    
    for book in books:
        # Split description into multiple lines if it exceeds a certain length
        max_description_width = 30  # Adjust as needed
        description = book.books.description
        description_lines = [description[i:i + max_description_width] for i in range(0, len(description), max_description_width)]
        data.append([
            book.books.book_name,
            "\n".join(description_lines),
                str(book.books.subject),
                str(book.books.grade),
                str(book.books.pages),
                str(book.quantity),
            ])
    orders_table = Table(data, colWidths=[100, 200, 100, 50, 50, 50])

    # Define the alternating row colors
    TableOddFill = colors.HexColor(0xEEEEEE)  # Light grey color
    TableEvenFill = colors.HexColor(0xFFFFFF)  # White color
    TableHeaderFill = colors.HexColor(0x3498DB)  # Header blue color

    orders_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Outer border
    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for data cells
    ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),  # Font style for data cells
    ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for header row
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font style for header row
    ('BACKGROUND', (0, 0), (-1, 0), TableHeaderFill),  # Header row background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
    ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Bottom padding
    ]))

    # Apply alternating row colors for data rows
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = TableEvenFill
        else:
            bg_color = TableOddFill
        orders_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), bg_color)]))
    elements.append(orders_table)
    elements.append(Spacer(1, 12))  # Add some space

  
    # Build the PDF document
    doc.build(elements)

   # Return the PDF file as a response for download
    with open("Books_in_store.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=Books_in_store.pdf"
        return response

def items_report(request):
    
    # Register the font
    # pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    
    pdfmetrics.registerFont(TTFont('Nyala', 'static/fonts/Nyala.ttf'))

 
    # Sample data from your models
    items = Store.objects.filter(is_item = True)
    # Create a PDF document
    doc = SimpleDocTemplate("Items_in_store.pdf", pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    style_heading = styles["Title"]
    style_normal = styles["Normal"]
    
    style_heading1 = styles["Heading1"]

   # Create a style using the registered font
    style_normal.fontName = 'Nyala'
    style_heading.fontName = 'Nyala'


    elements.append(Spacer(1, -50))  # Remove some space
    # Define the title text
    title_text = "አንደሉስ ት/ቤት"
    styles = getSampleStyleSheet()
    title = Paragraph("<b>{}</b>".format(title_text), style_heading)
    # Define the title text
    Entitle_text = "ANDELUS SCHOOL"
    styles = getSampleStyleSheet()
    Entitle = Paragraph("<b>{}</b>".format(Entitle_text), style_heading)

    # Load the image
    image_path = "static/img/login.png"
    logo = Image(image_path, width=65, height=60)

    # Create a table for layout
    data = [[title, logo, Entitle]]
    table = Table(data, colWidths=[200, 100 , 200], hAlign="CENTER")
    table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table)
    
    elements.append(Spacer(1, 10))  # Add some space

    #Add todays date
    today = [
        ["Date:", str(datetime.now().strftime('%d-%m-%Y'))],
        ["Ref.No:", "AND-Adama-00"],
    ]
    report_date = Table(today, colWidths=[60, 75] ,hAlign="RIGHT")
    report_date.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
    ]))
    elements.append(report_date)
    elements.append(Spacer(1, 12))  # Add some space

    
    # Add title
    title = Paragraph("<b>Items In Store</b>", style_heading)
    title_table = Table([[title]], colWidths=[500], hAlign="CENTER")
    elements.append(title_table)
    elements.append(Spacer(1, 12))  # Add some space

   
    # Add Orders Table
    data = [["Item Name", "Description", "Quantity"]]
    
    for item in items:
        # Split description into multiple lines if it exceeds a certain length
        max_description_width = 30  # Adjust as needed
        description = item.items.description
        description_lines = [description[i:i + max_description_width] for i in range(0, len(description), max_description_width)]
        data.append([
           item.items.item_name,
            "\n".join(description_lines),
                str(item.quantity),
            ])
    orders_table = Table(data, colWidths=[150, 200, 150])

    # Define the alternating row colors
    TableOddFill = colors.HexColor(0xEEEEEE)  # Light grey color
    TableEvenFill = colors.HexColor(0xFFFFFF)  # White color
    TableHeaderFill = colors.HexColor(0x3498DB)  # Header blue color

    # Apply styles to the table
    # Apply styles to the table
    # orders_table.setStyle(TableStyle([
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #     ('BACKGROUND', (0, 0), (-1, 0), TableHeaderFill),  # Header row background color
    #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
    #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Outer border
    #     ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
    #     ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),  # Font style
    #     ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding
    #     ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Bottom padding
    # ]))


    orders_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Outer border
    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for data cells
    ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),  # Font style for data cells
    ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for header row
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font style for header row
    ('BACKGROUND', (0, 0), (-1, 0), TableHeaderFill),  # Header row background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
    ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Bottom padding
    ]))

    # Apply alternating row colors for data rows
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = TableEvenFill
        else:
            bg_color = TableOddFill
        orders_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), bg_color)]))
    elements.append(orders_table)
    elements.append(Spacer(1, 12))  # Add some space

  
    # Build the PDF document
    doc.build(elements)

   # Return the PDF file as a response for download
    with open("Items_in_store.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=Items_in_store.pdf"
        return response

def wechi_report(request,order_id):
    pdfmetrics.registerFont(TTFont('Nyala', 'static/fonts/Nyala.ttf'))
   
    order_group = OrderGroup.objects.get(id=order_id)  # Assuming you have an OrderGroup with ID 1
    orders = order_group.orders.all()

    # Create a PDF document
    doc = SimpleDocTemplate("outgoing.pdf", pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    style_heading = styles["Title"]
    style_normal = styles["Normal"]
    style_heading1 = styles["Heading1"]

   # Create a style using the registered font
    style_normal.fontName = 'Nyala'
    style_heading.fontName = 'Nyala'

    elements.append(Spacer(1, -50))  # Remove some space
    # Define the title text
    title_text = "አንደሉስ ት/ቤት"
    styles = getSampleStyleSheet()
    title = Paragraph("<b>{}</b>".format(title_text), style_heading)
    # Define the title text
    Entitle_text = "ANDELUS SCHOOL"
    styles = getSampleStyleSheet()
    Entitle = Paragraph("<b>{}</b>".format(Entitle_text), style_heading)

    # Load the image
    image_path = "static/img/login.png"
    logo = Image(image_path, width=65, height=60)

    # Create a table for layout
    data = [[title, logo, Entitle]]
    table = Table(data, colWidths=[200, 100 , 200], hAlign="CENTER")
    table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table)

    elements.append(Spacer(1, 10))  # Add some space

    #Add todays date
    today = [
        ["Date:", str(datetime.now().strftime('%d-%m-%Y'))],
        ["Ref.No:", "AND-Adama-00"],
    ]
    report_date = Table(today, colWidths=[60, 75] ,hAlign="RIGHT")
    report_date.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
    ]))
    elements.append(report_date)
    elements.append(Spacer(1, 12))  # Add some space

        # Add title
    title = Paragraph("<b> ወጪ መጠይቅ ሪፖርት  Outgoing Request Report </b>", style_heading)
    title_table = Table([[title]], colWidths=[500], hAlign="CENTER")
    elements.append(title_table)
    elements.append(Spacer(1, 12))  # Add some space

   
   # Add Order Group Information
   # Create a table for order information
    order_info_data = [
        [Paragraph("<b>የጠየቀው_አካል:</b>", style_normal), Paragraph(order_group.user.first_name, style_normal)],
        [Paragraph("<b>የፈቀደው_አካል:</b>", style_normal), Paragraph(order_group.approved_by, style_normal)],
        [Paragraph("<b>Order_Type:</b>", style_normal), Paragraph(order_group.order_type, style_normal)],
        [Paragraph("<b>Date:</b>", style_normal), Paragraph(order_group.date.strftime('%d-%m-%Y'), style_normal)],
        [Paragraph("<b>Status:</b>", style_normal), Paragraph(order_group.status, style_normal)],
    ]
    order_info_table = Table(order_info_data, colWidths=[80, 80], hAlign="CENTER")
    order_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(order_info_table)
    elements.append(Spacer(1, 12))  # Add some space
    # Add Orders Table
    data = [["Product", "Qty","Unit","Sub_Unit" ,"Sub_Qty","Conf_Qty", "Iss_Qty","Conf_Date "]]
    for order in orders:
        data.append([
            order.books.subject + " Grade " + order.books.grade if order.books else order.items.item_name,
            str(order.quantity),
            str(order.unit),
            str(order.subunit),
            str(order.subunit_quantity),
            str(order.confirmed_quantity),
            str(order.issued_quantity),
            str(order.issued_date.strftime('%d-%m-%Y')),
        ])
    orders_table = Table(data, colWidths=[130, 50, 50, 60, 60, 60, 60, 60 ])

    # Define the alternating row colors
    TableOddFill = colors.HexColor(0xEEEEEE)  # Light grey color
    TableEvenFill = colors.HexColor(0xFFFFFF)  # White color
    TableHeaderFill = colors.HexColor(0x3498DB)  # Header blue color

    # Apply styles to the table
    
    orders_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Outer border
    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for data cells
    ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),  # Font style for data cells
    ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for header row
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font style for header row
    ('BACKGROUND', (0, 0), (-1, 0), TableHeaderFill),  # Header row background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
    ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Bottom padding
    ]))
    # Apply alternating row colors for data rows
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = TableEvenFill
        else:
            bg_color = TableOddFill
        orders_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), bg_color)]))
    elements.append(orders_table)
    elements.append(Spacer(1, 12))  # Add some space

    # Add Total Price and Received By
   
    # Build the PDF document
    doc.build(elements)

   # Return the PDF file as a response for download
    with open("outgoing.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=outgoing.pdf"
        return response

def gebi_report(request,order_id):
    pdfmetrics.registerFont(TTFont('Nyala', 'static/fonts/Nyala.ttf'))
   
    order_group = OrderGroup.objects.get(id=order_id)  # Assuming you have an OrderGroup with ID 1
    orders = order_group.orders.all()

    # Create a PDF document
    doc = SimpleDocTemplate("incoming.pdf", pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    style_heading = styles["Title"]
    style_normal = styles["Normal"]
    style_heading1 = styles["Heading1"]

   # Create a style using the registered font
    style_normal.fontName = 'Nyala'
    style_heading.fontName = 'Nyala'

    elements.append(Spacer(1, -50))  # Remove some space
    # Define the title text
    title_text = "አንደሉስ ት/ቤት"
    styles = getSampleStyleSheet()
    title = Paragraph("<b>{}</b>".format(title_text), style_heading)
    # Define the title text
    Entitle_text = "ANDELUS SCHOOL"
    styles = getSampleStyleSheet()
    Entitle = Paragraph("<b>{}</b>".format(Entitle_text), style_heading)

    # Load the image
    image_path = "static/img/login.png"
    logo = Image(image_path, width=65, height=60)

    # Create a table for layout
    data = [[title, logo, Entitle]]
    table = Table(data, colWidths=[200, 100 , 200], hAlign="CENTER")
    table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table)

    elements.append(Spacer(1, 10))  # Add some space


    today = [
        ["Date:", str(datetime.now().strftime('%d-%m-%Y'))],
        ["Ref.No:", "AND-Adama-00"],
    ]
    report_date = Table(today, colWidths=[60, 75] ,hAlign="RIGHT")
    report_date.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
    ]))
    elements.append(report_date)
    elements.append(Spacer(1, 12))  # Add some space
        # Add title
    title = Paragraph("<b> ገቢ መጠይቅ ሪፖርት  Incoming Request Report </b>", style_heading)
    title_table = Table([[title]], colWidths=[500], hAlign="CENTER")
    elements.append(title_table)
    elements.append(Spacer(1, 12))  # Add some space

   
   # Add Order Group Information
   # Create a table for order information
    order_info_data = [
        [Paragraph("<b>የተገዛለት_ክፍል :</b>", style_normal), Paragraph(order_group.order_for, style_normal)],
        [Paragraph("<b>ያስረከበው_አካል :</b>", style_normal), Paragraph(order_group.order_by, style_normal)],
        [Paragraph("<b>የተረከበው_አካል :</b>", style_normal), Paragraph(order_group.recieved_by, style_normal)],
        [Paragraph("<b>Date:</b>", style_normal), Paragraph(order_group.date.strftime('%d-%m-%Y'), style_normal)],
        [Paragraph("<b>Status:</b>", style_normal), Paragraph(order_group.status, style_normal)],
    ]
    order_info_table = Table(order_info_data, colWidths=[80, 80], hAlign="CENTER")
    order_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(order_info_table)
    elements.append(Spacer(1, 12))  # Add some space
    # Add Orders Table
    data = [["Product", "Qty","Unit","Sub_Unit" ,"Sub_Qty","U.Price", "T.Price"," With Tax"]]
    for order in orders:
        data.append([
            order.books.subject + " Grade " + order.books.grade if order.books else order.items.item_name,
            str(order.quantity),
            str(order.unit),
            str(order.subunit),
            str(order.subunit_quantity),
            str(order.unit_price),
            str(order.price),
            str(order.total_price),
        ])
    orders_table = Table(data, colWidths=[130, 50, 50, 60, 60, 60, 60, 60 ])

    # Define the alternating row colors
    TableOddFill = colors.HexColor(0xEEEEEE)  # Light grey color
    TableEvenFill = colors.HexColor(0xFFFFFF)  # White color
    TableHeaderFill = colors.HexColor(0x3498DB)  # Header blue color

    # Apply styles to the table
    
    orders_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Outer border
    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for data cells
    ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),  # Font style for data cells
    ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for header row
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font style for header row
    ('BACKGROUND', (0, 0), (-1, 0), TableHeaderFill),  # Header row background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
    ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Bottom padding
    ]))
    # Apply alternating row colors for data rows
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = TableEvenFill
        else:
            bg_color = TableOddFill
        orders_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), bg_color)]))
    elements.append(orders_table)
    elements.append(Spacer(1, 12))  # Add some space

    # Add Total Price and Received By
    total_price_received_by = [
        ["Total Price:", str(order_group.total_price)+" ብር"],
        ["Received By:", order_group.recieved_by],
    ]
    total_price_received_by_table = Table(total_price_received_by, colWidths=[60, 75] ,hAlign="RIGHT")
    total_price_received_by_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
    ]))
    elements.append(total_price_received_by_table)
    elements.append(Spacer(1, 12))  # Add some space

    # Build the PDF document
    doc.build(elements)

   # Return the PDF file as a response for download
    with open("incoming.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=incoming.pdf"
        return response

def generate_pdf_report(request):
    # Sample data from your models
    order_group = OrderGroup.objects.get(id=39)  # Assuming you have an OrderGroup with ID 1
    orders = Order.objects.all()

    # Create a PDF document
    doc = SimpleDocTemplate("order_group_report.pdf", pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    style_heading = styles["Title"]
    style_normal = styles["Normal"]
    
    style_heading1 = styles["Heading1"]

    elements.append(Spacer(1, -50))  # Remove some space
    # Define the title text
    title_text = "Andelus School"
    styles = getSampleStyleSheet()
    style_heading = styles["Title"]
    title = Paragraph("<b>{}</b>".format(title_text), style_heading)

    # Load the image
    image_path = "static/img/login.png"
    logo = Image(image_path, width=65, height=60)

    # Create a table for layout
    data = [[title, logo]]
    table = Table(data, colWidths=[350, 350], hAlign="CENTER")
    table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(table)
        # Add title
    title = Paragraph("<b>Order Group Report</b>", style_heading)
    title_table = Table([[title]], colWidths=[500], hAlign="CENTER")
    elements.append(title_table)
    elements.append(Spacer(1, 12))  # Add some space

   # Add Order Group Information
   # Create a table for order information
    order_info_data = [
        [Paragraph("<b>Order Type:</b>", style_normal), Paragraph(order_group.order_type, style_normal)],
        [Paragraph("<b>Order For:</b>", style_normal), Paragraph(order_group.order_for, style_normal)],
        [Paragraph("<b>Status:</b>", style_normal), Paragraph(order_group.status, style_normal)],
        [Paragraph("<b>Date:</b>", style_normal), Paragraph(order_group.date.strftime('%Y-%m-%d'), style_normal)]
    ]
    order_info_table = Table(order_info_data, colWidths=[80, 80], hAlign="CENTER")
    order_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(order_info_table)
    elements.append(Spacer(1, 12))  # Add some space
    # Add Orders Table
    data = [["Products", "Quantity", "Price", "Tax", "Unit"]]
    for order in orders:
        data.append([
            order.books.book_name if order.books else order.items.item_name,
            str(order.quantity),
            str(order.price),
            str(order.tax),
            order.unit
        ])
    orders_table = Table(data, colWidths=[200, 50, 50, 50, 50])

    # Define the alternating row colors
    TableOddFill = colors.HexColor(0xEEEEEE)  # Light grey color
    TableEvenFill = colors.HexColor(0xFFFFFF)  # White color
    TableHeaderFill = colors.HexColor(0x3498DB)  # Header blue color

    # Apply styles to the table
    # Apply styles to the table
    orders_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), TableHeaderFill),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Outer border
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Font style
        ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Bottom padding
    ]))

    # Apply alternating row colors for data rows
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = TableEvenFill
        else:
            bg_color = TableOddFill
        orders_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), bg_color)]))
    elements.append(orders_table)
    elements.append(Spacer(1, 12))  # Add some space

    # Add Total Price and Received By
    total_price_received_by = [
        ["Total Price:", str(order_group.total_price)],
        ["Received By:", order_group.recieved_by],
    ]
    total_price_received_by_table = Table(total_price_received_by, colWidths=[100, 200])
    total_price_received_by_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(total_price_received_by_table)
    elements.append(Spacer(1, 12))  # Add some space

    # Build the PDF document
    doc.build(elements)

   # Return the PDF file as a response for download
    with open("order_group_report.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=order_group_report.pdf"
        return response


def index(request):
    total_orders = OrderGroup.objects.count()
    total_items = Item.objects.count()
    total_books = Book.objects.count()

    if request.user.groups.filter(name='Director').exists():
        pending_orders_count = OrderGroup.objects.filter(status='Pending', user=request.user).count()
        accepted_orders_count = OrderGroup.objects.filter(status='Accepted', user=request.user).count()
        completed_orders_count = OrderGroup.objects.filter(status='Complete', user=request.user).count()

        total_orders = OrderGroup.objects.filter(user=request.user).count()
        total_items = Order.objects.filter(user=request.user, is_item=True).count()
        total_books = Order.objects.filter(user=request.user, is_book=True).count()
        outgoing_orders = OrderGroup.objects.filter(user=request.user, order_type='outgoing').order_by('-date')[:5]

        context = {
            'pending_orders_count': pending_orders_count,
            'accepted_orders_count': accepted_orders_count,
            'completed_orders_count': completed_orders_count,
            'total_orders': total_orders,
            'total_items': total_items,
            'total_books': total_books,
            'outgoing_orders': outgoing_orders,
        }
    else:
        incoming_orders = OrderGroup.objects.filter(order_type='incoming').order_by('-date')[:5]
        outgoing_orders = OrderGroup.objects.filter(order_type='outgoing').order_by('-date')[:5]
        pending_orders_count = OrderGroup.objects.filter(status='Pending').count()
        accepted_orders_count = OrderGroup.objects.filter(status='Accepted').count()
        completed_orders_count = OrderGroup.objects.filter(status='Complete').count()
        books = Store.objects.filter(is_book=True)[:5]
        items = Store.objects.filter(is_item=True)[:5]

        context = {
            'total_orders': total_orders,
            'total_items': total_items,
            'total_books': total_books,
            'books': books,
            'items': items,
            'incoming_orders': incoming_orders,
            'outgoing_orders': outgoing_orders,
            'pending_orders_count': pending_orders_count,
            'accepted_orders_count': accepted_orders_count,
            'completed_orders_count': completed_orders_count,
        }

    return render(request, 'index.html', context)

def book_store(request):
    page = 'book'
    book = Store.objects.filter(is_book = True)
    form = BookForm()
    context = {'books':book,'page':page, 'book_form': form}
    return render(request, 'store/store.html', context)

def item_store(request):
    page = 'item'
    item = Store.objects.filter(is_item = True)
    form = ItemForm()
    context = {'items':item ,'page':page,'item_form':form}
    return render(request, 'store/store.html', context)



@transaction.atomic
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                existing_book = Book.objects.get(
                    book_name=form.cleaned_data['book_name'],
                    grade=form.cleaned_data['grade'],
                    pages=form.cleaned_data['pages'],
                    subject=form.cleaned_data['subject'],
                )
                # If the book exists, add a message and redirect to the previous page

                messages.warning(request, 'Book already exists')
                return redirect(request.META.get('HTTP_REFERER', 'index'))

            except ObjectDoesNotExist:
                # If the book doesn't exist, save the form and redirect
                book = form.save()
                Store.objects.create(books=book, is_book=True)
                messages.success(request, 'Book added successfully')
                return redirect(reverse('product_detail', kwargs={'product_id': book.id}) + f'?p=book')
        else:
            # Form is not valid, add a message and redirect to the previous page
            messages.error(request, 'Invalid form data')
            return redirect(request.META.get('HTTP_REFERER', 'index'))

    # If the request method is not POST, redirect to the previous page
    messages.error(request, 'Invalid request')
    return redirect(request.META.get('HTTP_REFERER', 'index'))
    
@transaction.atomic
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                existing_item = Item.objects.get(
                item_name=form.cleaned_data['item_name'],
            )
                # If the item exists, add a message and redirect to the previous page
                messages.warning(request, 'Item already exists')
                return redirect(request.META.get('HTTP_REFERER', 'index'))

            except ObjectDoesNotExist:
                # If the book doesn't exist, save the form and redirect
                item = form.save()
                Store.objects.create(items=item, is_item=True)
                messages.success(request, 'Item added successfully')
                return redirect(reverse('product_detail', kwargs={'product_id': item.id}) + f'?p=item')
        else:
            # Form is not valid, add a message and redirect to the previous page
            messages.error(request, 'Invalid form data')
            return redirect(request.META.get('HTTP_REFERER', 'index'))

    # If the request method is not POST, redirect to the previous page
    messages.error(request, 'Invalid request')
    return redirect(request.META.get('HTTP_REFERER', 'index'))

# detail to add quantity and other like price , unit ... to the list
# def product_detail(request,product_id):
#     product_type = request.GET['p']
#     if request.user.groups.filter(name='Custodian').exists():
#         if product_type == 'book':
#             page = 'book'
#             product = Book.objects.get(id = product_id)
#             book = Store.objects.get(books = product)
#             product_quantity =  book.quantity
#             form = OrderForm()
#         elif product_type == 'item':
#             page = 'item'
#             product = Item.objects.get(id = product_id)
#             item = Store.objects.get(items = product)
#             product_quantity =  item.quantity
#             form = OrderForm( )
   
#     elif request.user.groups.filter(name='Director').exists():
#         if product_type == 'book':
#             page = 'book'
#             product = Book.objects.get(id = product_id)
#             book = Store.objects.get(books = product)
#             product_quantity =  book.quantity
#             form = StaffOrderForm()
#         elif product_type == 'item':
#             page = 'item'
#             product = Item.objects.get(id = product_id)
#             item = Store.objects.get(items = product)
#             product_quantity =  item.quantity
#             form = StaffOrderForm( )
#     context = {'product':product,'page':page, 'form':form,'product_quantity':product_quantity }
#     return render(request, 'store/product_detail.html', context)

def product_detail(request, product_id):
  
    try:
        product_type = request.GET.get('p')
        if product_type not in ['book', 'item']:
            messages.error(request, "Invalid product type")
            return redirect(request.META.get('HTTP_REFERER', 'your_default_url'))
    
        if request.user.groups.filter(name='Custodian').exists():
            form_class = OrderForm
        elif request.user.groups.filter(name='Director').exists():
            form_class = StaffOrderForm
        else:
            messages.error(request, "You do not have permission to view this page")
            return redirect(request.META.get('HTTP_REFERER', 'your_default_url'))

        if product_type == 'book':
            product = Book.objects.get(id=product_id)
            store = Store.objects.get(books=product)
        elif product_type == 'item':
            product = Item.objects.get(id=product_id)
            store = Store.objects.get(items=product)

        product_quantity = store.quantity
        form = form_class()

        context = {
            'product': product,
            'page': product_type,
            'form': form,
            'product_quantity': product_quantity,
        }
        return render(request, 'store/product_detail.html', context)
    except (Book.DoesNotExist, Item.DoesNotExist, Store.DoesNotExist):
        messages.error(request, "Product not found")
        return redirect(request.META.get('HTTP_REFERER', 'your_default_url'))
        

def store_detail(request, store_id):
    product_type = request.GET.get('p')
    product = get_object_or_404(Store, id=store_id)
    store_form = StoreForm(instance=product)
    book_form = BookForm(instance=product.books) if product.books else None
    item_form = ItemForm(instance=product.items) if product.items else None

    if product_type == 'book' and product.books:
        form = book_form
        form_class = BookForm
    elif product_type == 'item' and product.items:
        form = item_form
        form_class = ItemForm
    else:
        form = None
        form_class = None

    if request.method == 'POST' and form:
        store_form = StoreForm(request.POST, instance=product)
        form = form_class(request.POST, request.FILES, instance=getattr(product, product_type + 's'))
        if store_form.is_valid() and form.is_valid():
            store_form.save()
            form.save()
            if product_type == 'book':
                messages.success(request, 'Book updated successfully.')
                return redirect('book_store')
            elif product_type == 'item':
                messages.success(request, 'Item updated successfully.')
                return redirect('item_store')
        else:
            messages.error(request, 'Form submission failed. Please check the input.')

    context = {'product': product, 'product_type': product_type, 'book_form': book_form, 'item_form': item_form, 'store_form': store_form}
    return render(request, 'store/store_detail.html', context)        

# def store_detail(request,store_id):
#     product_type = request.GET['p']
#     product = Store.objects.get(id = store_id)
#     book_form = BookForm(instance= product.books)
#     store_form = StoreForm(instance= product)
#     item_form = ItemForm(instance= product.items)
#     if product_type == 'book':
#         if product.books:
#             if request.method == 'POST':
#                 store_form = StoreForm(request.POST,instance= product)
#                 book_form = BookForm(request.POST, request.FILES , instance= product.books)
#                 if store_form.is_valid() and book_form.is_valid():
#                     store_form.save()
#                     book_form.save()
#                 #return redirect(reverse('product_detail', kwargs={'product_id': book}) + f'?p=book')
#                 return redirect('book_store')
#     elif product_type == 'item':
#         if product.items:
#             if request.method == 'POST':
#                 store_form = StoreForm(request.POST,instance= product)
#                 item_form = ItemForm(request.POST, request.FILES ,instance= product.items)
#                 if store_form.is_valid() and item_form.is_valid():
#                     store_form.save()
#                     item_form.save()
#                 #return redirect(reverse('product_detail', kwargs={'product_id': book}) + f'?p=book')
#                 return redirect('item_store')
#     context = {'product':product, 'book_form':book_form, 'item_form':item_form, 'store_form':store_form}
#     return render(request, 'store/store_detail.html', context)

def finish_order(request):
    if request.method == 'POST':
        # Check if the cart is empty
        if not Cart(request).cart:
            messages.warning(request, 'Your List is empty. Please add some products before completing the order.')
            return redirect('list_summary')  # Adjust the URL name as per your project

        if request.user.groups.filter(name='Custodian').exists():
            return _handle_custodian_order(request)
        elif request.user.groups.filter(name='Director').exists():
            return _handle_director_order(request)
        else:
            messages.error(request, 'Access is forbidden. ')
            return redirect(request.META.get('HTTP_REFERER', 'index'))

    else:
        # Add message indicating the action is not allowed for the current request method
        messages.error(request, 'The action you requested is not allowed for the current request method.')
        return redirect(request.META.get('HTTP_REFERER', 'index'))

def _handle_custodian_order(request):
    # Handle Custodian's order completion logic
    order_for = request.POST.get('order_for')
    order_by = request.POST.get('order_by')
    recieved_by = request.POST.get('recieved_by')
    overall_total = request.POST.get('overall_total')
    # Validate form inputs
    if not all([order_for, order_by, recieved_by, overall_total]):
        messages.error(request, 'Please fill out all the fields.')
        return redirect('list_summary')
    
    # Get the cart and iterate through the products
    cart = Cart(request)
    with transaction.atomic():
        # Save the OrderGroup
        user = request.user
        order_group = OrderGroup(
            user=user, 
            order_type='incoming',
            status='Complete',
            order_for=order_for,
            order_by=order_by,
            date=datetime.today(),
            recieved_by=recieved_by,
            total_price=overall_total
        )
        order_group.save()
        for product_key, product_data in cart.cart.items():
            product_id, product_type = product_key.split('_')

            # Create an instance of the Order model for each product
            unit_price = product_data['price'] 
            total = product_data['quantity'] * product_data['price'] 
            tax_price = total * (float( product_data['tax'])/100)
            total_price = total + tax_price
            # Create an instance of the Order model for each product
            order = Order(
                user=user,
                quantity=product_data['quantity'],
                subunit_quantity=product_data['subunit_quantity'],
                price= total,
                unit_price= unit_price,
                tax= product_data['tax'],
                total_price= total_price,
                order_type='incoming',  # Set order type as needed
                unit=product_data['unit'],  # Assuming you want the last unit in the cart
                subunit=product_data['sub_unit'],  # Assuming you want the last unit in the cart
            )
            if product_type == 'book':
                book = Book.objects.get(id=product_id)
                order.books = book
                order.is_book = True
                store_product, _ = Store.objects.get_or_create(
                    books_id=product_id,
                    defaults={'is_book': True}
                )
            elif product_type == 'item':
                item = Item.objects.get(id=product_id)
                order.items = item
                order.is_item = True
                store_product, _ = Store.objects.get_or_create(
                    items_id=product_id,
                    defaults={'is_item': True}
                )
            order.save()

            if store_product:
                store_product.quantity += product_data['subunit_quantity']
                store_product.save()
            order_group.orders.add(order)
    
    # Clear the cart after completing the orders
    cart.clear()
    messages.success(request, 'Orders placed successfully.')
    return redirect(reverse('orders') + '?p=gebi')

def _handle_director_order(request):
    # Handle Director's order completion logic
    order_by = request.POST.get('order_by')
    password = request.POST.get('password')
    # Validate form inputs
    if not all([order_by, password]):
        messages.error(request, 'Please fill out all the fields.')
        return redirect('list_summary')
    
    # Check password
    if not request.user.check_password(password):
        messages.error(request, 'Incorrect password. Please try again.')
        return redirect('list_summary')
    
    # Get the cart and iterate through the products
    cart = Cart(request)
    with transaction.atomic():
        # Save the OrderGroup
        userr = request.user
        order_group = OrderGroup(
            user=userr, 
            order_type='outgoing',
            status='Pending',
            order_by=order_by,
            date=datetime.today(),
        )
        order_group.save()
        for product_key, product_data in cart.cart.items():
            product_id, product_type = product_key.split('_')

            # Create an instance of the Order model for each product
            order = Order(
                user=userr,
                quantity=product_data['quantity'],
                subunit_quantity=product_data['subunit_quantity'],
                order_type='outgoing',  # Set order type as needed
                unit=product_data['unit'],  # Assuming you want the last unit in the cart
                subunit=product_data['sub_unit'],  # Assuming you want the last unit in the cart
            )
            if product_type == 'book':
                book = Book.objects.get(id=product_id)
                order.books = book
                order.is_book = True
            elif product_type == 'item':
                item = Item.objects.get(id=product_id)
                order.items = item
                order.is_item = True
            order.save()
            order_group.orders.add(order)

    # Clear the cart after completing the orders
    cart.clear()
    messages.success(request, 'Orders placed successfully.')
    return redirect(reverse('orders') + '?p=wechi')

# def finish_order(request):
#     if request.user.groups.filter(name='Custodian').exists():
#         if request.method == 'POST':
#             order_for = request.POST.get('order_for')
#             order_by = request.POST.get('order_by')
#             recieved_by = request.POST.get('recieved_by')
#             overall_total = request.POST.get('overall_total')
#             #if request.user.groups.filter(name='Custodian').exists():
#             user = request.user
#             order_group = OrderGroup(user=user, 
#             order_type='incoming',
#             status='Complete',
#             order_for= order_for,
#             order_by= order_by,
#             date=datetime.today(),
#             recieved_by= recieved_by,
#             total_price= overall_total
#             )
#             order_group.save()
#             # Get the cart and iterate through the products
#             cart = Cart(request)
#             # Use a transaction to ensure atomicity
#         with transaction.atomic():
#             # Iterate through the cart
#             for product_key, product_data in cart.cart.items():
#                 product_id, product_type = product_key.split('_')
                 
#                 unit_price = product_data['price'] 
#                 total = product_data['quantity'] * product_data['price'] 
#                 tax_price = total * (float( product_data['tax'])/100)
#                 total_price = total + tax_price
#                 # Create an instance of the Order model for each product
#                 order = Order(
#                     user=user,
#                     quantity=product_data['quantity'],
#                     subunit_quantity=product_data['subunit_quantity'],
#                     price= total,
#                     unit_price= unit_price,
#                     tax= product_data['tax'],
#                     total_price= total_price,
#                     order_type='incoming',  # Set order type as needed
#                     unit=product_data['unit'],  # Assuming you want the last unit in the cart
#                     subunit=product_data['sub_unit'],  # Assuming you want the last unit in the cart
#                 )
#                 # Assuming 'books' and 'items' are related names in the Order model
#                 if product_type == 'book':
#                     book = Book.objects.get(id= product_id)
#                     order.books=book
#                     order.is_book = True
#                     store_product, created = Store.objects.get_or_create(
#                         books_id=product_id,
#                         defaults={'is_book': True}
#                     )
#                 elif product_type == 'item':
#                     item = Item.objects.get(id= product_id)
#                     order.items = item
#                     order.is_item = True
#                     store_product, created = Store.objects.get_or_create(
#                         items_id=product_id,
#                         defaults={'is_item': True}
#                     )
#                 order.save()
#                 if store_product:
#                     store_product.quantity += product_data['subunit_quantity']
#                     store_product.save()
#                 order_group.orders.add(order)
#         # Clear the cart after completing the orders
#         cart.clear()
#         order_group = OrderGroup.objects.filter(user = user, order_type= 'incoming')

#         return redirect(reverse('orders') + f'?p=gebi')
   
#     elif request.user.groups.filter(name='Director').exists():
#         if request.method == 'POST':
#             order_by = request.POST.get('order_by')
#             password = request.POST.get('password')
#               # Check if the provided password matches the user's password
#             if not request.user.check_password(password):
#                 messages.error(request, 'Incorrect password. Please try again.')
#                 return redirect(reverse('list_summary'))
#             #if request.user.groups.filter(name='Custodian').exists():
#             userr = request.user
#             order_group = OrderGroup(user=userr, 
#             order_type='outgoing',
#             status='Pending',
#             order_by= order_by,
#             date=datetime.today(),
#             )
#             order_group.save()
#             # Get the cart and iterate through the products
#             cart = Cart(request)
#             # Use a transaction to ensure atomicity
#         with transaction.atomic():
#             # Iterate through the cart
#             for product_key, product_data in cart.cart.items():
#                 product_id, product_type = product_key.split('_')

#                 # Create an instance of the Order model for each product
#                 order = Order(
#                     user=userr,
#                     quantity=product_data['quantity'],
#                     subunit_quantity=product_data['subunit_quantity'],
#                     # price=product_data['price'],
#                     # total_price=product_data['quantity'] * product_data['price'],
#                     order_type='outgoing',  # Set order type as needed
#                     unit=product_data['unit'],  # Assuming you want the last unit in the cart
#                     subunit=product_data['sub_unit'],  # Assuming you want the last unit in the cart
#                 )
#                 #Assuming 'books' and 'items' are related names in the Order model
#                 if product_type == 'book':
#                     book = Book.objects.get(id= product_id)
#                     order.books=book
#                     order.is_book = True
#                     # store_product, created = Store.objects.get_or_create(
#                     #     books_id=product_id,
#                     #     defaults={'is_book': True}
#                     # )
#                 elif product_type == 'item':
#                     item = Item.objects.get(id= product_id)
#                     order.items = item
#                     order.is_item = True
#                     # store_product, created = Store.objects.get_or_create(
#                     #     items_id=product_id,
#                     #     defaults={'is_item': True}
#                     # )
#                 order.save()
#                 # if store_product:
#                 #     store_product.quantity += product_data['quantity']
#                 #     store_product.save()
#                 order_group.orders.add(order)
#             # Clear the cart after completing the orders
#             cart.clear()
#             order_group = OrderGroup.objects.filter(user = userr, order_type= 'outgoing')

#             return redirect(reverse('orders') + f'?p=wechi')
#         return HttpResponseForbidden('Forbidden')

def orders(request):
    page = request.GET.get('p')  # Use get() to avoid KeyError if 'p' is not in GET parameters
    
    if page == 'gebi':
        if request.user.groups.filter(name='Custodian').exists():
            order_group = OrderGroup.objects.filter(user=request.user, order_type='incoming').order_by('-date')
        elif request.user.groups.filter(name='Manager').exists():
            order_group = OrderGroup.objects.filter(order_type='incoming').order_by('-date')
        else:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('index')  # Redirect to home or another appropriate page

    elif page == 'wechi':
        if request.user.groups.filter(name='Director').exists():
            order_group = OrderGroup.objects.filter(user=request.user, order_type='outgoing').order_by('-date')
        elif request.user.groups.filter(name='Custodian').exists():
            order_group = OrderGroup.objects.filter(
                Q(status='Complete') | Q(status='Accepted'), order_type='outgoing'
            ).order_by('-date')
        else:
            order_group = OrderGroup.objects.filter(order_type='outgoing').order_by('-date')
    else:
        messages.error(request, "Invalid page parameter.")
        return redirect('index')  # Redirect to home or another appropriate page

    context = {'order_group': order_group, 'page': page}
    return render(request, 'order/order.html', context)

# def orders(request):
#     if request.GET['p'] == 'gebi':
#         page =  request.GET['p']
#         if request.user.groups.filter(name='Custodian').exists():
#             order_group = OrderGroup.objects.filter( user = request.user, order_type= 'incoming').order_by('-date')
#         elif request.user.groups.filter(name='Manager').exists():
#             order_group = OrderGroup.objects.filter(order_type= 'incoming').order_by('-date')
#     elif request.GET['p'] =='wechi':
#         page =  request.GET['p']
#         if request.user.groups.filter(name='Director').exists():
#             order_group = OrderGroup.objects.filter( user = request.user, order_type= 'outgoing').order_by('-date')
#         elif request.user.groups.filter(name='Custodian').exists():
#             order_group = OrderGroup.objects.filter(Q(status='Complete') | Q(status='Accepted'), order_type='outgoing').order_by('-date')
#         else:
#             order_group = OrderGroup.objects.filter(order_type= 'outgoing').order_by('-date')
#     context= {'order_group': order_group, 'page':page}
#     return render(request, 'order/order.html', context)

def order_detail(request,order_id):
    order = get_object_or_404(OrderGroup, id=order_id)
    context = {'order':order}
    return render(request, 'order/order_detail.html', context)

def confirm_all_quantities(request):
    try:
        ordergroup_id = int(request.POST.get('ordergroup_id'))
        quantities_data = json.loads(request.POST.get('confirmed_quantities'))
    except (ValueError, TypeError, json.JSONDecodeError):
        messages.error(request, 'Invalid data format')
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    try:
        ordergroup = OrderGroup.objects.get(id=ordergroup_id)
    except OrderGroup.DoesNotExist:
        messages.error(request, f'OrderGroup with ID {ordergroup_id} does not exist')
        return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)

    for item_data in quantities_data:
        try:
            item_id = int(item_data['productId'])
            quantity = int(item_data['quantity'])
            item = ordergroup.orders.get(id=item_id)
            item.confirmed_quantity = quantity
            item.save()
        except (ValueError, TypeError, Order.DoesNotExist):
            messages.error(request, 'Invalid product data')
            return JsonResponse({'error': 'Invalid product data'}, status=400)

    # Update the status and the user who approved the order
    ordergroup.status = 'Accepted'
    ordergroup.approved_by = request.user.first_name
    ordergroup.save()

    messages.success(request, 'Confirmed quantities updated successfully')
    return JsonResponse({'success': 'Confirmed quantities updated successfully'})

# @require_POST
# def confirm_all_quantities(request):
#     try:
#         ordergroup_id = int(request.POST.get('ordergroup_id'))
#         quantities_data = json.loads(request.POST.get('confirmed_quantities'))
#     except (ValueError, TypeError, json.JSONDecodeError):
#         return JsonResponse({'error': 'Invalid data format'}, status=400)

#     try:
#         ordergroup = OrderGroup.objects.get(id=ordergroup_id)
#     except OrderGroup.DoesNotExist:
#         return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)

#     for item_data in quantities_data:
#         try:
#             item_id = int(item_data['productId'])
#             quantity = int(item_data['quantity'])
#             item = ordergroup.orders.get(id=item_id)
#             item.confirmed_quantity = quantity
#             item.save()
#         except (ValueError, TypeError, Order.DoesNotExist):
#             return JsonResponse({'error': 'Invalid product data'}, status=400)
#     ordergroup.status='Accepted'
#     ordergroup.approved_by = request.user.first_name
#     ordergroup.save()
#     return JsonResponse({'success': 'Confirmed quantities updated successfully'})


@require_POST
def issue_quantities(request):
    try:
        ordergroup_id = int(request.POST.get('ordergroup_id'))
        quantities_data = json.loads(request.POST.get('issued_quantities'))
    except (ValueError, TypeError, json.JSONDecodeError):
        messages.error(request, 'Invalid data format')
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    try:
        ordergroup = OrderGroup.objects.get(id=ordergroup_id)
    except OrderGroup.DoesNotExist:
        messages.error(request, f'OrderGroup with ID {ordergroup_id} does not exist')
        return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)

    for item_data in quantities_data:
        try:
            item_id = int(item_data['productId'])
            quantity = int(item_data['quantity'])
            product = ordergroup.orders.get(id=item_id)

            if product.is_book:
                store_book = Store.objects.get(books=product.books)
                difference = quantity - product.issued_quantity
                new_quantity = store_book.quantity - difference
                if new_quantity < 0:
                    raise ValidationError('Store quantity cannot be negative.')
                store_book.quantity = new_quantity
                store_book.save()
            elif product.is_item:
                store_item = Store.objects.get(items=product.items)
                difference = quantity - product.issued_quantity
                new_quantity = store_item.quantity - difference
                if new_quantity < 0:
                    raise ValidationError('Store quantity cannot be negative.')
                store_item.quantity = new_quantity
                store_item.save()

            product.issued_quantity = quantity
            product.save()
        except (ValueError, TypeError, Order.DoesNotExist):
            messages.error(request, 'Invalid product data')
            return JsonResponse({'error': 'Invalid product data'}, status=400)
        except Store.DoesNotExist:
            messages.error(request, 'Store item not found')
            return JsonResponse({'error': 'Store item not found'}, status=400)
        except ValidationError as e:
            messages.error(request, str(e))
            return JsonResponse({'error': str(e)}, status=400)

    ordergroup.status = 'Complete'
    ordergroup.save()

    messages.success(request, 'Issued quantities updated successfully')
    return JsonResponse({'success': 'Issued quantities updated successfully'})

# @require_POST
# def issue_quantities(request):
#     try:
#         ordergroup_id = int(request.POST.get('ordergroup_id'))
#         quantities_data = json.loads(request.POST.get('issued_quantities'))
#     except (ValueError, TypeError, json.JSONDecodeError):
#         return JsonResponse({'error': 'Invalid data format'}, status=400)

#     try:
#         ordergroup = OrderGroup.objects.get(id=ordergroup_id)
#     except OrderGroup.DoesNotExist:
#         return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)

#     for item_data in quantities_data:
#         try:
#             item_id = int(item_data['productId'])
#             quantity = int(item_data['quantity'])
#             product = ordergroup.orders.get(id=item_id)
#             if product.is_book:
#                 store_book = Store.objects.get(books=product.books)
#                 difference = quantity - product.issued_quantity
#                 new_quantity = store_book.quantity - difference
#                 if new_quantity < 0:
#                     raise ValidationError('Store quantity cannot be negative.')
#                 store_book.quantity = new_quantity
#                 store_book.save()
#             elif product.is_item:
#                 store_item = Store.objects.get(items=product.items)
#                 difference = quantity - product.issued_quantity
#                 new_quantity = store_item.quantity - difference
#                 if new_quantity < 0:
#                     raise ValidationError('Store quantity cannot be negative.')
#                 store_item.quantity = new_quantity
#                 store_item.save()

#             product.issued_quantity = quantity
#             product.save()
#         except (ValueError, TypeError, Order.DoesNotExist):
#             return JsonResponse({'error': 'Invalid product data'}, status=400)
#         except ValidationError as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     ordergroup.status = 'Complete'
#     ordergroup.save()
#     return JsonResponse({'success': 'issued quantities updated successfully'})

def remove_order(request):
    # Get the product ID and ordergroup ID from the POST data
    product_id = request.POST.get('product_id')
    ordergroup_id = int(request.POST.get('ordergroup_id'))

    try:
        ordergroup = OrderGroup.objects.get(id=ordergroup_id)
    except OrderGroup.DoesNotExist:
        messages.error(request, f'OrderGroup with ID {ordergroup_id} does not exist')
        return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)

    # Retrieve the order to be removed
    order_to_remove = get_object_or_404(Order, id=product_id)

    if ordergroup.orders.count() == 1:
        order_to_remove.delete()
        ordergroup.delete()
        messages.success(request, 'Order removed successfully')
        return JsonResponse({'success': True, 'redirect': 'store/orders?p=wechi'})
    else:
        order_to_remove.delete()
        messages.success(request, 'Order removed successfully')
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
    # Return a JSON response indicating success
    return JsonResponse({'success': True})

# @require_POST
# def remove_order(request):
#     # Get the product ID from the POST data
#     product_id = request.POST.get('product_id')
#     ordergroup_id = int(request.POST.get('ordergroup_id'))
#     try:
#         ordergroup = OrderGroup.objects.get(id=ordergroup_id)
#     except OrderGroup.DoesNotExist:
#         return JsonResponse({'error': f'OrderGroup with ID {ordergroup_id} does not exist'}, status=404)
#     # Retrieve the order to be removed
#     print(ordergroup.orders.count())
#     order_to_remove = get_object_or_404(Order, id=product_id)
#     if ordergroup.orders.count() == 1:
#         order_to_remove.delete()
#         ordergroup.delete()
#         return JsonResponse({'success': True, 'redirect': 'store/orders?p=wechi'})
#     else:
#         order_to_remove.delete()
#         # Perform the removal logic, you can customize this based on your needs
#     # Return a JSON response indicating success
#     return JsonResponse({'message': 'Order removed successfully'})




  ##################3####################################################33  
  ##################3####################################################33  
  ##################3####################################################33  
  ##################3####################################################33  
  ##################3####################################################33  
  ##################3####################################################33  




  
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list view
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list view
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_update.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Redirect to product list view
    return render(request, 'product_delete.html', {'product': product})



def teachers_list(request):
    teachers = User.objects.filter(groups__name='Teacher')
    return render(request, 'merekakebiya/teachers.html', {'teachers': teachers})


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            return JsonResponse({'success': True, 'product_id': product.id})
        else:
            # Form is invalid, return form errors
            errors = product_form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        # Handle GET request if needed
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)        



def add_product_given(request):
    if request.method == 'POST':
        product_given_form = ProductGivenForm(request.POST)
        product_given_detail_formset = ProductGivenDetailForm(request.POST)
        if product_given_form.is_valid() and product_given_detail_formset.is_valid():
            product_given = product_given_form.save()
            for form in product_given_detail_formset:
                product_given_detail = form.save(commit=False)
                product_given_detail.product_given = product_given
                product_given_detail.save()
            return redirect('success_url')  # Redirect to success page
    else:
        product_given_form = ProductGivenForm()
        product_given_detail_formset = ProductGivenDetailForm()
    

    context = {
        'product_given_form': product_given_form,
        'product_given_detail_formset': product_given_detail_formset,
    }

    return render(request, 'merekakebiya/asrekeb.html', context)