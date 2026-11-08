# Lecture 3 Answer

## Exercises

### 1. How the Lecture 1 (plain LLM) answer differs from the agent's

In Lecture 1, I observed that the plain LLM sometimes provided general knowledge instead of course-specific information.

For example, when I asked **"What is LoRA?"**, the model incorrectly interpreted LoRA as *Long Range*, a wireless communication technology used in IoT. It did not identify the course-specific meaning, Low-Rank Adaptation.

In Lecture 3, the agent has access to tools that allow it to retrieve information from the AIE2026 glossary and lecture summaries. Instead of relying only on its general knowledge, it can use the relevant course materials.

For example, when I requested a review question from Lecture 2, the agent called `make_quiz` and selected PEFT from the Lecture 2 glossary. The returned definition described PEFT as a method of fine-tuning that trains only a small number of additional or selected parameters rather than all model parameters.

The agent then presented the question without revealing the answer in its final response.

**Observation:** The agent provides a more course-oriented approach because it can retrieve information from the course glossary through tools. This helps address the limitations I observed with the plain LLM in Lecture 1.

### 2. Tool calls observed with `--trace`

I ran the following command:

```bash
uv run python -m app.agent --trace "Give me one review question from Lecture 02"
```

The trace showed the following tool call:

| Tool name | Arguments | Purpose |
|---|---|---|
| `make_quiz` | `{'lecture': 2}` | Generates a review question using a term from the Lecture 2 glossary. |

The tool returned a question about PEFT together with its definition.

I also ran:

```bash
uv run python -m app.agent --list-tools
```

This confirmed that three tools were available to the agent:

- `search_glossary`
- `get_lecture_summary`
- `make_quiz`

### 3. Number of LLM calls for one question

According to the trace output:

- **LLM requests:** 2
- **Tool calls:** 1
- **Input tokens:** 909
- **Output tokens:** 66
- **Cost:** $0.0004377

The two requests represent the model's tool-selection process and its subsequent response after receiving the tool result.

The sequence was:

1. The user submitted a request for a review question.
2. The model selected the `make_quiz` tool.
3. The tool retrieved a random term and its definition from the Lecture 2 glossary.
4. The model generated the final response and presented the question to the user.

### 4. Tool added and its docstring description

I implemented a tool called `make_quiz` in `app/tools.py` and registered it with the agent using:

```python
agent.tool_plain(tools.make_quiz)
```

The tool generates one question from the glossary of a specified lecture and returns its answer.

Its docstring description was:

> Generate one question from the glossary of the specified lecture and return its answer.
>
> This function is used when you want learners to review terminology from a particular lecture or when creating a quiz to test their understanding.
>
> The lecture parameter specifies the target lecture (a positive integer starting from 1).

The tool accepts a lecture number as an argument, selects a random glossary entry belonging to that lecture, and generates a question using the selected term and its definition.

### 5. Testing

I ran the test suite using:

```bash
uv run pytest -q
```

Result:

```text
17 passed in 5.82s
```

All 17 tests passed successfully.

---

## Homework

### Level 1: Basic

**What I did**

I rewrote the `INSTRUCTIONS` in `app/agent.py` and the tool docstrings in `app/tools.py` to improve how the agent understands and uses its tools.

I updated the instructions so that:

- The agent responds concisely in the user's language.
- It searches the glossary before answering questions about course terminology.
- It uses `get_lecture_summary` when asked about lecture content.
- It uses `make_quiz` when a learner requests a review question.
- It presents only the question unless the learner explicitly asks for the answer.
- It does not invent information that is missing from the course materials.

**Same question used before and after the changes**

```bash
uv run python -m app.agent --trace "Give me one review question from Lecture 02"
```

**Before the changes**

- Tool call: `make_quiz({'lecture': 2})`
- Number of tool calls: 1
- The agent selected PEFT and presented the question. Its final response also included the definition as an answer hint.
- LLM requests: `2`
- Input tokens: `909`
- Output tokens: `66`
- Cost: `$0.0004377`

**After the changes**

- Tool call: `make_quiz({'lecture': 2})`
- Number of tool calls: 1
- The agent selected Quantization and presented only the question without revealing the definition.
- LLM requests: `2`
- Input tokens: `1104`
- Output tokens: `32`
- Cost: `$0.0004112`

