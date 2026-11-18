# Chia việc · LAB 10 · Nhóm NgonThia (L3A)

File này là kế hoạch làm việc nội bộ của bàn, không nằm trong bài nộp. Nó trả lời: **ai làm gì, làm ở đâu, làm thế nào, ai phải chờ ai, và việc đó ảnh hưởng phần nào của ai.** Nguồn: `README.md`, `problem-set.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `RULES.md`, `SUBMISSION.md`, ba phiếu trong `templates/`, `docs/guide.md`, `submission/README.md`, và slide của buổi học (giờ thật).

---

## 0. Giờ thật của buổi học (từ slide)

Đề tính theo "phút" kể từ lúc bắt đầu. Slide đặt phút 0 = **13:30**. Dùng bảng này để canh giờ.

| Phút | Giờ | Mốc | Việc chính |
|---:|---|---|---|
| 0–15 | 13:30–13:45 | CP1 | Cài đặt, chia vai |
| 15–60 | 13:45–14:30 | CP2 | Viết Phiếu A (chưa chạy trợ lý) |
| **60–65** | **14:30–14:35** | CP2 | **Ký tiêu chí và push** |
| 65–85 | 14:35–14:55 | CP3 / 2A | Đo base, rủi ro, pre-mortem |
| 85–105 | 14:55–15:15 | CP3 / 2B | Dựng cổng |
| 105–115 | 15:15–15:25 | CP3 | Chốt vòng 1, quyết định v1 |
| 115–125 | 15:25–15:35 | | Nghỉ |
| 125–185 | 15:35–16:35 | CP4 | Nhận thẻ, phân tích, sửa |
| 185–200 | 16:35–16:50 | CP5 | Quyết định v2, gom bài |
| 200–240 | 16:50–17:30 | | Demo, đẩy bài lần cuối **trước 17:30** |
| | **11:59 sáng hôm sau** | | Hạn nộp link LMS (mỗi người) |

---

## 1. Phân vai

Đề có 3 vai. Bàn có 4 người nên vai **Kỹ sư cổng** có 2 người (Sang, Phương), đúng như đề cho phép ("1–2 người").

| Người | Vai | Việc chính | File sở hữu (chỉ người này sửa) |
|---|---|---|---|
| **Tiến** (trưởng nhóm) | Sản phẩm và kinh doanh **+ giữ máy chạy lệnh chính** | Tiêu chí và ký, cổng `business`, chạy mọi lệnh có mã lần chạy, quyết định v1 và v2, risk register, đẩy bài | `config/acceptance_criteria.json`, `operating_gates.json` mục `business`. Phiếu A mục A1 (1.1), A4 (1.6), A5. Phiếu B mục B0, B1, B7.4, B8. Phiếu C mục C0, C10, C12 |
| **Hoàng** | Vận hành và pháp lý | HAZOP, checklist 9 nhóm có PIC, cổng `operations` và `legal`, runbook, `submission.json` | `operating_gates.json` mục `operations` và `legal`. Phiếu A mục A1 (1.2), A2 (1.4). Phiếu B mục B4, B5, B7.5, B7.6. Phiếu C mục C3, C4, C5 (3.3), C11. `submission/submission.json` |
| **Sang** | Kỹ sư cổng, phụ trách **code cổng** | Dò trace, viết và sửa cổng trong `guards.py` | `lab10/guards.py`. Phiếu A mục A2 (1.3). Phiếu B mục B2, B7.1. Phiếu C mục C2, C7 (cột code), C9 |
| **Phương** | Kỹ sư cổng, phụ trách **dữ liệu, kiểm thử và chỉ số** | Bản đồ dữ liệu, behavioral test, kiểm chéo cổng của Sang, chỉ số theo dõi | `lab10/monitors.py`. Phiếu A mục A3 (1.5). Phiếu B mục B3, B7.2, B7.3. Phiếu C mục C1, C5 (3.2), C6, C8 |

Cả bàn cùng làm: pre-mortem (B6), quyết định v1 và v2 (Tiến cầm bút, cả bàn chốt).

**Vì sao chia vậy (so với bản trước):**
- Tiến giữ máy chạy lệnh nên được **bớt** các phiếu nặng chữ (bản đồ dữ liệu B3, specification C5, fault tree C6, chỉ số C8) để dồn sang Phương. Slide nhắc lỗi hay gặp là "một người làm hết, ba người ngồi xem".
- Sang và Phương **không chạm cùng file**: Sang giữ `guards.py`, Phương giữ `monitors.py`. Phương kiểm chéo code của Sang bằng cách chạy trên máy mình trước khi Tiến chạy bản chính thức.
- Hoàng giữ phần người, tiền, pháp lý, và hai phiếu dài nhất (B4, B5, B7.5).

---

## 2. Ba nguyên tắc sống còn

### 2.1. Chỉ MỘT máy chạy lệnh chính: máy của Tiến

Thư mục `runs/` nằm trong `.gitignore`, tức là **không lên GitHub**. Nhật ký `runs/journal.jsonl` và mã lần chạy chỉ có trên máy đã chạy lệnh. Team chấm lấy `submission/runs/` do lệnh 7 gom, nên các lệnh sau **bắt buộc chạy trên máy Tiến**:

| Lệnh | Chạy ở đâu |
|---|---|
| Lệnh 1 `criteria sign` (một lần) | Máy Tiến |
| Lệnh 2 `eval`, lệnh 4 `gate`, lệnh 6 `grade` (các lần dùng làm bằng chứng trong phiếu) | Máy Tiến |
| Lệnh 5 `checkpoint` (một lần) | Máy Tiến |
| Lệnh 7 `check_submission --collect` | Máy Tiến |
| Nhận thẻ từ `upstream` ở phút 125 | Máy Tiến |

Sang, Hoàng, Phương vẫn chạy `eval`, `trace` trên máy mình để **thử nhanh** (sau khi `git pull` lấy chữ ký của Tiến), nhưng **mã lần chạy ghi vào phiếu phải lấy từ máy Tiến**. Mô phỏng tất định nên cùng code ra cùng số, nên có thể đối chiếu.

Hệ quả: **mọi thứ Tiến chạy phải có code mới nhất của ba người kia.** Quy trình mỗi lần chạy: người sửa push → Tiến `git pull` → Tiến chạy → Tiến báo mã lần chạy lên nhóm.

### 2.2. Ba việc "một lần, không làm lại"

| Việc | Ai | Hậu quả nếu làm sai |
|---|---|---|
| Ký tiêu chí (`criteria sign`) rồi push ngay | Tiến | Chạy eval trước khi ký thì lệnh từ chối. Sửa tiêu chí sau khi ký thì **bài không được tính** (điều kiện qua) |
| Chốt cổng vòng 1 (`checkpoint`) | Tiến | Chỉ chạy được một lần. Chốt thiếu cổng thì mốc `prepared` yếu cho cả vòng 2 và mất bonus +5 |
| Cột v1 ở Phiếu B mục B8 | Tiến | Sau khi push không sửa được. v2 phải khớp tiêu chí đã ký |

### 2.3. Quy tắc Git cho 4 người cùng một repo

1. Trước khi làm: `git pull --no-rebase --no-edit`. Sau mỗi mục xong: `git add <file của mình> && git commit -m "..." && git push` (đừng dồn).
2. Chỉ `git add` file của mình, không `git add .` hay `git add -A`.
3. **Tắt format on save của VS Code** cho `config/acceptance_criteria.json`. Một dấu cách làm đổi hash. Sau khi ký, không ai mở file đó nữa.
4. Không sửa: `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`, `lab10/helpers.py`, `data/`, `incidents/`, `tests/`, các file khác trong `lab10/`. Hệ thống phát hiện bằng hash (`1 integrity ❌`).
5. Hai người sửa cùng phiếu mà báo conflict: giữ cả hai đoạn, đừng xoá của người kia, báo trong nhóm.
6. `user.name` mọi máy đều là `2A202603504` (README mục 2, bước 2b).
7. Ở phút 125, **chỉ máy Tiến** chạy `git pull ... upstream main` để nhận thẻ rồi push lên `origin`; ba máy kia chỉ `git pull origin main`.

---

## 3. Lấy gì từ Lab 9 (Day 9)

Lab 9 là bài cá nhân, và đề chỉ yêu cầu **chọn một bản làm bản chung**. Cả bàn dùng bản của **Tiến** (`D:\AI26\K5-L3A-DAY09-NguyenTranTien-2A202603504-EvaluationandFailureAnalysis`). Chỉ cần **hai file**:

| File | Dùng cho |
|---|---|
| `docs/PRD_v1.1.md` | Câu 1.1 và 1.2 (mục tiêu). Đề trỏ "PRD v1.1 §2, §3, §6". PRD của Tiến đánh số hơi khác: §2 là phạm vi pilot, §3 là định nghĩa "chạy đúng", §5 là cổng release và người chịu trách nhiệm, §6 là rủi ro còn mở. Lấy nội dung tương ứng, không cần khớp số mục |
| `docs/eval_card.md` | Tham chiếu: ngưỡng đã dùng, cách đọc khoảng tin cậy, giới hạn của MockLLM và 5 seed |

Cách dùng cụ thể:

| Lấy từ Lab 9 | Dùng ở Lab 10 | Cách dùng |
|---|---|---|
| PRD §3: an toàn = 0 (`approval_bypass`, `secret_leak`), `pass_rate ≥ 0.85`, `pass_5 ≥ 0.80` | Câu 1.6, ngưỡng trong `acceptance_criteria.json` | **Tham khảo, không chép.** Tên chỉ số khác (Lab 10 có `pass_k_min`, `wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) và bộ ticket khác (22 ticket, không phải 14). Đặt ngưỡng theo `ops_facts` của Lab 10 rồi giải thích được lúc demo |
| PRD §2 (phạm vi pilot), §5 (ai giữ cổng) | Câu 1.1, 1.2 | Mục tiêu cấp hệ thống cho 1.1. Người chịu trách nhiệm cho 1.2 |
| FM-03 `ticket_trust` (agent tin số ngày khách khai, đè lên DB), ví dụ `E-002@55` | Phiếu B mục B2 (`T-002@55`) và HAZOP B4 | Cùng một kiểu lỗi chìm. Đọc `docs/failure_taxonomy.md` và `docs/trace_case.md` của Lab 9 để viết bảng soát lỗi |
| FM-04…FM-08 (cộng/làm tròn sai, trừ hai lần, điều khoản cũ, hoàn nhầm claim khác, reply sai số tiền) | HAZOP B4, pre-mortem B6 | Gợi ý lý do thất bại kỹ thuật và cổng cho `issue_refund` |
| `eval_card.md`: "5 seed không phát hiện lỗi hiếm: (1−p)^5", "MockLLM không đại diện model thật", "14 item thì CI rộng" | Câu 1.5, B7.2, ba dòng bắt buộc ở C12 (đặc biệt dòng số 3) | Dùng làm lập luận. Số liệu phải gắn với Lab 10 |
| `business_rules.md` (trần theo đơn, approval hết hạn, claim anh em) | Chỉ để hiểu luật; **luật Lab 10 nằm ở `data/world.json` → `policies`** | Không chép sang |

