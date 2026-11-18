# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): NgonThia
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-NgonThia-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S6

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai trò | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Trần Tiến | 2A202603504 | Sản phẩm và kinh doanh (kiêm giữ máy chạy lệnh chính) | ✅ |
|   2 | Nguyễn Vũ Hoàng | 2A202603491 | Vận hành và pháp lý | |
|   3 | Nguyễn Ngọc Sang | 2A202603444 | Kỹ sư cổng (phụ trách `guards.py`) | |
|   4 | Đào Thị Thu Phương | 2A202603457 | Kỹ sư cổng (phụ trách dữ liệu, kiểm thử, `monitors.py`) | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenTranTien-2A202603504

### Phần việc phụ trách

Sản phẩm và kinh doanh, trưởng nhóm, giữ máy chạy lệnh chính (các lệnh có mã lần chạy đều chạy trên máy này vì thư mục `runs/` không lên GitHub).

- Đề: câu 1.1 · 1.6 · 2.1 · 2.9 · quyết định v1 (B8) và v2 (C12) · ba dòng bắt buộc (chủ trì).
- Phiếu: A mục A1 (1.1), A4 (1.6), A5 · B mục B0, B1, B7.4, B8 · C mục C0, C1, C10, C12.
- File: `config/acceptance_criteria.json` (điền và ký một lần), `config/operating_gates.json` mục `business`, `submission/submission.json`.
- PIC các dòng Chất lượng, Chi phí và Quyết định trong checklist 9 nhóm việc (Phiếu B mục B5).

### Đóng góp cụ thể

**Vòng 1**
- **Khởi tạo repo và nhóm:** tạo repo từ template, gắn `upstream`, điền bảng thành viên trong `TEAM.md`, chia việc cho cả nhóm và chỉ rõ ai chờ ai, đưa PRD v1.1 và eval card Lab 9 của tôi vào `lab9-ref/` làm tài liệu chung.
- **Tiêu chí (câu 1.1, 1.6):** viết mục tiêu cấp hệ thống, sáu câu "Nếu … thì chúng tôi sẽ …", hai câu ranh giới đầu ra và bốn câu soát; điền `acceptance_criteria.json` (ba chỉ số an toàn bằng 0, `pass_rate` ≥ 0,90, `pass_k` ≥ 0,80, chi phí ≤ 7.000 đ/ticket, ROI ≥ 0,3, 0 ca ùn) rồi **ký trước lần đo đầu tiên** (15:50), push ngay.
- **Đo và quyết định:** chạy các lệnh chính thức trên máy tôi: base (`R-base-before-…-bde05c`, chưa đạt 2 chỉ số an toàn do `T-002@55`), after (`R-base-after-…-13ea92`, 9/9 đạt), chốt cổng vòng 1 (`d950ec13`) và prepared (`R-base-prepared-…-e22afc`). Điền B0, B1 (lý lẽ tự chặn hay người duyệt).
- **Cổng kinh doanh (câu 2.9, B7.4):** đặt `daily_refund_cap_vnd` 500.000, `cost_budget_per_ticket_vnd` 1.500, `pilot_scope` = tất cả, `roi_min` 0,3, mỗi số có lý do từ `ops_limits` và `ops_facts`. Gửi Hoàng số ca mỗi giờ (≈ 2,75 ticket/giờ thường, ≈ 8 ticket/giờ cao điểm) để viết runbook.
- **Quyết định v1 (B8):** chọn Tiếp tục vì report không còn ngưỡng chưa đạt hay dòng vượt trần, ghi rõ bằng chứng còn thiếu là gói sự cố và bài kiểm tra ẩn.

**Vòng 2 (thẻ S6)**
- Nhận thẻ, ghi `Thẻ đã bốc: S6`, chạy `grade --incident S6` trên mốc prepared. Phát hiện `1 integrity ❌` do 19 file khoá bị Git đổi sang CRLF (`core.autocrlf=true`), kiểm từng file khớp hash khi quy về LF rồi khôi phục, chạy lại được `1 integrity ✅`.
- Điền C0, C1; sau khi Sang sửa `guards.py` và Hoàng bổ sung quy trình vận hành, chạy lại chính thức `eval --suite S6 --stage after`, `eval --suite base --stage after` và `grade`, thay mã lần chạy cục bộ của máy Sang bằng mã chính thức ở C7 đến C10, điền C12 (v2: giữ Tiếp tục), ba dòng bắt buộc và `submission.json`.

