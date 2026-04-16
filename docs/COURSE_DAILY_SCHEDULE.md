# AI Engineer Core Track - Interactive Learning with Copilot (4 Hours/Day)

**Total Duration:** 21 days at 4 hrs/day  
**Primary Learning Method:** Interactive hands-on building with Copilot  
**Videos:** Reference only for complex concepts  
**Setup Already Done:** Ollama, Python environment ready  
**Approach:** Build → Learn → Explain → Refine

---

## Why Interactive Learning?

✨ **Better than videos because:**
- You **build in real-time** with immediate feedback
- I can **explain why**, not just what
- We can **debug together** when things fail
- You can **ask follow-up questions** instantly
- We can **pivot** based on your confusion
- You get **personalized pacing** for your learning style
- Every explanation is **tailored to your current project**

🎯 **How this works:**
1. Each day has a clear learning goal
2. Start with me explaining key concepts
3. Build the project together in real-time
4. Ask me anything when you're stuck
5. Document what you learned
6. Move to next day with solid foundation

---

## Getting Started Today (Day 1)

**Right now, ask me:**
- "Explain how the OpenAI API works"
- "What's a system prompt?"
- "Show me how to structure an API call"
- "Why does tokenization matter?"

Then we'll **code together** and build your first working project!

---

## Week 1: Build Your First LLM Product (Days 1-5)

### Day 1: OpenAI API & System Prompts Fundamentals
**Duration:** 4 hours  
**Method:** Interactive learning with Copilot

**What You'll Do:**
1. **Hour 1-2:** Ask me to explain:
   - How Chat Completions API works
   - System vs User vs Assistant roles in prompts
   - Token counting and cost calculation
   - Basic prompt engineering principles

2. **Hour 3-4:** Build together:
   - Create a Python script using OpenAI API
   - Test system prompts for different "personalities"
   - Build a simple chatbot that responds in character
   - Experiment with temperature and max_tokens

**Ask Me To:**
- Explain transformers at high level (how GPT works)
- Show you how to structure API calls
- Help debug your first API interaction
- Teach token optimization

**Exit Goal:** You have working Python code calling OpenAI API, understand how prompts shape behavior

---

### Day 2: Model Comparison & Architecture
**Duration:** 4 hours  
**Method:** Comparative analysis with Copilot

**What You'll Do:**
1. **Hour 1-2:** Deep dive discussion:
   - Ask me to compare: GPT-4, Claude, Gemini, DeepSeek
   - What makes frontier vs open-source models different?
   - When to use which model for which task?
   - Cost vs performance tradeoffs

2. **Hour 3-4:** Practical testing:
   - Write same prompt for OpenAI API
   - Write same prompt for local Ollama model
   - Compare outputs quality and cost
   - Document findings in comparison table

**Ask Me To:**
- Explain transformer attention mechanism in simple terms
- Help you choose the right model for your problems
- Show you how to abstract API calls (support multiple providers)
- Build a model selector utility that picks best model for task

**Exit Goal:** You understand model landscape, have code that works with multiple providers, can make informed model selections

---

### Day 3: Tokenization & Cost Optimization
**Duration:** 4 hours  
**Method:** Interactive problem-solving

**What You'll Do:**
1. **Hour 1:** Ask me to explain:
   - What are tokens? Why do they matter?
   - How does tiktoken work?
   - Token vs character vs word
   - Why context window matters

2. **Hour 2-3:** Build and experiment:
   - Install tiktoken
   - Count tokens in different text samples
   - Build a prompt cost calculator for your use cases
   - Optimize prompts to reduce token usage

3. **Hour 4:** Understand economics:
   - Calculate costs for your projects
   - Compare pricing across models and providers
   - Build a budget tracker for your API usage

**Ask Me To:**
- Explain token efficiency techniques
- Help optimize your prompts
- Show you how to estimate costs before running
- Debug token counting issues

**Exit Goal:** You deeply understand tokens, can optimize prompts, predict and control costs

---

### Day 4: Prompt Engineering & Structured Output
**Duration:** 4 hours  
**Method:** Interactive experimentation

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - Few-shot prompting examples
   - Chain-of-thought prompting
   - JSON mode and structured outputs
   - Pydantic validation

2. **Hour 2-4:** Build together:
   - Create prompts that force JSON output
   - Build a Pydantic schema for structured data
   - Test JSON validation
   - Experiment: ask me how to improve accuracy

