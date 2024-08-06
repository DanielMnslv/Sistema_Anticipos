from django.db import models


class Anticipo(models.Model):
    centro_costo = models.CharField(max_length=50)
    nit = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    producto_servicio = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    vlr_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    retencion = models.DecimalField(max_digits=10, decimal_places=2)
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.CharField(max_length=200)
    foto_producto = models.ImageField(
        upload_to="fotos_productos/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def es_extension_valida(self):
        extensiones_validas = [".jpg", ".jpeg", ".png", ".gif"]
        return any(
            self.foto_producto.name.lower().endswith(ext) for ext in extensiones_validas
        )

    def __str__(self):
        return f"Centro de Costo: {self.centro_costo}, NIT: {self.nit}, Nombre: {self.nombre}, Producto/Servicio: {self.producto_servicio}, Cantidad: {self.cantidad}, Vlr. Unitario: {self.vlr_unitario}, Subtotal: {self.subtotal}, IVA: {self.iva}, Retención: {self.retencion}, Total a Pagar: {self.total_pagar}, Observaciones: {self.observaciones}"

    class Meta:
        db_table = "anticipos"
        ordering = ["-id"]
        unique_together = (("centro_costo", "nit", "producto_servicio"),)