Không copy hai file Lab 9 vào repo Lab 10 (không có chỗ nào trong bài nộp yêu cầu, và `docs/` có file bị khoá hash). Chỉ cần mở ra đọc, hoặc gửi nội dung cần dùng vào nhóm chat.

Lab 9 của Hoàng, Sang, Phương (nếu có) không cần dùng.

---

## 4. Sơ đồ phụ thuộc (ai chờ ai)

```
CP1 (13:30)    Tiến mời người, điền TEAM.md ─────────────► mọi người clone, gắn upstream, unittest
                                    │
CP2 (13:45)    Hoàng (1.2, 1.4) ──┐
               Sang  (1.3)  ──────┼──► TIẾN viết 1.1, 1.6 + acceptance_criteria.json ──► TIẾN KÝ + push (14:30–14:35)
               Phương (1.5)  ─────┘                                                              │
                                                                                                 ▼
CP3 / 2A       Tiến: pull ✓, chạy base (2.1) ──┬──► Phương (B3 dữ liệu), Hoàng (B5 dòng Chất lượng, Chi phí)
(14:35–14:55)  Sang: trace T-002@55 (2.2) ─────┴──► Hoàng (HAZOP: lệch nào "chưa thấy trên trace")
               Phương (2.3) ──► Hoàng (checklist B5 dòng Dữ liệu)
               CẢ BÀN: pre-mortem B6 (14:45–14:55) ───► chọn 2–3 lý do ──► MỞ KHOÁ khối 2B
                                                                      │
CP3 / 2B       Sang: code cổng (2.6) ◄───────────── lý do từ B6 ──────┘
(14:55–15:15)    │ push bản nháp lúc ~15:05
                 ▼
               Phương: pull bản nháp, chạy thử trên máy mình, behavioral test (2.8), báo ca hỏng cho Sang
               Tiến: cổng business (2.9, cần số base của chính Tiến) ──► Hoàng: operations/legal + runbook (2.10, cần số business của Tiến)
                                                                 │
chốt (15:15–15:25) Sang + Hoàng push bản cuối ───► Tiến pull ─► checkpoint ─► eval prepared ─► gate ─► điền B8 (v1) ─► push
                                                                 │
CP4 (15:35)    Tiến nhận thẻ + bốc ► ghi "Thẻ đã bốc" ► chạy grade (prepared)
               Phân tích (Sang + Phương trace; Hoàng C3, C4; Phương C5; cả bàn C6)
               Sửa: Sang (code) / Tiến (business) / Hoàng (operations, legal) / Phương (monitors) ► Tiến chạy lại mỗi lượt
                                                                 │
CP5 (16:35)    Tiến C12 (v2) + ba dòng ► Hoàng submission.json ► Tiến lệnh 7 ► Tiến đẩy bài (trước 17:30)
               Mọi người: mục cá nhân (exit ticket, ghi AI), nộp LMS trước 11:59 sáng hôm sau
```