**Prompts to Try:**
- Get LLM to output valid JSON
- Extract structured data from unstructured text
- Get consistent output format every time

**Ask Me To:**
- Show you prompt patterns that work
- Help debug when JSON is invalid
- Explain Pydantic and why it matters
- Show you error handling for bad outputs

**Exit Goal:** You can reliably get structured JSON from LLMs, validate it with Pydantic

---

### Day 5: Project 1 - AI Brochure Generator
**Duration:** 4 hours  
**Method:** Guided project building with Copilot

**Project Overview:**
Build an AI agent that:
- Takes a company URL or name as input
- Scrapes/researches the company
- Generates a professional sales brochure in JSON format
- Outputs formatted brochure

**What You'll Do:**
1. **Hour 1:** Design with me:
   - Ask me: "How should I structure this project?"
   - Discuss the flow: input → scrape → generate → validate → output
   - Design data structures with Pydantic

2. **Hour 2-3:** Build the pieces:
   - Web scraping (BeautifulSoup or requests)
   - Multiple LLM calls (research → brochure generation)
   - Pydantic validation for output
   - Error handling

3. **Hour 4:** Test and refine:
   - Test with real companies
   - Ask me how to improve output quality
   - Ensure JSON is always valid

**Ask Me To:**
- Help with web scraping
- Show you how to chain multiple API calls
- Debug validation errors
- Improve the brochure generation prompts
- Create a nice output format (JSON → Markdown or HTML)

**Exit Goal:** Working AI Brochure Generator app. Pass 3 test companies.

---

## Week 2: Multi-Modal & Function Calling (Days 6-8)

### Day 6: Function Calling & Tool Use
**Duration:** 4 hours  
**Method:** Interactive learning by building

**What You'll Do:**
1. **Hour 1:** Ask me to explain:
   - What is function calling in LLMs?
   - How do tools/functions work in OpenAI API?
   - Difference between tool_choice="auto" vs required
   - When and why to use function calling

2. **Hour 2-3:** Build a tool system:
   - Define tool schemas (function definitions)
   - Implement actual functions to call
   - Parse LLM outputs and call functions
   - Handle both tool calls and text responses

3. **Hour 4:** Test and iterate:
   - Create 3-5 sample tools
   - Ask me how to improve tool definition clarity
   - Test edge cases

**Tools to Build:**
- Calculator
- Web search
- Database query
- API call wrapper

**Ask Me To:**
- Show you how to design good tool schemas
- Help debug function calling issues
- Explain how LLMs "decide" which tool to use
- Optimize tool definitions for better decisions

**Exit Goal:** You can define tools, parse function calls, and execute them. Understand why function calling enables agents.

---

### Day 7: Project 2 - Multi-Modal Customer Support Agent
**Duration:** 4 hours  
**Method:** Guided project with interactive debugging

**Project Overview:**
Build an airline customer support agent that:
- Accepts text, image, and audio inputs
- Uses vision for ticket uploads, flight confirmations
- Processes audio for voice complaints
- Uses function calling for: booking lookup, refund processing, policy queries
- Returns human-like responses with actions

**What You'll Do:**
1. **Hour 1:** Design with me:
   - Define tool set (search_booking, process_refund, lookup_policy, etc.)
   - Design system prompt for airline support personality
   - Plan input/output flow

2. **Hour 2-3:** Build piece by piece:
   - Image processing (GPT-4 Vision)
   - Audio transcription (Whisper or built-in)
   - Text processing with function calling
   - Orchestrate all three input types

3. **Hour 4:** Create UI:
   - Simple Gradio interface or Flask API
   - Test with sample scenarios

**Ask Me To:**
- Show you how to handle multiple input types
- Help integrate Whisper for audio
- Debug multi-modal processing
- Build the function definitions for airline operations
- Create realistic test scenarios

**Exit Goal:** Fully functional multi-modal support agent. Process text, image, and audio correctly.

---

### Day 8: Open-Source Models & HuggingFace Ecosystem
**Duration:** 4 hours  
**Method:** Interactive exploration and comparison

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - Open-source model landscape (LLaMA, Mistral, DeepSeek, etc.)
   - When to use open-source vs frontier models
   - Running models locally vs via services
   - Hugging Face hub and model discovery

2. **Hour 2-3:** Get hands-on:
   - Load 2-3 open-source models from HuggingFace
   - Run them locally (via Ollama or transformers)
   - Build a comparison benchmark
   - Test on same prompts as Day 2

