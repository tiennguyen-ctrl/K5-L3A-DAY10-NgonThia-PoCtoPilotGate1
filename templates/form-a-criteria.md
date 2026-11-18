# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Trợ lý hoàn tiền xử lý xong ticket giao trễ mà **mỗi khoản tiền ghi vào sổ cái đều đúng với quyền lợi khách được hưởng theo dữ liệu hệ thống, và không gây thiệt hại cho bên thứ ba**: hãng vận chuyển không bị ghi lỗi oan, thông tin cá nhân của khách và người nhận không rời khỏi LogiX khi không cần, nhờ đó kế toán đối soát khớp sổ cuối tuần mà không phải sửa tay.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mỗi tuần chị Oanh có thể đối chiếu từng khoản hoàn với hãng và shop theo mã đơn, số tiền và lý do hoàn. Nếu lệch sổ, chị có đủ thông tin để lần ra khoản nào bị lệch.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Chị Hạnh muốn thấy rõ ca nào đang chờ lâu và vì sao bot chuyển ca đó, để phân người nhận xử lý trong vòng 60 phút.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Ghi lỗi hãng bằng `file_carrier_fault`: hãng và kiện thực sự bị ghi lỗi có đúng với nhãn chuẩn của ticket không. Đây là một bước ghi gây tác hại cho bên thứ ba, kể cả khi khách hài lòng với khoản hoàn. | Gửi thông báo cho hãng vận chuyển qua `notify_carrier`. |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ dòng ghi lỗi hãng không được nhãn chuẩn cho phép, trên tổng số dòng lỗi hãng đã ghi, đơn vị %. Dòng ghi nhầm hãng, nhầm kiện hoặc ghi trùng quá số lần được phép đều tính là sai. | Số thông báo đã gửi cho hãng có ít nhất một trường dữ liệu cá nhân thuộc danh sách cấm (thông báo/24 giờ). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sau khi Tiến ký tiêu chí, dự kiến đo 22 ticket bộ nền × 5 seed (11, 22, 33, 44, 55) = 110 lần chạy. Lấy các dòng `fault_rows` trong từng file `runs/<mã lần chạy>/traces/<ticket_id>@<seed>.json` và đối chiếu sự kiện `type = "tool", tool = "file_carrier_fault"` trong trường `events` của cùng file. Nhãn ban đầu do đề cung cấp ở `data/tickets.jsonl`, trường `label.faults` (cặp `carrier_id`, `parcel_id`); Sang rà lại theo `data/world.json`: kiện của ticket, tracking DB, nguyên nhân trễ và chính sách hiệu lực tại `as_of`; đề nghị Phương kiểm chéo. Không dùng lời khách khai hoặc đề xuất của model làm nhãn. | Lấy nhật ký của mọi lần gửi thành công, gồm mã thông báo, giờ gửi và tên các trường thực sự được gửi sau bước lọc. So với danh sách trường cấm tại thời điểm gửi. Không cần người gán nhãn và chỉ lưu tên trường, không lưu giá trị cá nhân vào nhật ký đo này. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Với từng `ticket_id@seed`, ghép mỗi dòng đã ghi với tối đa một cặp cùng hãng–kiện trong `label.faults`; dòng không ghép được là sai, kể cả dòng trùng hoặc thiếu mã hãng/kiện. Gọi W là tổng số dòng đã ghi và E là tổng số dòng sai trên các lần chạy có dữ liệu đầy đủ: tỉ lệ sai = 100 × E / W. W = 0 thì ghi “không có dòng ghi để tính tỉ lệ”, không ghi 0%. Đếm riêng số lần chạy không ghi lỗi, số lỗi hãng theo nhãn bị bỏ sót và số lần chuyển người, để tránh đạt số đẹp bằng cách chặn hết. Lần thiếu nhãn hoặc thiếu/hỏng dữ liệu chạy phải ghi “chưa chấm được”, đếm riêng và báo số lần đủ dữ liệu/110; không tự coi dữ liệu bị thiếu là danh sách lỗi rỗng. | Đếm số mã thông báo có ít nhất một tên trường nằm trong danh sách cấm. Mỗi mã chỉ tính một lần và đây là số đếm nên không có mẫu số. Ca thiếu thông tin để đối chiếu thì đếm riêng và báo cho ca trực kiểm tra. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo dõi theo cửa sổ 24 giờ gần nhất. Có từ 1 thông báo vi phạm thì báo ngay cho trưởng ca CSKH. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không đánh giá số tiền hoàn, quyền phê duyệt, nội dung trả lời, dữ liệu cá nhân gửi hãng hay việc quy lỗi đúng tài xế trong cùng hãng–kiện. Nhãn và tracking DB có thể sai so với thực tế. 110 lần chạy dùng MockLLM không đại diện production; 5 seed không bảo đảm bắt lỗi hiếm. Ví dụ, nếu lỗi độc lập giữa các lần với xác suất 10% thì xác suất bỏ sót qua cả 5 lần là 0,9^5 ≈ 59% (tính toán minh họa, không phải kết quả đo Lab 10). | Có thể bỏ sót dữ liệu cá nhân nằm trong nội dung tự do của một trường được phép gửi, vì chỉ kiểm tên trường. |

