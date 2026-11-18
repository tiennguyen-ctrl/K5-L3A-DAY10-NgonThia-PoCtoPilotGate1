"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Cổng vòng 1: K1 đối chiếu quyền lợi từ DB, K3 xác minh lỗi hãng,
K2 giữ trần hoàn tự động đọc từ config. Mốc base vẫn dùng _noop_guards.
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    # K1/K3 dùng cùng phiên bản hiệu lực; không tin cờ index_active.
    try:
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    except (KeyError, TypeError, ValueError):
        policy = None
    if policy is None:
        ctx.log("policy_unavailable")
        return Verdict.escalate("không xác định được chính sách hiệu lực, cần người kiểm tra")
    ctx.log("policy_pinned", policy_id=policy["policy_id"])
    return Verdict.allow(policy_id=policy["policy_id"])


def _facts(ctx, action):
    """Chỉ đọc dữ kiện; không dùng text, seed, nhãn hay state riêng của evaluator."""
    if action.get("ticket_id") != ctx.ticket.get("ticket_id"):
        raise ValueError("lệnh ghi không thuộc ticket đang xử lý")
    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    if order is None or action.get("order_id") != order["order_id"]:
        raise ValueError("không xác định được đúng đơn của lệnh ghi")
    if order["customer_id"] != ctx.ticket.get("customer_id"):
        raise ValueError("người yêu cầu không phải chủ đơn")
    if not order.get("parcels"):
        raise ValueError("đơn chưa có tracking kiện")
    parcel_id = ctx.ticket.get("parcel_id")
    if parcel_id and not any(p["parcel_id"] == parcel_id for p in order["parcels"]):
        raise ValueError("kiện được yêu cầu không thuộc đơn")
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    if delay > 0 and not parcel.get("delay_cause"):
        raise ValueError("tracking chưa ghi nguyên nhân trễ")
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        raise ValueError("không có chính sách hiệu lực")
    return order, parcel, delay, policy


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool not in ("issue_refund", "file_carrier_fault"):
        return Verdict.allow()
    try:
        order, parcel, delay, policy = _facts(ctx, action)
    except (KeyError, TypeError, ValueError) as exc:
        ctx.log("source_check_failed", tool=tool, reason=str(exc))
        if tool == "issue_refund":
            return Verdict.escalate("chưa đủ dữ kiện đáng tin để hoàn tiền: " + str(exc))
        # Tiền có thể đã ghi trước bước này; không chuyển người sau khi đã hoàn.
        return Verdict.deny("chưa đủ căn cứ ghi lỗi hãng: " + str(exc))

    if tool == "issue_refund":
        # K1: không sửa số tiền rồi vô tình bỏ qua bước phê duyệt của agent.
        expected = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        asked = action.get("amount_vnd")
        if expected <= 0 or type(asked) is not int or asked != expected:
            ctx.log("refund_blocked", asked_vnd=asked, expected_vnd=expected,
                    db_delay_days=delay, policy_id=policy["policy_id"])
            return Verdict.deny("số tiền đề xuất không khớp quyền lợi theo tracking và chính sách")

        # K2: cùng quy tắc với host; chỉ trần hoàn TỰ ĐỘNG, không tự đặt con số.
        cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
        if cap is not None and not action.get("approval_id"):
            spent = ctx.tools.auto_refund_today_vnd()
            if spent + asked > cap:
                ctx.log("daily_refund_cap_blocked", spent_vnd=spent, asked_vnd=asked, cap_vnd=cap)
                return Verdict.escalate("vượt trần hoàn tự động trong ngày, cần người duyệt")

    if tool == "file_carrier_fault":
        # K3: có nguyên nhân CARRIER chưa đủ; phải đạt cả ngưỡng trễ theo DB.
        if not H.carrier_at_fault(policy, parcel, delay):
            ctx.log("carrier_fault_blocked", parcel_id=parcel["parcel_id"],
                    db_delay_days=delay, policy_id=policy["policy_id"])
            return Verdict.deny("tracking và chính sách không cho phép ghi lỗi hãng")
        if ctx.tools.lookup_carrier(parcel["carrier_id"]) is None:
            ctx.log("carrier_fault_blocked", parcel_id=parcel["parcel_id"], reason="unknown_carrier")
            return Verdict.deny("tracking chưa xác định được hãng hợp lệ")
        correct = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                   "driver_id": parcel.get("driver_id"), "delay_days": delay}
        if any(action.get(key) != value for key, value in correct.items()):
            ctx.log("carrier_fault_corrected", **correct)
            return Verdict.modify("đối chiếu hãng, kiện và số ngày trễ với tracking", **correct)

    return Verdict.allow()