3. **Hour 4:** Integration:
   - Modify your brochure generator to support open-source models
   - Compare cost vs quality

**Models to Try:**
- LLaMA 2/3
- Mistral (7B, 8x7B)
- DeepSeek models
- Local Ollama models

**Ask Me To:**
- Show you how to load models from HuggingFace
- Help compare outputs vs GPT-4
- Explain model quantization and optimization
- Help with memory/speed optimization for larger models
- Build a model loader abstraction

**Exit Goal:** Can load and run open-source models, understand tradeoffs, integrate into your apps.

---

## Week 3: Code Generation & Audio Processing (Days 9-11)

### Day 9: Code Generation with LLMs
**Duration:** 4 hours  
**Method:** Interactive building and learning

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - How do LLMs generate code?
   - Prompt patterns for code generation
   - Testing and validating generated code
   - Using code models (Codex, Code Llama)

2. **Hour 2-4:** Build a code generator:
   - Create a system that generates Python code from descriptions
   - Add code validation/execution
   - Build test suite for generated code
   - Compare frontier vs open-source code models

**Features to Add:**
- Syntax validation
- Execution testing in sandbox
- Code quality checks
- Refactoring suggestions

**Ask Me To:**
- Show prompt patterns for better code
- Help validate generated code safely
- Debug code generation issues
- Explain why some models are better at code
- Build a code evaluation framework

**Exit Goal:** Working code generator that can create valid, testable Python code from prompts.

---

### Day 10: Project 4 - Python to C++ Optimizer
**Duration:** 4 hours  
**Method:** Guided challenging project

**Project Overview:**
Build an AI-assisted code optimizer that:
- Takes Python code as input
- Uses LLM to suggest C++ equivalent
- Benchmarks performance improvement
- Validates correctness
- Explains optimizations made

**What You'll Do:**
1. **Hour 1:** Plan with me:
   - Discuss prompting strategy for C++ conversion
   - Design validation approach
   - Plan benchmarking methodology

2. **Hour 2-3:** Build:
   - Create prompts for code conversion
   - Implement code validation (syntax, logic)
   - Build benchmarking harness
   - Compare Python vs C++ performance

3. **Hour 4:** Evaluation:
   - Test on algorithmic problems
   - Measure performance improvement
   - Document conversion quality

**Sample Code to Convert:**
- Fibonacci calculation
- List sorting
- Matrix multiplication
- Search algorithms

**Ask Me To:**
- Help design good prompts for conversion
- Show how to validate C++ code
- Help benchmark and measure improvement
- Debug generated C++ code
- Explain performance differences

**Exit Goal:** Successfully convert and optimize Python to C++, achieving measurable speedup.

---

### Day 11: Project 3 - Audio to Meeting Minutes
**Duration:** 4 hours  
**Method:** Multi-step interactive building

**Project Overview:**
Build a tool that:
- Accepts audio file (or live recording)
- Transcribes to text
- Extracts key points and decisions
- Generates action items with owners and deadlines
- Compares open-source vs frontier models

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - Audio transcription (Whisper, APIs)
   - Prompt design for extracting key points
   - Action item identification strategies
   - Markdown formatting

2. **Hour 2-3:** Build the pipeline:
   - Audio transcription (local Whisper or API)
   - LLM processing for extraction
   - Pydantic models for structured output
   - Test with real meeting recordings

3. **Hour 4:** Polish:
   - Handle different audio qualities
   - Compare model outputs (GPT-4 vs open-source)
   - Test accuracy on sample meetings

**Example Formats:**
```
# Meeting Minutes
**Date:** 2024-01-15
**Attendees:** Alice, Bob, Carol

## Key Decisions
- Decision 1: Move to Cloud migration
- Decision 2: Increase budget for Q2

## Action Items
- [ ] Alice: Prepare cloud migration plan (2/15)
- [ ] Bob: Setup test environment (2/10)
```

**Ask Me To:**
- Help with audio processing
- Show transcription services comparison
- Debug LLM extraction accuracy
- Help design Pydantic models
- Optimize prompt for better extraction
- Compare outputs across models

**Exit Goal:** Fully working meeting minutes tool. Process real audio, extract accurate action items.

---

## Week 4: RAG Mastery (Days 12-15)

### Day 12: Vector Embeddings & Semantic Search
**Duration:** 4 hours  
**Method:** Interactive experimentation with Copilot

