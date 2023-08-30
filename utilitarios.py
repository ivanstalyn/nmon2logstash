import re
#Funciones
mes = {'JAN':'01','FEB':'02','MAR':'03','APR':'04','MAY':'05','JUN':'06','JUL':'07','AUG':'08','SEP':'09','OCT':'10','NOV':'11','DEC':'12'};

#Filtros
filtros = {
  'zzzz' : re.compile(r"ZZZZ,(T.*),(.*),(.*)"),
  'fecha' : re.compile(r"(.*)-(.*)-(.*)"),
  'hostname' : re.compile(r"AAA,host,(\w+)"),
  'memoriareal': re.compile(r"BBBP,\d+,vmstat -v,\"\s+(\d+) memory pages\""),
  'CPUNCabecera' : re.compile(r"(CPU\d+),(CPU .*?),(.*)"),
  'CPUNDatos' : re.compile(r"(CPU\d+),(T\d+),(.*)"),
  'CPUALLCabecera' : re.compile(r"(CPU_ALL),(CPU .*?),(.*)"),
  'CPUALLDatos' : re.compile(r"(CPU_ALL),(T\d+),(.*)"),
  'LPARCabecera' : re.compile(r"(LPAR),(Logica.*?),(.*)"),
  'LPARDatos' : re.compile(r"(LPAR),(T\d+),(.*)"),
  'POOLSCabecera' : re.compile(r"(POOLS),(Multiple.*?),(.*)"),
  'POOLSDatos' : re.compile(r"(POOLS),(T\d+),(.*)"),
  'DISKBUSYCabecera' : re.compile(r"(DISKBUSY),(Disk.+?),(.*)"),
  'DISKBUSYDatos' : re.compile(r"(DISKBUSY),(T\d+),(.*)"),
  'DISKREADCabecera' : re.compile(r"(DISKREAD),(Disk.+?),(.*)"),
  'DISKREADDatos' : re.compile(r"(DISKREAD),(T\d+),(.*)"),
  'DISKWRITECabecera' : re.compile(r"(DISKWRITE),(Disk.+?),(.*)"),
  'DISKWRITEDatos' : re.compile(r"(DISKWRITE),(T\d+),(.*)"),
  'DISKXFERCabecera' : re.compile(r"(DISKXFER),(Disk.+?),(.*)"),
  'DISKXFERDatos' : re.compile(r"(DISKXFER),(T\d+),(.*)"),
  'DISKRXFERCabecera' : re.compile(r"(DISKRXFER),(Transfers.+?),(.*)"),
  'DISKRXFERDatos' : re.compile(r"(DISKRXFER),(T\d+),(.*)"),
  'DISKBSIZECabecera' : re.compile(r"(DISKBSIZE),(Disk.+?),(.*)"),
  'DISKBSIZEDatos' : re.compile(r"(DISKBSIZE),(T\d+),(.*)"),
  'DISKRIOCabecera' : re.compile(r"(DISKRIO),(Disk.+?),(.*)"),
  'DISKRIODatos' : re.compile(r"(DISKRIO),(T\d+),(.*)"),
  'DISKWIOCabecera' : re.compile(r"(DISKWIO),(Disk.+?),(.*)"),
  'DISKWIODatos' : re.compile(r"(DISKWIO),(T\d+),(.*)"),
  'DISKAVGRIOCabecera' : re.compile(r"(DISKAVGRIO),(Average.+?),(.*)"),
  'DISKAVGRIODatos' : re.compile(r"(DISKAVGRIO),(T\d+),(.*)"),
  'DISKAVGWIOCabecera' : re.compile(r"(DISKAVGWIO),(Average.+?),(.*)"),
  'DISKAVGWIODatos' : re.compile(r"(DISKAVGWIO),(T\d+),(.*)"),
  'DISKSERVCabecera' : re.compile(r"(DISKSERV),(Disk.+?),(.*)"),
  'DISKSERVDatos' : re.compile(r"(DISKSERV),(T\d+),(.*)"),
  'DISKREADSERVCabecera' : re.compile(r"(DISKREADSERV),(Disk.+?),(.*)"),
  'DISKREADSERVDatos' : re.compile(r"(DISKREADSERV),(T\d+),(.*)"),
  'DISKWRITESERVCabecera' : re.compile(r"(DISKWRITESERV),(Disk.+?),(.*)"),
  'DISKWRITESERVDatos' : re.compile(r"(DISKWRITESERV),(T\d+),(.*)"),
  'DISKWAITCabecera' : re.compile(r"(DISKWAIT),(Disk.+?),(.*)"),
  'DISKWAITDatos' : re.compile(r"(DISKWAIT),(T\d+),(.*)"),
  'MEMCabecera' : re.compile(r"(MEM),(Memory.*?),(.*)"),
  'MEMDatos' : re.compile(r"(MEM),(T\d+),(.*)"),
  'MEMNEWCabecera' : re.compile(r"(MEMNEW),(Memory.*?),(.*)"),
  'MEMNEWDatos' : re.compile(r"(MEMNEW),(T\d+),(.*)"),
  'MEMUSECabecera' : re.compile(r"(MEMUSE),(Memory.*?),(.*)"),
  'MEMUSEDatos' : re.compile(r"(MEMUSE),(T\d+),(.*)"),
  'MEMPAGES4KBCabecera' : re.compile(r"(MEMPAGES4KB),(MemoryPages.*?),(.*)"),
  'MEMPAGES4KBDatos' : re.compile(r"(MEMPAGES4KB),(T\d+),(.*)"),
  'MEMPAGES64KBCabecera' : re.compile(r"(MEMPAGES64KB),(MemoryPages.*?),(.*)"),
  'MEMPAGES64KBDatos' : re.compile(r"(MEMPAGES64KB),(T\d+),(.*)"),
  'PAGECabecera' : re.compile(r"(PAGE),(Paging.*?),(.*)"),
  'PAGEDatos' : re.compile(r"(PAGE),(T\d+),(.*)"),
  'PAGINGCabecera' : re.compile(r"(PAGING),(PagingSpace.*?),(.*)"),
  'PAGINGDatos' : re.compile(r"(PAGING),(T\d+),(.*)"),
  'PROCCabecera' : re.compile(r"(PROC),(Processes.*?),(.*)"),
  'PROCDatos' : re.compile(r"(PROC),(T\d+),(.*)"),
  'FILECabecera' : re.compile(r"(FILE),(File.*?),(.*)"),
  'FILEDatos' : re.compile(r"(FILE),(T\d+),(.*)"),
  'NETCabecera' : re.compile(r"(NET),(Network.*?),(.*)"),
  'NETDatos' : re.compile(r"(NET),(T\d+),(.*)"),
  'NETPACKETCabecera' : re.compile(r"(NETPACKET),(Network.*?),(.*)"),
  'NETPACKETDatos' : re.compile(r"(NETPACKET),(T\d+),(.*)"),
  'NETSIZECabecera' : re.compile(r"(NETSIZE),(Network.*?),(.*)"),
  'NETSIZEatos' : re.compile(r"(NETSIZE),(T\d+),(.*)"),
  'NETERRORCabecera' : re.compile(r"(NETERROR),(Network.*?),(.*)"),
  'NETERRORDatos' : re.compile(r"(NETERROR),(T\d+),(.*)"),
  'TOPCabecera' : re.compile(r"(TOP),(\+PID.*)"),
  'TOPDatos' : re.compile(r"(TOP),(\d+),(T\d+),(.*)"),
  'UARGCabecera' : re.compile(r"(UARG),(\+Time),(.*)"),
  'UARGDatos' : re.compile(r"(UARG),(T\d+),(.*)"),
  'SUMMARYCabecera' : re.compile(r"(SUMMARY),(Summary of Processes),(.*)"),
  'SUMMARYDatos' : re.compile(r"(SUMMARY),(T\d+),(.*)"),
}