**Sử dụng AI.** Có dùng Claude (Claude Code trong VS Code và claude.ai) để đọc đề và code, soạn nháp các mục trong Phiếu A, B, C, lập kế hoạch chia việc, chạy các lệnh theo yêu cầu của tôi và soát lại số liệu với report. Các ngưỡng trong tiêu chí, các con số trong `operating_gates.json` mục `business` và quyết định v1, v2 là do tôi chọn và giải thích được; tôi tự chạy lệnh ký tiêu chí.

### Bằng chứng

- Tiêu chí: commit ký `206dccc` (15:50, trước mọi lần đo), A1 và A4 `7b1194c`, A5 `f2013ed`. Hash tiêu chí `37806ada` còn nguyên trong mọi report.
- Cổng `business` (B7.4) `244f442`. Chốt vòng 1 và v1 `c1e4a26` (hash chốt `d950ec13`); PIC ký và ngày quyết định lại `1992317`.
- Mã lần chạy vòng 1: base `R-base-before-20261118-155314-bde05c`, after `R-base-after-20261118-164904-13ea92`, prepared `R-base-prepared-20261118-171152-e22afc` (Phiếu B, B0 dòng 1 đến 3).
- Vòng 2: thẻ `f3461b0`; C0 và C1 `3b85690`; mã chính thức S6 after `R-S6-after-20261118-215633-88a606`, bộ nền `R-base-after-20261118-215634-88a606`, grade `R-S6-grade-20261118-215638-88a606` (**PASS-VISIBLE**); C7 đến C12 và mã chính thức `24b577b`.

### Exit ticket

Điều học được: ngưỡng phải viết và ký trước khi nhìn số, và cổng đặt ngoài model (ở bước ghi, đọc từ tracking thay vì từ chữ của ticket) mới thật sự chặn được tác hại; một lỗi chìm như `T-002@55` khách không thấy sai nhưng hãng chịu thiệt. Điều còn chưa chắc: chi phí thực tế khi tính cả công người xử lý các ca bị hoãn (ước khoảng 6.479 đ/ticket, sát ngưỡng 7.000 đ, chưa đo) và kết quả trên bài kiểm tra ẩn, vì dữ liệu ở đây là mock và mẫu nhỏ.

## NguyenVuHoang-2A202603491

### Phần việc phụ trách

Em phụ trách vận hành và pháp lý: phân tích rủi ro, checklist 9 nhóm, runbook, hai mục `operations` và `legal` trong config, và phần cập nhật hồ sơ sau sự cố S6.

### Đóng góp cụ thể

- **Phiếu A (1.2, 1.4):** Viết mục tiêu cho chị Oanh và chị Hạnh, đề xuất cách theo dõi thông báo gửi hãng có trường dữ liệu cá nhân bị cấm.
- **Phiếu B (2.4a, 2.4b, 2.5):** Làm HAZOP cho `issue_refund`, điền checklist 9 nhóm và tổng hợp ba cổng ưu tiên vòng 1 dựa trên trace `T-002@55` và report base.
- **Phiếu B (2.8, 2.10):** Bổ sung phần đối chiếu ticket thử `O-1010`. Điền config vận hành và pháp lý, viết runbook 1–3 và tính tải giờ cao điểm ở B7.5–B7.6. Nhóm bố trí một người duyệt với công suất 6 ca/giờ, so với khoảng 1,9 ca/giờ ước tính lúc cao điểm.
- **Phiếu C (3.7):** Cập nhật cây nguyên nhân sau sửa, thêm hai dòng sổ rủi ro, làm lại checklist 9 nhóm và viết runbook 4–5 cho thẻ S6.
- **Sử dụng AI:** Có dùng AI để soạn và soát nội dung các phiếu, đối chiếu số liệu với repo, chỉnh config và chạy lại trace thử ở câu 2.8.

### Bằng chứng

- Phiếu A, A1–A2: `1216bfa`. Phiếu B, B4–B6: `041d505`, `0a1c9d8`; đối chiếu `T-002@55` và report base `R-base-before-20261118-155314-bde05c`.
- Phiếu B, B7.3: `ddf3cf5`; thử `O-1010`, seed 11, base hoàn sai 70.000đ và after chặn khoản hoàn. B7.5–B7.6 và config: `907a884`, `16f1e72`.
- Phiếu C, C9–C11: tham chiếu kết quả S6 cục bộ của Sang `R-S6-after-20261118-174216-88a606` và grade `R-S6-grade-20261118-174219-88a606`.

