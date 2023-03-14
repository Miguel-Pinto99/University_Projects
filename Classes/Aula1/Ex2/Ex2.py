#!/usr/bin/python3

maxinum_number = 1000

def isPrime(value):

    print(' \nChecking if ' + str(value) + ' is prime:')

    for i in range(2,value):
        # Em Python não é preciso inicializar variavéis do ciclo for
        # Em Python, começasse a contar na posicao 0. logo o 1 é a posição 0, 2 corresponde a 1, 3 a 2 ...

        remainder = value % i
        print('Division by ' + str(i) + ' is '+ str(remainder))
        if remainder == 0 :
            print(str(value) + ' is not prime because division by ' + str(i) + ' has 0 remainder')
            return False

    return True

def main():
    print("Starting to compute prime numbers up to" + str(maxinum_number -1))
    # Em Python não é preciso inicializar variavéis
    # Range=Sequencia de numeros que começa em 0 e acaba em Maximum_number
    count=0
    for i in range(0,maxinum_number):
        if isPrime(i):
            print('Number '+str(i)+' is prime.')
            count = count+1
        else:
            print('Number '+str(i)+ ' is not prime')

    print('Há ' + str(count) + ' numeros primos entre 1 e ' + str(maxinum_number))


if __name__ == "__main__":
    main()

    #EXPLICAÇÂO
    #1- MANDO CORRER A FUNÇÂO MAIN() POR CAUSA DO IF.SEMPRE QUE O CODIGO É CHAMADO, COMO O NOME DA FUNÇÃO É IGUAL AO SEU
#PROPRIO NOME, ESTA INICIA
    #2-PARA i, DE 0 ATÉ AO NUMERO MAXIMO, VAMOS CORRER ESTA FUNÇÃO.COMEÇA NO 0,1,2,3,....
    #3-SE A FUNÇÃO ISPRIME() FOR VERDADEIRA, O IF CONFIRMA A SUA PERMISSA E IMPRIME QUE O NUMERO É PRIMO. CASO CONTRÁ-
#RIO, IMPRIME QUE NÃO É.
    #4-EXEMPLO PARA O NUMERO 5.__ISPRIME(5)__.A VARIAVEL VALUE É 5. ASSIM VAMOS CORRER UM CICLO FOR DE RANGE 2-5 ONDE I-
#REMOS DIVIDIR CADA NUMERO DO CICLO FOR POR 5. SE ALGUMA DIVISAO DER RESTO 0 QUER DIZER QUE O NUMERO NAO É PRIMO LOGO A
#FUNÇAO RETORNA O VALOR FALSE. CASO A DIVISAO POR 2/3/4/5, NENHUMA DER RESTO 0 , O NUMERO É PRIMO.