diccionario_cabeceras = {
  'CPUS' : ['CPU',  filtros['CPUNCabecera'], filtros['CPUNDatos']],
  'CPU_ALL' : ['CPUALL',  filtros['CPUALLCabecera'], filtros['CPUALLDatos']],
  'LPAR' : ['LPAR',  filtros['LPARCabecera'], filtros['LPARDatos']],
  'POOLS' : ['POOLS',  filtros['POOLSCabecera'], filtros['POOLSDatos']],
  'MEM' : ['MEMORIA',  filtros['MEMCabecera'], filtros['MEMDatos']],
  'MEMNEW' : ['MEMORIA',  filtros['MEMNEWCabecera'], filtros['MEMNEWDatos']],
  'MEMUSE' : ['MEMORIA',  filtros['MEMUSECabecera'], filtros['MEMUSEDatos']],
  'MEMPAGES4KB' : ['MEMORIA',  filtros['MEMPAGES4KBCabecera'], filtros['MEMPAGES4KBDatos']],
  'MEMPAGES64KB' : ['MEMORIA',  filtros['MEMPAGES64KBCabecera'], filtros['MEMPAGES64KBDatos']],
  'DISKBUSY' : ['DISCO',  filtros['DISKBUSYCabecera'], filtros['DISKBUSYDatos']],
  'DISKREAD' : ['DISCO',  filtros['DISKREADCabecera'], filtros['DISKREADDatos']],
  'DISKWRITE' : ['DISCO',  filtros['DISKWRITECabecera'], filtros['DISKWRITEDatos']],
  'DISKXFER' : ['DISCO',  filtros['DISKXFERCabecera'], filtros['DISKXFERDatos']],
  'DISKRXFER' : ['DISCO',  filtros['DISKRXFERCabecera'], filtros['DISKRXFERDatos']],
  'DISKBSIZE' : ['DISCO',  filtros['DISKBSIZECabecera'], filtros['DISKBSIZEDatos']],
  'DISKRIO' : ['DISCO',  filtros['DISKRIOCabecera'], filtros['DISKRIODatos']],
  'DISKWIO' : ['DISCO',  filtros['DISKWIOCabecera'], filtros['DISKWIODatos']],
  'DISKAVGRIO' : ['DISCO',  filtros['DISKAVGRIOCabecera'], filtros['DISKAVGRIODatos']],
  'DISKAVGWIO' : ['DISCO',  filtros['DISKAVGWIOCabecera'], filtros['DISKAVGWIODatos']],
  'DISKSERV' : ['DISCO',  filtros['DISKSERVCabecera'], filtros['DISKSERVDatos']],
  'DISKREADSERV' : ['DISCO',  filtros['DISKREADSERVCabecera'], filtros['DISKREADSERVDatos']],
  'DISKWRITESERV' : ['DISCO',  filtros['DISKWRITESERVCabecera'], filtros['DISKWRITESERVDatos']],
  'DISKWAIT' : ['DISCO',  filtros['DISKWAITCabecera'], filtros['DISKWAITDatos']],
  'PAGE' : ['PAGINACION',  filtros['PAGECabecera'], filtros['PAGEDatos']],
  'PAGING' : ['PAGINACION',  filtros['PAGINGCabecera'], filtros['PAGINGDatos']],
  'PROC' : ['PAGINACION',  filtros['PROCCabecera'], filtros['PROCDatos']],
  'FILES' : ['FILES',  filtros['FILECabecera'], filtros['FILEDatos']],
  'NETWORK' : ['NETWORK',  filtros['NETCabecera'], filtros['NETDatos']],
  'NETPACKET' : ['NETWORK',  filtros['NETPACKETCabecera'], filtros['NETPACKETDatos']],
  'NETSIZE' : ['NETWORK',  filtros['NETSIZECabecera'], filtros['NETSIZEatos']],
  'NETERROR' : ['NETWORK',  filtros['NETERRORCabecera'], filtros['NETERRORDatos'] ],
  'UARG' : ['PROCESOS',  filtros['UARGCabecera'], filtros['UARGDatos'] ],
  'TOP' : ['PROCESOS',  filtros['TOPCabecera'], filtros['TOPDatos'] ],
  'SUMMARY' : ['SUMMARY',  filtros['SUMMARYCabecera'], filtros['SUMMARYDatos'] ],
}

