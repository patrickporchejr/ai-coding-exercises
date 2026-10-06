# Exercise 11: RAG Over a Help Center

**Skills:** chunking, retrieval, grounded generation with citations, and evaluating retrieval separately from answers.
**Time box:** 90 minutes. **Needs:** an Anthropic API key.

## The interview prompt

> `corpus/` holds the help-center articles for Tidepool, a (fictional) team-scheduling product. Build a question-answering system over it: retrieve the relevant passages, have Claude answer using only those passages, and cite the sources.
>
> Then show me how well it works. `questions.jsonl` has 20 questions with the documents a correct answer should come from.

## Input
- **`corpus/*.md`**: 16 articles. Each starts with front matter containing `title` and `last_updated`.
- **`questions.jsonl`**: one object per line with `id`, `question`, `gold_docs` (the source documents an answer should come from; empty means the docs can't answer it), and `reference_answer`.

## Requirements
1. **Chunk the corpus.** Choose a chunking strategy and be ready to justify it.
2. **Retrieve.** Return the top-k chunks for a question. **BM25 or TF-IDF is fine**, from scratch or with a small library such as `rank-bm25` or scikit-learn. You don't need a vector database.
3. **Generate a grounded answer.** Claude answers from the retrieved chunks only and cites the documents it used. If the chunks don't contain the answer, it says so instead of guessing.
4. **Evaluate retrieval on its own.** Report recall@k (did the gold documents show up in the top k?) for at least two values of k.
5. **Evaluate answers.**
   - *Code checks*: each cited document actually appears in the retrieved chunks, and unanswerable questions get a refusal.
   - *Model grader*: is the answer correct against `reference_answer`, and is it supported by the retrieved text (faithfulness)? Use structured output.
6. **Report and find failures.** Give per-question results and the averages. For each failure, say whether retrieval or generation caused it.

## Stretch
- Swap in embeddings and compare recall@k with your keyword retriever. Anthropic doesn't offer an embeddings API, so this means another provider (the Anthropic docs point to Voyage AI) or a local model such as `sentence-transformers`.
- Combine keyword and embedding scores (hybrid retrieval), or rerank the top 20 with Claude.

## Debrief questions
- Why measure retrieval separately from answer quality? What would you miss if you only graded final answers?
- Two articles disagree about pricing. How did your system decide which to trust? Did that come from retrieval, the prompt, or luck?
- What did your chunk size trade off? What happened to the multi-document question?
- Why use a fictional product for this exercise? What would go wrong with a well-known one?
- How would this design change for 1 million documents, or for documents that change daily?
