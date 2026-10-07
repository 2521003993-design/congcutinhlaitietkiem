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
