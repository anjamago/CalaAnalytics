from .singleton import SingletonMeta
from app.utils.util import age
import yaml
import os
import pandas as pd


class LoadFiles(metaclass=SingletonMeta):
    def getYaml(self, filepath):
        with open(filepath, 'r') as file_descriptor:
            data = yaml.load(file_descriptor)
        return data

    def getData(self, config):
        blob = config.get('blob')
        files = config.get('filesnames')

        table = self.LoadFileExcel(blob, files, self.loadFileTxt(blob, files))

        dataFrame = pd.DataFrame({
            "Nombre": table['NOMBRE'],
            "Apellido": table['APELLIDO'],
            "Cedula": table['CEDULA'],
            "Nacimiento": table['NACIMIENTO'],
            "Nombre Completo": "",
            "Edad": table['NACIMIENTO'].apply(age),
            "Tipo de pedido": table['Tipo de pedido'],
            "Numero de pedido": table['numero de pedido'],
        })
        dataFrame = dataFrame.drop_duplicates(['Cedula', 'Tipo de pedido'])
        dataFrame['Nombre Completo'] = dataFrame[[
            'Nombre', 'Apellido']].apply(' '.join, axis=1)
        return dataFrame

    def LoadFileExcel(self, blob, files, bufferTxt):
        excel = blob + '/' + files[0]
        buffer = pd.read_excel(os.path.abspath(
            excel), 'Hoja1', engine='openpyxl')

        buffer = buffer.rename(columns={'cc_cliente': 'CEDULA'})
        return buffer[[
            'numero de pedido', 'Tipo de pedido', 'CEDULA']].merge(bufferTxt, on="CEDULA", how="left")

    def loadFileTxt(self, blob, files):
        txt = blob + '/' + files[1]
        return pd.read_table(os.path.abspath(txt), header=0)
