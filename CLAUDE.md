# CLAUDE.md — NLP Learning Hub

## 1. Project Identity

Project name: NLP Learning Hub

Project title: Natural Language Processing dengan Python untuk Pemula hingga Mahir

Primary language: Bahasa Indonesia.

Primary programming language: Python.

Documentation framework: MkDocs using the existing repository template.

Primary learning project: Klasifikasi teks Twitter/X terkait kebencanaan menjadi Emergency dan Non-Emergency.

Target audience: Pemula yang belum memiliki pengetahuan NLP, kemudian berkembang hingga mampu membangun, mengevaluasi, dan melakukan deployment aplikasi NLP.

## 2. Rules for Working in This Repository

Before modifying files:

1. Read this file and inspect the existing repository.
2. Inspect `mkdocs.yml`, the active theme, plugins, dependencies, navigation, CSS, JavaScript, and existing documentation.
3. Follow the actual repository configuration. Do not assume the documentation directory is named `docs`.
4. Preserve the existing template and unrelated user changes.
5. Never replace existing project files blindly.
6. Avoid unnecessary dependencies, configuration changes, and broad refactoring.
7. Follow the project's detailed curriculum and implementation plan when available.
8. If a required specification is missing, inspect the repository and make the smallest reasonable decision.
9. Do not claim that code, tests, builds, or experiments succeeded unless they have actually been executed and verified.

Use small, reviewable implementation steps. Finish and validate one logical stage before starting another.

### 2.1 Project documents (read before continuing work)

- `SPEC_NLP_LEARNING_HUB.md` (repository root): master specification. It holds the full curriculum (Level 0–7), the main project (Stages A–H), the directory layout, and the implementation order (Stages 1–8). It is not published by MkDocs. Do not copy the curriculum into this file.
- `docs/IMPLEMENTATION_PLAN.md`: current repository state, technical decisions, and the status of each implementation stage. Update it at the end of every stage.
- `docs/lampiran/audit-verifikasi.md`: log of checks that were actually run, failed, or not yet done.

If this file and the specification conflict on lesson format or code-explanation depth, this file wins (it is stricter). The specification wins on curriculum scope and stage order.

Practical facts: the content directory is `docs/`; code examples live in `examples/` and are included in pages through `pymdownx.snippets`; the local Python environment is `.venv/` (install with `requirements.txt` and `requirements-ml.txt`; `requirements-dl.txt` is optional and heavy).

## 3. Teaching Philosophy

Write all learning materials in Bahasa Indonesia.

Assume the reader is a complete beginner.

Do not assume the reader already understands:

- Programming terminology.
- Python syntax.
- Data structures.
- Mathematics used in machine learning.
- Statistics and probability.
- Linguistics and text processing.
- Machine learning algorithms.
- Deep learning architectures.

Explain prerequisite concepts before using them.

Teach concepts progressively:

1. Explain the problem in everyday language.
2. Introduce the technical term.
3. Explain why the concept is needed.
4. Describe how it works.
5. Show a simple example.
6. Explain the example step by step.
7. Apply the concept to disaster-related social media text.
8. Discuss common mistakes and limitations.
9. Provide exercises with solutions and explanations.
10. Summarize the main concepts.

Do not replace detailed teaching with brief definitions or lists of terminology.

Prefer clarity, conceptual understanding, and reproducibility over brevity.

## 4. Mandatory Rules for Python Code Explanations

This section has high priority for every lesson, tutorial, notebook, and programming example.

### 4.1 Never leave long code unexplained

When a code example contains multiple logical steps, explain it in small, understandable sections.

Do not present a long Python script and provide only a short paragraph saying what the script does.

For long code, use the following teaching sequence:

1. Explain the overall goal of the program.
2. Show a short overview of the processing flow.
3. List the required libraries and explain their purposes.
4. Explain the expected input and output.
5. Divide the implementation into logical code blocks.
6. Explain each block before or immediately after presenting it.
7. Explain important lines and statements individually.
8. Show how the output changes after each important step.
9. Explain how the blocks connect into a complete program.
10. Present the complete integrated code only when it helps the reader understand or run the entire solution.

### 4.2 Use progressive code chunks

Break code into small chunks according to their logical purpose.

For example, a text classification lesson should not immediately present a complete training pipeline.

Instead, teach it in stages:

- Part 1: Import libraries.
- Part 2: Prepare a small example dataset.
- Part 3: Inspect the data.
- Part 4: Separate text features and labels.
- Part 5: Split training and test data.
- Part 6: Convert text into TF-IDF features.
- Part 7: Train a model.
- Part 8: Generate predictions.
- Part 9: Evaluate the predictions.
- Part 10: Interpret the results.

Each part must be understandable on its own and clearly connected to the previous part.

