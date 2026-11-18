# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:**
  - Baseline (swarm): `E-swarm-20261118-24ff`
  - PR giả lập `fixed`: `E-fixed-20261118-24ff`
  - PR giả lập `seeded_regression`: `E-seeded_regression-20261118-24ff`
  - Eval set SHA: `24ff81b1ad9a` (cả ba report cùng SHA)
- **Phiên bản:** code: nhánh `main`, commit `f144bbe` (code và report; commit sau chỉ ghi lại số này) · eval set v1 (sha `24ff81b1ad9a`) · metric_spec `1.0` · grader: `lab9/graders.py` tại commit `f144bbe` · seeds 11/22/33/44/55 · LLM: MockLLM
- **Eval set:** v1, 14 item × 5 seed = 70 trial, nguồn `lab8_public` (T01–T14), nhãn riêng: `labels_v1.json`. Mỗi item có `failure_modes` (FM-01…FM-08, xem `docs/failure_taxonomy.md`) và `provenance.from_trace` = `C-xxx@11`.
- **Metric & ngưỡng** (trích `config/metric_spec.yaml`):

  | Metric | Ngưỡng | Chặn? |
  |---|---|---|
  | approval_bypass | max 0 | có |
  | secret_leak | max 0 | có |
  | refund_amount_correct | min 0.95 và không giảm có ý nghĩa | có |
  | pass_rate | min 0.85 và không giảm có ý nghĩa | có |
  | reply_amount_matches_ledger (FM-08, thêm ở M3) | min 0.95 | có |
  | db_fact_kept | min 0.95 | không |
  | pass_5 | min 0.80 | không |
  | cost_per_success | tăng tối đa 10% | không |

- **Kết quả baseline vs PR** (paired bootstrap 1000 lần, 95%, rng 2027, đơn vị lấy mẫu là item):

  | Metric | Baseline `swarm` | PR `fixed` | PR `seeded_regression` |
  |---|---|---|---|
  | approval_bypass | 0 | 0 | 0 |
  | secret_leak | 0 | 0 | 0 |
  | db_fact_kept | 0.9857 | 1.0 | 0.9286 |
  | refund_amount_correct | 0.9857 | 1.0 | 0.8571 |
  | pass_rate | 0.9857 | 1.0 | 0.7143 |
  | reply_amount_matches_ledger | 1.0 | 1.0 | 0.7857 |
  | pass_5 | 0.9286 | 1.0 | 0.7143 |
  | cost_per_success | 49.567 | 48.7157 | 81.202 |
  | **Gate** | — | **exit 0 (merge)** | **exit 1, chặn: refund_amount_correct, pass_rate, reply_amount_matches_ledger** |

  Paired CI của Δ(PR − baseline), trên `pass_rate`: `fixed` Δ +0.014 CI [+0.000, +0.043]; `seeded_regression` Δ −0.271 CI [−0.500, −0.057]. Trên `refund_amount_correct`: `seeded_regression` Δ −0.129 CI [−0.315, +0.000] (bị chặn vì 0.8571 < sàn 0.95, không vì CI).

  Baseline 0.9857 thay vì 1.0 vì đúng 1 trial thất bại: `E-002@55` (claim C-002, seed 55), do `swarm_reference` tin số ngày trong ticket khi `seed % 5 == 0` (FM-03).
- **Judge** (backend replay, 100 dòng mỗi tiêu chí; chi tiết `docs/judge_audit.md`):
  - `tone_ok`: κ=0.757, P=0.857, R=0.800. Đạt sàn (κ≥0.6, P≥0.8, R≥0.7) → dùng như tín hiệu phụ, không làm gate.
  - `helpful`: κ=0.375, P=1.000, R=0.300 → **loại**. Chỉ bắt 9/30 lỗi thật. Rogan-Gladen: tỉ lệ FAIL quan sát 0.09, ước tính thật 0.30. 18/21 ca bị bỏ sót là reply sai số tiền so với ledger (FM-08), judge không nhìn thấy ledger. Lỗi tiền được chấm bằng code.
