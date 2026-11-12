from django.shortcuts import render
from django.views.generic import ListView
from .models import Producto


# VISTA BASADA EN FUNCIÓN (FBV)
def home(request):
    contexto = {
        "titulo": "Bienvenida a TechZone",
        "total": Producto.objects.count(),
        "disponibles": Producto.objects.filter(stock__gt=0).count(),
        "agotados": Producto.objects.filter(stock=0).count(),
    }
    return render(request, "home.html", contexto)


# VISTA BASADA EN CLASE (CBV)
class ProductoListView(ListView):
    model = Producto
    template_name = "catalogo.html"
    context_object_name = "productos"

    def get_queryset(self):
        # QuerySet 1: solo productos con stock, ordenados por precio
        queryset = Producto.objects.filter(stock__gt=0).order_by("precio")

        # QuerySet 2: filtro por categoría ?categoria=...
        categoria = self.request.GET.get("categoria", "").strip()
        if categoria:
            queryset = queryset.filter(categoria__iexact=categoria)

        # QuerySet 3: búsqueda por nombre ?q=...
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(nombre__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = (
            Producto.objects.values_list("categoria", flat=True)
            .distinct()
            .order_by("categoria")
        )
        context["categoria_actual"] = self.request.GET.get("categoria", "")
        context["q"] = self.request.GET.get("q", "")
        context["agotados"] = Producto.objects.filter(stock=0)
        return context