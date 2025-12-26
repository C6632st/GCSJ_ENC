# Home.py
import streamlit as st
# 页面配置
st.set_page_config(
    page_title="对称密码学算法可视化平台",
    page_icon="🔐",
    layout="centered"
)

# 主标题与介绍
st.title("🔐 对称密码学算法可视化平台")
st.markdown(
    """
    本平台旨在帮助学习者直观理解主流对称加密算法的工作原理与流程。

    请下方或通过侧边栏选择支持的算法之一，进入对应的交互式演示界面：
    """
)

# 算法选择卡片（美观且易用）
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.image("https://cdn-icons-png.flaticon.com/512/2523/2523390.png", width=80)  # 可选图标
        st.subheader("AES")
        st.caption("高级加密标准 · 安全高效")
        if st.button("进入 AES", type="primary", use_container_width=True):
            st.switch_page("pages/aes.py")

with col2:
    with st.container(border=True):
        st.image("https://cdn-icons-png.flaticon.com/512/3063/3063495.png", width=80)
        st.subheader("DES")
        st.caption("数据加密标准 · 经典但已过时")
        if st.button("进入 DES", type="primary", use_container_width=True):
            st.switch_page("pages/des.py")

with col3:
    with st.container(border=True):
        st.image("https://cdn-icons-png.flaticon.com/512/732/732220.png", width=80)
        st.subheader("SM4")
        st.caption("国密标准 · 中国商用密码")
        if st.button("进入 SM4", type="primary", use_container_width=True):
            st.switch_page("pages/sm4.py")
# ====== 专属主页侧边栏 ======
with st.sidebar:
    st.title("🔐 密码学可视化平台")
    st.markdown("---")

    st.subheader("🎯 平台目标")
    st.caption("通过交互式演示，帮助理解对称加密算法的核心流程与差异。")

    st.subheader("🧩 支持算法")
    st.markdown("""
    - **AES**：现代标准，广泛用于 TLS、文件加密  
    - **DES**：经典算法，教学用途（已不安全）  
    - **SM4**：中国国家商用密码标准（GM/T 0002-2012）
    """)

    st.subheader("📚 使用建议")
    st.caption("点击卡片进入对应算法页面，调整参数并观察加密过程。")

    st.markdown("---")
    st.caption("© 2025 对称密码学教学平台 | 基于 Python + Streamlit")
# 底部说明（可选）
st.markdown("---")
st.caption("""
💡 提示：每个算法页面均包含参数设置、加解演示、中间过程可视化等功能。  
📚 适合密码学课程教学、自学或实验参考。
""")