**Comparison and observations**

| Metric | Before | After |
|---|---:|---:|
| Tool calls | 1 | 1 |
| LLM requests | 2 | 2 |
| Input tokens | 909 | 1104 |
| Output tokens | 66 | 32 |
| Cost | $0.0004377 | $0.0004112 |

The tool selection and arguments remained unchanged. However, the selected question changed from PEFT to Quantization because `make_quiz` randomly selects a glossary entry.

The updated instructions helped the agent withhold the answer unless explicitly requested. The final response also became shorter.

One observation is that the input token count increased even though the output token count decreased. This is likely related to the longer instructions and tool descriptions supplied to the model.

**Testing**

```bash
uv run pytest -q
```

Result:

```text
17 passed in 5.82s
```

All 17 tests passed.

---

### Level 2: Implementation

**Objective**

Implement a `save_learning_log` tool that allows the agent to save learning records in the `learning_log/` directory. Since saving records is a potentially irreversible action, the agent must request user approval before executing the tool.

**What I implemented**

I created the `save_learning_log` function in `app/tools.py`.

The function:

- Accepts a learning record as a string.
- Checks that the record is not empty.
- Creates the `learning_log/` directory if it does not exist.
- Adds a timestamp to the record.
- Appends the record to `learning_log/learning_log.md`.

I registered the tool in `app/agent.py` using:

```python
agent.tool_plain(
    tools.save_learning_log,
    requires_approval=True
)
```

I also included `DeferredToolRequests` in the agent's output type:

```python
agent = Agent(
    instructions=INSTRUCTIONS,
    output_type=[str, DeferredToolRequests]
)
```

**Approval workflow**

I implemented a CLI approval mechanism that:

1. Detects when the agent returns `DeferredToolRequests`.
2. Displays the requested tool and its arguments.
3. Asks the user to approve or reject the operation.
4. Passes the approval decision back to the agent.
5. Resumes execution if approval is granted.

**Testing the tool**

I first checked the available tools:

```bash
uv run python -m app.agent --list-tools
```

The output confirmed that four tools were available:

- `search_glossary`
- `get_lecture_summary`
- `make_quiz`
- `save_learning_log`

I then tested the learning record tool using:

```bash
uv run python -m app.agent --trace "Save this learning record: Today I learned how AI agents use tools and how approval is required before executing sensitive actions."
```

The CLI displayed the approval prompt:

```text
Approve save_learning_log with arguments {'record': 'Today I learned how AI agents use tools and how approval is required before executing sensitive actions.'}? [y/N]:
```

I entered `y` to approve the operation.

The trace confirmed that the tool was called successfully:

```text
[tool call] save_learning_log({'record': 'Today I learned how AI agents use tools and how approval is required before executing sensitive actions.'})
[tool return] save_learning_log -> 学習記録を learning_log/learning_log.md に保存しました。
```

**Verifying the saved record**

I used:

```bash
cat learning_log/learning_log.md
```

The file contained:

```text
## 2026-11-08T16:01:11+00:00

Today I learned how AI agents use tools and how approval is required before executing sensitive actions.
```

This confirmed that the record was successfully saved with a timestamp.

**Final testing**

I ran:

```bash
uv run pytest -q
```

Result:

```text
21 passed in 4.85s
```

All 21 tests passed successfully.

**Observation**

This exercise demonstrated how approval-required tools can introduce human oversight into an AI agent's workflow.

Instead of allowing the model to execute a potentially irreversible operation immediately, Pydantic AI pauses execution and returns a deferred tool request. The CLI then collects the user's approval before allowing the operation to continue.

---

### Level 3: Advanced

**Option (a): Reimplementing the agent using Google's Agent Development Kit (ADK)**

**Objective**

Use the same instructions and tools as the original Pydantic AI agent, rewrite the agent-building section using Google's ADK, run it with `adk run`, and compare the implementations and their responses.

#### 1. Setting up Google ADK

I installed Google ADK in the existing project using:

```bash
uv add google-adk
```

I then created a separate `adk_agent/` package containing:

- `adk_agent/__init__.py`
- `adk_agent/agent.py`

I configured the Google API key for ADK and launched the agent using:

