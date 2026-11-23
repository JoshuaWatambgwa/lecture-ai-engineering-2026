# Lecture 4 Answers

## Exercise

- **Agreement rates by criterion (before rubric modification):**
  - Grounding: 6/9 (66.7%)
  - Scope: 8/10 (80%)
  - Hint: 8/10 (80%)
  - Clarity: 7/10 (70%)
  - Lecture Mark (code): 4/10 (40%)
  - Overall: 5/9 (55.6%)

- **Number of items requiring review (before modification):** 1 item (#05).

- **Criterion modified and policy added:**

  I modified the Grounding criterion. The new policy allows the agent to provide a general explanation of a term that is not in the glossary, provided it clearly states that the term is not in the glossary and does not present the explanation as an official course definition.

- **Agreement rates by criterion and number of items requiring review (after rubric modification):**
  - Grounding: 5/9 (55.6%)
  - Scope: 8/10 (80%)
  - Hint: 8/10 (80%)
  - Clarity: 8/10 (80%)
  - Lecture Mark (code): 4/10 (40%)
  - Overall: 4/9 (44.4%)
  - Items requiring review: 1 item (#06).

- **Items where the instructor's labels and my labels differed, and reasons for my judgments:**

  - **#03 Grounding:** The response correctly interpreted the unfamiliar term as LoRA and explained it consistently with the glossary.
  - **#05 Grounding:** The response clearly stated that the term was not in the glossary before providing a general explanation.
  - **#06 Grounding:** The LLM marked this as requiring review because the response provided specific code that constituted the homework answer.
  - **#10 Grounding:** The response made an unsupported claim that Lecture 14 would be added later, contrary to the reference.
  - **#08 and #09 Hint:** The questions were unrelated to homework, so this criterion should automatically pass.

- **Observations / Questions:**

  The number of items requiring review remained unchanged at one, although the item changed from #05 to #06. Grounding agreement decreased from 6/9 to 5/9, while Clarity improved from 7/10 to 8/10. Overall agreement decreased from 5/9 to 4/9. The policy change did not produce the expected improvement in Grounding agreement, suggesting that the revised policy may need further refinement.

## Homework

- **Level completed:** Basic

- **What I did:**

  Changed the grading model (`AIE_MODEL`) from `gemini-3.5-flash-lite` to `gemini-3.8-flash`. I kept the modified rubric, temperature (0), and the same 10 evaluation cases unchanged. I then reran the evaluation to compare the two models.

- **Results:**

  | Criterion | gemini-3.5-flash-lite | gemini-3.8-flash |
  |---|---:|---:|
  | Grounding | 5/9 | 6/10 |
  | Scope | 8/10 | 8/10 |
  | Hint | 8/10 | 8/10 |
  | Clarity | 8/10 | 7/10 |
  | Lecture Mark | 4/10 | 4/10 |
  | Overall agreement | 4/9 | 5/10 |
  | Needs review | 1 | 0 |
  | Coverage | 90% | 100% |
  | Mismatches | 16 | 17 |

  Overall agreement increased from 44.4% to 50%. Grounding improved, Scope and Hint remained unchanged, while Clarity decreased. The number of items requiring review decreased from one to zero.

- **Observations / Questions:**

  gemini-3.8-flash achieved slightly higher overall agreement and evaluated all 10 cases without requiring manual review. However, the number of mismatches increased from 16 to 17, and not all criteria improved. This suggests that changing the grading model does not necessarily improve performance across every evaluation criterion.