### Ma trận phụ thuộc rút gọn

| Việc | Chờ ai | Ảnh hưởng tới ai |
|---|---|---|
| Tiến ký tiêu chí | Hoàng (ngưỡng ops, điều kiện dừng), Sang (độ khả thi `pass_rate`, `pass_k`), Phương (1.5) | **Cả bàn**: không ai chạy eval được trước khi Tiến push và mọi người pull |
| Tiến chạy base (2.1) | Tiến đã ký + push | Phương (B3), Hoàng (B5, số hàng chờ cho `operations`), Sang (biết ca nào hỏng) |
| Hoàng HAZOP (B4) | Sang (trace `T-002@55`) | Pre-mortem B6, cổng của Sang |
| Pre-mortem B6 | Cả bàn xong 2A | **Sang** (chọn cổng nào để code), Tiến/Hoàng (con số nào đặt) |
| Sang code cổng | B6 xong; số `business` của Tiến nếu cổng đọc `ctx.gates` | Phương (không có code thì không kiểm chéo được), Tiến (không có code thì không chạy `after`), Hoàng (cổng nào có thì runbook phải khớp) |
| Phương kiểm chéo cổng | Bản nháp của Sang | Sang (báo ca hỏng sớm, trước khi Tiến chốt) |
| Tiến cổng `business` | Số base của chính Tiến | Hoàng (runbook ghi phạm vi, chi phí khi thêm người), Sang (cổng đọc trần hoàn) |
| Hoàng cổng `operations`, `legal`, runbook | Tiến (`pilot_scope`, ngân sách) | Tiến (số người trực làm đổi chi phí và ROI so với ngưỡng đã ký), Tiến (`checkpoint` cần `operations.pic` không trống) |
| Tiến `checkpoint` | **Sang, Hoàng đã push bản cuối; Phương đã kiểm chéo** | Mọi thứ ở vòng 2 (mốc `prepared`) |
| Tiến điền B8 (v1) | Hoàng (PIC ký, ngày quyết định lại) | `submission.json` (`decision_v1`), C12 |
| Tiến grade trước khi sửa | Thẻ đã nhận; `Thẻ đã bốc:` đúng số | **Tất cả** phân tích vòng 2 |
| Sang sửa code vòng 2 | C2 và C6 xong | Tiến (chạy lại), Phương (kiểm regression), C7, C9 |
| Tiến/Hoàng đổi config vòng 2 | C6 xong, biết nguyên nhân ở "người/tiền/phạm vi" | Tiến (phải chạy lại, mỗi lần chỉ đổi MỘT thứ) |
| Phương chỉ số theo dõi (3.6) | Sang (sự kiện `ctx.log` nào) | `grade` (thiếu thì `6 monitor ❌`), C8, C10 (dấu hiệu phải là metric có thật) |
| Tiến C12 (v2) | Mã 3 mốc (Tiến tự có), Hoàng (dòng vượt trần), Sang (giảm hay ngăn), Phương (dòng 3) | `submission.json`, lệnh 7 |
| Tiến lệnh 7 | Hoàng điền `submission.json`; mọi phiếu đủ mục | Việc đẩy bài |

---

## 5. Chi tiết theo mốc thời gian

Ký hiệu: **[T]** Tiến · **[H]** Hoàng · **[S]** Sang · **[P]** Phương.

### CP1 · 13:30–13:45 · Cài đặt

| Việc | Ai | Làm ở đâu / thế nào | Chờ ai | Ảnh hưởng |
|---|---|---|---|---|
| **Xác nhận Public hay Private với Lab Coach** | [T] | Slide ghi "Chọn **Public**, không cần mời team chấm", nhưng cùng slide lại ghi lỗi thường gặp "Để repo Private, team chấm không mở được link", và README mục 2 ghi **Private** + mời team chấm. Ba nguồn mâu thuẫn. Hỏi Lab Coach rồi làm theo, và ghi lại câu trả lời | Lab Coach | Nếu repo Private mà team chấm không vào được thì bài không được chấm |
| Mời Hoàng, Sang, Phương (quyền Write) và (nếu cần) tài khoản team chấm (Read) | [T] | GitHub → Settings → Collaborators | Lab Coach cho tên tài khoản | Ba bạn không push được nếu chưa được mời |
| Chấp nhận lời mời, clone, gắn `upstream`, đặt `user.name = 2A202603504`, email `2A202603504@example.com` | Cả 4 | README mục 2, bước 2 đến 2b | [T] mời xong | Danh tính Git đồng nhất |
| Chạy `python -m unittest discover -s tests` thấy `Ran 13 tests … OK` | Cả 4 | Trên Windows dùng `python` nếu `python3` không chạy | | |
| Commit và push [TEAM.md](TEAM.md) và file này | [T] | `git add TEAM.md chia-viec.md` | | Ba bạn `git pull` để thấy vai |
| Chốt dùng **PRD v1.1 và eval card của Tiến** (mục 3) | Cả bàn | Tiến gửi hai file vào nhóm chat | | [T] (1.1), [H] (1.2) |

### CP2 · 13:45–14:35 · Phiếu A rồi ký

**Chưa ai chạy `eval`** (máy cũng sẽ từ chối). Trong lúc này [S] và [P] đọc `lab10/guards.py`, `lab10/helpers.py`, `docs/guide.md` Phụ lục C, `data/world.json`, và `docs/failure_taxonomy.md` của Lab 9 để chuẩn bị vòng cổng.