### Exit ticket

Em thấy một đơn có thể tách thành nhiều kiện, nên lúc có tranh chấp phải lần theo từng kiện trước khi quy lỗi cho hãng hay tài xế. Em còn chưa chắc một người trực có xử lý kịp khi ca thiếu mã kiện và ca cần đối soát với hãng dồn vào cùng một lúc.


## NguyenNgocSang-2A202603444

### Phần việc phụ trách

Nguyễn Ngọc Sang · MSSV `2A202603444` · Kỹ sư cổng. Phụ trách đo ở mức bước (A2, câu 1.3), dò trace và phân tích rủi ro vòng 1 (B2, B6), triển khai cổng (B7.1) và sửa cổng, bổ sung chỉ số theo dõi cho thẻ S6 (C7, C8).

### Đóng góp cụ thể

- Thiết kế thước đo offline cho bước `file_carrier_fault` dựa trên nhãn hãng–kiện, có cách tính cho dòng trùng và dữ liệu thiếu. Dò `T-002@55` và đối chiếu với FM-03 của Lab 9. Agent dùng 5 ngày khách khai thay cho 2 ngày trong tracking, dẫn đến hoàn sai 20.000đ và ghi oan một lỗi cho VNX. Ghi phân tích vào B2 và chuẩn bị dự thảo B6 để nhóm chọn cổng vòng 1.
- Triển khai ba cổng đã chọn ở B6. K1 kiểm quyền lợi hoàn từ tracking và chính sách hiệu lực, K3 kiểm điều kiện ghi lỗi và xác minh đúng hãng–kiện, K2 đọc trần hoàn tự động theo ngày từ cấu hình. Ghi nguồn dữ liệu và điều kiện của từng cổng vào B7.1.
- Sửa hai nhánh của S6. Khi ticket thiếu mã kiện và có nhiều hãng đủ căn cứ ghi lỗi, chuyển người xác minh trước khi ghi tiền. Khi hãng chạm trần lỗi tự động theo ngày của Ops, hoãn riêng lệnh ghi lỗi và giữ khoản hoàn hợp lệ. Bổ sung quy trình xác minh, đối soát trong `operations.stop_conditions`.
- Thêm `ambiguous_parcel_rate` và `carrier_fault_review_rate` vào `MONITORS` để theo dõi ca cần xác minh kiện và ca cần xem xét lỗi hãng. Ghi cách tính và kết quả đo ở C8.
- **Sử dụng AI.** Dùng Codex để đọc tài liệu và code, phân tích trace, soạn các mục trong phiếu, triển khai cổng và chỉ số theo dõi, chạy kiểm tra và soạn mục cá nhân này.

### Bằng chứng