**What You'll Do:**
1. **Hour 1:** Ask me to explain:
   - What are embeddings? How do they encode meaning?
   - Semantic search vs keyword search
   - Cosine similarity and distance metrics
   - Vector databases (Pinecone, Qdrant, Weaviate, etc.)

2. **Hour 2-3:** Build and experiment:
   - Generate embeddings for text samples (using OpenAI API)
   - Build a simple similarity search
   - Test with different embedding models
   - Compare embedding quality

3. **Hour 4:** Optimize:
   - Batch embedding operations
   - Understand dimensionality
   - Compare cost of different embedding models

**Ask Me To:**
- Explain how embeddings capture meaning
- Show you different embedding models
- Help choose the right embedding model
- Build efficient similarity search
- Optimize for speed and cost
- Debug semantic search accuracy issues

**Technologies to Try:**
- OpenAI Embeddings API
- Hugging Face embeddings
- FAISS for local similarity search
- Simple Pinecone demo

**Exit Goal:** Understand embeddings deeply. Build working semantic search that finds relevant documents.

---

### Day 13: Building RAG Backend & Retrieval Strategies
**Duration:** 4 hours  
**Method:** Hands-on with architectural guidance

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - RAG pipeline architecture
   - Retrieval strategies (BM25, semantic, hybrid)
   - Ranking and reranking
   - Chunking strategies for documents

2. **Hour 2-3:** Build the pieces:
   - Set up vector database (local Qdrant or Chroma)
   - Implement document chunking
   - Build hybrid search (keyword + semantic)
   - Add ranking/reranking layer

3. **Hour 4:** Optimize:
   - Test retrieval quality on sample queries
   - Measure recall and precision
   - Optimize chunk size and chunk overlap

**Ask Me To:**
- Show different retrieval strategies
- Help design document chunks
- Debug retrieval quality issues
- Explain when to use hybrid vs pure semantic
- Build a reranker layer
- Optimize for speed/quality tradeoff

**Vector Databases to Explore:**
- Chroma (simple, local)
- Qdrant (scalable, feature-rich)
- Pinecone (managed, easy)
- Weaviate (open source)

**Exit Goal:** Working RAG backend that retrieves relevant context accurately. Understand retrieval quality metrics.

---

### Day 14: Project 5 - RAG Knowledge Worker (Salesforce Data Guru)
**Duration:** 4 hours  
**Method:** Full RAG pipeline building with guidance

**Project Overview:**
Build an AI system that:
- Ingests Salesforce-like data (customers, deals, products)
- Creates embeddings for all data
- Retrieves relevant context for queries
- Generates accurate answers without hallucinations
- Validates answers against source data

**What You'll Do:**
1. **Hour 1:** Design with me:
   - Data structure for Salesforce mock data
   - Chunking and embedding strategy
   - RAG prompt design
   - Quality metrics

2. **Hour 2-3:** Build the system:
   - Create sample Salesforce data (CSV/JSON)
   - Implement data ingestion and chunking
   - Build embeddings pipeline
   - Implement RAG query answering
   - Add source citation

3. **Hour 4:** Validate:
   - Test with realistic Salesforce queries
   - Verify no hallucinations
   - Cite sources for all answers
   - Measure retrieval quality

**Sample Queries to Handle:**
- "What's the largest deal in progress?"
- "List all customers from NYC"
- "What's our product strategy for Enterprise?"
- "Which customers have churn risk?"

**Ask Me To:**
- Help design the data ingestion
- Debug retrieval issues
- Improve answer quality
- Add filtering/metadata-based retrieval
- Build evaluation metrics for accuracy
- Show how to handle fuzzy matching
- Debug hallucination problems

**Exit Goal:** RAG system that accurately answers business questions without hallucinations. All answers cite sources.

---

### Day 15: Advanced RAG & LangChain LCEL
**Duration:** 4 hours  
**Method:** Interactive refactoring and optimization

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - LangChain Expression Language (LCEL)
   - Composing AI pipelines
   - Async/streaming in chains
   - Error handling in RAG systems

2. **Hour 2-3:** Refactor your RAG system:
   - Rebuild Salesforce Data Guru using LCEL
   - Make it async for better performance
   - Add streaming responses
   - Improve error handling

3. **Hour 4:** Advanced techniques:
   - Multi-step retrieval
   - Query decomposition
   - Result filtering and ranking
   - Batch processing