| Việc | Ai | Làm ở đâu / thế nào | Chờ ai | Ảnh hưởng |
|---|---|---|---|---|
| Câu 1.1: một mục tiêu cấp hệ thống, khác "model trả lời đúng" | [T] | Phiếu A, A1. Dựa PRD v1.1 của Tiến | PRD | Gốc của câu tiêu chí 1.6 |
| Câu 1.2: mục tiêu nhìn từ chị Oanh (kế toán đối soát) và chị Hạnh (trưởng ca CSKH) | [H] | Phiếu A, A1. Dựa PRD và `data/world.json` → `staff` | PRD | [T] dùng để chọn `queue_stuck_max` (chị Hạnh) |
| Câu 1.3: offline metric cho MỘT bước của agent | [S] | Phiếu A, A2, cột "Offline". Ví dụ mẫu trong phiếu (đừng chép). Gợi ý bước "chọn độ trễ" hoặc "ghi lỗi hãng", liên hệ FM-03 của Lab 9 | | [S] dùng lại bảng ba ô này cho C8 |
| Câu 1.4: telemetry production (không nhãn, có khung thời gian, ngưỡng báo động) | [H] | Phiếu A, A2, cột "Telemetry" | | Gợi ý cho Runbook 2 (B7.5) |
| Câu 1.5: đọc khoảng tin cậy, chọn (a)–(d) | [P] cầm bút, cả bàn bàn | Phiếu A, A3. Số 0,98 và [0,94; 1,0] là số minh hoạ. Có thể dùng ý "(1−p)^5" từ eval card Lab 9 | | Không ảnh hưởng file khác |
| **Câu 1.6**: câu "Nếu … thì chúng tôi sẽ …" cho 5 chỉ số + 1 nên có, 2 câu ranh giới đầu ra, 4 câu soát | [T] viết; [H] góp số ops; [S] góp độ khả thi | Phiếu A, A4. Xem `config/acceptance_criteria.example.json` nhưng **không chép ngưỡng** (rubric C1 trừ điểm) | 1.3, 1.4 và ý kiến [H], [S] | Quyết định **mọi** phép so sánh về sau, `decision_rule` v1, v2 |
| Điền `config/acceptance_criteria.json`: `team` = `K5-L3A-DAY10-NgonThia-PoCtoPilotGate1` (giống hệt tên repo), `signed_by`, 5 ngưỡng `required`, `escalation_rate_max`, `business_ops` (`cost_per_ticket_vnd_max`, `roi_min`, `queue_stuck_max`), `stop_condition`, 4 dòng `decision_rule` | [T] | Gợi ý đề: 3 chỉ số an toàn có thể để 0. Chi phí, ROI: xem `data/world.json` → `ops_facts` (làm tay 10.000 đ/ticket; LLM không quá 1.500 đ/ticket; một người duyệt 6 ca/giờ; phí giữ chỗ 30.000 đ/người/ca) | | **Điều kiện qua** + rubric C1 (15 điểm). Ngưỡng quá chặt thì khó qua, quá lỏng thì bị hỏi lúc demo |
| **Ký** (14:30–14:35): `python -m lab10.criteria sign`, rồi chạy **đúng dòng git** máy in ra (`git add ... && git commit -m 'Sign acceptance criteria' && git push -u origin main`) | [T] | Máy Tiến. Một lần | [H], [S] đồng ý ngưỡng | **Chặn cả bàn**. Sai `team` thì −5 điểm |
| Điền A5 (giờ ký, mã commit, đã push chưa) | [T] | Phiếu A, A5 | Đã ký | |
| `git pull` lấy tiêu chí đã ký về | [S], [H], [P] | 14:35 | [T] push xong | Cần để chạy thử trên máy mình |

### CP3 · 14:35–14:55 · Khối 2A · Đo, rủi ro (chưa sửa code hay config)

| Việc | Ai | Làm ở đâu / thế nào | Chờ ai | Ảnh hưởng |
|---|---|---|---|---|
| **Câu 2.1**: chạy base, đọc ngưỡng `[CHƯA]`, khối "kinh doanh và vận hành", khối "theo kho và hãng"; lý lẽ tự chặn vs người duyệt | [T] | `python -m lab10.eval --suite base --stage base --note "baseline"` rồi `python -m lab10.gate --run runs/<mã>/report.json`. Phiếu B, B1 và dòng 1 của B0. **Gửi mã lần chạy và ảnh output vào nhóm ngay** | [T] đã ký | [P] (B3), [H] (số hàng chờ, checklist), [S] (ca nào hỏng) |
| **Câu 2.2**: dò `T-002@55`, bảng soát lỗi | [S] | `python -m lab10.trace --suite base --ticket T-002 --seed 55`. Phiếu B, B2. Xếp mỗi lỗi vào giới hạn hệ thống / ngữ cảnh / **chìm**. Đối chiếu FM-03 của Lab 9 | [T] ký xong | [H] đọc để biết nhánh nào "đã thấy" khi làm HAZOP |
| **Câu 2.3**: bản đồ dữ liệu và một ví dụ drift | [P] | Phiếu B, B3. Mở `data/world.json`: `policies`, `orders[].parcels`, `ops_limits`, `ops_facts`. [T] đọc lại câu "con số nào của Bản tiêu chí bị ảnh hưởng" | | [H] cần cho checklist dòng Dữ liệu; C3.5 ở vòng 2 mở lại mục này |
| **Câu 2.4a**: HAZOP một vòng trên một tool ghi (≥ 3 dòng, một dòng là nhánh chưa thấy trên trace, thêm ≥ 2 dòng ngoài kỹ thuật) | [H] | Phiếu B, B4. Gợi ý tool `issue_refund`. Dòng ngoài kỹ thuật: người duyệt, ngân sách, phạm vi pilot, dữ liệu gửi bên thứ ba | Trace của [S] | B6 và cổng của [S] |
| **Câu 2.4b**: checklist 9 nhóm, **mỗi dòng một PIC có tên người** | [H] điền, mỗi người nhận PIC | Phiếu B, B5. Gợi ý PIC: 1 Chất lượng [T] · 2 Dữ liệu [P] · 3 Bảo mật [S] · 4 Quyền hạn [S] · 5 Hiệu năng [H] · 6 Chi phí [T] · 7 Vận hành [H] · 8 Con người, pháp lý [H] · 9 Quyết định [T] | [T] (mã lần chạy), [P] (B3), [S] (B2) | Thiếu PIC có tên thì rubric C2 trừ |
| **Câu 2.5**: pre-mortem 4 lăng kính, chọn 2–3 lý do thành cổng | Cả bàn. [T] chủ trì, [S] ghi lên phiếu | Phiếu B, B6. 2 phút im lặng viết 2 lý do mỗi người → đọc vòng tròn → xếp lăng kính (kỹ thuật, kinh doanh, con người và vận hành, pháp lý; lăng kính trống phải viết thêm) → chọn 2–3 lý do | Xong 2.1–2.4 | **Mở khoá khối 2B**: [S] sẽ code đúng các lý do này |

