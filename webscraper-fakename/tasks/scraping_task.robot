*** Settings ***
Documentation     Coleta identidades do fakenamegenerator.com, salva em CSV e envia por email.
Library           ../libraries/ScraperLibrary.py
Library           DateTime


*** Variables ***
${QUANTIDADE}     10
${PASTA_SAIDA}    ${CURDIR}${/}..${/}output


*** Tasks ***
Coletar Identidades E Enviar Por Email
    [Documentation]    Task principal: coleta N identidades, gera o CSV e envia por email.
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${caminho_csv}=    Set Variable    ${PASTA_SAIDA}${/}identidades_${timestamp}.csv

    Coletar Identidades    ${QUANTIDADE}
    Salvar Identidades Em Csv    ${caminho_csv}
    Enviar Csv Por Email

    Log To Console    CSV gerado e enviado: ${caminho_csv}

Somente Coletar Sem Enviar Email
    [Documentation]    Só coleta e gera o CSV, sem enviar email. Útil para testar o scraping.
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${caminho_csv}=    Set Variable    ${PASTA_SAIDA}${/}identidades_${timestamp}.csv

    Coletar Identidades    ${QUANTIDADE}
    Salvar Identidades Em Csv    ${caminho_csv}

    Log To Console    CSV gerado (sem envio de email): ${caminho_csv}