**Advanced Features to Add:**
- Multi-turn conversation memory
- Query refinement (ask for clarification)
- Filter results before ranking
- Combine multiple retrieval methods
- Streaming responses
- Request timeout handling

**Ask Me To:**
- Show LCEL chain patterns
- Help build async pipelines
- Debug chain composition issues
- Explain when to use different chain types
- Optimize for latency
- Handle errors gracefully
- Show streaming implementation

**Exit Goal:** Advanced RAG system using LCEL. Handles complex queries, streaming, async processing. Production-ready error handling.

---

## Week 5: Fine-Tuning & Optimization (Days 16-18)

### Day 16: Fine-Tuning Fundamentals
**Duration:** 4 hours  
**Method:** Interactive learning and preparation

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - When should you fine-tune vs use RAG vs few-shot?
   - Fine-tuning mechanics (what actually changes)
   - Training data requirements
   - Cost and performance tradeoffs

2. **Hour 2-3:** Prepare for fine-tuning:
   - Design training data format
   - Create sample dataset (price prediction use case)
   - Split train/validation/test sets
   - Understand evaluation metrics

3. **Hour 4:** Explore options:
   - OpenAI fine-tuning API
   - HuggingFace fine-tuning
   - LoRA and QLoRA efficient methods
   - When to use each approach

**Ask Me To:**
- Explain the fine-tuning process
- Help design training data
- Show data formatting requirements
- Explain overfitting and prevention
- Build evaluation scripts
- Suggest optimizer and learning rate
- Explain inference optimization

**Use Case: E-commerce Price Prediction**
- Input: product description, category, sales history
- Output: predicted price
- Goal: Improve accuracy over frontier model

**Exit Goal:** Deep understanding of fine-tuning. Training dataset prepared and validated. Ready to fine-tune.

---

### Day 17: Project 6 - Fine-Tune Frontier Model for Price Prediction
**Duration:** 4 hours  
**Method:** Guided fine-tuning with monitoring

**Project Overview:**
Build a specialized price prediction model by:
- Creating comprehensive training dataset
- Fine-tuning GPT-4 or Claude on price data
- Validating on holdout test set
- Comparing to base model

**What You'll Do:**
1. **Hour 1:** Data preparation:
   - Generate/gather e-commerce product data
   - Format for fine-tuning (OpenAI JSONL format or similar)
   - Split into train/validation/test
   - Analyze data quality

2. **Hour 2-3:** Fine-tuning:
   - Submit fine-tuning job to OpenAI (or equivalent)
   - Monitor training progress
   - Validate on validation set
   - Create inference script

3. **Hour 4:** Evaluation:
   - Test on holdout set
   - Compare accuracy vs base model
   - Calculate pricing errors (MAE, RMSE)
   - Document improvements

**Sample Training Data (JSONL):**
```json
{"prompt": "Product: iPhone 15Pro\nCategory: Electronics\nRam: 8GB\nStorage: 256GB\n\nPrice estimation:", "completion": " $999"}
{"prompt": "Product: Winter Jacket\nCategory: Clothing\nBrand: Nike\nSize: M\n\nPrice estimation:", "completion": " $149"}
```

**Ask Me To:**
- Help prepare training data correctly
- Show how to format for fine-tuning
- Monitor and debug training
- Help evaluate model quality
- Compare costs vs performance
- Adjust hyperparameters
- Handle overfitting

**Exit Goal:** Fine-tuned frontier model that predicts prices accurately. Outperforms base model on your specific task.

---

### Day 18: Project 7 - Fine-Tune Open-Source Model with QLoRA
**Duration:** 4 hours  
**Method:** Hands-on efficient training with Copilot guidance

**Project Overview:**
Fine-tune an open-source model on same price prediction task:
- Use same training data as Day 17
- Apply QLoRA for memory-efficient training
- Compare cost and performance vs frontier model
- Show you can compete with large models

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - QLoRA: what it is and why it matters
   - Parameter-efficient fine-tuning
   - Memory optimization
   - Inference speed tradeoffs

2. **Hour 2-3:** Fine-tune:
   - Load open-source model (LLaMA, Mistral)
   - Apply QLoRA with HuggingFace/PEFT
   - Train on same price prediction data
   - Monitor training metrics

