import streamlit as st
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 NGUYỄN KHÁNH NGÂN 2521003993")
st.write("Tính toán tiền lãi theo phương pháp **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

st.subheader("📋 Thông tin khoản gửi")

principal = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

term = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

interest_type = st.radio(
    "Hình thức tính lãi",
    ["Lãi đơn", "Lãi kép"],
    horizontal=True
)

interest_rate = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

payment_method = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if principal <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if interest_rate < 0:
        st.error("Lãi suất không hợp lệ.")
        st.stop()

    # Lãi suất dạng thập phân
    annual_rate = interest_rate / 100

    # Thời gian tính theo năm
    years = term / 12

    # Xác định số kỳ nhận lãi
    if payment_method == "Lãnh lãi theo tháng":
        periods = term
        rate_per_period = annual_rate / 12
        period_name = "tháng"

    elif payment_method == "Lãnh lãi theo quý":
        periods = term // 3

        # Nếu kỳ hạn không chia hết cho 3
        remaining_months = term % 3

        if periods == 0:
            st.warning(
                "Kỳ hạn phải từ 3 tháng trở lên nếu chọn lãnh lãi theo quý."
            )
            st.stop()

        rate_per_period = annual_rate / 4
        period_name = "quý"

    else:
        periods = 1
        rate_per_period = annual_rate
        period_name = "kỳ hạn"

    # =========================
    # LÃI ĐƠN
    # =========================

    if interest_type == "Lãi đơn":

        # Tổng tiền lãi
        total_interest = principal * annual_rate * years

        # Lãi mỗi tháng
        monthly_interest = principal * annual_rate / 12

        # Lãi mỗi quý
        quarterly_interest = principal * annual_rate / 4

        # Tiền lãi định kỳ
        if payment_method == "Lãnh lãi theo tháng":
            periodic_interest = monthly_interest

        elif payment_method == "Lãnh lãi theo quý":
            periodic_interest = quarterly_interest

        else:
            periodic_interest = total_interest

        total_amount = principal + total_interest

    # =========================
    # LÃI KÉP
    # =========================

    else:

        # Lãi kép cuối kỳ:
        # A = P(1+r)^n
        if payment_method == "Lãnh lãi cuối kỳ":

            total_amount = principal * (1 + annual_rate / 12) ** term
            total_interest = total_amount - principal

            # Lãi kỳ cuối
            periodic_interest = (
                total_amount
                - principal * (1 + annual_rate / 12) ** (term - 1)
            )

        # Lãi kép theo tháng
        elif payment_method == "Lãnh lãi theo tháng":

            balance = principal
            total_interest = 0

            for _ in range(term):
                interest = balance * rate_per_period
                balance += interest
                total_interest += interest

            total_amount = balance

            # Lãi của kỳ cuối
            previous_balance = total_amount / (1 + rate_per_period)
            periodic_interest = total_amount - previous_balance

        # Lãi kép theo quý
        else:

            balance = principal
            total_interest = 0

            for _ in range(periods):
                interest = balance * rate_per_period
                balance += interest
                total_interest += interest

            # Xử lý số tháng lẻ nếu kỳ hạn không chia hết cho 3
            if remaining_months > 0:
                extra_interest = (
                    balance
                    * annual_rate
                    * remaining_months
                    / 12
                )

                balance += extra_interest
                total_interest += extra_interest

            total_amount = balance

            # Lãi của quý cuối
            previous_balance = (
                total_amount / (1 + rate_per_period)
                if remaining_months == 0
                else total_amount - (
                    balance * annual_rate * remaining_months / 12
                )
            )

            periodic_interest = (
                total_amount - previous_balance
            )

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.success("✅ Đã tính toán xong!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            format_money(periodic_interest)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_money(total_interest)
        )

    st.metric(
        "💰 Tổng tiền gốc + lãi",
        format_money(total_amount)
    )

    # =========================
    # 🔎 CHỨC NĂNG:
    # SO SÁNH LÃI ĐƠN VÀ LÃI KÉP
    # =========================

    st.divider()

    st.subheader("🔎 So sánh Lãi đơn và Lãi kép")

    # Tính tổng tiền theo LÃI ĐƠN
    simple_total = principal + (
        principal * annual_rate * years
    )

    # Tính tổng tiền theo LÃI KÉP
    if payment_method == "Lãnh lãi theo tháng":

        compound_total = (
            principal * (1 + annual_rate / 12) ** term
        )

    elif payment_method == "Lãnh lãi theo quý":

        compound_balance = principal

        for _ in range(periods):
            compound_balance *= (1 + annual_rate / 4)

        if remaining_months > 0:
            compound_balance += (
                compound_balance
                * annual_rate
                * remaining_months
                / 12
            )

        compound_total = compound_balance

    else:

        compound_total = (
            principal * (1 + annual_rate / 12) ** term
        )

    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        st.metric(
            "💵 Tổng tiền - Lãi đơn",
            format_money(simple_total)
        )

    with compare_col2:
        st.metric(
            "📈 Tổng tiền - Lãi kép",
            format_money(compound_total)
        )

    difference = compound_total - simple_total

    if difference > 0:
        st.success(
            f"📈 Với khoản gửi này, **lãi kép cao hơn lãi đơn "
            f"{format_money(difference)}**."
        )

    elif difference < 0:
        st.info(
            f"💵 Với khoản gửi này, **lãi đơn cao hơn lãi kép "
            f"{format_money(abs(difference))}**."
        )

    else:
        st.info(
            "⚖️ Hai phương pháp cho kết quả bằng nhau."
        )

    # =====================================================
    # 📈 CHỨC NĂNG MỚI 1:
    # BIỂU ĐỒ TĂNG TRƯỞNG TIỀN THEO THỜI GIAN
    # =====================================================

    st.divider()

    st.subheader("📈 Biểu đồ tăng trưởng khoản tiền")

    st.write(
        "Biểu đồ mô phỏng sự thay đổi của số tiền theo từng tháng "
        "trong thời gian gửi."
    )

    simple_growth = []
    compound_growth = []

    simple_balance = principal
    compound_balance_chart = principal

    for month in range(1, term + 1):

        # Lãi đơn tăng đều mỗi tháng
        simple_balance = (
            principal
            + principal * annual_rate * month / 12
        )

        simple_growth.append(simple_balance)

        # Lãi kép
        if payment_method == "Lãnh lãi theo quý":

            if month % 3 == 0:
                compound_balance_chart *= (
                    1 + annual_rate / 4
                )

            elif month == term and month % 3 != 0:
                remaining = month % 3
                compound_balance_chart += (
                    compound_balance_chart
                    * annual_rate
                    * remaining
                    / 12
                )

        else:

            compound_balance_chart *= (
                1 + annual_rate / 12
            )

        compound_growth.append(compound_balance_chart)

    chart_data = {
        "Lãi đơn": simple_growth,
        "Lãi kép": compound_growth
    }

    st.line_chart(chart_data)

    # =====================================================
    # 🎯 CHỨC NĂNG MỚI 2:
    # MỤC TIÊU TÀI CHÍNH
    # =====================================================

    st.divider()

    st.subheader("🎯 Mục tiêu tài chính")

    target_amount = st.number_input(
        "Nhập số tiền mục tiêu muốn đạt được (VNĐ)",
        min_value=0.0,
        value=20_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    if target_amount > 0:

        # Hệ số tăng trưởng lãi đơn
        simple_factor = 1 + annual_rate * years

        # Hệ số tăng trưởng lãi kép
        if payment_method == "Lãnh lãi theo tháng":

            compound_factor = (
                1 + annual_rate / 12
            ) ** term

        elif payment_method == "Lãnh lãi theo quý":

            compound_factor = (
                (1 + annual_rate / 4) ** periods
            )

            if remaining_months > 0:
                compound_factor *= (
                    1
                    + annual_rate * remaining_months / 12
                )

        else:

            compound_factor = (
                1 + annual_rate / 12
            ) ** term

        # Số tiền gốc cần có để đạt mục tiêu
        required_simple = (
            target_amount / simple_factor
            if simple_factor > 0
            else 0
        )

        required_compound = (
            target_amount / compound_factor
            if compound_factor > 0
            else 0
        )

        target_col1, target_col2 = st.columns(2)

        with target_col1:
            st.metric(
                "💵 Gốc cần có - Lãi đơn",
                format_money(required_simple)
            )

        with target_col2:
            st.metric(
                "📈 Gốc cần có - Lãi kép",
                format_money(required_compound)
            )

        # Kiểm tra khoản tiền hiện tại
        if total_amount >= target_amount:

            st.success(
                f"🎉 Khoản tiền hiện tại **đạt mục tiêu "
                f"{format_money(target_amount)}**!"
            )

        else:

            missing_amount = target_amount - total_amount

            st.warning(
                f"⚠️ Khoản tiền hiện tại **chưa đạt mục tiêu**. "
                f"Còn thiếu khoảng **{format_money(missing_amount)}**."
            )

    # =====================================================
    # 💡 CHỨC NĂNG MỚI 3:
    # PHÂN TÍCH TỰ ĐỘNG
    # =====================================================

    st.divider()

    st.subheader("💡 Phân tích kết quả")

    interest_percentage = (
        total_interest / principal * 100
        if principal > 0
        else 0
    )

    if interest_type == "Lãi kép":

        st.write(
            f"📈 Với **lãi kép**, khoản tiền của bạn tăng khoảng "
            f"**{interest_percentage:.2f}%** so với số tiền gốc."
        )

        if compound_total > simple_total:
            st.write(
                f"💰 So với lãi đơn, lãi kép giúp khoản tiền cuối kỳ "
                f"cao hơn khoảng **{format_money(difference)}**."
            )

    else:

        st.write(
            f"💵 Với **lãi đơn**, khoản tiền tăng khoảng "
            f"**{interest_percentage:.2f}%** so với số tiền gốc."
        )

        if simple_total < compound_total:
            st.write(
                f"📊 Nếu chuyển sang lãi kép với cùng số tiền, "
                f"kỳ hạn và lãi suất, số tiền cuối kỳ có thể cao hơn "
                f"lãi đơn khoảng **{format_money(difference)}**."
            )

    if term >= 12:
        st.write(
            "⏳ Kỳ hạn từ 12 tháng trở lên nên tác động của "
            "việc tái đầu tư tiền lãi trong mô hình lãi kép "
            "thể hiện rõ hơn."
        )
    else:
        st.write(
            "⏱️ Với kỳ hạn ngắn, chênh lệch giữa lãi đơn và "
            "lãi kép thường không quá lớn."
        )

    # =========================
    # CHI TIẾT
    # =========================

    st.divider()

    st.subheader("📝 Chi tiết khoản gửi")

    st.write(f"**Số tiền gốc:** {format_money(principal)}")
    st.write(f"**Kỳ hạn:** {term} tháng")
    st.write(f"**Lãi suất:** {interest_rate:.2f}%/năm")
    st.write(f"**Phương pháp:** {interest_type}")
    st.write(f"**Hình thức lãnh lãi:** {payment_method}")

    st.divider()

    # =========================
    # CÔNG THỨC
    # =========================

    with st.expander("📚 Xem công thức tính"):

        if interest_type == "Lãi đơn":

            st.markdown(
                """
                **Công thức lãi đơn:**

                `Tiền lãi = Tiền gốc × Lãi suất năm × Thời gian`

                Trong đó:

                - Lãi suất được tính theo năm.
                - Thời gian được quy đổi về năm.
                - Tiền lãi không được cộng vào tiền gốc để tiếp tục sinh lãi.
                """
            )

        else:

            st.markdown(
                """
                **Công thức lãi kép:**

                `A = P × (1 + r)ⁿ`

                Trong đó:

                - `A`: Tổng số tiền nhận được
                - `P`: Tiền gốc ban đầu
                - `r`: Lãi suất của mỗi kỳ
                - `n`: Số kỳ tính lãi

                Với lãnh lãi theo tháng, lãi suất năm được chia cho 12.

                Với lãnh lãi theo quý, lãi suất năm được chia cho 4.
                """
            )

st.divider()

st.caption("💡 Công cụ tính toán mang tính tham khảo. Lãi suất thực tế của ngân hàng có thể áp dụng các quy định khác.")