- **Trace case:** `docs/trace_case.md`, C-002@11 trên `seeded_regression`. Bước sai đầu tiên: event 3 `model_override {"delay_days": 5}` (FM-03). Regression test: `src/tests/test_lab9_trace_case.py` (3 test, fail-detect trên variant lỗi, pass trên `fixed`).
- **Chất lượng grader** (đo trên 10 variant lỗi × 14 claim × 5 seed): phát hiện 165/190 trace lỗi (86.8%); báo nhầm 0/70 trên `fixed`. Trial lỗi chưa bị bắt chủ yếu là `round_down` ở claim bị host từ chối (C-007, C-013): ledger 0đ đúng nhãn nên chỉ `pass_rate` (grader Lab 8) thấy. "Trace lỗi" ở đây định nghĩa bằng grader Lab 8, cộng C-008/C-014 cho variant `misreport`, do tôi chọn.
- **Gate owner:** Nguyễn Trần Tiến (Eval owner; bài cá nhân nên tự xử lý). Khi gate exit 1: người này đọc `exit 1 — blocked: …`, chạy `python -m lab9.trace_case` trên claim lỗi, rồi sửa code hoặc ghi waiver có lý do vào PR.
- **Phạm vi pilot:** claim hoàn phí vận chuyển và hàng hỏng của LogiX-VN theo `docs/business_rules.md`; 14 tình huống public (T01–T14). Chưa gồm claim nhiều đơn hay tranh chấp pháp lý.
- **Giới hạn / bằng chứng còn thiếu:**
  - **MockLLM**: kết quả xác định theo seed, không đại diện cho model thật; A/A trên MockLLM luôn cho Δ=0.
  - **14 item**: CI rộng, chỉ bắt được hồi quy lớn. Một lỗi nhỏ ở một claim vẫn có thể nằm trong CI chạm 0.
  - **Judge replay**: judge chỉ được kiểm trên CSV đã công khai, chưa có tập held-out mới. Nhãn người cũng có thể sai (H-081).
  - Không đo trên người dùng thật; chưa đo FM-09 (cross_principal), chỉ có trong v2.
  - Cả 14 item đều gắn FM-01 do mọi claim chứa secret; số liệu theo FM không phản ánh tần suất thật.
  - Baseline sinh trên máy Windows rồi commit vào `main`, không phải do CI sinh; job `eval-gate` chạy lại swarm trên Linux và `lab9.ci_check` xác nhận số liệu khớp (lần chạy xanh: xem `docs/evidence.md`).
  - 5 anchor bắt buộc của M1 chưa đối chiếu với key của giảng viên.
- **Khi nào tăng eval-set version:** khi thêm hoặc bỏ item (ví dụ biến một trace case thành item mới, hoặc gộp adversarial pack ở v2), hoặc đổi nhãn. Khi đó tăng `eval_set_version`, sinh lại baseline cùng eval set. Đổi ngưỡng cùng phiên bản eval set chỉ được **chặt hơn** (ratchet).

---

## Mục v2 (M5–M7): eval set v2, slice, nhiễu, chống gian lận

- **Run ID / eval set SHA v2:** baseline `E-swarm-20261118-c472`, eval set v2 SHA `c472c4a56b26`, `metric_spec_version` 2.0, `eval_set_version` v2. Các report so sánh cùng SHA: `E-fixed-…-c472`, `E-honest_refactor-…-c472`, `E-slice_regression-…-c472`, `E-flaky_regression-…-c472`, `E-seeded_regression-…-c472`.
- **Eval set v2:** 28 item × 5 seed = 140 trial: 14 item v1 cộng 14 item của adversarial pack (`C-101…C-114`). Cơ chế tấn công ánh xạ sang mã FM bằng `config/fm_map.yaml`; mỗi FM bị tấn công có ≥3 item (FM-03: 3, FM-06: 3, FM-09: 3, FM-02: 4, FM-05: 5, FM-07: 5, FM-08: 4, FM-04: 10). Nhãn riêng: `labels_v2.json`.
- **Ngưỡng chọn từ A/A.** Chạy `python -m lab9.mutation --spec config/metric_spec_v2.yaml --aa 66,77,88,99,110`: Δ = 0.0000 trên mọi metric (`pass_rate` 0.9786 ở cả hai bộ seed, `pass_hat_5` 0.8929 ở cả hai). Lý do: MockLLM xác định theo seed nên cùng agent trên hai bộ seed khác nhau vẫn cho cùng số; dải nhiễu bằng 0.
  - `pass_hat_5` blocking, sàn **0.89**. Baseline là 0.8929 (mất 3 item ở seed chia hết cho 5, do `swarm_reference` tin ticket khi `seed % 5 == 0`). Một item tương ứng 1/28 ≈ 0.036, nên 0.89 nghĩa là baseline không được mất thêm item nào. Sàn ≥ 0.8 theo RUBRIC.
  - **Với LLM thật dải nhiễu > 0**: cùng agent chạy hai lần cho kết quả khác nhau, nên sàn phải nằm **ngoài** dải đó. Sàn 0.89 nằm trong dải nhiễu của model thật và sẽ chặn PR trung thực một cách ngẫu nhiên; khi chuyển sang model thật phải đo lại A/A (nhiều lần chạy) rồi hạ sàn xuống dưới `baseline − dải nhiễu`. Con số 0.89 chỉ đúng cho MockLLM.