The exact number of chunks should depend on the complexity of the lesson. Avoid breaking simple code into unnecessarily tiny fragments.

### 4.3 Explain Python syntax for beginners

When a new syntax or concept appears, explain it in context.

Examples include:

- `import`
- Variables and assignment
- Strings and lists
- Dictionaries
- Functions and parameters
- Return values
- Loops and conditions
- List comprehensions
- Lambda functions
- Classes and objects
- Exception handling
- Type annotations
- Context managers
- Decorators
- Generators
- Asynchronous functions
- Python package imports
- Pipeline APIs
- Method chaining

Do not explain every familiar character in every example. Focus on syntax that is new, important, or likely to confuse a beginner.

### 4.4 Explain the input, output, and intermediate values

For each significant code block, explain:

- What data enters the block.
- What each important variable represents.
- What transformation occurs.
- What data leaves the block.
- What the output means.
- How to check whether the result is correct.

When useful, show small intermediate tables, sample strings, array shapes, data types, or printed outputs.

Distinguish expected illustrative output from output actually produced by an executed experiment.

### 4.5 Explain why the code is written that way

Do not merely explain what a statement does.

Also explain why the approach is appropriate, what problem it solves, and what alternatives exist.

For example, when using `train_test_split`, explain:

- Why a dataset is divided.
- What training and test data are used for.
- Why evaluating on training data alone is misleading.
- What `test_size` means.
- Why `random_state` is useful.
- When `stratify` is appropriate.
- Why preprocessing that learns corpus statistics must be fitted only on training data.

### 4.6 Explain errors and debugging

For important examples, explain likely mistakes, such as:

- Missing imports.
- Incorrect file paths.
- Missing Python packages.
- Incorrect column names.
- Unexpected missing values.
- Incorrect data types.
- Shape mismatches.
- Data leakage.
- Incorrect label encoding.
- Incompatible library APIs.
- Overfitting.
- Incorrect metric interpretation.

When demonstrating an error, explain the cause, how to recognize it, and how to fix it.

### 4.7 Use a complete example only after teaching its components

A complete integrated script is useful for reproducibility, but it must not replace the step-by-step explanation.

After the individual chunks have been explained, provide a consolidated script when appropriate.

Clearly distinguish:

- Educational snippets.
- An integrated runnable example.
- Production-oriented implementation.

Avoid presenting production abstractions, advanced design patterns, or complex helper functions before the reader understands their purpose.

## 5. Mandatory Structure for Learning Materials

Every substantive lesson should include the following sections, adapted to the topic.

1. Judul materi.
2. Tingkat kesulitan.
3. Tujuan pembelajaran.
4. Prasyarat.
5. Pengantar dan motivasi.
6. Konsep dasar.
7. Penjelasan mendalam.
8. Cara kerja atau alur proses.
9. Contoh sederhana.
10. Contoh dalam konteks Twitter/X kebencanaan.
11. Praktik Python jika relevan.
12. Penjelasan kode per bagian.
13. Contoh output dan interpretasinya.
14. Kesalahan umum dan debugging.
15. Kelebihan dan keterbatasan metode.
16. Latihan bertahap.
17. Kunci jawaban dan pembahasan.
18. Kuis singkat.
19. Ringkasan.
20. Glosarium istilah baru.
21. Referensi yang relevan.
22. Materi prasyarat atau materi berikutnya.

For reference pages, glossaries, installation guides, and appendices, use an appropriate structure instead of forcing every section into the page.

A lesson must be detailed enough that a beginner can study it independently without needing to ask what each major step means.

## 6. Depth and Accuracy Requirements

Explain concepts from intuition to technical details.

Where appropriate, include:

- Formal definitions.
- Mathematical notation and explanations of symbols.
- Worked numerical examples.
- Diagrams or flow descriptions.
- Comparisons with related methods.
- Advantages and disadvantages.
- Practical use cases.
- Failure modes.
- Reproducible Python experiments.

When introducing mathematics, explain each symbol and use a small numerical example before presenting a more general formula.

Do not introduce unnecessary mathematical complexity before the required foundations have been taught.

Do not make a page longer merely to meet a word count. Add depth through examples, reasoning, interpretation, and exercises.

## 7. Consistent Disaster Classification Case Study

Use the same overarching case study throughout the curriculum:

Classification of Indonesian Twitter/X posts into:

- `Emergency`
- `Non-Emergency`

Explain the operational definition of both labels in the project documentation.

Do not classify a post as Emergency merely because it contains a disaster keyword.

Consider context, intent, reported incident, request for assistance, urgency, temporal relevance, and ambiguity.

Use illustrative examples such as:

- "Tolong, air banjir sudah masuk ke rumah kami."
- "Pemerintah mengumumkan pembangunan tanggul untuk mengurangi risiko banjir."
- "Gempa terasa kuat, warga diminta menjauhi bangunan yang rusak."
- "Saya sedang membaca berita tentang gempa tahun lalu."

