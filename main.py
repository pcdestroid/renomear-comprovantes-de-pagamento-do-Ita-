import json
import os
import PyPDF2
import keyboard
import time

#renomear comprovantes do banco itaú em uma determinada pasta

x = json.load(open('config.json', 'r'))
pasta = x.get('pasta')
nome = ''; cnpj = ''; valor = ''

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        textoPDF = PyPDF2.PdfFileReader(os.path.join(diretorio, arquivo)).getPage(0).extractText()
        print('Renomenando arquivo: ' + arquivo)
        
        #Banco Itaú - Comprovante de Pagamento TED C – outra titularidade
        if textoPDF.find("SISPAG FORNECEDORES TED") > 0:
            print('Tipo de comprovante: SISPAG FORNECEDORES TED')
            #Pegar nome
            if textoPDF.find("Nome do favorecido:") > 0:
                nome = textoPDF[textoPDF.find("Nome do favorecido:")+19:len(textoPDF)][0:textoPDF[textoPDF.find("Nome do favorecido:")+19:len(textoPDF)].find(" ")]
                print("Fornecedor: " + nome)
            #Pegar CNPJ
            if textoPDF.find("CPF/CNPJ:") > 0:
                cnpj = textoPDF[textoPDF.find("CPF/CNPJ:")+9:len(textoPDF)][0:textoPDF[textoPDF.find("CPF/CNPJ:")+9:len(textoPDF)].find("Número")]
            #Pegar valor
            if textoPDF.find("Valor da TED:") > 0:
                valor = textoPDF[textoPDF.find("Valor da TED:")+13:len(textoPDF)][0:textoPDF[textoPDF.find("Valor da TED:")+13:len(textoPDF)].find("Finalidade:")].replace("R$ ","")
            #Renomear o arquivo
            if os.path.exists(pasta+'/'+arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf") == False:
                old_file = os.path.join(pasta, arquivo)
                new_file = os.path.join(pasta, arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                print('Renomeado para: ' + arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                os.rename(old_file, new_file) 

        #Comprovante de pagamento de boleto
        if textoPDF.find("pagamento de boleto") > 0:
            print('Tipo de comprovante: Pagamento de boleto')
            #Pegar nome    
            if textoPDF.find("Beneficiário: ") > 0:
                nome = textoPDF[textoPDF.find("Beneficiário: ")+14:len(textoPDF)][0:textoPDF[textoPDF.find("Beneficiário: ")+14:len(textoPDF)].find(" ")].replace(" ","")
                print("Fornecedor: " + nome)
            #Pegar CNPJ
            if textoPDF.find("CPF/CNPJ:") > 0:
                cnpj = textoPDF[len(textoPDF[0:textoPDF.find("Valor do boleto") - 11]) - 19:textoPDF.find("Valor do boleto") - 11].replace("/","").replace("-","").replace(".","").replace(" ","")
            #Pegar valor
            if textoPDF.find("Valor do boleto (R$); ") > 0:
                valor = textoPDF[textoPDF.find("Valor do boleto (R$); ")+22:len(textoPDF)][0:textoPDF[textoPDF.find("Valor do boleto (R$); ")+22:len(textoPDF)].find(" ")].replace(" ","")
            #Renomear o arquivo
            if os.path.exists(pasta+'/'+arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf") == False:
                old_file = os.path.join(pasta, arquivo)
                new_file = os.path.join(pasta, arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                print('Renomeado para: ' + arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                os.rename(old_file, new_file)

        #Banco Itaú - Comprovante de Transferência
        if textoPDF.find("SISPAG TRANSF TITUL TED") > 0:
            print('Tipo de comprovante: SISPAG TRANSF TITUL TED')
            #Pegar nome
            nome = textoPDF[textoPDF.find("Transferência via TED C")+23:textoPDF.find("Transferência efetuada")]
            nome = nome[nome.find("-")+1:len(nome)]
            nome = nome[1:nome.find(" ")]
            print("Fornecedor: " + nome)
               
            #Pegar CNPJ
            cnpj = textoPDF[textoPDF.find("Transferência via TED C")+23:textoPDF.find("Transferência efetuada")]
            cnpj = cnpj[cnpj.find("-")+1:len(cnpj)]
            
            if cnpj.find("/") > 0:
                cnpj = cnpj[cnpj.find("/")-10:len(cnpj)]
                cnpj = cnpj[0:cnpj.find("-")+3]
                cnpj = cnpj[len(cnpj)-18:len(cnpj)].replace(" ","").replace("/","").replace(".","").replace("-","")
            if len(cnpj) > 14:
                cnpj = cnpj[cnpj.find("-")-11:len(cnpj)]
                cnpj = cnpj[0:cnpj.find("-")+3].replace(".","").replace("-","")

            #Pegar valor
            valor = textoPDF[textoPDF.find("Transferência via TED C")+23:textoPDF.find("Transferência efetuada")]
            valor = valor[valor.find("-")+1:len(valor)]
            valor = valor[valor.find("-")+1:len(valor)]
            valor = valor[valor.find("-")+1:len(valor)]
            valor = valor[valor.find("-")+2:len(valor)].replace(" ","")
            #Renomear o arquivo
            if os.path.exists(pasta+'/'+arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf") == False:
                old_file = os.path.join(pasta, arquivo)
                new_file = os.path.join(pasta, arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                print('Renomeado para: ' + arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                os.rename(old_file, new_file)

        #Banco Itaú - Comprovante de Transferência (BOLETO)
        if textoPDF.find("SISPAG FORNECEDORES") > 0:
            print('Tipo de comprovante: SISPAG FORNECEDORES')
            #Pegar nome
            nome= textoPDF[textoPDF.find("Autenticação:")+13:len(textoPDF)]
            nome= nome[nome.find("-")+2:len(nome)]
            nome= nome[0:nome.find(" ")]
            print("Fornecedor: " + nome)
            #Pegar CNPJ
            cnpj = '00000000000000' #Não tem CNPJ
            if textoPDF.find("CPF/CNPJ:") > 0:
                cnpj = textoPDF[textoPDF.find("Autenticação:"):textoPDF.find("Transferência efetuada em")]
                cnpj = cnpj[cnpj.find("/")+1:len(cnpj)]
                if cnpj.find("/")>0:
                    cnpj = cnpj[cnpj.find("/")-10:len(cnpj)]
                    cnpj = cnpj[0:cnpj.find("-")+3].replace(" ","").replace("/","").replace(".","").replace("-","")

            #Pegar valor
            valor= textoPDF[textoPDF.find("Autenticação:")+13:len(textoPDF)]
            valor= valor[valor.find("-")+2:len(valor)]
            valor = valor[0:valor.find("Transferência efetuada em")]
            valor = valor[valor.find("-")+2:len(valor)]
            if valor.find("-") >0:
                valor = valor[valor.find("-")+1:len(valor)] 
            if valor.find("/") >0:
                valor = valor[valor.find("/")+8:len(valor)]
            if valor.find("-") >0:
                valor = valor[valor.find("-")+2:len(valor)]
                print(valor)
            #Renomear o arquivo
            if os.path.exists(pasta+'/'+arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf") == False:
                old_file = os.path.join(pasta, arquivo)
                new_file = os.path.join(pasta, arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                print('Renomeado para: ' + arquivo[0:arquivo.find("-")+1]+cnpj+'-'+valor+".pdf")
                os.rename(old_file, new_file)
        print('...')
        time.sleep(1)
    print('Press ESC para sair...')
    keyboard.wait("esc")