3. **Hour 4:** Compare:
   - Evaluate on test set
   - Compare accuracy: fine-tuned frontier vs fine-tuned open-source
   - Calculate total cost (training + inference)
   - Analyze speed and latency

**Technical Stack:**
```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
# QLoRA with 4-bit quantization for efficiency
```

**Key Metrics to Compare:**
| Metric | Frontier (Day 17) | Open-Source (Day 18) |
|--------|---|---|
| Accuracy on test set | ? | ? |
| Training cost | ? | ? |
| Inference cost per call | ? | ? |
| Latency (ms) | ? | ? |
| Total cost to deploy | ? | ? |

**Ask Me To:**
- Explain QLoRA in detail
- Help implement LoRA adapters
- Debug training issues
- Optimize memory usage
- Show inference optimizations
- Compare models fairly
- Analyze cost vs performance

**Exit Goal:** Fine-tuned open-source model that's competitive with frontier model. You understand efficient fine-tuning techniques. Know when to use QLoRA vs full fine-tuning.

---

## Week 6: Agents & Production Deployment (Days 19-21)

### Day 19: Agent Architecture & LangGraph
**Duration:** 4 hours  
**Method:** Building understanding through implementation

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - Agent loops: observation-action-thought cycles
   - State machines and decision trees
   - LangGraph framework fundamentals
   - Tool definition and routing

2. **Hour 2-3:** Build a simple agent:
   - Create agent state definition
   - Define tools (calculator, web search, API calls)
   - Build agent loop with conditional branching
   - Implement tool execution

3. **Hour 4:** Advanced patterns:
   - Streaming agent outputs
   - Error handling in loops
   - Memory and context management
   - Testing agent behavior

**Sample Tools to Build:**
- Calculator (math operations)
- Web search simulator
- Database lookup
- File operations
- Weather API

**Ask Me To:**
- Explain LangGraph concepts
- Show agent patterns and examples
- Help design state schemas
- Debug agent decision logic
- Build tool schemas
- Handle streaming and errors
- Show memory patterns

**Exit Goal:** Understand agents deeply. Build working agent with 3+ tools. Understand control flow and routing.

---

### Day 20: Project 8 - Junior Developer Pod (Multi-Agent System)
**Duration:** 4 hours  
**Method:** Complex orchestration with Copilot guidance

**Project Overview:**
Build a multi-agent team that collaborates to deliver features:
- **PM Agent:** Analyzes requirements, creates specifications
- **Dev Agent:** Writes code based on specs
- **QA Agent:** Tests code and reports issues
- **Manager Agent:** Coordinates work and makes decisions

**What You'll Do:**
1. **Hour 1:** Design with me:
   - Agent roles and responsibilities
   - Communication protocol between agents
   - State definitions for coordination
   - Success criteria for feature delivery

2. **Hour 2-3:** Build the team:
   - Create each agent personality with system prompts
   - Define tools each agent can use (Git, execution, testing)
   - Implement manager/supervisor logic
   - Build agent communication protocol

3. **Hour 4:** Test collaboration:
   - Give team a feature requirement
   - Watch agents coordinate
   - Debug coordination issues
   - Measure success (code quality, test coverage)

**Feature to Build (Example):**
```
Requirement: Build user authentication system
- Login with email/password
- Password reset flow
- Session management
- Security best practices
```

**Agent Tools:**
- PM Agent: semantic search for similar requirements, create specifications
- Dev Agent: code generation, syntax checking, Git operations
- QA Agent: test generation, test execution, bug reporting
- Manager: task assignment, priority setting, final approval

**Ask Me To:**
- Help design agent personalities
- Show agent communication patterns
- Debug multi-agent issues
- Build effective prompts for each agent
- Implement tool calling for agents
- Handle conflicts between agents
- Optimize team workflow

**Exit Goal:** Working multi-agent system. Team successfully takes a requirement from specification to tested, working code. Agents collaborate effectively.

---

### Day 21: Production Deployment & Monitoring
**Duration:** 4 hours  
**Method:** End-to-end deployment with Copilot support

**What You'll Do:**
1. **Hour 1:** Ask me about:
   - Deployment strategies (Docker, serverless, cloud)
   - API design for agents
   - Scaling considerations
   - Monitoring and observability

2. **Hour 2-3:** Deploy the Junior Developer Pod:
   - Create REST API endpoints for each agent
   - Set up Docker containerization
   - Deploy to Azure/cloud (free tier)
   - Configure logging and monitoring

