#!/usr/bin/env python3

import urllib.request
import re
import sys

def usage():
    print('Modo de uso: {0} "ENCOMENDA[1]" "ENCOMENDA[2]" ... "ENCOMENDA[N]"'.format(sys.argv[0]))
    sys.exit(1)

def encomenda(lista):
    for codigo in lista:
        content = []
        address = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI='
        with urllib.request.urlopen(address + codigo) as url:
            for line in url.readlines():
                content.append(line.decode('iso-8859-1'))
                
        content = [ elem.rstrip() for elem in content if 'rowspan' in elem ]
        
        if len(content) == 0:
            print('Encomenda {0} não foi encontrada'.format(codigo))
        else:
            print('\n\nHistórico do objeto: {0}\n'.format(codigo))
            for data in content:
                [(dia, local, sit)] = re.findall('<tr><td rowspan.+>(.*)</td><td>(.*)</td><td><FONT.*>(.*)</font>.*', data)
                dia = " ".join(dia.split())
                local = " ".join(local.split())
                sit = " ".join(sit.split())
                
                print('Data: {0}'.format(dia))
                print('Local: {0}'.format(local))
                print('Situação: {0}'.format(sit))
                print()

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        usage()
    
    args = [ elem.upper() for elem in sys.argv[1:] if len(elem) == 13 ]

    if len(args) == 0:
        print('Código de encomenda inválido\nO código deve ter 13 dígitos')
        usage()
    else:
        encomenda(args)

if __name__ == '__main__':
    main()
