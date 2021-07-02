from django.shortcuts import render
from django.views import generic
from .forms import ParametersForm
from . import soporte

# Create your views here.

def index(request):
    return render(request, "index.html")

def acercade(request):
    return render(request, "acercade.html")

#REVISAAAAAAAAAAAAAAAAAR
class simulacion(generic.FormView):
    form_class = ParametersForm
    template_name = 'tp.html'

    def form_valid(self, form):

        dias = form.cleaned_data['dias']
        diaInicio = form.cleaned_data['diaInicio']
        diaFin = form.cleaned_data['diaFin']
        limiteReposicion = form.cleaned_data['limiteReposicion']
        cantReposicion = form.cleaned_data['cantReposicion']
        stock = form.cleaned_data['stock']
        capacidad_almacen = form.cleaned_data['capacidad']

        stocki = stock
        km = 350  # costo mantenimiento
        ko = 50000  # costo del pedido
        ks = 9500  # costo del stock-out
        ki = 2000  # costo de imagen
        kp = 0  # costo x pedido por carburador
        kc = 8000  # costo de sobrepasar la capacidad del almacén
        estadoPedido = ""
        cont = 0

        matriz = [[0] * 15 for f in range(2)]

        if cantReposicion <= 100:
            kp = cantReposicion * 6000
        elif cantReposicion <= 300:
            kp = cantReposicion * 5800
        elif cantReposicion <= 500:
            kp = cantReposicion * 5300
        elif cantReposicion <= 700:
            kp = cantReposicion * 5000
        else:
            kp = cantReposicion * 4600

        registros = diaFin - diaInicio
        matrizCopia = [[0] * 15 for f in range(registros)]

        # logica
        banderaRecorrido = False
        for i in range(dias + 1):
            faltante = 0
            if i == 0:
                matriz[0][4] = stock
                banderaRecorrido = True
            elif (banderaRecorrido):
                # dias
                matriz[1][0] = matriz[0][0] + 1
                dia = matriz[1][0]

                # Demanda
                matriz[1][1] = soporte.generarDemanda()
                demanda = matriz[1][1]

                # Demora
                matriz[1][2] = soporte.generarDemora()
                demora = matriz[1][2]

                # Disponible
                stockAnterior = matriz[0][4]
                matriz[1][3] = stockAnterior

                diaLlegadaAnterior = matriz[0][7]
                if dia == diaLlegadaAnterior:
                    matriz[1][3] += cantReposicion

                disponible = matriz[1][3]

                # Stock
                if demanda >= disponible:
                    matriz[1][4] = 0
                    faltante = -(disponible - demanda)
                else:
                    matriz[1][4] = disponible - demanda

                stock = matriz[1][4]

                # Faltante
                matriz[1][5] = faltante

                # Orden
                estadoPedidoAnterior = matriz[0][6]

                if diaLlegadaAnterior == dia:
                    estadoPedido = "L"
                    matriz[1][2] = ""
                elif estadoPedidoAnterior == "P":
                    estadoPedido = "P"
                    matriz[1][2] = ""
                elif estadoPedidoAnterior == "S":
                    estadoPedido = "P"
                    matriz[1][2] = ""
                elif stock < limiteReposicion:
                    estadoPedido = "S"
                else:
                    estadoPedido = ""
                    matriz[1][2] = ""
                matriz[1][6] = estadoPedido

                # Llegada
                if estadoPedido == "S":
                    matriz[1][7] = demora + dia
                elif estadoPedido == "P":
                    matriz[1][7] = matriz[0][7]
                else:
                    matriz[1][7] = ""

                # Costo de Ko
                if estadoPedido == "S":
                    matriz[1][8] = ko + ki + kp
                else:
                    matriz[1][8] = 0

                # Costo de KM
                matriz[1][9] = stock * km

                # Costo de KS
                matriz[1][10] = faltante * ks

                # Costo de KC
                if disponible > capacidad_almacen:
                    matriz[1][11] = (disponible - capacidad_almacen) * kc
                else:
                    matriz[1][11] = 0

                # Total
                matriz[1][12] = matriz[1][8] + matriz[1][9] + matriz[1][10] + matriz[1][11]

                # Total AC
                matriz[1][13] = matriz[1][12] + matriz[0][13]

                # Promedio
                matriz[1][14] = round(matriz[1][13] / dia, 2)

                if diaFin > dia and dia >= diaInicio:
                    for k in range(15):
                        matrizCopia[cont][k] = matriz[1][k]
                    cont += 1

                banderaRecorrido = False
            else:
                # dias
                matriz[0][0] = matriz[1][0] + 1
                dia = matriz[0][0]

                # Demanda
                matriz[0][1] = soporte.generarDemanda()
                demanda = matriz[0][1]

                # Demora
                matriz[0][2] = soporte.generarDemora()
                demora = matriz[0][2]

                # Disponible
                stockAnterior = matriz[1][4]
                matriz[0][3] = stockAnterior

                diaLlegadaAnterior = matriz[1][7]
                if dia == diaLlegadaAnterior:
                    matriz[0][3] += cantReposicion

                disponible = matriz[0][3]

                # Stock
                if demanda >= disponible:
                    matriz[0][4] = 0
                    faltante = -(disponible - demanda)
                else:
                    matriz[0][4] = disponible - demanda

                stock = matriz[0][4]

                # Faltante
                matriz[0][5] = faltante

                # Orden
                estadoPedidoAnterior = matriz[1][6]

                if (diaLlegadaAnterior == dia):
                    estadoPedido = "L"
                    matriz[0][2] = ""
                elif estadoPedidoAnterior == "P":
                    estadoPedido = "P"
                    matriz[0][2] = ""
                elif estadoPedidoAnterior == "S":
                    estadoPedido = "P"
                    matriz[0][2] = ""
                elif stock < limiteReposicion:
                    estadoPedido = "S"
                else:
                    estadoPedido = ""
                    matriz[0][2] = ""
                matriz[0][6] = estadoPedido

                # Llegada
                if estadoPedido == "S":
                    matriz[0][7] = demora + dia
                elif estadoPedido == "P":
                    matriz[0][7] = matriz[1][7]
                else:
                    matriz[0][7] = ""

                # Costo de Ko
                if estadoPedido == "S":
                    matriz[0][8] = ko + ki + kp
                else:
                    matriz[0][8] = 0

                # Costo de KM
                matriz[0][9] = stock * km

                # Costo de KS
                matriz[0][10] = faltante * ks

                # Costo de KC
                if disponible > capacidad_almacen:
                    matriz[0][11] = (disponible - capacidad_almacen) * kc
                else:
                    matriz[0][11] = 0

                # Total
                matriz[0][12] = matriz[0][8] + matriz[0][9] + matriz[0][10] + matriz[0][11]

                # Total AC
                matriz[0][13] = matriz[0][12] + matriz[1][13]

                # Promedio
                matriz[0][14] = round(matriz[0][13] / dia, 2)

                if diaFin > dia and dia >= diaInicio:
                    for k in range(15):
                        matrizCopia[cont][k] = matriz[0][k]
                    cont += 1

                banderaRecorrido = True

        if banderaRecorrido:
            vectorResultado = matriz[0]
        else:
            vectorResultado = matriz[1]

        return render(self.request, self.template_name,
                      {"vectorResultado": vectorResultado, "RegistrosTotal": registros, "matrizResultado": matrizCopia,
                       "vectorEntrada": [dias, diaInicio, diaFin, limiteReposicion, cantReposicion, stocki]})

