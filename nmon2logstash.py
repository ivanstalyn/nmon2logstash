#!/usr/bin/python3
import glob, os, argparse
import posixpath
import progressbar as pgbar
import pandas as pd
from utilitarios import filtros, diccionario_cabeceras, convertir_fecha, imprimir_info,imprimir_datos_csv,get_nombre_aplicacion

def capturainfo(opcion, origen, directoriodestino):
  opciones = opcion.split(sep=",")

  for filename in glob.glob(origen):

    archivo = posixpath.split(filename)
    archivo_nombre_original = archivo[1]
    archivo = archivo[1].split('.')[0]
    print(f'Archivo: {archivo_nombre_original}')
    top_CSV = False
    uarg_CSV = False

    with open(os.path.join(os.getcwd(),filename),'r',encoding='utf8') as f:
      
      lineas = f.readlines()
      servidor_hostname = ''
      memoria_real = 0.0
      metricas = {}
      zzzz_id = ''
      zzzz_timestamp = ''
      key_previa = ''
      nro_lineas = len(lineas)

      widgets = [
            pgbar.Bar('█', f'Procesando archivo {archivo_nombre_original} ({nro_lineas} registros) : [', ']'), ' ', pgbar.Percentage(),
            ' (',
            pgbar.ETA(), 
            ') ']
        
      

      bar = pgbar.ProgressBar(maxval=nro_lineas, widgets=widgets)
      progres_bar=0
      bar.start()

      for linea in lineas:
        progres_bar = progres_bar + 1
        bar.update(progres_bar)

        linea_header = linea.split(sep=',')

        #obtener hostname
        if(servidor_hostname == '' and linea_header[0] == 'AAA' and linea_header[1] == 'host'):
          servidor_hostname = linea_header[2].lower().strip()
          continue
        
        #obtener memoria real
        if(memoria_real == 0 and linea_header[0] == 'BBBP'):
          b_memoria_real_regex = filtros['memoriareal'].match(linea)
          if(b_memoria_real_regex != None):
            memoria_real = float(b_memoria_real_regex.group(1).strip())
            continue
        
        #obtener ID, fecha y hora de la muestra
        if(linea_header[0] == 'ZZZZ'):
          zzzz_id = linea_header[1]
          zzzz_timestamp = f'{convertir_fecha(linea_header[3])}T{linea_header[2]}.000-05:00'
          continue

        opcion_aceptada = False
        tmp_opcion = linea_header[0]
        rgx = ''
        try:
          if(linea_header[0][:3] == 'CPU'):
            tmp_opcion = 'CPUS'
          
          if(linea_header[0] == 'CPU_ALL'):
            tmp_opcion = 'CPU_ALL'

          rgx = diccionario_cabeceras.get(tmp_opcion,"none")
          if(opciones[0]=="ALL"):
            if(rgx != "none"):
              opcion_aceptada = True
          else:
            if(rgx!="none"):
              opciones.index(tmp_opcion)
              opcion_aceptada = True

        except ValueError:
          opcion_aceptada = False
        
        if( opcion_aceptada ):
          if( zzzz_id == '' ):
            b_cabecera_regex = rgx[1].match(linea)
            if(b_cabecera_regex != None):
              if(b_cabecera_regex.group(1) == 'TOP'):
                #eliminio Time de la lista. Indice 2
                top_arr = b_cabecera_regex.group(0).split(',')
                top_arr[1], top_arr[2] = top_arr[2], top_arr[1]
                metricas[b_cabecera_regex.group(1)] = top_arr
                cabecera = f'timestamp,servidor,aplicacion,ZZZZ,PID,CPU pct,Usr pct,Sys pct,Threads,Size,ResText,ResData,CharIO,RAM pct,Paging,Command'
                imprimir_datos_csv(directoriodestino + "/" + archivo,'TOP',cabecera)
                top_CSV = True
              elif(b_cabecera_regex.group(1)=='UARG'):
                metricas[b_cabecera_regex.group(1)] = b_cabecera_regex.group(0).split(',')
                cabecera = f'ZZZZ,PID,PPID,Command,Threads,USER,GROUP,FullCommand'
                imprimir_datos_csv(directoriodestino + "/" + archivo,'UARG',cabecera)
                uarg_CSV = True
              else:
                metricas[b_cabecera_regex.group(1)] = b_cabecera_regex.group(0).split(',')
              continue
    
          b_datos_regex = rgx[2].match(linea)
          if(b_datos_regex != None):
            datos_arr = b_datos_regex.group(0).split(",")
            try:
              if(b_datos_regex.group(1)=='TOP'):
                datos_arr[1], datos_arr[2] = datos_arr[2], datos_arr[1]
                if(memoria_real>0.0):
                  res_text = float(datos_arr[8])
                  res_data = float(datos_arr[9])
                  datos_arr[11] = "{:.6f}".format(((res_text + res_data)/memoria_real)*100.0/4.0)

                datos = ",".join([*[zzzz_timestamp,servidor_hostname,get_nombre_aplicacion(datos_arr[13])],*datos_arr[1:14]])
                imprimir_datos_csv(directoriodestino + "/" + archivo,'TOP',datos)

              elif(b_datos_regex.group(1)=='UARG'):
                if(len(datos_arr) == 9 ):
                  datos = ",".join([*datos_arr[1:9]])
                  imprimir_datos_csv(directoriodestino + "/" + archivo,'UARG',datos)
                else:
                  datos = ",".join([*[datos_arr[1],datos_arr[2],'0','na','0','na','na','na na na na']])
                  imprimir_datos_csv(directoriodestino + "/" + archivo,'UARG',datos)

              else:
                imprimir_info(directoriodestino + "/" + archivo, zzzz_timestamp, servidor_hostname, rgx[0], metricas[b_datos_regex.group(1)], datos_arr )
              key_previa = b_datos_regex.group(1)
            except KeyError:
              metricas[b_datos_regex.group(1)] = metricas[key_previa]
              imprimir_info(directoriodestino + "/" + archivo, zzzz_timestamp, servidor_hostname, rgx[0], metricas[b_datos_regex.group(1)], datos_arr )
              key_previa = b_datos_regex.group(1)
      bar.finish()
      if(top_CSV and uarg_CSV):
        widgets = [
            pgbar.Bar('█', f'Extrayendo procesos TOP {archivo_nombre_original} : [', ']'), ' ', pgbar.Percentage(),
            ' (',
            pgbar.ETA(), 
            ') ']
        
        bar = pgbar.ProgressBar(maxval=5, widgets=widgets)
        bar.start()
        df_procesos_top = pd.read_csv(f'{directoriodestino}/{archivo}_TOP_.csv', sep=",")
        bar.update(1)
        df_procesos_uarg = pd.read_csv(f'{directoriodestino}/{archivo}_UARG_.csv', sep=",")
        df_procesos_uarg.drop(labels=['ZZZZ','Command','Threads'], axis = 1, inplace = True)
        bar.update(2)
        df_tabla_inner_trx = df_procesos_top.set_index('PID').join(df_procesos_uarg.set_index('PID'), rsuffix='_uarg', how='inner')
        df_tabla_inner_trx = df_tabla_inner_trx.reindex(columns = ['timestamp','ZZZZ','servidor','aplicacion','CPU pct','Usr pct','Sys pct','Threads','Size','ResText','ResData','CharIO','RAM pct','Paging','Command','PPID','USER','GROUP','FullCommand'])
        df_tabla_inner_trx.insert(3, 'seccion', 'PROCESO')
        bar.update(3)
        df_tabla_inner_trx.to_csv(f'{directoriodestino}/{archivo}_PROCESOS_.csv', index = True, encoding='utf-8')

        bar.update(4)
        os.remove(f'{directoriodestino}/{archivo}_TOP_.csv')
        os.remove(f'{directoriodestino}/{archivo}_UARG_.csv')

        bar.finish()
        print(f'Resumen de procesos encontrados en {archivo_nombre_original}:')
        print(f'Número de procesos TOP encontrados: {len(df_procesos_top)}')
        print(f'Número de procesos UARG encontrados: {len(df_procesos_uarg)}')
    print('---------------------------------------------------------')
              

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("archivo_nmon", 
                      help="Ruta al archivo nmon.")

  parser.add_argument("directorio_salida_reporte", 
                      help="Directorio de destino de los reportes.")
  
  parser.add_argument("-s", 
                      "--seccion", 
                      help="Sección del reporte que se requiere.",
                      default='ALL')

  args = parser.parse_args()
  capturainfo(args.seccion, args.archivo_nmon, args.directorio_salida_reporte)

if __name__ == "__main__":
    main()
    print(f'Proceso terminado!')