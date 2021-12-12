import json
import os
import PyPDF2

#renomear comprovantes do banco itaú em uma determinada pasta

x = json.load(open('config.json', 'r'))
pasta = x.get('pasta')
nome = ''; cnpj = ''; valor = ''

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        textoPDF = PyPDF2.PdfFileReader(os.path.join(diretorio, arquivo)).getPage(0).extractText()
        
        #Banco Itaú - Comprovante de Pagamento TED C – outra titularidade
        if textoPDF.find("SISPAG FORNECEDORES TED") > 0:
            #Pegar nome    
            if textoPDF.find("Nome do favorecido:") > 0:
                nome = textoPDF[textoPDF.find("Nome do favorecido:")+19:len(textoPDF)][0:textoPDF[textoPDF.find("Nome do favorecido:")+19:len(textoPDF)].find(" ")]
            #Pegar CNPJ
            if textoPDF.find("CPF/CNPJ:") > 0:
                cnpj = textoPDF[textoPDF.find("CPF/CNPJ:")+9:len(textoPDF)][0:textoPDF[textoPDF.find("CPF/CNPJ:")+9:len(textoPDF)].find("Número")]
            #Pegar valor
            if textoPDF.find("Valor da TED:") > 0:
                valor = textoPDF[textoPDF.find("Valor da TED:")+13:len(textoPDF)][0:textoPDF[textoPDF.find("Valor da TED:")+13:len(textoPDF)].find("Finalidade:")].replace("R$ ","")
            
        #Comprovante de pagamento de boleto
        if textoPDF.find("pagamento de boleto") > 0:
            #Pegar nome    
            if textoPDF.find("Beneficiário: ") > 0:
                nome = textoPDF[textoPDF.find("Beneficiário: ")+14:len(textoPDF)][0:textoPDF[textoPDF.find("Beneficiário: ")+14:len(textoPDF)].find(" ")].replace(" ","")
            #Pegar CNPJ
            if textoPDF.find("CPF/CNPJ:") > 0:
                cnpj = textoPDF[len(textoPDF[0:textoPDF.find("Valor do boleto") - 11]) - 19:textoPDF.find("Valor do boleto") - 11].replace("/","").replace("-","").replace(".","").replace(" ","")
            #Pegar valor
            if textoPDF.find("Valor do boleto (R$); ") > 0:
                valor = textoPDF[textoPDF.find("Valor do boleto (R$); ")+22:len(textoPDF)][0:textoPDF[textoPDF.find("Valor do boleto (R$); ")+22:len(textoPDF)].find(" ")].replace(" ","")
            
        if os.path.exists(pasta+'/'+nome+'-'+cnpj+'-'+valor+".pdf") == False:
            old_file = os.path.join(pasta, arquivo)
            new_file = os.path.join(pasta, nome+'-'+cnpj+'-'+valor+".pdf")
            os.rename(old_file, new_file)

        print("Comprovante de pagamento: ")
        print(nome)
        print(cnpj)
        print(valor)
            
            


           