def convertir_fecha(_fecha):
  str_fecha = ''
  b_fecha_regex = filtros['fecha'].search(_fecha)
  if(b_fecha_regex != None):
     y = b_fecha_regex.group(3)
     m = mes[b_fecha_regex.group(2)]
     d = b_fecha_regex.group(1)
     str_fecha = y+"-"+m+"-"+d
  return str_fecha

def imprimir_info(archivo_reporte, zzzztimestamp, servidorhostname, seccion, listametricas, listavalores ):
  
  metricaid = listametricas[0];
  zzzzid = listavalores[1];
  n_metricas = len(listametricas)
  n_valores = len(listavalores)

  for index, metricasubtipo in enumerate(listametricas):
     try:
       if (index > 1 ):
         f = open(archivo_reporte + "_"+seccion + "_.csv", "a")
         if (seccion == 'DISCO'):
           f.write(f'{zzzztimestamp},{zzzzid},{servidorhostname},{seccion},{metricasubtipo.strip()},{metricaid.strip()},{listavalores[index]}\n')
         else:
           tmp_metricasubtipo = metricasubtipo.replace("%"," pct ").strip()
           tmp_metricasubtipo = tmp_metricasubtipo.replace("+","").strip()
           
           #Esto coloca pct al final de cualquier nombre de métrica
           if(tmp_metricasubtipo.find("pct ")>=0):            
            tmp_metricasubtipo = tmp_metricasubtipo.replace("pct ","").strip()
            tmp_metricasubtipo = f'{tmp_metricasubtipo} pct'

           f.write(f'{zzzztimestamp},{zzzzid},{servidorhostname},{seccion},{metricaid.strip()},{tmp_metricasubtipo},{listavalores[index]}\n')

         f.close()
     except IndexError:
       print(f'{zzzztimestamp},{zzzzid},{servidorhostname},{seccion}')
       print(f'Lista métricas: {n_metricas} --> {listametricas}')
       print(f'Lista valores: {n_valores} --> {listavalores}')
       exit(1)

