# Lecture 2 Answer

## Exercise

- Model and settings used (`config` from `result.json`): Qwen/Qwen3.5-0.8B , LoRA without quantization (32-bit), run on a Tesla T4 in Google Colab. Settings: num_train_epochs 20, lr 0.0002, lora_r 16, lora_alpha 32, warmup_steps 6, seed 42, max_seq_len 512, max_new_tokens 96, greedy generation (do_sample false). Libraries: transformers 5.18.0, peft 0.21.1, trl 1.14.2, torch 2.11.0+cu130.
- Did I run the training myself (`executed_training_myself`): Yes (range that could be executed: I ran Sections 0 to 7 myself; I did not run the optional Section 8).
- Before training: `format_rate` = 0.2857 (6 of 21) / `content_rate` = 0.1905 (4 of 21)
- After training: `format_rate` = 1.0000 (21 of 21) / `content_rate` = 0.8571 (18 of 21)
- Questions that regressed: none (the regressed list is empty).
- Remaining failures after training and their type (asserted on unsupported questions / escaped by asking for confirmation on evidence-based questions / format corruption): 3 of 21 questions still fail.
  1. "PDF 以外でも出せますか" is in the FAQ, but the model answered "not covered" with needs_review true. Type: escaped by asking for confirmation on an evidence-based question.
  2. "成績はいつ出ますか" is not in the FAQ, but the model answered with the assignment deadline and needs_review false. Type: asserted on an unsupported question.
  3. "オフィスアワーは事前予約が必要ですか" is not in the FAQ, but the model answered with the office hours and needs_review false. Type: asserted on an unsupported question.
  There is no format corruption after training. Before training, all 15 format failures had the reason missing_key (valid JSON with answer, but needs_review was missing).
- Results for knowledge questions (Section 6) (before training classification → after training classification) and observations:

  | Question | Before → After |
  | --- | --- |
  | Final assignment deadline (not in FAQ) | asserted → asserted |
  | Instructor's name (not in FAQ) | format_error → needs_review |
  | Next lecture topic (not in FAQ) | format_error → needs_review |
  | Assignment deadline (control, in the FAQ) | format_error → asserted |

  Observations: before training, the model made up a next lecture topic ("AI 技術の活用と倫理"). After training, it asked for review on the instructor's name and the next lecture topic, which is the wanted behavior. For the final assignment deadline it still gave the normal deadline with needs_review false, which is an unfounded assertion. The "FAQ にある" column in the notebook table shows False for the control question even though it is in the FAQ, so I treated that column as unreliable for that row.
- What changed through training / what did not change: Training fixed the format very quickly. format_rate went from 0.2857 to 1.0000, and content_rate from 0.1905 to 0.8571, with no regressions. Training took 245 seconds, the loss fell from 1.4317 (step 10) to 0.0132 (step 40), and only 6,389,760 of 758,782,784 parameters (0.8421 percent) were trained. What did not change reliably is the judgment of whether the FAQ supports an answer: 2 of the 6 test questions that are not in the FAQ, and 1 of the 3 unknown knowledge questions, were still answered with a flat assertion. After training, the answers also came back almost word for word from the FAQ text. This is only what I saw on this small made-up FAQ in one run.

## Homework

- Level attempted: Basic
- Settings or data changed: I changed only num_train_epochs in CONFIG, from 20 to 10. All other settings stayed the same. I used Runtime, Restart session, and ran the notebook from the top both times. The editor would not let me change one line in the Section 1 cell, so I replaced the whole cell with the same contents and only changed 20 to 10. The new `result.json` shows num_train_epochs 10.
- Results (comparison table or numbers):

  | | Original (20 epochs) | Changed (10 epochs) |
  | --- | --- | --- |
  | Steps | 40 | 20 |
  | Loss at step 10 | 1.4317 | 1.4337 |
  | Loss at step 20 | 0.0646 | 0.0767 |
  | Final loss | 0.0132 (step 40) | 0.0767 (step 20) |
  | Training time | 245 seconds | 125 seconds |
  | format_rate before training | 0.2857 | 0.2857 |
  | content_rate before training | 0.1905 | 0.1905 |
  | format_rate after training | 1.0000 (21 of 21) | 1.0000 (21 of 21) |
  | content_rate after training | 0.8571 (18 of 21) | 0.8571 (18 of 21) |
  | both_rate after training | 0.8571 (18 of 21) | 0.8571 (18 of 21) |
  | Regressed questions | none | none |

  Remaining failures (3 of 21 in each run):

  | Run | Failed questions |
  | --- | --- |
  | 20 epochs | "PDF 以外でも出せますか" (in the FAQ, dodged with "not covered"); "成績はいつ出ますか" and "オフィスアワーは事前予約が必要ですか" (not in the FAQ, asserted with needs_review false) |
  | 10 epochs | "PDF 以外でも出せますか" (same dodge); "課題の文字数に制限はありますか" and "参考文献の書き方に指定はありますか" (not in the FAQ, needs_review true, but the answer text mixed in wording from other FAQ items) |

  With 10 epochs, all 6 test questions that are not in the FAQ got needs_review true. With 20 epochs, 4 of the 6 did. In the knowledge questions (Section 6), the categories were the same in both runs. The only difference was the wording of the instructor's name answer: "運営に確認が必要です" at 20 epochs, and "この FAQ には記載がありません。質問は受け付けます。" at 10 epochs. The files are result_original.json (20 epochs) and result_10_epochs.json (10 epochs).
- Considerations on when fine-tuning is appropriate and when it is not: Halving the epochs made training about twice as fast (245 seconds to 125 seconds), and the final loss was higher (0.0132 to 0.0767), but format_rate and content_rate did not change. So for learning the output format, 10 epochs was already enough on this data. The failures were different in the two runs, but I ran each setting only once, and the notebook says GPU training is not fully reproducible even with a fixed seed. So I cannot say that fewer epochs caused the different failures. I can only report what happened in these two runs.

  Fine-tuning seems to fit when I want the model to follow a fixed output format. It took about four minutes, trained less than 1 percent of the parameters, and format_rate went from 0.2857 to 1.0000. It did not do enough when the model has to decide whether the FAQ actually contains the answer. In both runs it still made mistakes on questions that are not in the FAQ, either by asserting an answer or by mixing in wrong wording, and the final assignment deadline question was asserted in both runs. The trained model also copied FAQ sentences almost word for word, so it looks like it reproduced the training data. I only tested one small model and one small made-up FAQ, so these conclusions apply only to this data.

### What I verified myself

- I ran every cell myself in Google Colab on a Tesla T4, and I copied all numbers from the notebook output and from the result.json files, not from memory.
- The first time I ran the before-training evaluation, format_rate was 1.0, which did not look like an untrained model. An AI assistant pointed out that the trained adapter was probably still loaded in the session. I restarted the session and ran Sections 0 to 3 again, and then format_rate was 0.2857, so I used that result and threw away the first one.
- I checked that the before-training scores were exactly the same in both runs (format_rate 0.2857, content_rate 0.1905), so the two runs started from the same conditions.
- I checked that the training output showed 20 steps and 10.0 epochs for the changed run, and 40 steps and 20.0 epochs for the original run, and that the result.json of the changed run shows num_train_epochs 10.
- I looked at the question-by-question tables of the two runs, and the remaining failures listed above come from those tables.
- I used an AI assistant to explain the steps and to help organize and word this write-up. I did not verify why the model made each mistake, so I only describe what the outputs show.
