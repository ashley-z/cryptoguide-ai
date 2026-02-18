"""
CryptoGuide AI — Automated Evaluation Suite
Measures: Retrieval Accuracy, Answer Quality, Citation Accuracy, Latency, Cost
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import List, Dict, Any

from dotenv import load_dotenv
load_dotenv()

# Add parent dir so we can import rag
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rag import RAGPipeline

# ── Constants ──────────────────────────────────────────────
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
GROUND_TRUTH_PATH = os.path.join(EVAL_DIR, "ground_truth.json")
REPORT_PATH = os.path.join(EVAL_DIR, "eval_report.md")

# Rough cost estimates (per 1K tokens)
COST_EMBED_INPUT = 0.0001     # text-embedding-ada-002
COST_HAIKU_INPUT = 0.00025    # claude-3-haiku input
COST_HAIKU_OUTPUT = 0.00125   # claude-3-haiku output
AVG_INPUT_TOKENS = 1200
AVG_OUTPUT_TOKENS = 400


def load_ground_truth() -> List[Dict]:
    with open(GROUND_TRUTH_PATH, 'r') as f:
        data = json.load(f)
    return data["test_cases"]


def check_retrieval_accuracy(retrieved_docs: List[Dict], expected_source: str) -> bool:
    """Check if the expected source appears in the retrieved documents."""
    for doc in retrieved_docs:
        meta = doc.get('metadata', {})
        source = meta.get('source', '')
        if expected_source.lower() in source.lower():
            return True
    return False


def check_keyword_coverage(answer: str, expected_keywords: List[str]) -> float:
    """Check what fraction of expected keywords appear in the answer."""
    answer_lower = answer.lower()
    found = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
    return found / len(expected_keywords) if expected_keywords else 0.0


def check_citation_accuracy(answer: str, num_sources: int) -> float:
    """Check if the answer contains citation references like [1], [2]."""
    import re
    citations = set(re.findall(r'\[(\d+)\]', answer))
    if not citations:
        return 0.0
    valid = sum(1 for c in citations if 1 <= int(c) <= num_sources)
    return valid / len(citations) if citations else 0.0


def estimate_cost() -> float:
    """Estimate cost per query based on token usage."""
    input_cost = (AVG_INPUT_TOKENS / 1000) * COST_HAIKU_INPUT
    output_cost = (AVG_OUTPUT_TOKENS / 1000) * COST_HAIKU_OUTPUT
    embed_cost = (AVG_INPUT_TOKENS / 1000) * COST_EMBED_INPUT
    return input_cost + output_cost + embed_cost


def run_evaluation():
    """Run full evaluation suite against ground truth dataset."""
    print("=" * 60)
    print("CryptoGuide AI — Evaluation Suite")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Init pipeline
    rag = RAGPipeline()
    test_cases = load_ground_truth()

    results = []
    total_start = time.time()

    for tc in test_cases:
        print(f"\n[{tc['id']}/{len(test_cases)}] {tc['protocol'].upper()}: {tc['question'][:60]}...")

        # Measure latency
        start = time.time()

        # Step 1: Retrieve
        docs = rag.retrieve_context(tc['question'], tc['protocol'])
        retrieval_time = time.time() - start

        # Step 2: Generate
        gen_start = time.time()
        result = rag.generate_answer(tc['question'], tc['protocol'])
        generation_time = time.time() - gen_start
        total_time = time.time() - start

        answer = result['answer']
        sources = result['sources']

        # Metrics
        retrieval_accurate = check_retrieval_accuracy(docs, tc['expected_source'])
        keyword_coverage = check_keyword_coverage(answer, tc['expected_keywords'])
        citation_accuracy = check_citation_accuracy(answer, len(sources))
        cost = estimate_cost()

        r = {
            "id": tc['id'],
            "protocol": tc['protocol'],
            "question": tc['question'],
            "category": tc['category'],
            "retrieval_accurate": retrieval_accurate,
            "keyword_coverage": keyword_coverage,
            "citation_accuracy": citation_accuracy,
            "latency_s": round(total_time, 2),
            "retrieval_time_s": round(retrieval_time, 2),
            "generation_time_s": round(generation_time, 2),
            "cost_usd": round(cost, 5),
            "num_sources": len(sources),
            "answer_preview": answer[:150] + "..."
        }
        results.append(r)

        status = "✅" if retrieval_accurate else "❌"
        print(f"  {status} Retrieval: {retrieval_accurate} | Keywords: {keyword_coverage:.0%} | "
              f"Citations: {citation_accuracy:.0%} | Latency: {total_time:.1f}s")

    total_duration = time.time() - total_start

    # Aggregate
    n = len(results)
    retrieval_acc = sum(1 for r in results if r['retrieval_accurate']) / n
    avg_keyword = sum(r['keyword_coverage'] for r in results) / n
    avg_citation = sum(r['citation_accuracy'] for r in results) / n
    avg_latency = sum(r['latency_s'] for r in results) / n
    avg_cost = sum(r['cost_usd'] for r in results) / n
    total_cost = sum(r['cost_usd'] for r in results)

    # Per-protocol breakdown
    protocols = ['aave', 'compound', 'uniswap']
    proto_stats = {}
    for p in protocols:
        p_results = [r for r in results if r['protocol'] == p]
        if p_results:
            proto_stats[p] = {
                'count': len(p_results),
                'retrieval': sum(1 for r in p_results if r['retrieval_accurate']) / len(p_results),
                'keywords': sum(r['keyword_coverage'] for r in p_results) / len(p_results),
                'citations': sum(r['citation_accuracy'] for r in p_results) / len(p_results),
                'latency': sum(r['latency_s'] for r in p_results) / len(p_results),
            }

    # Print summary
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"  Retrieval Accuracy:  {retrieval_acc:.0%}  (target: ≥85%)")
    print(f"  Keyword Coverage:    {avg_keyword:.0%}  (proxy for answer quality)")
    print(f"  Citation Accuracy:   {avg_citation:.0%}  (target: ≥90%)")
    print(f"  Average Latency:     {avg_latency:.1f}s  (target: <15s)")
    print(f"  Average Cost/Query:  ${avg_cost:.4f}  (target: <$0.05)")
    print(f"  Total Eval Cost:     ${total_cost:.4f}")
    print(f"  Total Duration:      {total_duration:.0f}s")

    # Generate report
    generate_report(results, retrieval_acc, avg_keyword, avg_citation,
                    avg_latency, avg_cost, total_cost, total_duration, proto_stats)

    # Save raw results
    raw_path = os.path.join(EVAL_DIR, "eval_results.json")
    with open(raw_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📊 Report saved to: {REPORT_PATH}")
    print(f"📄 Raw results saved to: {raw_path}")


def generate_report(results, retrieval_acc, avg_keyword, avg_citation,
                    avg_latency, avg_cost, total_cost, total_duration, proto_stats):
    """Generate markdown evaluation report."""

    def status_icon(val, target):
        return "✅" if val >= target else "⚠️"

    lines = [
        f"# CryptoGuide AI — Evaluation Report",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Test Cases:** {len(results)}  ",
        f"**Total Duration:** {total_duration:.0f}s  ",
        f"**Total Cost:** ${total_cost:.4f}",
        f"",
        f"---",
        f"",
        f"## Aggregate Metrics",
        f"",
        f"| Metric | Result | Target | Status |",
        f"|---|---|---|---|",
        f"| Retrieval Accuracy | {retrieval_acc:.0%} | ≥85% | {status_icon(retrieval_acc, 0.85)} |",
        f"| Keyword Coverage | {avg_keyword:.0%} | ≥75% | {status_icon(avg_keyword, 0.75)} |",
        f"| Citation Accuracy | {avg_citation:.0%} | ≥90% | {status_icon(avg_citation, 0.90)} |",
        f"| Avg Latency | {avg_latency:.1f}s | <15s | {status_icon(1 - avg_latency/15, 0)} |",
        f"| Avg Cost/Query | ${avg_cost:.4f} | <$0.05 | {status_icon(1 - avg_cost/0.05, 0)} |",
        f"",
        f"---",
        f"",
        f"## Per-Protocol Breakdown",
        f"",
        f"| Protocol | Questions | Retrieval | Keywords | Citations | Avg Latency |",
        f"|---|---|---|---|---|---|",
    ]

    for p, s in proto_stats.items():
        lines.append(
            f"| {p.capitalize()} | {s['count']} | {s['retrieval']:.0%} | "
            f"{s['keywords']:.0%} | {s['citations']:.0%} | {s['latency']:.1f}s |"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## Per-Question Results",
        f"",
        f"| # | Protocol | Category | Retrieval | Keywords | Citations | Latency |",
        f"|---|---|---|---|---|---|---|",
    ]

    for r in results:
        ret_icon = "✅" if r['retrieval_accurate'] else "❌"
        lines.append(
            f"| {r['id']} | {r['protocol']} | {r['category']} | {ret_icon} | "
            f"{r['keyword_coverage']:.0%} | {r['citation_accuracy']:.0%} | {r['latency_s']}s |"
        )

    # Failures section
    failures = [r for r in results if not r['retrieval_accurate']]
    if failures:
        lines += [
            f"",
            f"---",
            f"",
            f"## Retrieval Failures",
            f"",
        ]
        for r in failures:
            lines.append(f"- **Q{r['id']}** ({r['protocol']}): {r['question']}")

    lines.append("")
    with open(REPORT_PATH, 'w') as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    run_evaluation()
