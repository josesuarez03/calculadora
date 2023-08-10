import sys
def presupuesto(servicio1, servicio2, grupo):
    print("Servicio\n1. Sin promo (1)\n2. Con Promo(2)\n3. Salir")
    try:
        opcion = int(input("introduce una opcion: "))
        if (opcion == 1):
            try:
                n_serv= int(input("introduce la cantidad de servicios a consumir: "))
                total = (servicio1 * n_serv) / grupo
                bs = float(input("introduce el precio del dolar: "))
                total_bs = total * bs
                print(f"Cada persona debe pagar {total} $ o {total_bs} bs")
            except:
                print('error')
                presupuesto(sin_promo,con_promo,person)
        elif (opcion==2) :
            try:
                n_serv= int(input("introduce la cantidad de servicios a consumir: "))
                total = (servicio2 * n_serv) / grupo
                bs = float(input("introduce el precio del dolar: "))
                total_bs = total * bs
                print(f"Cada persona debe pagar {total} $ o {total_bs} bs")
            except:
                print('error')
                presupuesto(sin_promo,con_promo,person)
        else:
            sys.exit("adios")
    except:
        print ("Error")
        presupuesto(sin_promo,con_promo,person)

con_promo = 20
sin_promo = 25

try:
    person = int(input("introducir la cantidad de personas: "))
except:
    print("error")
    presupuesto()
presupuesto(sin_promo, con_promo, person)