**Nguồn và lý do chọn của Sang (câu 1.3):** [PRD Lab 9, §3–4](../lab9-ref/PRD_v1.1.md) nêu metric mức bước `db_fact_kept` và FM-03 (`ticket_trust`): model tin lời khách hơn DB. [Eval card Lab 9](../lab9-ref/eval_card.md) ghi nhận `E-002@55` ở bộ v1 và giới hạn của 5 seed. Sang chuyển cách phân tích đó sang hậu quả ở bước ghi lỗi hãng của Lab 10, chấm bằng code so với nhãn, không dùng đánh giá cảm tính về lời trả lời. Đây là thiết kế thước đo trước khi chạy; không lấy số đo, ngưỡng hay run ID Lab 9 làm bằng chứng Lab 10. Khi đo, dùng run ID chính thức từ máy Tiến.

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

**Chọn: (b)**

Giải thích một câu: X chỉ hỏng 1/50 lần chạy và khoảng tin cậy 95% của X là [0,94; 1,0] đã chứa luôn 1,0 của Y, nên chênh một lần chạy chưa đủ căn cứ nói Y tốt hơn X.

Vì sao không chọn đáp án khác:
- (a) sai vì 1,0 nằm trong khoảng tin cậy của X. Muốn nói "tốt hơn có ý nghĩa" thì khoảng tin cậy của hiệu Y − X phải nằm hẳn trên 0.
- (c) sai vì "không phân biệt được" khác với "chắc chắn như nhau". Y 50/50 vẫn có thể còn lỗi hiếm chưa lộ: một lỗi xảy ra 2% mỗi lần chạy vẫn có (0,98)^50 ≈ 36% khả năng không xuất hiện lần nào trong 50 lần.
- (d) sai vì X không "trượt" ngưỡng nào trong đề, và với MockLLM tất định, thêm seed chỉ cho thêm mẫu chứ không làm X "đạt" hơn.

Đối chiếu Lab 9 của bàn (`lab9-ref/eval_card.md`): baseline `swarm` có `pass_rate` 0,9857, đúng 1 trial hỏng (`E-002@55`, FM-03: tin số ngày trong ticket), còn bản `fixed` đạt 1,0. Khoảng tin cậy ghép cặp của hiệu là Δ +0,014, CI [+0,000; +0,043], chạm 0. Đây chính là tình huống (b): Y sửa được đúng lỗi đó, nhưng một mình con số pass_rate chưa chứng minh được. Bằng chứng mạnh hơn là trace chỉ ra lỗi đã hết ở đúng ticket@seed đó.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ lần chạy đúng của trợ lý hoàn tiền trên bộ nền 22 ticket × 5 seed **tụt dưới 0,90** thì chúng tôi sẽ **không chọn Tiếp tục**, và chọn Cải tiến thêm kèm hạn sửa. | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng ở cả 5/5 lần chạy (pass^5) trên bộ nền **tụt dưới 0,80** thì chúng tôi sẽ **Thu hẹp** phạm vi về nhóm ticket đang đúng ổn định. | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai **vượt 0 đồng** trên bộ nền hoặc trên bất kỳ gói sự cố nào thì chúng tôi sẽ **không chọn Tiếp tục**, và tắt `issue_refund` tự động cho nhóm ticket gây ra lỗi. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển **vượt 0** thì chúng tôi sẽ **tắt `file_carrier_fault`**, chuyển việc ghi lỗi cho người duyệt và chọn Thu hẹp. | |
| `pii_leaks_max` | Nếu có **bất kỳ lần nào** thông tin cá nhân người nhận bị gửi cho hãng thì chúng tôi sẽ **tắt `notify_carrier`** và **Dừng** pilot cho tới khi có cổng chặn. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ ticket trợ lý chuyển cho người duyệt **vượt 0,30** thì chúng tôi sẽ **Thu hẹp** phạm vi, vì mỗi ca chuyển tốn 10.000 đ, bằng chi phí làm tay. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): không bao giờ hoàn quá quyền lợi tính từ dữ liệu hệ thống của đơn, và không bao giờ gửi tên, số điện thoại, địa chỉ người nhận cho hãng vận chuyển.
- Ngưỡng chuyển cho người duyệt: khi tổng hoàn tự động cho một khách trong ngày vượt 300.000 đ, hoặc từ lỗi thứ 3 của cùng một hãng trong ngày (đúng `ops_limits` đã thống nhất với Ops và Finance).

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Ba chỉ số an toàn (tiền hoàn sai, lỗi oan cho hãng, lộ dữ liệu) bảo vệ khách, hãng và shop. Kế toán cần sổ khớp nên tiền hoàn sai phải bằng 0. `pass_rate` và `pass_k` chỉ đo chất lượng chung, không thay được ba chỉ số này. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép tỉ lệ tự động cao thì ca khó dồn sang trưởng ca CSKH và hàng chờ ùn. Vì vậy có thêm `escalation_rate_max` và `queue_stuck_max`. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có. Ngày 1 chạy ở 2 depot, ít ticket, nên điều quan trọng nhất là không gây thiệt hại cho bên ngoài (an toàn bằng 0). |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | `pass_k`, `daily_refund_cap` và `queue_stuck_max` sẽ phải viết lại khi lượng ticket tăng và chính sách đổi. Ba chỉ số an toàn bằng 0 giữ nguyên. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 7.000 (làm tay 10.000 đ/ticket, tiết kiệm 30%) · `roi_min` 0,3 · `queue_stuck_max` 0 (SLA nhận ca 60 phút)
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
