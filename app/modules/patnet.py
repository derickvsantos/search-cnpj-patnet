import re
import requests
from bs4 import BeautifulSoup
from app.resources import config, selectors
from app.modules.pdf_extract import PDFExtractor

class Patnet(PDFExtractor):
    """
    Classe para interação com o sistema PAT, login, busca de CNPJ e extração de PDF.
    """
    def __init__(self, cnpj):
        """
        Inicializa a classe Patnet.

        Args:
            cnpj (str): CNPJ da empresa.
        """
        self.session = requests.Session()
        self.cnpj = cnpj
        self.inscricao_pat = None
        self.dados_extracao = {}

    def criar_payload_comum(self, url):
        """
        Cria o payload comum para as requisições baseando-se no estado atual da página.

        Args:
            url (str): URL para a qual a requisição GET será feita para obter o estado da página.

        Returns:
            dict: Payload comum contendo __ASYNCPOST, __VIEWSTATE, __VIEWSTATEGENERATOR e __EVENTVALIDATION.
        """
        try:
            response = self.session.request(method="GET", url=url, headers=config.HEADERS, timeout=10)
        except requests.exceptions.ReadTimeout as e:
            raise Exception("Portal PATNET fora do ar ou instavel")
        soup = BeautifulSoup(response.content, "html.parser")
        
        payload = {
            "__ASYNCPOST": "true",
            "__VIEWSTATE": soup.find("input", {"id": "__VIEWSTATE"})["value"],
            "__VIEWSTATEGENERATOR": soup.find("input", {"id": "__VIEWSTATEGENERATOR"})["value"]
        }
        eventvalidation = soup.find("input", {"id": "__EVENTVALIDATION"})
        if eventvalidation:
            payload["__EVENTVALIDATION"] = eventvalidation.get("value", None)
        return payload

    def login(self):
        """
        Realiza o login no sistema PAT.

        Returns:
            Response: Resposta da requisição de login.

        Raises:
            ValueError: Se houver erro no login.
        """
        payload_comum = self.criar_payload_comum(config.URL + "LoginPAT.aspx")
        payload_login = selectors.PAYLOAD_LOGIN
        payload_login.update(payload_comum)
        payload_login["ctl00$PlaceHolderConteudo$txtUsuario"] = config.USER
        payload_login["ctl00$PlaceHolderConteudo$txtSenha"] = config.PWD
        response = self.session.request(method="POST",
                                        url=config.URL + "LoginPAT.aspx", 
                                        data=payload_login,
                                        headers=config.HEADERS, timeout=5)

        self.verificar_erro(selectors.LOGIN, response.text)
        return response

    def reemitir_comprovante(self):
        """
        Inicia o processo de remissão do comprovante no sistema PAT.

        Returns:
            Response: Resposta da requisição de busca de CNPJ.
        """
        payload_comum = self.criar_payload_comum(config.URL + "Beneficiaria/ReemitirComprovanteInscricao.aspx")
        payload_reemissao = selectors.PAYLOAD_REMISSAO
        payload_reemissao.update(payload_comum)

        response_inicial = self.session.request(method="POST", 
                                                url=config.URL + "Beneficiaria/ReemitirComprovanteInscricao.aspx",
                                                data=payload_reemissao,
                                                headers=config.HEADERS)

        return response_inicial, payload_comum

    def buscar_cnpj(self, response_html, payload_comum):
        """
        Realiza a busca de um CNPJ específico no sistema PAT.

        Args:
            response_html (str): Resposta HTML da página inicial de reemissão.
            payload_comum (dict): Payload comum contendo __ASYNCPOST, __VIEWSTATE, __VIEWSTATEGENERATOR e __EVENTVALIDATION.

        Returns:
            Response: Resposta da requisição de busca de CNPJ.

        Raises:
            ValueError: Se houver erro na busca do CNPJ.
        """
        viewstate = re.search(r'__VIEWSTATE\|(.*?)\|', response_html.text).group(1)

        payload_busca = selectors.PAYLOAD_BUSCA
        payload_busca.update(payload_comum)
        payload_busca["ctl00$PlaceHolderConteudo$txtCNPJCEI"] = self.cnpj
        payload_busca['__VIEWSTATE'] = viewstate

        final_response = self.session.request(method="POST", 
                                              url=config.URL + "Beneficiaria/ReemitirComprovanteInscricao.aspx", 
                                              data=payload_busca, 
                                              headers=config.HEADERS)

        self.verificar_erro(selectors.CONSULTA_CNPJ, final_response.text)
        return final_response

    def verificar_erro(self, erros, texto):
        """
        Verifica se há erros específicos no texto da resposta.

        Args:
            erros (list): Lista de strings de erros para verificar.
            texto (str): Texto da resposta HTML.

        Raises:
            ValueError: Se algum dos erros especificados for encontrado no texto.
        """
        for erro in erros:
            if erro.upper() in texto.upper():
                print(f'Erro encontrado: {erro}')
                raise ValueError(erro)

    def pegar_pdf(self):
        """
        Realiza a requisição para pegar o PDF do comprovante.

        Returns:
            Response: Resposta da requisição de download do PDF.
        """
        url = config.URL + "Relatorios/ImprimirComprovanteEmpresaBeneficiaria.aspx?tpComprovante=Completo"
        response = self.session.request(method="GET", url=url, headers=config.HEADERS)
        return response

    def start(self):
        """
        Inicia o processo completo de login, reemissão de comprovante e extração de dados do PDF.

        Returns:
            dict: Dados extraídos do PDF.
        """
        self.login()
        response_inicial, payload_comum = self.reemitir_comprovante()
        self.buscar_cnpj(response_inicial, payload_comum)
        pdfBytes = self.pegar_pdf()
        return self.process_pdf(pdfBytes.content)