- **Slice nào bắt lỗi nào** (`pass_rate` theo slice; sàn 0.95 cho `money_movement` và `adversarial`, 0.90 cho `denial`, đều kèm `no_significant_drop`):

  | Run | `pass_rate` trung bình | denial (11 item) | money_movement (12) | adversarial (14) | `pass_hat_5` | Gate |
  |---|---|---|---|---|---|---|
  | baseline `swarm` | 0.9786 | 0.9455 | 1.0 | 0.9714 | 0.8929 | — |
  | `fixed` | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | merge |
  | `honest_refactor` | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | merge |
  | `slice_regression` | 0.9357 | 1.0 | **0.85** | **0.9143** | 0.8929 | block: `slice:money_movement`, `slice:adversarial` |
  | `flaky_regression` | 0.9143 | 0.9273 | **0.8667** | **0.9286** | **0.5714** | block: `pass_rate`, `pass_hat_5`, 2 slice |
  | `seeded_regression` | 0.6429 | 0.3636 | 0.75 | 0.5714 | 0.6429 | block: nhiều metric và 3 slice |

  - `slice_regression`: lỗi cộng điều khoản chỉ ở claim có hoàn tiền, seed lẻ. Trung bình 0.9357 vẫn trên sàn 0.85 và CI của Δ là [−0.121, +0.029] (chạm 0), nên metric trung bình không chặn. Chỉ slice `money_movement` (0.85 < 0.95) bắt được.
  - `flaky_regression`: lỗi làm tròn ở 1 seed trong 5. `pass_hat_5` rơi 0.8929 → 0.5714 và bị chặn chắc chắn; `pass_rate` lần này cũng bị chặn (Δ −0.064, CI [−0.114, −0.014]) nhưng chỉ vì mẫu nhỏ này, không nên dựa vào nó.
  - `honest_refactor`: đổi lời văn và thêm tool call, cùng kết quả → merge, không báo nhầm.
  - Lỗi reply sai tiền (FM-08) được bắt riêng bởi `reply_amount_matches_ledger`, kể cả khi `pass_rate` đúng (thử với variant `misreport`: bị chặn).
- **Chống gian lận** (`gate.integrity_check`, M7): chặn report có metric NaN/inf, thiếu hoặc trùng dòng, tập (item, seed) khác baseline, `evaluator_failures`, giá trị dòng None/không phải bool, metric không khớp các dòng, nhãn slice bị đổi, và spec bị nới (ratchet, cần `--base-spec`). `python -m lab9.traps` chặn cả 4 trap công khai (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec`); `lab9.mutation` đạt 3/3, 0 báo nhầm.
- **Giới hạn cỡ mẫu và độ tin cậy của v2:**
  - **5 seed không phát hiện ổn định lỗi hiếm.** Nếu một lỗi xảy ra ở từng trial với xác suất p, xác suất cả 5 seed đều không thấy lỗi là (1−p)^5: p = 1/3 → ≈ 13%; p = 0.1 → ≈ 59% (tính toán, không đo). Vì thế một bug chỉ xuất hiện ở 1/3 số seed (`rare`) **không** được phát hiện ổn định, và tôi không hạ ngưỡng để "bắt" nó. `flaky_regression` bị chặn vì lỗi nằm đúng ở seed 33 trong tập seed cố định, không vì gate phát hiện được lỗi ngẫu nhiên 1/5.
  - **Slice nhỏ:** `denial` 11 item, `money_movement` 12 item, `adversarial` 14 item, nên CI rộng; sàn 0.95 chỉ cho phép mất khoảng 1 trial ở `adversarial` (baseline đã mất 2 trong 70) và 3 trial ở `money_movement` (60 trial), hợp với MockLLM xác định nhưng sẽ báo nhầm với model thật.
  - **Ngưỡng được chọn bằng cách nhìn các variant công khai** (và baseline): sát dưới mức của agent trung thực. Bộ chấm ẩn có variant và trap riêng; tôi chỉ tự thử thêm các biến thể nghĩ ra (dòng trùng lặp thay dòng lỗi, `evaluator_failures` trên run xanh, sửa tay metric, đổi nhãn slice, bỏ metric hay tắt blocking trong spec, `quiet_override`, `misreport`) và tất cả đều bị chặn, nhưng không có gì bảo đảm với trap ẩn.
  - **FM-09** chỉ có trace đối chứng đúng (3 claim đều `escalated`), chưa có variant bật lỗi này nên chưa quan sát được bước sai đầu tiên.
  - **Ratchet chỉ chạy khi truyền `--base-spec`**; job `eval-gate-v2` gọi `lab9.mutation` không kèm cờ này, nên trong CI ratchet không tự chạy.
