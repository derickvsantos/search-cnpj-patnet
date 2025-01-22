"""
Biblioteca responsável por seletores de formulario de navegação e erros.
"""
############  LISTA DE ERROS ###################
CONSULTA_CNPJ = ["Forneça um número de CNPJ/CEI ou CNO para consulta!", 
                 "Inscrição não encontrada ou Inativa!"]

LOGIN = ["CPF inválido!", "Dados inválidos!"]

############  FORMULARIOS DE REQUISICAO ###################
PAYLOAD_LOGIN = {
            "ctl00$ScriptManager1": "ctl00$PlaceHolderConteudo$UpdatePanel1|ctl00$PlaceHolderConteudo$btnLogin",
            "ctl00$PlaceHolderConteudo$btnLogin": "Acessar"
            }

PAYLOAD_REMISSAO = {
            "ctl00$ScriptManager1": "ctl00$PlaceHolderConteudo$panel|ctl00$PlaceHolderConteudo$rdbCNPJ",
            "__EVENTTARGET": "ctl00$PlaceHolderConteudo$rdbCNPJ",
            "ctl00$PlaceHolderConteudo$grupoCNPJCEI": 'rdbCNPJ',
            "ctl00$PlaceHolderConteudo$grupoTipoComprovante": "rdbCompleto",
        }

PAYLOAD_BUSCA = {
            "ctl00$ScriptManager1": "ctl00$PlaceHolderConteudo$panel|ctl00$PlaceHolderConteudo$btnConfirmar",
            "ctl00$PlaceHolderConteudo$grupoCNPJCEI": 'rdbCNPJ',
            "ctl00$PlaceHolderConteudo$grupoTipoComprovante": "rdbCompleto",
            "ctl00$PlaceHolderConteudo$btnConfirmar": "Confirmar"
        }   