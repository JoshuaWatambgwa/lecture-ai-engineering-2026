## Exercise

- **Agreement rates by criterion (before modification):**
  - Grounding: 6/9 (66.7%)
  - Scope: 8/10 (80%)
  - Hint: 8/10 (80%)
  - Clarity: 7/10 (70%)
  - Lecture Mark (code): 4/10 (40%)
  - Overall: 5/9 (55.6%)

- **Number of items requiring review (before modification):** 1 item (#05).

- **Criterion modified and the policy added:**

  I modified the Grounding criterion. The new policy allows the agent to provide a general explanation of a term that is not in the glossary, provided it clearly states that the term is not in the glossary and does not present the explanation as an official course definition.

- **Agreement rates by criterion and number of items requiring review (after modification):**
  - Grounding: 5/9 (55.6%)
  - Scope: 8/10 (80%)
  - Hint: 8/10 (80%)
  - Clarity: 8/10 (80%)
  - Lecture Mark (code): 4/10 (40%)
  - Overall: 4/9 (44.4%)
  - Items requiring review: 1 item (#06).

- **Items where the instructor's labels and my labels differed, and reasons for my judgments:**

  - **#03 Grounding:** I considered the response correct because it correctly interpreted the unfamiliar term as LoRA and explained it consistently with the glossary.
  - **#05 Grounding:** I considered the response correct because it clearly stated that the term was not in the glossary before providing a general explanation.
  - **#06 Grounding:** The LLM marked this as requiring review because the response provided specific code that constituted the homework answer.
  - **#10 Grounding:** I considered the response incorrect because it claimed that Lecture 14 would be added later, contrary to the expected behaviour.
  - **#08 and #09 Hint:** I considered the responses correct because the questions were unrelated to homework, so this criterion should automatically pass.

- **Observations / Questions:**

  The number of items requiring review remained unchanged at one, although the item changed from #05 to #06. Grounding agreement decreased from 6/9 to 5/9, while Clarity improved from 7/10 to 8/10. Overall agreement decreased from 5/9 to 4/9. The policy change did not produce the expected improvement in Grounding agreement. This suggests that the revised policy may need further refinement. I also observed that some disagreements were caused by the interpretation of the evaluation criteria rather than factual errors in the responses.