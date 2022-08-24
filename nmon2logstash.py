#!/usr/bin/python3
import glob, os, argparse
from posixpath import split
import progressbar as pgbar
import pandas as pd
from utilitarios import convertir_fecha, imprimir_info, filtros, get_nombre_aplicacion, lista_secciones, diccionario_cabeceras

def capturainfo(opcion, origen, directoriodestino):
  opciones = opcion.split(sep=",")
  for filename in glob.glob(origen):
    df_procesos_top = pd.DataFrame()
    df_procesos_uarg = pd.DataFrame()

    archivo = filename.split('/')
    archivo = archivo[len(archivo)-1].split('.')[0]
    print(f'Archivo: {archivo}')

    with open(os.path.join(os.getcwd(),filename),'r',encoding='utf8') as f:
      
      lineas = f.readlines()
      servidor_hostname = ''
      memoria_real = 0.0
      metricas = {}
      zzzz_id = ''
      zzzz_timestamp = ''
      key_previa = ''
      n = len(lineas)

      print(f'Total de líneas para analizar: {n}')

      bar = pgbar.ProgressBar(maxval=n, widgets=[pgbar.Bar('=', '[', ']'), ' ', pgbar.Percentage()])
      p=0
      bar.start()

      for linea in lineas:
        p = p + 1
        bar.update(p)

        linea_header = linea.split(sep=',')

        #obtener hostname
        if(servidor_hostname == '' and linea_header[0] == 'AAA' and linea_header[1] == 'host'):
          servidor_hostname = linea_header[1].lower()
          continue
        
        #obtener memroria real
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

        opcion_encontrada = False
        llave_cabecera = 'none'
        try:
          opciones.index(linea_header[0])
          opcion_encontrada = True
        except ValueError:
          opcion_encontrada = False
        
        if( opcion_encontrada or opcion == 'ALL'):
          rgx = diccionario_cabeceras.get(linea_header[0])
          if( zzzz_id == '' ):
            b_cabecera_regex = rgx[1].match(linea)
            if(b_cabecera_regex != None):
              if(b_cabecera_regex.group(1) == 'TOP'):
                #eliminio Time de la lista. Indice 2
                top_arr = b_cabecera_regex.group(0).split(',')
                top_arr[1], top_arr[2] = top_arr[2], top_arr[1]
                metricas[b_cabecera_regex.group(1)] = top_arr
              else:
                metricas[b_cabecera_regex.group(1)] = b_cabecera_regex.group(0).split(',')
              continue
    
          b_datos_regex = rgx[2].match(linea)
          if(b_datos_regex != None):
            datos_arr = b_datos_regex.group(0).split(",")
            try:
              if(b_datos_regex.group(1)=='TOP'):
                
                datos_arr[1], datos_arr[2] = datos_arr[2], int(datos_arr[1])
                if(memoria_real>0.0):
                  res_text = float(datos_arr[8])
                  res_data = float(datos_arr[9])
                  datos_arr[11] = "{:.6f}".format(((res_text + res_data)/memoria_real)*100.0/4.0)
                
                temp_df = pd.DataFrame([[*[zzzz_timestamp,servidor_hostname,get_nombre_aplicacion(datos_arr[13])],*datos_arr[1:14]]], columns=['timestamp','servidor','aplicacion','ZZZZ','PID','CPU pct','Usr pct','Sys pct','Threads','Size','ResText','ResData','CharIO','RAM pct','Paging','Command'])
                df_procesos_top = df_procesos_top.append(temp_df, ignore_index=True)

              elif(b_datos_regex.group(1)=='UARG'):
                temp_df = ''
                if(len(datos_arr) == 9 ):
                  temp_df = pd.DataFrame([[*datos_arr[1:9]]], columns=['ZZZZ_uarg','PID_uarg','PPID','Command_uarg','Threads_uarg','USER','GROUP','FullCommand'])
                else:
                  temp_df = pd.DataFrame([[*[datos_arr[1],datos_arr[2],0,'na',0,'na','na','na']]], columns=['ZZZZ_uarg','PID_uarg','PPID','Command_uarg','Threads_uarg','USER','GROUP','FullCommand'])
                df_procesos_uarg = df_procesos_uarg.append(temp_df, ignore_index=True)
              else:
                imprimir_info(directoriodestino + "/" + archivo, zzzz_timestamp, servidor_hostname, rgx[0], metricas[b_datos_regex.group(1)], datos_arr )
              key_previa = b_datos_regex.group(1)
            except KeyError:
              metricas[b_datos_regex.group(1)] = metricas[key_previa]
              imprimir_info(directoriodestino + "/" + archivo, zzzz_timestamp, servidor_hostname, rgx[0], metricas[b_datos_regex.group(1)], datos_arr )
              key_previa = b_datos_regex.group(1)
      bar.finish()
      #acá va el código para cruzar dataframes
      print(f'Numero de procesos TOP: {len(df_procesos_top)}')
      print(f'Numero de procesos UARG: {len(df_procesos_uarg)}')
      print(f'Cruzar tablas')
      df_tabla_inner_trx = df_procesos_top.set_index('PID').join(df_procesos_uarg.set_index('PID_uarg'), how='inner')
      print(f'Numero de registros cruzados left: {len(df_tabla_inner_trx)}')
      df_procesos_top.to_csv(directoriodestino + "/" +'top.csv', index = False, encoding='utf-8')
      df_procesos_uarg.to_csv(directoriodestino + "/" +'uarg.csv', index = False, encoding='utf-8')
      df_tabla_inner_trx.to_csv(directoriodestino + "/" +'top_uarg_inner.csv', index = False, encoding='utf-8')
      

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