Xong khối này khi: có mã lần chạy base; `T-002@55` được xếp loại lỗi; pre-mortem đủ bốn lăng kính.

### CP3 · 14:55–15:15 · Khối 2B · Dựng cổng phòng ngừa

| Việc | Ai | Làm ở đâu / thế nào | Chờ ai | Ảnh hưởng |
|---|---|---|---|---|
| **Câu 2.6**: code 2–3 cổng. Mỗi cổng ứng với một lý do B6 hoặc một dòng HAZOP | [S] | `lab10/guards.py`: `pre_guard(ctx)` (trước khi đọc ticket) hoặc `write_gate(ctx, action)` (trước mỗi lệnh ghi). Đặt kiểm tra **trước dòng `return Verdict.allow()` cuối hàm**. Dùng `Verdict.allow/deny/escalate/modify`. Hàm tra cứu: `lab10/helpers.py`. **Không viết theo mã ticket hay câu chữ cụ thể** (test ẩn bắt). Đọc ngưỡng từ `ctx.gates`, không gõ cứng số. **Push bản nháp lúc ~15:05**, bản cuối trước 15:12 | B6 | [P] kiểm chéo; [T] chạy chính thức; [H] cổng nào có thì runbook phải khớp |
| **Kiểm chéo cổng**: pull bản nháp của [S], chạy `eval --stage after` và `unittest` trên máy mình, báo ca mới hỏng | [P] | Phiếu B, B7.1 cột "ca đang đúng nào bị hỏng" | Bản nháp của [S] | [S] sửa sớm trước khi [T] chốt |
| Điền Phiếu B, B7.1 (bảng 2–3 cổng) | [S] điền cột cổng; [T] điền mã lần chạy `base · after` | Phiếu B, B7.1 | [T] chạy bản chính thức | Rubric C3 |
| **Câu 2.7**: 2 bước tránh rò rỉ dữ liệu (không chỉnh trên chính bộ dùng để chấm) | [P] | Phiếu B, B7.2. Gắn với 22 ticket bộ nền, gói sự cố, bài kiểm tra ẩn. Có thể dẫn ý "ngưỡng chọn sau khi nhìn variant công khai" của eval card Lab 9 | | Giữ [S] khỏi "overfit" bộ nền |
| **Câu 2.8**: behavioral test: một tính chất + hai ticket hiểm chạy bằng `--adhoc` | [P] viết; [H] (người không code) cùng thử | `python -m lab10.trace --suite base --stage after --adhoc "..." --order O-10xx --customer C-xx`. Phiếu B, B7.3. Giữ 2 ticket này cho demo | Code của [S] | Bằng chứng cổng không phụ thuộc câu chữ cụ thể |
| **Câu 2.9**: cổng kinh doanh: `daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`, **mỗi số một câu lý do có số** | [T] | `config/operating_gates.json` mục `business` và Phiếu B, B7.4. Số lấy từ `ops_limits` (ngân sách hoàn tự động 2.000.000 đ/ngày, 300.000 đ/khách/ngày, LLM 1.500 đ/ticket), `ops_facts`. `roi_min` phải **khớp tiêu chí đã ký** | Báo cáo base | [H] viết runbook dựa vào các số này; cổng [S] đọc `daily_refund_cap_vnd` |
| **Câu 2.10 (a)**: cổng vận hành và pháp lý | [H] | `operating_gates.json` mục `operations` (`pic`, `approver_id`, `reviewers_on_shift`, `review_capacity_per_hour`, `max_queue_wait_minutes`, `stop_conditions`, `alert_channel`) và `legal` (`pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause`). `pic`, `approver_id` là **mã nhân viên trong `world.json`** (ví dụ `NV-TUNG`, `NV-HANH`). **`pic` không được trống** | Số `business` của [T] | Thêm người trực làm chi phí mỗi ticket tăng 30.000 đ/người/ca. Cổng `pii` và `carrier_fault` tự có hiệu lực, [S] không cần code lại |
| **Câu 2.10 (b)**: runbook phần 1–3 và mục **Giờ cao điểm** | [H] | Phiếu B, B7.5 và B7.6. **Mọi số phải khớp `operating_gates.json` và report** (rubric C3 trừ nếu lệch) | Số của [T] và [H] | Người trực giữa đêm đọc đúng tờ này |
| Chạy chính thức `eval --stage after`, `unittest` | [T] | `python -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."` | Push của [S], [H] | Không có ca mới hỏng so với base mới được chốt |

### Chốt · 15:15–15:25 · Cổng vòng 1 và quyết định v1

Làm **đúng thứ tự**; [T] chỉ bắt đầu khi [S] và [H] đã báo "push bản cuối" và [P] đã báo "kiểm chéo xong".

| # | Việc | Ai | Lệnh / nơi làm |
|---|---|---|---|
| 1 | Push bản cuối: `guards.py` [S], `operations`/`legal` [H] (`business` của [T] đã có) | [S], [H] | Báo vào nhóm "đã push" |
| 2 | Kiểm chéo lần cuối, báo "không có ca hỏng" | [P] | |
| 3 | `git pull`, chạy unittest, kiểm `operations.pic` không trống | [T] | |
| 4 | **Chốt**: `python -m lab10.checkpoint` | [T] | In `ĐÃ CHỐT cổng vòng 1 …`. Từ đây không sửa `guards_round1.py`, `operating_gates.round1.json`, `round1.lock` |
| 5 | `eval --suite base --stage prepared`, rồi `gate --run runs/<mã>/report.json` | [T] | Gửi mã lên nhóm |
| 6 | **Điền cột v1** ở B8: một quyết định, ba bằng chứng có mã lần chạy, dòng `decision_rule` khớp, kho/hãng xấu nhất, ngày quyết định lại, PIC ký | [T] cầm bút, cả bàn chốt; [H] cho PIC ký và ngày quyết định lại | Phiếu B, B8. Chọn **Tiếp tục** khi còn vượt trần hoặc ngưỡng chưa đạt là quyết định **không đạt** |
| 7 | Commit và push (lệnh ở cuối B8) | [T] | `git add lab10/guards.py lab10/guards_round1.py config/operating_gates.json config/operating_gates.round1.json config/round1.lock templates/form-b-evaluation-gates.md` rồi commit `"LAB 10: chốt cổng vòng 1, quyết định v1"` |

