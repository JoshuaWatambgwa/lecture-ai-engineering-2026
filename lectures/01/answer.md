# Lecture 1 Answer

## Exercise

- Model response to a course-specific question (homework level 3) (summary is fine):
Q1: “What is the definition of LLM Fundamental as defined in lecture 1?”

Model response: The model gave a general explanation of LLM fundamentals, covering next-token prediction, Transformers, tokenization, pretraining, and fine-tuning. It admitted it did not know the specific course.

Comparison with glossary: The answer did not provide the course-specific definition. The glossary defines an LLM as a model trained on large amounts of text that predicts the next token from its input and generates text. It can perform tasks such as question answering, summarization, and code generation by changing the prompt.

Input/output tokens: 15 / 458.

Q2:“What is LoRA?”
Model response: The model incorrectly interpreted LoRA as Long Range, a wireless communication technology used in IoT.

Comparison with glossary: The glossary defines LoRA (Low-Rank Adaptation) as a parameter-efficient fine-tuning method that keeps pretrained model weights fixed while training two small matrices to adapt the model. The response was unrelated to the course's intended meaning.

Input/output tokens: 5 / 816.

## Homework

## Level attempted: Basic 

What I did:
- Asked the same question, “What is the definition of AI engineering according to the AIE2026 course?”, twice times  using gemini-3.5-flash-lite.
- Tried switching to gemini-3.8-flash to compare the responses from a different model.
- Compared the answers with the official AIE2026 glossary.

Result:
- The first response used 19 input tokens and 434 output tokens.
- The second response used 19 input tokens and 446 output tokens.
- Both responses gave general definitions of AI engineering rather than the exact definition from the course glossary.
- The attempt with gemini-3.8-flash failed with a 503 Model is busy error, and token usage was unavailable.


Observations / questions:
- The same model produced slightly different answers to the same question, with differences in wording and detail.
- Both answers discussed building and deploying AI applications, but they did not closely follow the course glossary.
- The glossary emphasizes using pretrained foundation models, connecting them to data and tools, and evaluating and improving applications iteratively.
- Changing the model did not produce a successful comparison because gemini-3.8-flash returned an error.

 Question: How can I make the model follow the course glossary more closely and give more consistent, course-specific answers?


## Implementation Level
What I did:
- Asked the model, “What is pretraining according to the AIE2026 course?”
- Asked the follow-up question, “Not referring to any course, what is pretraining?”
- Asked another follow-up, “Ohhh, specific task training,” to clarify my understanding of pretraining.


Result:
The model explained pretraining as general training on large datasets and clarified the difference between pretraining and fine-tuning, which adapts a model for specific tasks. The application maintained conversation history, allowing me to ask follow-up questions without manually resending previous messages.

Observations / questions:
- The model used previous messages to understand and answer follow-up questions.
- Input token usage increased from 16 to 738 and then 1,472 tokens as the conversation continued.
- The follow-up questions helped clarify the concept through an interactive conversation.
- The initial response was not specific to the AIE2026 course, even though I asked for the course definition.
- Question: How can conversation history be managed efficiently to reduce token usage while preserving context?


## Advanced: Response time and token count comparison


What I did:

- Measured response time and token usage while asking the model questions about AI engineering and pretraining.
- Compared responses from `gemini-3.5-flash-lite` and attempted to test `gemini-3.8-flash`.
- Asked different questions, including a course-specific question about AI engineering, a question about pretraining, and follow-up questions to explore the concept further.
- Observed what happened when a model request failed with a `503 Model is busy` error.

Result:

| Model / question | Response time | Input tokens | Output tokens |
|---|---:|---:|---:|
| Gemini 3.5 Flash Lite — AI engineering, attempt 1 | 2.224 s | 19 | 434 |
| Gemini 3.5 Flash Lite — AI engineering, attempt 2 | 2.614 s | 19 | 446 |
| Gemini 3.8 Flash — AI engineering | 2.004 s | Unavailable | Unavailable |
| Gemini 3.5 Flash Lite — pretraining | 3.565 s | 16 | 710 |
| Follow-up: pretraining outside the course | 6.144 s | 738 | 727 |
| Follow-up: specific-task training | 1.811 s | 1,472 | 211 |

The Gemini 3.8 Flash request failed with a `503 Model is busy` error, so it did not provide a successful response for comparison.

Observations / questions:

- Response time varied across requests. For example, the initial pretraining question took 3.565 seconds, while its first follow-up took 6.144 seconds.
- Longer conversation history was associated with higher input token counts. The follow-up requests used 738 and 1,472 input tokens, compared with 16 tokens for the initial pretraining question.
- Output token usage varied considerably depending on the question and response. The initial pretraining answer generated 710 output tokens, while the final follow-up generated 211.
- Repeating the same AI engineering question produced slightly different answers and output token counts, even when using the same model.
- The model did not always provide course-specific answers, showing that a fast response does not necessarily mean an accurate or relevant response.
- The failed Gemini 3.8 Flash request demonstrates that model availability can affect successful completion, regardless of the measured response time.

**Relationship to free-quota rate limits:**

Repeated requests and long conversations can consume more of an available free usage quota because each request may process input tokens and generate output tokens. Follow-up questions can be particularly expensive when the application includes the previous conversation history in each request. Rate limits may also restrict how frequently a model can be called, while a `503 Model is busy` error indicates that the service was temporarily unavailable or overloaded; it does not, by itself, prove that a free quota was exhausted.

Conclusion:

Measuring response time and token usage helps evaluate model performance and efficiency. To make a fair comparison between models, I would ask the same questions under similar conditions and compare successful requests, response times, token counts, and answer quality.