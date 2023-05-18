import mysql.connector
from datetime import datetime
import time

cnx = mysql.connector.connect(
  host="209.45.83.59",
  user="sistemas",
  password="qbJITBTz29o8Svf",
  database="supermercados_sa"
)
cursor = cnx.cursor()


class base_datos:
    def __int__(self):
        self.tablas = ['detalle_inventario','indicadores_inv_local','informecobertura_mix']

    def detalle_inv(self,cod_spsa,cod_proveeedor,descripcion,um,marcas,total,locales,cd,mix,q):
        sql = "INSERT INTO `detalle_inventario`(`cod_spsa`, `cod_proveeedor`, `descripcion`, `um`, `marcas`, `total`, `locales`, `cd`, `mix`, `q`, `fecha`)" \
              " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        fecha_actual = datetime.now()
        fecha_texto = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')

        val = (cod_spsa,cod_proveeedor,descripcion,um,marcas,total,locales,cd,mix,q,fecha_texto)
        cursor.execute(sql, val)
        cnx.commit()

    def indicadores_inv(self, cod_local,descripcion,stock_unidades,stock_costo,dias_stock,mix,quiebres,sin_venta,stock_negativo):
        sql = "INSERT INTO `indicadores_inv_local`(`cod_local`, `descripcion`, `stock_unidades`, `stock_costo`, `dias_stock`, `mix`, `quiebres`, `sin_venta`, `stock_negativo`, `fecha`) VALUES (" \
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        fecha_actual = datetime.now()
        fecha_texto = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')

        val = (cod_local,descripcion,stock_unidades,stock_costo,dias_stock,mix,quiebres,sin_venta,stock_negativo,fecha_texto)
        cursor.execute(sql, val)
        cnx.commit()

    def informe_cob(self,cod_spsa,cod_proveeedor,descripcion_producto,marca,estado,catalogo_locales,cobertura):
        sql = "INSERT INTO `informe_cobertura_mix`(`cod_spsa`, `cod_proveeedor`, `descripcion_producto`, `marca`, `estado`, `catalogo_locales`, `cobertura`, `fecha`) VALUES (" \
                  "%s,%s,%s,%s,%s,%s,%s,%s)"
        # sq = (20325756,0,'BATAN-CULANTRO-FRESCO-X3SBS','UN','BATAN',11.740,11.560,180.00,759,21,'2023-05-03 15:30:00')
        # fecha = datetime.now()
        fecha_actual = datetime.now()
        fecha_texto = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')

        val = (cod_spsa,cod_proveeedor,descripcion_producto,marca,estado,catalogo_locales,cobertura,fecha_texto)
        cursor.execute(sql, val)
        cnx.commit()

if __name__ == "__main__":
    db = base_datos()
    #db.detalle_inv(00000000,0,'BATAN-CULANTRO-FRESCO-X3SBS','UN','BATAN',11.740,11.560,180.00,759,21)
    #db.indicadores_inv(922,"SPSA-CD-MASS-SUR",290.00,450.00,0.00,3,0,0,0)
    #db.informe_cob(20325755,"","BATAN-AJI-PANCA-FRESCO-X3SBS","BATAN","ACTIVO",758,68.10)




"""
for i in range(num_df):
    print("++++++++\n")
    Ci = data.loc[i, 'Codigo interno']
    Np = data.loc[i, 'Nombre del producto']
    Cb = data.loc[i, 'Código de barras']
    St = data.loc[i, 'Stock  (Wilkins80)']
    Ps = data.loc[i, 'Presentación']
    Ub = data.loc[i, 'Ubicación predeterminada']
    print(Ci, Np, Cb, St, Ps, Ub)
    insertar(Ci, Np, Cb, St, Ps, Ub)
"""