```bash
uv run adk run adk_agent
```

#### 2. Agent implementation

I reused the existing instructions from `app/agent.py` and the tool implementations from `app/tools.py`.

The ADK agent was configured as follows:

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from app import tools

root_agent = Agent(
    name="aie2026_learning_agent",
    model="gemini-3.5-flash-lite",
    description="AIE2026 learning support agent",
    instruction=INSTRUCTIONS,
    tools=[
        tools.search_glossary,
        tools.get_lecture_summary,
        tools.make_quiz,
        FunctionTool(
            tools.save_learning_log,
            require_confirmation=True,
        ),
    ],
)
```

The same four tools were registered:

- `search_glossary`
- `get_lecture_summary`
- `make_quiz`
- `save_learning_log`

The `save_learning_log` function was wrapped in `FunctionTool` with `require_confirmation=True` to require user approval before execution.

#### 3. Testing the ADK agent

**Test 1: Review question generation**

I asked:

```text
Give me one review question from Lecture 02
```

The agent returned:

```text
第2回からの復習問題です：

「ランク（LoRAのr）」とは何ですか？
```

The question was about the rank (r) in LoRA.

**Test 2: Glossary lookup**

I asked:

```text
What is LoRA?
```

The agent correctly identified LoRA as Low-Rank Adaptation, a PEFT technique.

It explained that the pretrained model weights remain frozen while the weight updates are represented using the product of two smaller low-rank matrices. It also explained the benefits in terms of reduced training parameters, computational cost and memory usage.

The agent identified Lecture 02 as the related lecture.

**Test 3: Learning-log approval**

I submitted:

```text
Save this learning record: Today I learned how LoRA uses low-rank matrices for parameter-efficient fine-tuning.
```

ADK paused execution and displayed:

```text
[HITL confirm] Please approve or reject the tool call save_learning_log() by responding with a FunctionResponse with an expected ToolConfirmation payload.
Type "yes" to confirm, anything else to reject.
```

I entered:

```text
yes
```

The agent then confirmed:

```text
学習記録を保存しました。
```

This demonstrated that ADK's human-in-the-loop confirmation mechanism was working.

#### 4. Verifying the saved learning record

I exited the ADK chat and ran the following command in the terminal:

```bash
cat learning_log/learning_log.md
```

The file contained both learning records:

```text
## 2026-11-08T16:01:11+00:00

Today I learned how AI agents use tools and how approval is required before executing sensitive actions.

## 2026-11-08T16:27:30+00:00

Today I learned how LoRA uses low-rank matrices for parameter-efficient fine-tuning.
```

This confirmed that the ADK agent successfully appended the second record to the same learning-log file after receiving approval.

#### 5. Comparison of Pydantic AI and Google ADK

| Aspect | Pydantic AI | Google ADK |
|---|---|---|
| Agent creation | `Agent()` | `Agent()` |
| Instruction parameter | `instructions` | `instruction` |
| Tool registration | Individual registration using `tool_plain()` | Tools supplied through a list |
| Model configuration | Configured through the Pydantic AI provider/model setup | Specified in the `Agent` constructor |
| Tool approval | `requires_approval=True` | `require_confirmation=True` |
| Approval handling | `DeferredToolRequests` and custom CLI handling | Built-in ADK confirmation flow |
| Execution | Custom Python CLI | `adk run` |

#### 6. Observations and conclusion

Both frameworks successfully implemented the AIE2026 learning support agent using the same instructions and existing tool functions.

Both agents were able to:

- Generate course-specific review questions.
- Retrieve course terminology through glossary lookup.
- Save learning records to the same Markdown file.
- Require user approval before executing the learning-log tool.

The main difference I observed was in how the frameworks handle agent construction, tool registration and approval workflows.

With Pydantic AI, I had to implement explicit deferred-tool handling and a custom CLI approval mechanism using `DeferredToolRequests`.

With Google ADK, I used `FunctionTool` with `require_confirmation=True`, and the ADK interactive runner handled the confirmation interaction.

This exercise helped me understand that different agent frameworks can provide similar capabilities while exposing different abstractions and execution workflows. It also demonstrated the importance of reusing existing tools and instructions when comparing agent frameworks.git branch --show-current