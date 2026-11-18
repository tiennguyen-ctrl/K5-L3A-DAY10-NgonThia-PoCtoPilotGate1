"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _has_event(trial, type_, kinds=None):
    for e in trial.get("events") or []:
        if e.get("type") == type_ and (kinds is None or e.get("kind") in kinds):
            return True
    return False


def model_override_rate(trials):
    """Kỹ thuật (Phương): tỉ lệ trial mà agent lấy số trong ticket đè lên số của tracking DB.

    Dữ liệu: sự kiện `model_override` agent tự ghi vào trace; không cần nhãn.
    Cách tính: số trial có ít nhất một `model_override` / tổng số trial (mỗi trial đếm một lần).
    Tăng đột ngột = khách đang khai số khác DB nhiều hơn, hoặc DB đang thiếu/lệch.
    """
    return sum(_has_event(t, "model_override") for t in trials) / max(1, len(trials))


GUARD_BLOCK_KINDS = ("refund_blocked", "carrier_fault_blocked", "carrier_fault_corrected",
                     "daily_refund_cap_blocked", "source_check_failed", "policy_unavailable")


def guard_block_rate(trials):
    """Phát hiện (Phương): tỉ lệ trial mà cổng của bàn phải chặn, sửa hoặc từ chối một lệnh ghi.

    Dữ liệu: sự kiện `type = "guard"` do lab10/guards.py ghi qua ctx.log (tên `kind` do Sang bàn giao).
    Cách tính: số trial có ít nhất một sự kiện guard thuộc GUARD_BLOCK_KINDS / tổng số trial.
    Bộ nền sạch thì gần 0; tăng nghĩa là agent đang đề xuất lệnh ghi sai nhiều hơn và cổng đang gánh.
    """
    return sum(_has_event(t, "guard", GUARD_BLOCK_KINDS) for t in trials) / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "guard_block_rate": guard_block_rate,
}
STARTER_MONITORS = ("escalation_rate",)
