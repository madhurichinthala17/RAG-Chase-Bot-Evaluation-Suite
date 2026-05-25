from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig
from deepeval.models import OllamaModel
from deepeval.dataset import EvaluationDataset
import os
from pathlib import Path

PDF_PATH = str(Path(__file__).parent.parent.parent / "data" / "raw_docs" / "JPmorgan10kReport.pdf")

assert os.path.exists(PDF_PATH), f"PDF not found at {PDF_PATH}"

retrievermodel = OllamaModel(model="deepseek-r1:8b")

synthesizer = Synthesizer(model=retrievermodel)

goldens = synthesizer.generate_goldens_from_docs(
    document_paths=[PDF_PATH],
    include_expected_output=True,
    max_goldens_per_context=1,
    context_construction_config=ContextConstructionConfig(
        chunk_size=600,
        chunk_overlap=100,
        max_retries=3,  
    ),
)

dataset = EvaluationDataset(goldens=goldens)
dataset.push("Synthetic Golden from Doc")