Lưu ý: ba người kia phải `pull` trước khi sửa tiếp phiếu B.

### Nghỉ · 15:25–15:35

Cả bàn `git pull`. [H] rà các phiếu A, B còn mục nào trống. [S], [P] đọc lại `docs/guide.md` Phụ lục C, D.

### CP4 · 15:35–16:35 · Sự cố

**15:35–15:45 · Nhận thẻ, đo trước khi sửa (câu 3.0)**

| Việc | Ai | Làm thế nào | Chờ ai | Ảnh hưởng |
|---|---|---|---|---|
| Bốc thẻ S1–S8 (mỗi cặp bàn một người) | [T] | Bàn **chỉ làm đúng thẻ này**, không mở thẻ của bàn khác | Lab Coach báo "đã phát" | Quyết định ai nặng việc ở vòng 2 (bảng "phần riêng theo thẻ") |
| Nhận thẻ: `git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main` | **Chỉ [T]**, rồi push lên origin | Kiểm `ls incidents/` thấy `S1` … `S8` và `incident-cards.md` | | Ba máy kia chỉ `git pull origin main` |
| Ghi số thẻ vào dòng `Thẻ đã bốc:` đầu Phiếu C và dòng `Thẻ sự cố đã bốc` ở TEAM.md | [T] | Đúng số, ví dụ `S3` | Đã bốc | `grade` báo "KHÔNG KHỚP" nếu sai |
| `python -m lab10.grade --incident Sx` khi **chưa sửa gì**; điền C0 | [T] | Thấy `1 integrity ✅` và `Thẻ đã bốc … khớp` | Thẻ đã nhận | Mốc `prepared` là gốc so sánh với `after` |
| C1: cổng vòng 1 đỡ được gì, dòng nào vượt trần, mở lại pre-mortem bằng bút khác màu | [P] cầm bút, [H] góp lăng kính con người và pháp lý | Phiếu C, C1 | Report của [T] | Bonus +5 nếu `prepared` gần `after` |

**15:45–16:05 · Phân tích hazard (câu 3.1–3.4)**

| Việc | Ai | Làm thế nào |
|---|---|---|
| C2: dò ≥ 2 ticket hỏng theo **hai kiểu khác nhau**, bảng soát lỗi (≥ 2 lỗi nguồn khác nhau, ≥ 1 lỗi chìm), tác hại (cho ai, đo bằng gì, bao nhiêu ở base) | [S] cầm bút, [P] dò ticket thứ hai | `python -m lab10.trace --suite Sx --ticket Sx-01 --seed 11`, rồi ticket khác. Phiếu C, C2 |
| C3: phần riêng theo thẻ (bảng dưới) | [H] chính; [P] với S1, S3, S5 | Phiếu C, C3 |
| C4: HAZOP của thẻ (≥ 3 dòng, một dòng chưa thấy trên trace; **không ghi đè HAZOP vòng 1**) | [H], [S] chỉ tool và tham số | Phiếu C, C4 |
| C5, câu 3.2: một specification mà vi phạm sẽ gây tác hại, kiểm được bằng code hoặc một số trong report | [P] | Phiếu C, C5 |
| C5, câu 3.3: một giả định về môi trường sai ngoài thực tế (thứ nằm ngoài phần mềm) | [H] | Phiếu C, C5. Là nguồn cho dòng bắt buộc số 1 ở v2 |
| C6: fault tree trước khi sửa: đỉnh là tác hại, ≥ 2 nhánh ở 2 tầng khác nhau (kỹ thuật / kinh doanh / con người), **mỗi lá có bằng chứng** (`ticket@seed` hoặc dòng report) | Cả bàn, [P] vẽ | Phiếu C, C6. Thiếu bằng chứng ở lá thì rubric C5 trừ |

Phần riêng theo thẻ (C3), điền **một** dòng theo số bốc:

| Thẻ | Điền gì | Ai |
|---|---|---|
| S1 | C1 + C3.5 (mở lại bản đồ dữ liệu, trường `parcel`) | [P] (là chủ B3), [H] đọc |
| S2 | C3.1 mức kiểm soát của con người ở từng lệnh ghi | [H] |
| S3 | C1 + C3.5 (bảng `policies`, `delay_cause`) | [P] |
| S4 | C1 + Giờ cao điểm ở B7.6 (bút khác màu). **Bỏ qua C3** | [H] |
| S5 | C1 + C3.5 + C8 cho con số chi phí mỗi ticket theo kho | [P] |
| S6 | C3.2 hình dung của người và của hệ thống (đơn vị chịu lỗi: đơn / kiện / chặng / tài xế) | [H], [S] đọc trace `parcels` |
| S7 | C3.3 hiệu chỉnh lòng tin (người đặt hàng, người nhận) | [H] |
| S8 | C3.4 (nhân viên duyệt, trưởng ca) + một dòng "hoàn trên hạn mức" ở C3.1 | [H] |

**16:05–16:30 · Sửa đúng chỗ (câu 3.5, 3.6)**

Tuỳ nguyên nhân, chỗ sửa khác nhau. **Mỗi lần chạy chỉ đổi MỘT thứ** (`--note "đổi MỘT thứ: ..."`), nên các sửa đổi xếp hàng qua máy [T].

| Nguyên nhân (đọc từ fault tree C6) | Sửa ở đâu | Ai |
|---|---|---|
| Kỹ thuật: dữ liệu, tool, quyền hạn | `lab10/guards.py` (thêm nhánh trong `write_gate` / `pre_guard`, giữ các cổng vòng 1) | [S] |
| Tiền, phạm vi, ngân sách | `operating_gates.json` mục `business` (`pilot_scope`, `daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`) | [T] |
| Người, quy trình, pháp lý | `operating_gates.json` mục `operations` (`reviewers_on_shift`, `review_sampling_pct`, `decision_note`, `max_queue_wait_minutes`) và `legal` | [H] |
| **Chỉ số theo dõi mới** (bắt buộc ≥ 1; `escalation_rate` có sẵn không tính) | `lab10/monitors.py`: thêm hàm phía trên dict `MONITORS` (nhận `trials`, trả về một số), đăng ký `"tên": hàm`. Phiếu C, C8 | [P]. Cần [S] cho biết `ctx.log` nào cổng đã ghi vào trace |

