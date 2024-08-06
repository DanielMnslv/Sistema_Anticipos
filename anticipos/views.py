from django.shortcuts import render, redirect, get_object_or_404
import os
import uuid
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import messages
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import json
import logging
from django.http import HttpResponse, JsonResponse
from .models import Anticipo
from django.core.paginator import Paginator


def inicio(request):
    opciones_edad = [(str(edad), str(edad)) for edad in range(1, 1000)]
    data = {"opciones_edad": opciones_edad}
    return render(request, "anticipos/form_anticipo.html", data)


def listar_anticipos(request):
    anticipos = Anticipo.objects.all()
    paginator = Paginator(anticipos, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    data = {"anticipos": page_obj}
    return render(request, "anticipos/lista_anticipos.html", data)


def view_form_carga_masiva(request):
    return render(request, "anticipos/form_carga_masiva.html")


def detalles_anticipos(request, id):
    anticipo = get_object_or_404(Anticipo, id=id)
    data = {"anticipo": anticipo}
    return render(request, "anticipos/detalles.html", data)


def registrar_anticipos(request):
    if request.method == "POST":
        centro_costo = request.POST.get("centro_costo")
        nit = request.POST.get("nit")
        nombre = request.POST.get("nombre")
        producto_servicio = request.POST.get("producto_servicio")
        cantidad = request.POST.get("cantidad")
        vlr_unitario = request.POST.get("vlr_unitario")
        subtotal = request.POST.get("subtotal")
        iva = request.POST.get("iva", 0.00)
        retencion = request.POST.get("retencion")
        total_pagar = request.POST.get("total_pagar")
        observaciones = request.POST.get("observaciones")
        foto_producto = request.FILES.get("foto_producto")

        if foto_producto:
            foto_producto = generate_unique_filename(foto_producto)

        anticipo = Anticipo(
            centro_costo=centro_costo,
            nit=nit,
            nombre=nombre,
            producto_servicio=producto_servicio,
            cantidad=cantidad,
            vlr_unitario=vlr_unitario,
            subtotal=subtotal,
            iva=iva,
            retencion=retencion,
            total_pagar=total_pagar,
            observaciones=observaciones,
            foto_producto=foto_producto,
        )
        anticipo.save()

        messages.success(
            request, f"La anticipo para {nit} se registró correctamente 😉"
        )
        return redirect("listar_anticipos")

    return redirect("inicio")


def view_form_update_anticipo(request, id):
    anticipo = get_object_or_404(Anticipo, id=id)
    data = {"anticipo": anticipo}
    return render(request, "anticipos/form_update_anticipo.html", data)


def actualizar_anticipo(request, id):
    if request.method == "POST":
        anticipo = get_object_or_404(Anticipo, id=id)
        anticipo.centro_costo = request.POST.get("centro_costo")
        anticipo.nit = request.POST.get("nit")
        anticipo.nombre = request.POST.get("nombre")
        anticipo.producto_servicio = request.POST.get("producto_servicio")
        anticipo.cantidad = request.POST.get("cantidad")
        anticipo.vlr_unitario = request.POST.get("vlr_unitario")
        anticipo.subtotal = request.POST.get("subtotal")
        anticipo.iva = request.POST.get("iva")
        anticipo.retencion = request.POST.get("retencion")
        anticipo.total_pagar = request.POST.get("total_pagar")
        anticipo.observaciones = request.POST.get("observaciones")

        if "foto_producto" in request.FILES:
            anticipo.foto_producto = generate_unique_filename(
                request.FILES["foto_producto"]
            )

        anticipo.save()
        messages.success(
            request, f"El anticipo para {anticipo.nit} se actualizó correctamente 😉"
        )
        return redirect("listar_anticipos")

    return redirect("inicio")


def informe_anticipo(request):
    try:
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="informe_anticipo.pdf"'
        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(letter),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20,
        )
        styles = getSampleStyleSheet()
        style_heading = styles["Heading1"]
        style_body = styles["BodyText"]

        datos = Anticipo.objects.all()
        if not datos.exists():
            return HttpResponse(
                "No hay datos de anticipos disponibles para generar el informe."
            )

        contenido = []
        encabezados = (
            "centro_costo",
            "nit",
            "nombre",
            "producto/servicio",
            "cantidad",
            "vlr_unit",
            "subtotal",
            "iva",
            "retencion",
            "total_pagar",
            "observaciones",
            "Fecha",
        )
        contenido.append(encabezados)

        for anticipo in datos:
            contenido.append(
                (
                    anticipo.centro_costo,
                    anticipo.nit,
                    anticipo.nombre,
                    anticipo.producto_servicio,
                    anticipo.cantidad,
                    anticipo.vlr_unitario,
                    anticipo.subtotal,
                    anticipo.iva,
                    anticipo.retencion,
                    anticipo.total_pagar,
                    anticipo.observaciones,
                    anticipo.created_at.strftime("%Y-%m-%d"),
                )
            )

        tabla = Table(
            contenido, repeatRows=1
        )  # repeatRows=1 asegura que la cabecera se repita en cada página
        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        contenido_pdf = []
        contenido_pdf.append(Paragraph("Informe de Anticipos", style_heading))
        contenido_pdf.append(
            Paragraph(
                "Este es un informe generado automáticamente con los datos de Anticipos.",
                style_body,
            )
        )
        contenido_pdf.append(tabla)

        doc.build(contenido_pdf)
        return response

    except Exception as e:
        logging.error(f"Error al generar el informe PDF: {str(e)}")
        return HttpResponse(f"Error al generar el informe PDF: {str(e)}")


