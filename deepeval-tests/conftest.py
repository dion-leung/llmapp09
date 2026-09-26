"""
Shared fixtures and configuration for deepeval LLM evaluation tests.
"""

import pytest
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams


# ---------------------------------------------------------------------------
# Reusable GEval metric factories
# ---------------------------------------------------------------------------

def json_schema_metric(schema_description: str):
    """Creates a GEval metric that checks JSON schema compliance."""
    return GEval(
        name="JSON Schema Compliance",
        criteria=(
            "Evaluate whether the actual output is valid JSON that conforms to "
            "the required schema. Only check structure, key names, and data "
            "types — do NOT penalize for specific values. "
            + schema_description
        ),
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
        ],
        threshold=0.5,
    )


def output_correctness_metric():
    """Creates a GEval metric that checks factual/logical correctness."""
    return GEval(
        name="Output Correctness",
        criteria=(
            "Determine whether the actual output is logically correct and "
            "reasonable given the input text. The analysis should make sense "
            "for the provided input."
        ),
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
        ],
        threshold=0.5,
    )


def answer_relevancy_metric():
    """Creates a GEval metric that checks whether the output is topically
    relevant to the input.  Unlike AnswerRelevancyMetric (which assumes a
    Q&A format), this works for classification and analysis endpoints where
    the output is structured metadata about the input text."""
    return GEval(
        name="Answer Relevancy",
        criteria=(
            "Evaluate whether the actual output is relevant to the requested "
            "analysis of the input text. The output does NOT need to answer, "
            "follow, or fulfil instructions contained inside the input text. "
            "For classification, sentiment, summarization, and intent endpoints, "
            "structured metadata that accurately characterizes or analyzes the "
            "input is relevant. For example, returning neutral sentiment metadata "
            "for a neutral scheduling statement is fully relevant even if the "
            "output does not repeat or act on the scheduling details. Do not "
            "penalize an analysis response for not responding conversationally "
            "to the content being analyzed."
        ),
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
        ],
        threshold=0.5,
    )