def imprimir_info_fast(archivo_reporte, zzzzid, zzzztimestamp, servidorhostname, seccion, metrica, metricasubtipo, valor ):
  f = open(archivo_reporte + "_"+seccion + "_.csv", "a")
  f.write(f'{zzzztimestamp},{zzzzid},{servidorhostname},{seccion},{metrica.strip()},{metricasubtipo.strip()},{valor}\n')
  f.close()

def imprimir_datos_csv(archivo_reporte, seccion, datos):
  f = open(archivo_reporte + "_"+seccion + "_.csv", "a")
  f.write(f'{datos}\n')
  f.close()

def get_nombre_aplicacion(proceso,fullcommand):
  aplicacion = proceso
  if(proceso == 'DataFlowEngine'):
    aplicacion = 'IBM Integration BUS DataFlowEngine'
  
  if(proceso == 'bipbroker'):
    aplicacion = 'IBM Integration BUS bipbroker'
                  
  if(proceso == 'amqzlaa0' ):
    aplicacion = 'IBM Websphere MQ'

  if(proceso == 'kmqdc' ):
    aplicacion = 'APM WebSphere MQ Monitoring'
  
  if(proceso == 'kqiagent' ):
    aplicacion = 'Tivoli Monitoring'

  if(proceso == 'fcp_daemon'):
    aplicacion = 'Tivoli Monitoring'

  if(proceso == 'java'):
    b_datos_regex = re.compile(r'(.*)-Dosgi\.install\.area=\/usr\/IBM\/WebSphere\/AppServer(.*)').match(fullcommand)
    if(b_datos_regex != None):
      aplicacion = 'WebSphere'


  return aplicacion

def get_propiedades_aplicacion(aplicacion, fullcommand):
  parametros = 'na'
  if(aplicacion == 'IBM Integration BUS DataFlowEngine'):
    parametros = fullcommand

  if(aplicacion == 'WebSphere'):
    b_datos_regex = re.compile(r'(.*)-Dosgi\.configuration\.area=\/profiles\/(.*)\/servers\/(.*)\/configuration(.*)').match(fullcommand)
    if(b_datos_regex != None):
      parametros = f'{b_datos_regex.group(2)} {b_datos_regex.group(3)}'

  return parametros