Quy trình mỗi lượt sửa:

1. Người sửa push và nhắn nhóm.
2. [P] kiểm chéo nhanh trên máy mình (`eval --suite base --stage after`) và báo ca hỏng.
3. [T] `git pull`, chạy `python -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."`.
4. [T] chạy thêm `python -m lab10.eval --suite base --stage after --note "kiểm lại bộ nền sau khi sửa"` (kiểm regression) và `python -m lab10.grade --incident Sx`.
5. [T] báo kết quả. Cần thấy `1 integrity ✅`, `3 visible ✅`, `5 regression ✅`, `6 monitor ✅`.

**Cảnh báo (rubric C4, 25 điểm):**
- Không chặn hết, không thu hẹp `pilot_scope` về 0, không xếp thật nhiều người trực. Report đo cả độ phủ, chi phí, ROI. `visible` và `regression` chỉ ✅ khi độ phủ pilot > 0.
- Không viết code theo mã ticket (`Sx-01`) hay câu chữ cụ thể. Test ẩn dùng đơn, khách, cách viết, ngày khác.

**16:30–16:35 · Ghi phần đã sửa (câu 3.7)**

| Việc | Ai | Phiếu C |
|---|---|---|
| C7: bảng sửa (nhánh → nguyên nhân → chỗ sửa → tầng → **giảm hay ngăn** → mã lần chạy) | [S] cột code, [T] cột business, [H] cột operations/legal | C7 |
| C8: chỉ số theo dõi mới (ba ô) | [P] | C8 |
| C9: fault tree sau khi sửa (nút `VÀ [gate … hỏng]`, nhánh còn hở) | [S] vẽ, [H] soát | C9 |
| C10: ≥ 1 dòng risk register (cột "Dấu hiệu" phải là metric có trong `monitors.py` hoặc report) | [T] cầm bút (vì "mỗi dòng phải đổi được một quyết định"), [P] cho metric | C10 |
| C11: cập nhật checklist 9 nhóm (một PIC có tên mỗi dòng), **Runbook 4 và 5** | [H] | C11 |

### CP5 · 16:35–17:30 · Quyết định v2, demo, nộp

| Việc | Ai | Làm thế nào | Chờ ai | Ảnh hưởng |
|---|---|---|---|---|
| **C12: quyết định v2**: đổi hay giữ so với v1, vì con số nào; mã 3 mốc; dòng `decision_rule` khớp; "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ" | [T] cầm bút, cả bàn chốt | Phiếu C, C12. **Commit ký và hash chốt vòng 1 phải giống v1** | [H] (dòng vượt trần), [S] | `submission.json`, điều kiện qua |
| **Ba dòng bắt buộc** (có số, không chung chung): ① giả định môi trường có thể sai ② cổng chỉ GIẢM hay NGĂN, vì sao ③ cần đo lại gì ở pilot thật vì data là mock | [T] chủ trì; ① [H]; ② [S]; ③ [P] (dùng ý từ eval card Lab 9) | C12. Rubric C6: chung chung, không gắn số bị trừ | | Chép nguyên sang `submission.json` mục `three_lines` |
| Điền `submission/submission.json`: `team` (giống tiêu chí), `members` (dạng `"NguyenTranTien-2A202603504"`, đủ 4 người, khớp TEAM.md), `incident`, `decision_v1`, `decision_v2`, `three_lines` | [H] | Quyết định chỉ nhận: `Tiếp tục`, `Thu hẹp`, `Cải tiến thêm`, `Dừng`. Thiếu MSSV hoặc không khớp TEAM.md thì −5 | C12 xong | Lệnh 7 |
| **Lệnh 7**: `python -m lab10.check_submission --collect`, sửa từng dòng `[THIẾU]` theo `->`, chạy lại tới `ĐỦ THÀNH PHẦN` | [T] | Máy Tiến, trên đúng code và config cuối cùng. Phiếu còn nguyên mẫu cũng báo THIẾU | `submission.json` của [H]; mọi phiếu đủ mục | Điều kiện qua |
| **Demo** 5 phút/bàn: chiếu 3 cột `base · prepared · after` của report lệnh 6; nói cổng vòng 1 đỡ được gì, phần sửa là code/con số/người, quyết định v2 | [T] mở đầu và nói quyết định; [S] nói code; [H] nói con số và người; [P] nói chỉ số theo dõi và ticket hiểm | | | Lab Coach hỏi soi cho C5, C6 |
| **Phản biện**: bàn kia đưa ticket hiểm hoặc đổi một con số trong `operating_gates.json` | [T] chạy; [H] hoặc [S] trả lời | | | |
| **Sau demo: trả mọi con số đã đổi thử về bản v2**, chạy lại `grade --incident Sx` và lệnh 7 | [T] chạy; người đổi số trả lại | Quên thì lệnh 7 báo "báo cáo không chạy trên đúng code và config hiện tại" | | |
| Đẩy bài: `git add -u && git add submission templates TEAM.md && git commit -m "LAB 10: bài nộp" && git push -u origin main` | [T] | Chỉ push lên `origin`, **không bao giờ lên `upstream`**. **Trước 17:30** | Lệnh 7 xong | |
| Viết **exit ticket** và ghi **đã dùng AI cho phần nào** trong mục cá nhân TEAM.md (RULES.md bắt buộc nếu có dùng AI) | Mỗi người, mục của mình | Đủ 4 mục: Phần việc, Đóng góp, Bằng chứng (mã commit, mã chạy, dòng phiếu), Exit ticket | | Thiếu mục cá nhân thì người đó **không có điểm cá nhân** |
| Gửi link repo cho team chấm | [T] | Theo cách Lab Coach hướng dẫn | | |
| **Nộp link repo trên LMS** bằng tài khoản cá nhân | **Cả 4 người, mỗi người một lần** | Hạn **11:59 sáng hôm sau** (GMT+7) | | **Ai không nộp thì không có bài** |

---

## 6. Việc của từng người (tóm tắt để in ra)

### Tiến · Sản phẩm và kinh doanh · trưởng nhóm · máy chạy chính
- [ ] Hỏi Lab Coach Public/Private; mời 3 bạn (+ team chấm nếu cần); TEAM.md; gửi PRD v1.1 và eval card Lab 9
- [ ] Phiếu A: 1.1, 1.6 (4 câu soát), ranh giới đầu ra; điền và **ký** `acceptance_criteria.json`, push ngay
- [ ] Phiếu B: B0, B1 (chạy base), B7.4 + mục `business`, B8 (v1)
- [ ] Lệnh 2, 4, 5, 6, 7 trên máy mình; nhận thẻ từ `upstream`; bốc thẻ; ghi `Thẻ đã bốc:`
- [ ] Phiếu C: C0, C10, C12 (v2); đẩy bài; nộp LMS; mục cá nhân TEAM.md
- Chờ: Hoàng, Sang (ngưỡng ký); Sang, Hoàng (bản cuối trước chốt); Phương (kiểm chéo)
- Làm chậm: **cả bàn** (nếu ký trễ hoặc chạy chậm)