- Commit `0b4de7a` ghi thước đo ở [Phiếu A, mục A2](templates/form-a-criteria.md#a2). [Phiếu B, mục B2](templates/form-b-evaluation-gates.md#b2) dẫn trace `T-002@55`, dòng 02–03 và 05–10, đối chiếu với baseline chính thức `R-base-before-20261118-155314-bde05c`.
- Commit `b17051f` ghi code cổng vòng 1 và bảng [B7.1](templates/form-b-evaluation-gates.md#b7). Lần chạy chính thức của Tiến `R-base-after-20261118-164904-13ea92` đạt 110/110. Sang tự chạy lại với mã `R-base-after-20261118-163804-dafe28`, cũng đạt 110/110 và 13 test công khai đều qua.
- [C7](templates/form-c-incident.md#c7) và [C8](templates/form-c-incident.md#c8) ghi kết quả từng lượt sửa S6. Trên máy Sang, từ `prepared` đến `after`, hoàn sai giảm từ 270.000đ xuống 0đ và lỗi hãng oan từ 20 xuống 0. Run `R-S6-after-20261118-174216-88a606` đạt 60/60 và run nền `R-base-after-20261118-174217-88a606` đạt 110/110. Cả 13 test công khai và 9 kiểm tra bổ sung vòng 2 đều qua. Mỗi monitor mới ghi nhận 10/60 trial trên S6 và 0/110 trial trên bộ nền.
- Báo cáo `R-S6-grade-20261118-174219-88a606` ghi `PASS-VISIBLE` tại thời điểm chạy, trước khi dọn bảy thư mục thẻ khác. Lần chạy đó chỉ kiểm thử công khai. Nhật ký từng lần đo cục bộ ở `runs/sang-task35-36-runlog.json`.

### Exit ticket

- **Điều học được.** Em học được rằng cổng phải kiểm theo đúng đơn vị chịu trách nhiệm. Với đơn nhiều kiện, việc chọn nhầm kiện có thể ghi lỗi oan cho một hãng dù khoản hoàn trông hợp lý. Vì vậy, nếu chưa rõ kiện nào, em đặt bước xác minh trước khi ghi tiền.
- **Điều còn chưa chắc.** Em chưa biết người trực có xử lý kịp các lỗi hãng bị hoãn khi nhiều đơn đến cùng lúc trong pilot thật hay không. Monitor chỉ đếm ca cần xem xét. Em muốn đo thêm thời gian từ lúc ghi sự kiện đến lúc xác minh xong và chi phí đối soát mỗi ca.

## DaoThiThuPhuong-2A202603457

### Phần việc phụ trách

Kỹ sư cổng (phụ trách dữ liệu, kiểm thử và `lab10/monitors.py`). Bản đồ dữ liệu, behavioral test, kiểm chéo cổng của Sang, chỉ số theo dõi.

- Đề: câu 1.5 · 2.3 · 2.7 · 2.8 (cùng Hoàng) · kiểm chéo cổng vòng 1 · 3.1–3.4 của thẻ S6 · chỉ số theo dõi cho câu 3.6.
- Phiếu: A mục A3 · B mục B3, B7.2, B7.3 · C mục C2, C3.2, C4, C5 (3.2 và 3.3), C6.
- File: `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`, `lab10/monitors.py`.
- PIC dòng **Dữ liệu** trong checklist 9 nhóm việc (Phiếu B mục B5).

### Đóng góp cụ thể

**Vòng 1**
- **Câu 1.5 (A3):** chọn (b), giải thích bằng khoảng tin cậy của X đã chứa 1,0; loại từng đáp án còn lại; đối chiếu với số liệu Lab 9 của bàn (`E-002@55`, CI hiệu chạm 0).
- **Câu 2.3 (B3):** bản đồ dữ liệu từ `data/world.json` (trường then chốt, nguồn sự thật hay bản sao, định dạng, đơn nhiều kiện O-1013, kiện chưa giao O-1011/O-1014). Ví dụ drift: REFUND-v3 → REFUND-v4 ngày 01/12/2026 (quan hệ vào–ra đổi), gắn với ngưỡng đã ký và số mốc base. Tìm ra dòng kho `?` trong report base là ticket `T-018` hỏi đơn `O-9999` không tồn tại, tốn 10.359đ/ticket (đắt hơn làm tay).
- **Câu 2.7 (B7.2):** hai bước tránh rò rỉ dữ liệu (cổng chỉ dựa vào nguồn sự thật, soát mã ticket/mã đơn trong `guards.py`; tách bộ dùng để chỉnh với bộ dùng để kết luận).
- **Câu 2.8 (B7.3):** viết tính chất và 2 ticket hiểm (O-1010 khai trễ 8 ngày; O-1005 khai lỗi hãng khi tracking là `CUSTOMER_ABSENT`), chạy ở cả mốc base và after: ticket 1 base hoàn sai 70.000đ, after bị cổng K1 chặn; ticket 2 đúng ở cả hai mốc (cổng không chặn nhầm). Chuẩn bị ô để Hoàng tự chạy và đọc kết quả.
- **Kiểm chéo nhãn `label.faults`** cho thước đo câu 1.3 của Sang: 22/22 ticket bộ nền khớp tracking và chính sách; 3 ca T-009, T-017, T-019 để trống vì vượt hạn mức / hoàn trùng / đòi tiền cho đơn của người khác.
- **Kiểm chéo cổng vòng 1 của Sang trước khi Tiến chốt:** 9/9 ĐẠT, không có ca mới hỏng, `T-002@55` hết hỏng, unittest OK. Phát hiện máy bị đổi xuống dòng CRLF (`core.autocrlf=true`) làm hash file tiêu chí và file khoá lệch dù nội dung không đổi; sửa trên máy mình và báo nhóm trước khi chốt.

**Vòng 2 (thẻ S6)**
- **Câu 3.1 (C2):** dò `S6-01@11` (base), `S6-20@11`, `S6-21@11`, `S6-42@11` (prepared); bảng soát lỗi 3 lỗi có 3 nguồn khác nhau (ghi nhầm kiện: chìm; tự chọn hãng khi khách không nói kiện: ngữ cảnh; dồn lỗi thứ 3+ cho GHSH trong ngày: chìm); nêu tác hại và đọc khối kinh doanh, vận hành, theo kho và hãng.
- **C3.2:** hình dung của điều phối/tài xế hãng và kế toán đối soát (đơn vị chịu lỗi là **kiện**) so với hệ thống (đơn vị là **đơn**).
- **C4:** HAZOP 4 dòng trên `file_carrier_fault` (WRONG, INCOMPLETE, PERTURBED, INVALID; dòng INVALID là nhánh chưa thấy trên trace).
- **C5:** specification (câu 3.2) và giả định môi trường (câu 3.3).
- **C6:** fault tree trước khi sửa, 4 nhánh ở 4 tầng, có nút VÀ, mỗi lá có bằng chứng `ticket@seed`.
- **`lab10/monitors.py`:** thêm `model_override_rate` và `guard_block_rate` (đọc sự kiện guard Sang bàn giao). `guard_block_rate` trên S6: base 0,0 → prepared 0,4167; trên bộ nền after 0,0091.

### Bằng chứng

- **Commit:** `802953a` (A3, câu 1.5) · `f724864` (B3, B7.2, nháp B7.3) · `a8ae895` (B3 cập nhật số base, B7.3 kết quả 2 ticket hiểm, `lab10/monitors.py`) · `50318af` và `582ce23` (Phiếu C: C2, C3.2, C4, C5, C6 thẻ S6).
- **Mã lần chạy trên máy Phương** (chỉ để kiểm chéo, số trong phiếu lấy từ máy Tiến): `R-base-after-20261118-165548-dd198c` (kiểm chéo bản cuối vòng 1, 9/9 ĐẠT, tiêu chí hash `37806ada` còn nguyên) · `R-base-before-20261118-165818-eb223c`, `R-base-after-20261118-165819-eb223c` (thử monitor trên bộ nền) · `R-S6-before-20261118-172234-eb223c`, `R-S6-prepared-20261118-172235-eb223c` (đối chiếu số mốc base/prepared của thẻ S6, khớp với `R-S6-before/prepared-20261118-171452-e22afc` của Tiến).
- **Dòng trong phiếu:** Phiếu A mục A3 · Phiếu B mục B3, B7.2, B7.3, dòng 2 "Dữ liệu" ở B5 (PIC) · Phiếu C mục C2, C3.2, C4, C5, C6.

### Dùng AI

Có dùng trợ lý AI (Claude Code) để: đọc và tóm tắt tài liệu lab; soạn nháp câu trả lời các mục A3, B3, B7.2, B7.3, C2, C3.2, C4, C5, C6; chạy lệnh `eval`, `gate`, `trace` để lấy bằng chứng; kiểm chéo nhãn; tìm nguyên nhân lỗi hash do CRLF; viết nháp hai hàm trong `lab10/monitors.py`. Mọi con số trong phiếu lấy từ lần chạy thật hoặc `data/world.json`; Phương đã đọc lại và tự commit từng phần. Không dùng AI để viết code theo mã ticket hay câu chữ cụ thể.

### Exit ticket

- **Một điều học được:** một tỉ lệ đạt cao có thể che tác hại cho bên thứ ba. Bộ nền đạt 0,99 nhưng chỉ toàn đơn một kiện; gói S6 lộ ra hệ thống hiểu "đơn" trong khi người chịu hậu quả hiểu "kiện", và lỗi chìm nằm đúng ở chỗ hai cách hiểu đó vênh nhau.
- **Một điều còn chưa chắc:** khi chuyển các ca mơ hồ sang người duyệt, chi phí mỗi ticket ước tính lên khoảng 4.830–6.500đ, sát ngưỡng 7.000đ đã ký; chưa chắc ngưỡng này còn giữ được khi lượng đơn tách kiện ngoài thực tế lớn hơn mock.