These examples are teaching illustrations, not a validated annotation dataset. Their labels must follow the documented operational definitions.

Explain that classification errors have different consequences. Discuss false negatives for emergency reports, false positives, class imbalance, uncertainty, and the need for human verification in operational response systems.

## 8. Dataset and Research Integrity

Distinguish synthetic educational data from real research data.

Never fabricate experimental results, citations, DOIs, source provenance, or dataset statistics.

Do not download or scrape Twitter/X data automatically unless explicitly requested and the proposed access method has been checked for applicable requirements.

Document the source, permitted use, data preparation, label definitions, limitations, and evaluation methodology of any real dataset.

Do not expose personal information or credentials in examples, notebooks, logs, or generated documentation.

Avoid data leakage by separating training and test data correctly and fitting learned transformations inside the training pipeline.

Use reproducible random seeds where appropriate and explain their limitations.

Do not claim a model is suitable for operational emergency response without appropriate validation.

## 9. Python and NLP Technical Standards

Use Python as the primary programming language.

Prefer standard Python for introductory programming concepts, pandas for tabular data, and scikit-learn for classical machine learning.

Introduce specialized libraries only when they add clear educational value.

Use the following progression where appropriate:

1. Python fundamentals.
2. String manipulation and regular expressions.
3. pandas and exploratory text analysis.
4. Text preprocessing.
5. Bag of Words and TF-IDF.
6. Multinomial Naive Bayes.
7. Logistic Regression.
8. Linear SVM.
9. Evaluation and error analysis.
10. Word embeddings and deep learning.
11. Transformer models and IndoBERT.
12. FastAPI and deployment.

Explain the purpose of every major library and the reason for choosing an algorithm.

Do not assume that a more complex model will perform better.

Use pipelines, clear variable names, modular functions, and appropriate tests.

Avoid unnecessary abstractions in beginner lessons. Introduce reusable abstractions after the underlying logic is understood.

## 10. MkDocs Documentation Standards

Follow the existing MkDocs theme and repository configuration.

Before adding a plugin or changing configuration, check whether the required feature already exists.

Use consistent navigation, filenames, headings, internal links, code blocks, tables, and admonitions supported by the active theme.

Follow existing repository conventions for Markdown headings.

Keep each main concept in a separate, logically named Markdown file.

Avoid monolithic pages containing multiple unrelated lessons.

Ensure code snippets, relative links, notebook paths, and navigation entries remain consistent.

Do not change the deployment workflow unless required and documented.

## 11. Exercises and Assessment

Exercises must progress from easy to difficult.

Use a mixture of:

- Conceptual questions.
- Code-reading exercises.
- Fill-in-the-code tasks.
- Debugging exercises.
- Small programming assignments.
- Text preprocessing challenges.
- Model evaluation exercises.
- Mini-projects.

Provide answer keys and explain why the answers are correct.

Do not reveal a solution without explaining the reasoning.

Use disaster-related text examples whenever relevant.

Include practical checkpoints at the end of each level.

## 12. References and Citations

Prefer official documentation and relevant primary research sources.

Use references that support the actual statements being made.

Verify bibliographic details and URLs before adding them.

Distinguish academic research papers from official documentation, tutorials, and informal articles.

Never invent citations.

Explain when an implementation detail depends on a particular library version.

## 13. Implementation and Validation Workflow

Work in small, reviewable stages.

For each stage:

1. Inspect relevant existing files.
2. State the intended scope briefly.
3. Implement the requested content.
4. Run applicable checks.
5. Fix issues caused by the changes.
6. Summarize files created or modified.
7. Report tests and builds that were actually run.
8. Identify unresolved issues.
9. Record the next logical step in the project implementation plan.

Do not regenerate the entire documentation site unnecessarily.

Do not rewrite previously completed lessons unless there is a specific reason.

When continuing work, inspect the implementation plan and current repository state before deciding what remains to be done.

Prioritize complete, accurate, pedagogically effective lessons over the number of files created.

## 14. Definition of Done

A lesson is complete when:

- Its explanation is appropriate for its intended audience.
- Prerequisites are clear.
- Important concepts are explained in sufficient depth.
- Long code is divided into understandable sections.
- Every significant code section has a clear explanation.
- Inputs, outputs, and intermediate results are interpreted.
- Exercises include solutions and reasoning.
- References are relevant and verified.
- Internal links and navigation are correct.
- Code has been tested when feasible, and testing status is accurately reported.

A project stage is complete only when its deliverables and validation status are documented.

The primary objective is to create a reliable, detailed, self-guided NLP learning resource in Bahasa Indonesia, not merely a collection of Markdown files.