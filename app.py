import streamlit as st
from datetime import datetime
import os
# 引入专业自动刷新组件（无阻塞、无卡顿）
from streamlit_autorefresh import st_autorefresh

import pytz  # 必须加这个
# 北京时间（正确、稳定、永远不报错）
beijing_tz = pytz.timezone(u'Etc/GMT-8')  # "Asia/Shanghai")

# website address: https://auto-stratey-data-from-wcz.streamlit.app/

# ===================== 固定文件路径 =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_FILE = os.path.join(BASE_DIR, "latest_data.csv")

# ===================== 会员授权配置（到期时间改为2026年，永久有效） =====================
MEMBER_AUTH = {
    # "USER202501": "2026-12-31",
    # "VIP202502": "2026-12-31",
    "shijinniubi": "2026-12-31",
    "wczzmy": "2026-12-31",
}

# ===================== 初始化会话状态 =====================
if "auth_pass" not in st.session_state:
    st.session_state.auth_pass = False

# ===================== 页面配置 =====================
st.set_page_config(page_title="我的数据展示站", page_icon="📊")
st.title("📊 个人Python数据展示平台")

# ===================== 验证函数（修复日期格式错误！） =====================
def check_auth(code: str) -> tuple[bool, str]:
    now = datetime.now().date()
    if code not in MEMBER_AUTH:
        return False, "❌ 授权码无效"
    try:
        # ✅ 修复：%m 是月份（正确），之前写成 %M 分钟（错误）
        expire_date = datetime.strptime(MEMBER_AUTH[code], "%Y-%m-%d").date()
    except:
        return False, "❌ 日期格式错误"
    if now > expire_date:
        return False, "❌ 会员已过期（到期：{}）".format(expire_date)
    return True, "✅ 验证成功！会员有效期至：{}）".format(expire_date)

# ===================== 登录界面 =====================
auth_code = st.text_input("请输入授权码", type="password")
if st.button("验证登录"):
    if auth_code.strip():
        status, msg = check_auth(auth_code.strip())
        st.info(msg)
        st.session_state.auth_pass = status
    else:
        st.warning("请输入授权码")

# # ===================== 实时读取数据（无缓存） =====================
# @st.cache_data(ttl=1)
# def load_latest_data():
#     try:
#         df_new = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
#         return df_new
#     except Exception as e:
#         return None

# ===================== 数据展示 + 5秒自动刷新（核心修复） =====================
if st.session_state.auth_pass:
    st.divider()
    st.subheader("📈 实时数据展示（5秒自动刷新）")

    # ===================== 🔥 仅新增：实时展示图片 代码开始 =====================
    st.subheader("🖼️ 实时展示图片")
    try:
        # 加载GitHub仓库中的 wcz_display.jpg
        st.image("wcz_display.jpg", caption="实时展示图片", use_column_width=True)

    except Exception as e:
        st.warning("⏳ 图片加载中，请稍候...")
    # ===================== 🔥 新增代码结束 =====================

    # 手动刷新按钮（原有代码）
    st.success("💡 系统每5秒自动刷新，点击按钮可立即刷新！")
    if st.button("🔄 立即刷新数据"):
        st.rerun()

    # ✅ 核心：5秒自动刷新（无阻塞、无报错、无untouchable）
    # 仅登录成功后生效，刷新间隔5000毫秒=5秒
    st_autorefresh(interval=5000, limit=None, key="autorefresh")

    st.caption('✅ 数据最后更新：{}'.format(datetime.strftime(datetime.now(tz=beijing_tz), format='%d/%m/%Y, %H:%M:%S')))

    # df = load_latest_data()
    # if df is not None:
    #     # 展示表格 + 图表
    #     st.dataframe(df, use_container_width=True)
    #     st.line_chart(df, x="日期", y="数据值")
    #     # 显示最后更新时间
    #     st.caption(f"✅ 数据最后更新：{df['更新时间'].iloc[-1]}")
    # else:
    #     st.error("❌ 未找到数据文件！请先运行 data_generator.py 生成数据！")

else:
    st.warning("🔒 请输入有效授权码查看数据")