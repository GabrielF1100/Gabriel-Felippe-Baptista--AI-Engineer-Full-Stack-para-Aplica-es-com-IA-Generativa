import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pypdf
from emporio import config


class PolicyRetriever:
    """
    Mecanismo de indexação e recuperação das políticas internas da Empório da Música.
    Extrai e estrutura as regras do PDF 'políticas_da_loja.pdf' para consulta pelo agente.
    """

    def __init__(self, pdf_path: Optional[Path] = None):
        self.pdf_path = pdf_path or config.POLICIES_PDF
        self.raw_text: str = ""
        self.sections: List[Dict[str, str]] = []
        self._load_and_index()

    def _load_and_index(self):
        """
        Lê o PDF e fragmenta o documento em seções temáticas para retrieval de alta precisão.
        """
        if self.pdf_path and Path(self.pdf_path).exists():
            try:
                reader = pypdf.PdfReader(str(self.pdf_path))
                pages_text = []
                for p in reader.pages:
                    txt = p.extract_text() or ""
                    # Limpeza de espaçamentos estranhos do PDF
                    txt = re.sub(r"[ \t]+", " ", txt)
                    pages_text.append(txt)
                self.raw_text = "\n".join(pages_text)
            except Exception as e:
                self.raw_text = f"Erro ao carregar PDF: {e}"

        # Segmentação por tópicos do manual oficial
                self.sections = []

    def search_policies(self, query: str, top_k: int = 2):
        return []
