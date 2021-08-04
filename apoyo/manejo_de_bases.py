import gspread as gs
import pandas as pd
import string
import datetime as dt

class Base_de_datos():
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, key, pestanna):
        """Constructor"""
        
        self.key = key
        self.pestanna = pestanna
        self.gc = gs.service_account(filename='accesos.json')
        self.sh = self.gc.open_by_key(self.key)
        self.worksheet = self.sh.worksheet(self.pestanna)
        self.hoy = dt.datetime.now()

    #----------------------------------------------------------------------
    def generar_dataframe(self):
        """[...]"""

        self.dataframe = pd.DataFrame(self.worksheet.get_all_records())
        return self.dataframe

    #----------------------------------------------------------------------
    def imprimir_dataframe(self):
        """[...]"""

        self.tabla = self.generar_dataframe()
        print(self.tabla)

    #----------------------------------------------------------------------
    def identificar_fila_por_variable(self, variable):
        """[...]"""

        self.variable = variable
        self.cell = self.worksheet.find(self.variable)
        return self.cell.row
    
    #----------------------------------------------------------------------
    def listar_datos_de_fila(self, variable):
        """[...]"""

        self.variable = variable
        self.fila = self.identificar_fila_por_variable(self.variable)
        self.values_list = self.worksheet.row_values(self.fila)
        return self.values_list

    #----------------------------------------------------------------------
    def cambiar_un_dato_de_una_fila(self, variable, posicion_de_dato, nuevo_valor_de_dato):
        """[...]"""
        
        self.variable = variable
        self.posicion_de_dato = posicion_de_dato
        self.nuevo_valor_de_dato = nuevo_valor_de_dato
        self.fila = self.identificar_fila_por_variable(self.variable)
        self.worksheet.update_cell(self.fila, self.posicion_de_dato, self.nuevo_valor_de_dato)

    #----------------------------------------------------------------------
    def cambiar_los_datos_de_una_fila(self, variable, lista_de_nuevos_valores):
        """[...]"""

        self.variable = variable
        self.lista_de_nuevos_valores = lista_de_nuevos_valores

        self.fila_identificada = self.identificar_fila_por_variable(self.variable)
        self.values_list = self.worksheet.row_values(self.fila_identificada)

        listAlphabet = list(string.ascii_uppercase)
        newlist = []
        for i in listAlphabet:
            first_letter = i
            for i in listAlphabet:
                combinacion = first_letter + i
                newlist.append(combinacion)
        newlistAlphabet = listAlphabet + newlist
        newlistNumbers = list(range(1,len(newlistAlphabet)+1))
        equivalencias = pd.DataFrame(list(zip(newlistNumbers, newlistAlphabet)), columns= ['Número', 'Letra'])

        self.celda_inicial = 'A' + str(self.fila_identificada)
        self.criterio_para_buscar = equivalencias['Número'] == len(self.values_list)+1
        self.equivalencia_encontrada = equivalencias[self.criterio_para_buscar]
        self.lista_de_valores_en_letra = self.equivalencia_encontrada['Letra'].tolist()
        self.valor_en_letra = self.lista_de_valores_en_letra[0]
        self.celda_final = self.valor_en_letra + str(self.fila_identificada)
        self.rango_a_cambiar = self.celda_inicial + ':' + self.celda_final
        self.worksheet.update(self.rango_a_cambiar, [self.lista_de_nuevos_valores])

    #----------------------------------------------------------------------
    def agregar_datos(self, lista_de_datos):
        """[...]"""

        self.lista_de_datos_sencilla = lista_de_datos
        self.worksheet.append_row(self.lista_de_datos_sencilla)
    
    #----------------------------------------------------------------------
    def agregar_datos_generando_codigo(self, lista_de_datos):
        """[...]"""

        self.lista_de_datos = lista_de_datos
        tabla = self.generar_dataframe()
        if tabla.empty == True:
            numero = 1
        elif dt.datetime.strptime(tabla['fecha_hora_creacion'].tolist()[-1], "%Y-%m-%d %H:%M:%S.%f").year != self.hoy.year:
            numero = 1
        else:
            last = tabla['numero'].tolist()[-1]
            numero = last + 1
        self.codigo = self.pestanna + "-" + str(self.hoy.year) + "-" + str(numero)
        self.datos_obligatorios = [self.codigo, str(self.hoy), numero]
        self.lista_de_datos_completos = self.datos_obligatorios + self.lista_de_datos
        self.worksheet.append_row(self.lista_de_datos_completos)
