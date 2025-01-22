import PyPDF2
import re
import io
from datetime import datetime

from PyPDF2.errors import PdfReadError
import traceback

class PDFExtractor: 
    """
    Classe para extração de informações de PDFs de comprovantes de inscrição no PAT.
    """

    def extract_text_from_pdf(self, bytesPdf):
        """
        Extrai o texto de todas as páginas de um arquivo PDF.

        Args:
            bytesPdf (bytes): Conteúdo do arquivo PDF em bytes.

        Returns:
            list: Lista de strings, cada string contém o texto de uma página do PDF.
        """
        pdf_file = io.BytesIO(bytesPdf)
        leitor_pdf = PyPDF2.PdfReader(pdf_file)
        return [pagina.extract_text() for pagina in leitor_pdf.pages]

    def extract_inscricao_pat(self, text):
        """
        Extrai o número de inscrição no PAT do texto da primeira página do PDF.

        Args:
            text (str): Texto extraído da primeira página do PDF.
        """
        regex_inscricao_pat = r'Inscrição no PAT:\s*(\d+)'
        ins_pat = re.search(regex_inscricao_pat, text)
        if ins_pat:
            self.inscricao_pat = ins_pat.group(1)
            self.dados_extracao['inscricao_pat'] = ins_pat.group(1)
        else:
            self.inscricao_pat = None
            self.dados_extracao['inscricao_pat'] = None
    
    def extract_cnpj(self, texto):
        """
        Extrai o cnpj do texto da primeira página do PDF.

        Args:
            text (str): Texto extraído da primeira página do PDF.
        """
        regex_cnpj = r"CNPJ\| CNO\|CAEPF:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})"
        cnpj = re.search(regex_cnpj, texto)
        if cnpj:
            cnpj_raw = cnpj.group(1)
            cnpj = cnpj_raw.replace('.', '').replace('/', '').replace('-', '')
            self.dados_extracao['cnpj'] = cnpj
        else:
            self.dados_extracao['cnpj'] = None

    def extract_razao_social(self, texto):
        """
        Extrai a razão social do texto da primeira página do PDF.

        Args:
            text (str): Texto extraído da primeira página do PDF.
        """
        regex_razao_social = r'Razão Socia\|\|Nome Obral:\s*(.*?)\s*Endereço:'
        razao_social = re.search(regex_razao_social, texto)
        if razao_social:
            self.dados_extracao['razao_social'] = razao_social.group(1)
        else:
            self.dados_extracao['razao_social'] = None

    def extract_data_inscricao(self, texto):
        """
        Extrai a data de inscrição.

        Args:
            text (str): Texto extraído da primeira página do PDF.
        """
        regex_data = r"Data da Inscrição:\s*(\d{2}/\d{2}/\d{4})"
        data_ins = re.search(regex_data, texto)
        if data_ins:
            data_inscricao = data_ins.group(1)
            self.dados_extracao['data_inscricao'] = datetime.strptime(data_inscricao, "%d/%m/%Y").strftime("%Y-%m-%d")
        else:
            self.dados_extraca['data_inscricao'] = None

    def process_page(self, text):
        """
        Processa uma página do PDF para extrair e atualizar os dados.

        Args:
            text (str): Texto extraído da página do PDF.
        """
        split_dados = text.split("Q.t. de trabalhador(es) beneficiado(s) por faixa salarial no")[1:]

        for texto in split_dados:
            resultado = self.extract_dados(texto)
            if resultado:
                self.dados_extracao.update(resultado)
                break

    def extract_total_beneficiarios(self, text):
        """
        Extrai informações adicionais do texto da última página do PDF.

        Args:
            text (str): Texto extraído da última página do PDF.
        """

        split_dados = text.split("Dados da Execução do Programa Consolidados")[1]
        regex_total = r'Total:\s*(\d+)'

        resultados_total = re.findall(regex_total, split_dados)
        self.dados_extracao['total_beneficiarios'] = resultados_total[-1]

    def extract_email(self, texto):
        """
        Extrai o e-mail do texto do PDF.

        Args:
            text (str): Texto extraído da última página do PDF.
        """
        split_dados = texto.split("Dados da Execução do Programa Consolidados")[1]
        regex_email = r'E-mail:\s*([\w\.-]+@[\w\.-]+\.\w+)'
        email = re.search(regex_email, split_dados)
        if email:
            self.dados_extracao['email'] = email.group(1)
    
    def process_pdf(self, bytesPdf):
        """
        Processa um arquivo PDF para extrair todos os dados necessários.

        Args:
            bytesPdf (bytes): Conteúdo do arquivo PDF em bytes.

        Returns:
            dict: Dicionário com todos os dados extraídos do PDF.

        Raises:
            ValueError: Se ocorrer um erro na extração do PDF.
        """
        try:
            pages_text = self.extract_text_from_pdf(bytesPdf)
            for num, text in enumerate(pages_text):
                text = text.replace('\n', ' ')
                if num == 0:
                    self.extract_inscricao_pat(text)
                    self.extract_cnpj(text)
                    self.extract_razao_social(text)
                    self.extract_data_inscricao(text)
            self.extract_total_beneficiarios(pages_text[-1])
            self.extract_email(pages_text[-1])
            return self.dados_extracao
        except PdfReadError as e:
            logger.log_processo(f'Erro na leitura do PDF extraido. Detalhes: {e}')
            raise ValueError(f"Erro na leitura do PDF")
        except Exception:
            logger.log_processo(f'Erro na extração do PDF. Detalhes: {traceback.format_exc()}')
            raise ValueError("Erro na extração do PDF")