3. **Hour 4:** Production hardening:
   - Add rate limiting
   - Implement error handling
   - Set up LangSmith observability
   - Test end-to-end workflow
   - Create usage documentation

**Deployment Architecture:**
```
Junior Developer Pod API
├── /requirements (POST)
├── /status (GET)
├── /code (GET)
├── /tests (GET)
└── /logs (GET)

Backend:
├── PM Agent service
├── Dev Agent service
├── QA Agent service
├── Manager service
└── Shared vector DB (for context)
```

**Technologies:**
- FastAPI for REST API
- Docker for containerization
- Azure Container Instances or similar
- LangSmith for tracing
- Prometheus/Grafana for metrics (optional)

**Ask Me To:**
- Help design API contracts
- Show Docker Compose setup
- Deploy to Azure
- Set up monitoring
- Debug deployment issues
- Implement health checks
- Create API documentation
- Optimize for production performance

**Exit Goal:** Fully deployed production system. Multi-agent Junior Developer Pod accessible via API. Full observability and monitoring. Ready to demo or use in production.

---

## Summary by Phase

| Phase | Days | Focus | Key Projects | Primary Learning |
|-------|------|-------|--------------|------------------|
| **Phase 1: Foundations** | 1-5 | APIs, Models, Tokenization, Prompting | Brochure Generator | Copilot explanations + hands-on coding |
| **Phase 2: Multi-Modal + Functions** | 6-8 | Function Calling, Multi-Modal, Open-Source | Support Agent, Audio Tool | Building real systems with guidance |
| **Phase 3: Code Gen + Audio** | 9-11 | Code Generation, Audio Processing | Code Optimizer, Meeting Minutes | Debugging and optimization support |
| **Phase 4: RAG Systems** | 12-15 | Embeddings, Retrieval, LCEL | Salesforce Data Guru | Architectural guidance and troubleshooting |
| **Phase 5: Fine-Tuning** | 16-18 | Fine-tuning, QLoRA, Efficiency | Price Prediction Models | Training and optimization assistance |
| **Phase 6: Agents & Deployment** | 19-21 | Agent Loops, Orchestration, Deployment | Developer Pod, Production API | Complex system design and deployment help |

---

## Daily Routine (4 Hours)

### Typical Day Structure:

**Hour 1: Learning & Design**
- Ask me to explain a core concept
- Discuss architecture for the day's task
- Review patterns and best practices
- Ask questions until clear

**Hour 2-3: Implementation**
- Build code together with my guidance
- Ask me for help with issues
- Test incrementally
- Refactor and optimize

**Hour 4: Polish & Reflect**
- Debug any remaining issues
- Document what you learned
- Prepare questions for next day
- Commit working code

### Interaction Model:
- **You:** Ask me to explain concepts, show patterns, help debug
- **Me:** Provide explanations, code examples, architectural guidance, debugging help
- **Together:** Build real projects that work

---

## Tips for Success with Interactive Learning

✅ **Ask questions:**
- "Why does this work this way?"
- "What would happen if...?"
- "Can you explain this pattern?"
- "How would you solve this differently?"

✅ **Show your work:**
- Share code snippets when stuck
- Tell me what you tried
- Describe the error you're seeing
- Ask specific questions, not vague ones

✅ **Build, don't just watch:**
- Code along as I explain
- Make mistakes and fix them together
- Experiment with variations
- Test edge cases

✅ **Document learning:**
- Keep notes on what you learned
- Document patterns you discovered
- Create reusable code templates
- Record gotchas and solutions

---

## Success Metrics

- [ ] Day 5: Brochure Generator working - you understand API calls, chaining, JSON
- [ ] Day 8: Multi-source model loading - you can use frontier + open-source
- [ ] Day 11: Audio processing tool - you handle multiple input modalities
- [ ] Day 15: RAG system retrieves accurate context - you understand embeddings
- [ ] Day 18: Fine-tuned model competitive - you know cost/performance tradeoffs
- [ ] Day 21: Deployed multi-agent system - you understand production AI systems

---

## Getting Help

When you get stuck:
1. **Ask me for explanation:** "Explain how function calling works"
2. **Show me code:** Paste your code and error message
3. **Ask for patterns:** "Show me the pattern for handling this"
4. **Request debugging:** "Help me debug why this is failing"
5. **Discuss alternatives:** "What's another way to approach this?"

I'm here to be your AI mentor and coding partner throughout this journey!