def eliminar_anticipo(request):
    if request.method == "POST":
        id_anticipo = json.loads(request.body)["idAnticipo"]
        anticipo = get_object_or_404(Anticipo, id=id_anticipo)
        anticipo.delete()
        return JsonResponse({"resultado": 1})
    return JsonResponse({"resultado": 1})


def cargar_archivo(request):
    try:
        if request.method == "POST":
            archivo_xlsx = request.FILES["archivo_xlsx"]
            if archivo_xlsx.name.endswith(".xlsx"):
                df = pd.read_excel(archivo_xlsx, header=3)
                for _, row in df.iterrows():
                    centro_costo = row["centro_costo"]
                    nit = row["nit"]
                    nombre = row["nombre"]
                    producto_servicio = row["producto_servicio"]
                    cantidad = row["cantidad"]
                    vlr_unitario = row["vlr_unitario"]
                    subtotal = row["subtotal"]
                    iva = row["iva"]
                    retencion = row["retencion"]
                    total_pagar = row["total_pagar"]
                    observaciones = row["observaciones"]

                    Anticipo.objects.update_or_create(
                        cantidad=cantidad,
                        defaults={
                            "centro_costo": centro_costo,
                            "nit": nit,
                            "nombre": nombre,
                            "producto_servicio": producto_servicio,
                            "cantidad": cantidad,
                            "vlr_unitario": vlr_unitario,
                            "subtotal": subtotal,
                            "iva": iva,
                            "retencion": retencion,
                            "total_pagar": total_pagar,
                            "observaciones": observaciones,
                            "foto_producto": "",
                        },
                    )

                return JsonResponse(
                    {
                        "status_server": "success",
                        "message": "Los datos se importaron correctamente.",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status_server": "error",
                        "message": "El archivo debe ser un archivo de Excel válido.",
                    }
                )
        else:
            return JsonResponse(
                {"status_server": "error", "message": "Método HTTP no válido."}
            )
    except Exception as e:
        logging.error("Error al cargar el archivo: %s", str(e))
        return JsonResponse(
            {
                "status_server": "error",
                "message": f"Error al cargar el archivo: {str(e)}",
            }
        )


def generate_unique_filename(file):
    extension = os.path.splitext(file.name)[1]
    unique_name = f"{uuid.uuid4()}{extension}"
    return SimpleUploadedFile(unique_name, file.read())
