from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
import zipfile
import os
import time
import pandas as pd
import xlrd
from db import base_datos

#sistemas@emaransac.com
#Sm~18jn57



class scrap:
    def __init__(self):

        self.s = Service('F:\\YERSON\\chromedriver.exe')
        self.ruta_descarga = "D:\\"
        """
        self.s = Service("/home/yerson/Downloads/chromedriver_linux64/chromedriver")
        self.ruta_descarga = "/home/yerson/Downloads/"
        """

        self.db = base_datos()

        self.file_name = ""
        self.count = 0

        chromeOptions = Options()
        chromeOptions.add_experimental_option("prefs", {
            "download.default_directory": "D:\\",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(service=self.s,options=chromeOptions)

        #self.opciones = webdriver.Chrome(service=self.s,options=chromeOptions)
        #self.servicio = Service(self.s)
        #self.driver = webdriver.Chrome()
        self.action = ActionChains(self.driver)
    def reset_file_name(self):
        self.file_name = ""

    def getFileName(self):
        print("{ >> Get file name << }")
        for archivo in os.listdir(self.ruta_descarga):
            if archivo.endswith(".zip"):
                self.file_name = os.path.splitext(archivo)[0]
                print("filename get: ",self.file_name)
                return self.file_name


    def unsip(self):
        print("{ >> Unzip file << }")
        #print("este error: ",self.ruta_descarga+self.getFileName())
        print("Ruta descarga: ",self.ruta_descarga)
        print("Ruta nombre: ", self.getFileName())
        ruta = self.ruta_descarga + self.getFileName()+'.zip'
        with zipfile.ZipFile(str(ruta), 'r') as zip_ref:
            zip_ref.extractall(self.ruta_descarga)
        print("file unzip success!!!")

    def removFile(self):
        print("{ >> Remove file << }")
        os.remove(os.path.splitext(self.ruta_descarga+self.getFileName())[0]+'.zip')
        os.remove(self.ruta_descarga+self.file_name+'.xls')
        print("file removed")

    def file_df_remove(self):
        print("{ >>  file && Remove<< }")
        self.unsip()
        #ruta = self.ruta_descarga+self.getFileName()
        ruta = "D:\\" + self.getFileName()
        #ruta = ruta[:-4]
        file = ruta+'.xls'
        print("fil <|>: ",file)
        df = pd.read_excel(file)
        #++++++++++++++++++++++++******
        #  INSERTAR A LA BASE DE DATOS
        #******************************
        num_df = df.shape[0]
        print(df.columns)

        if self.count == 0:
            for index, i in df.iterrows():
                print("++++++++\n")
                f = df.loc[i,'Cód. Local']
                Ci = df.loc[i,'Descripción']
                Np = df.loc[i, 'Stock Unidades']
                Ec = df.loc[i,'Stock a Costo']
                Cb = df.loc[i, 'Días de Stock']
                St = df.loc[i, 'Mix']
                Ps = df.loc[i, 'Quiebres']
                U = df.loc[i, 'Sin Venta']
                b = df.loc[i, 'Stock Negativo']
                print(f,Ci, Np, Cb, St, Ps, U,b)
        elif self.count == 1:
            for index, i in df.iterrows():
                print("++++++++\n")
                f = df.loc[i, 'Cód. Local']
                Ci = df.loc[i, 'Descripción']
                Np = df.loc[i, 'Stock Unidades']
                Cb = df.loc[i, 'Stock a Costo']
                St = df.loc[i, 'Días de Stock']
                Ps = df.loc[i, 'Mix']
                U = df.loc[i, 'Quiebres']
                b = df.loc[i, 'Sin Venta']
                ty = df.loc(i,'Stock Negativo')
                print(f,Ci, Np, Cb, St, Ps, U, b,ty)
                #insertar(Ci, Np, Cb, St, Ps, Ub)
        elif self.count == 2:
            for index, i in df.iterrows():
                print("++++++++\n")
                f = df.loc[i, 'Cód. SPSA']
                Ci = df.loc[i, 'Cód. Proveedor']
                Np = df.loc[i, 'Descripción Producto']
                Cb = df.loc[i, 'Marca']
                St = df.loc[i, 'Estado']
                Ps = df.loc[i, 'Catalogado (Locales)']
                U = df.loc[i, '% Cobertura']
                print(f,Ci, Np, Cb, St, Ps, U)

        #self.db.detalle_inv()

        #print(df)
        self.removFile()
        self.count+=1


    def login(self):
        self.driver.get('https://b2b.intercorpretail.pe')

        dropdownbox = self.driver.find_elements(by=By.TAG_NAME, value='Option')
        i = 0;
        while i < len(dropdownbox):
            if dropdownbox[i].text == 'Supermercados Peruanos S.A.':
                dropdownbox[i].click()
                break
            i += 1
        Ingresar = self.driver.find_element(by=By.CLASS_NAME,value='btn.btn-primary.btn-sm')
        Ingresar.click()

        email = self.driver.find_element(by=By.NAME,value='username')
        email.send_keys("ventas@emaransac.com")
        time.sleep(1)
        contrasenia = self.driver.find_element(by=By.NAME,value='password')
        contrasenia.send_keys("VENTAS2023")
        login = self.driver.find_element(by=By.CLASS_NAME,value='pf-c-button.pf-m-primary.pf-m-block.btn-lg')
        login.click()
        time.sleep(3)
        print("[ >> Login << ]")


    def abastecimiento(self):
        time.sleep(3)
        triangle = self.driver.find_element(By.XPATH, value='//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[3]/div/span[3]')
        self.action.click(triangle).perform()
        time.sleep(1)
        print("[ >> 1. Init << ]")

        abast = self.driver.find_element(By.XPATH, value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/span[1]/span[2]')
        self.action.click(abast).perform()
        print("[ >> 2. Abastecimiento.. << ]")
        time.sleep(15)

        detalle = self.driver.find_element(By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/span[1]/span')
        #/html/body/div[2]/div[2]/div/div/span[1]/span
        #//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/span[1]/span
        #
        self.action.move_to_element(detalle)
        self.action.click(detalle).perform()
        time.sleep(3)
        print("[ >> 3. Detalle Inv << ]")

        generar = self.driver.find_element(by=By.CLASS_NAME,value='v-button.v-widget.btn-filter-search.v-button-btn-filter-search')
        generar.click()
        time.sleep(6)
        print("[ >> 4. Generar informe << ]")

        descargar = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/div')
        descargar.click()
        time.sleep(8)
        print("[ >> 5. Descargar <<]")

        exel = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div/div/span[2]/label')
        exel.click()
        time.sleep(6)
        print("[ >> 6. Formato << ]")

        archivo = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[3]/div/div/div[1]/div')
        archivo.click()
        time.sleep(6)
        print("[ >> 7. Archivo .xls << ]")

        zip = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/a/span')
        zip.click()
        print("[ >> 8. Descarga .zip << ]")
        time.sleep(12)

    def detalleinv(self):
        triangle = self.driver.find_element(By.XPATH, value='//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[3]/div/span[3]')
        self.action.click(triangle).perform()
        time.sleep(1)
        print("[ >> 1. Init << ]")

        abast = self.driver.find_element(By.XPATH, value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/span[1]/span[2]')
        self.action.click(abast).perform()
        time.sleep(7)
        print("[ >> 2. Abastecimiento.. << ]")

        local = self.driver.find_element(By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/span[2]/span')
        self.action.move_to_element(local)
        self.action.click(local).perform()
        time.sleep(3)
        print("[ >> 3. Detalle Inv << ]")

        generar = self.driver.find_element(by=By.CLASS_NAME,value='v-button.v-widget.btn-filter-search.v-button-btn-filter-search')
        generar.click()
        time.sleep(6)
        print("[ >> 4. Generar informe << ]")


        Descarga = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div[3]/div/div[1]/div')
        Descarga.click()
        time.sleep(6)
        print("[ >> 5. Descargar << ]")


        exel = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/div[1]/div')
        exel.click()
        time.sleep(2)
        print("[ >> 6. Formato << ]")


        Exel  = self.driver.find_element(by=By.XPATH,value= '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div/div/span[2]/label')
        Exel.click()
        print("[ >> 7. Archivo .xls << ]")
        time.sleep(2)


        Seleccionar = self.driver.find_element(by=By.XPATH,value= '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[3]/div/div/div[1]/div')
        Seleccionar.click()
        time.sleep(5)
        print("[ >> 8. Seleccionar << ]")


                                                         #'//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]'
        #'v-slot v-align-center v-align-middle'
        zip = self.driver.find_element(by=By.XPATH,value= '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]')
        zip.click()
        print("[ >> 9. Descarga .zip.. << ]")
        time.sleep(2)

    def informeCv(self):
        time.sleep(1)
        triangle = self.driver.find_element(By.XPATH, value='//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[3]/div/span[3]')
        self.action.click(triangle).perform()
        time.sleep(4)
        print("[ >> 1. Init << ]")

        abast = self.driver.find_element(By.XPATH, value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/span[1]/span[2]')
        self.action.click(abast).perform()
        time.sleep(6)
        print("[ >> 2. Abastecimiento << ]")



        detalle = self.driver.find_element(By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/span[3]/span')
        self.action.move_to_element(detalle)
        self.action.click(detalle).perform()
        time.sleep(3)
        print("[ >> 3. Detalle Inv << ]")


        generar = self.driver.find_element(by=By.CLASS_NAME,value='v-button.v-widget.btn-filter-search.v-button-btn-filter-search')
        generar.click()
        time.sleep(8)
        print("[ >> 4. Generar informe << ]")


        Descarga = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div[3]/div/div[1]/div')
        Descarga.click()
        time.sleep(5)
        print("[ >> 5. Descargar << ]")


        exel = self.driver.find_element(by=By.XPATH,value='//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/div[1]/div')
        exel.click()
        time.sleep(5)
        print("[ >> 6. Formato << ]")


        Exel  = self.driver.find_element(by=By.XPATH,value= '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div/div/span[2]/label')
        Exel.click()
        time.sleep(5)
        print("[ >> 7. Archivo .xls << ]")


        Seleccionar = self.driver.find_element(by=By.XPATH,value= '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[3]/div/div/div[1]/div')
        Seleccionar.click()
        time.sleep(12)
        print("[ >> 8. Seleccionar << ]")


        zip = self.driver.find_element(by=By.XPATH,value= '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]')
        zip.click()
        print("[ >> 9. Descarga .zip << ]")

        time.sleep(3)

    def init(self):
        self.login()

        print("[ >> 1.Abastecimiento << ]")
        self.abastecimiento()
        self.file_df_remove()
        time.sleep(5)
        self.reset_file_name()


        print("[ >> 2.Detalle Inv << ]")
        self.detalleinv()
        self.file_df_remove()
        time.sleep(5)
        self.reset_file_name()


        print("[ >> 3. Informe cobertura << ]")
        self.informeCv()
        self.file_df_remove()
        self.reset_file_name()
        print("[ >> fin << ]")


if __name__ == '__main__':
    sc = scrap()
    #sc.file_df_remove()
    sc.init()
    #sc.file_df_remove()
    sc.driver.quit()

"""
sales
invoice_type_id
    tipo 3 --> note_cretito

2 tablas de notas de cretido


sales2

sales2_details
"""