### Hoàng · Vận hành và pháp lý
- [ ] Phiếu A: 1.2, 1.4
- [ ] Phiếu B: B4 (HAZOP), B5 (checklist 9 nhóm, đủ PIC có tên), B7.5 (mục `operations`, `legal`, runbook 1–3), B7.6 (giờ cao điểm)
- [ ] Phiếu C: C3 (phần riêng theo thẻ), C4 (HAZOP thẻ), C5 (3.3), C7 cột operations/legal, C11 (checklist, runbook 4–5)
- [ ] Điền `submission/submission.json`
- [ ] Mục cá nhân TEAM.md, nộp LMS
- Chờ: Sang (trace), Tiến (số base, `business`)
- Làm chậm: Tiến (PIC ký ở B8; `checkpoint` cần `operations.pic` không trống; lệnh 7 cần `submission.json`)

### Sang · Kỹ sư cổng (code)
- [ ] Phiếu A: 1.3
- [ ] Phiếu B: B2 (trace `T-002@55`), B7.1 (2–3 cổng trong `guards.py`)
- [ ] Phiếu C: C2 (bảng soát lỗi), sửa `guards.py`, C7 cột code, C9
- [ ] Mục cá nhân TEAM.md, nộp LMS
- Chờ: Tiến ký, B6 (pre-mortem), Phương báo ca hỏng
- Làm chậm: Phương (không có code thì không kiểm chéo), Tiến (không chạy được `after`, `checkpoint`), Hoàng (runbook khớp cổng)

### Phương · Kỹ sư cổng (dữ liệu, kiểm thử, chỉ số)
- [ ] Phiếu A: 1.5
- [ ] Phiếu B: B3 (bản đồ dữ liệu, drift), B7.2, B7.3 (behavioral test)
- [ ] Kiểm chéo `guards.py` của Sang trên máy mình trước khi Tiến chốt
- [ ] Phiếu C: C1, C5 (3.2), C6 (vẽ fault tree), C8 + `lab10/monitors.py`
- [ ] Mục cá nhân TEAM.md, nộp LMS
- Chờ: Tiến chạy base; Sang push bản nháp; Sang cho biết sự kiện `ctx.log`
- Làm chậm: Hoàng (checklist dòng Dữ liệu), Sang (báo ca hỏng chậm thì Sang sửa chậm), `grade` (thiếu monitor thì `6 monitor ❌`)

---

## 7. Điểm rubric và người chịu trách nhiệm chính

| Tiêu chí | Điểm | Người chịu trách nhiệm | Hay mất điểm ở |
|---|---:|---|---|
| C1 Tiêu chí và cách đo (Phiếu A, 1.1–1.6) | 15 | Tiến (Hoàng, Sang, Phương góp) | Chép ngưỡng từ file example; thiếu `business_ops` hoặc `decision_rule` |
| C2 Rủi ro trước sự cố (B1–B6) | 15 | Hoàng (Phương, Sang, Tiến) | HAZOP < 3 dòng hoặc không có dòng ngoài kỹ thuật; checklist thiếu PIC có tên; pre-mortem thiếu lăng kính |
| C3 Cổng vòng 1 và quyết định v1 | 15 | Sang (code), Hoàng (runbook), Tiến (B8) | Không có mốc `prepared`; runbook không khớp số trong config |
| C4 Kết quả máy đo và test ẩn | 25 | Sang, Phương, Tiến | Chặn hết, thu hẹp về 0, quá nhiều người trực, regression, xử lý riêng theo mã ticket |
| C5 Phân tích và sửa sự cố | 20 | Cả bàn | Fault tree thiếu bằng chứng ở lá; không có chỉ số theo dõi mới; thiếu risk register |
| C6 Quyết định v2 và ba dòng | 10 | Tiến | Ba dòng chung chung, không có số; không nói đổi hay giữ so với v1 |

Điều kiện qua (không đạt thì không được tính điểm): ký **trước** lần đo đầu và không đổi; file khoá còn nguyên (`1 integrity ✅`); v2 khớp bằng chứng và tiêu chí đã ký; lệnh 7 in `ĐỦ THÀNH PHẦN`. Trừ chung: sai tên repo hoặc `team` không khớp −5; `members` thiếu MSSV hoặc không khớp TEAM.md −5.

---

## 8. Lỗi hay gặp (đọc trước khi bắt đầu)

| Lỗi | Phòng tránh |
|---|---|
| Chạy `eval` trước khi ký | Máy từ chối. Ký trước, push rồi mới chạy |
| `team` trong JSON khác tên repo | Luôn là `K5-L3A-DAY10-NgonThia-PoCtoPilotGate1` |
| Mở và lưu lại `acceptance_criteria.json` sau khi ký | Report báo `criteria ❌`. Khôi phục bằng `git restore --source=<mã commit ký> -- config/acceptance_criteria.json config/acceptance_criteria.lock` |
| Sửa `guards_round1.py` hoặc `operating_gates.round1.json` | `integrity ❌`. Chỉ sửa `guards.py` và `operating_gates.json` |
| Chạy `checkpoint` khi chưa đủ push | Chốt thiếu cổng, không chốt lại được |
| Nhận thẻ trên 4 máy | Chỉ máy Tiến nhận từ `upstream` |
| Dùng mã lần chạy từ máy khác để ghi phiếu | Mã đó không có trong `submission/runs/` của máy Tiến. Dùng mã từ máy Tiến |
| Quên trả số đã đổi thử sau demo | Chạy lại `grade` và lệnh 7 trước khi đẩy bài |
| Cổng viết theo `T-002` hoặc câu chữ cụ thể | Test ẩn bắt. Viết theo nguồn sự thật (`helpers.db_delay_days`, `entitlement_vnd`…) |
| Cổng "cho chắc thì chuyển người" ở mọi chỗ | Hàng chờ ùn, chi phí tăng. Report đo cả hai |
| Một người làm hết, ba người ngồi xem (slide nhắc) | Mỗi người có phiếu và file riêng ở mục 1 |
| Commit API key hoặc `.env` | Lab không cần khoá API |
