# sidebar_utils.py
import streamlit as st

def pub_render_sidebar(algorithm_name: str, description: str):
    """
    渲染侧边栏：统一部分 + 动态部分
    """
    # === 统一内容（所有页面都一样）===
    st.sidebar.title("🔐 密码学可视化平台")
    st.sidebar.markdown("---")
    # st.sidebar.caption("© 2025 对称加密教学平台")
    st.sidebar.caption("支持 AES / DES / SM4")

    # === 动态内容（根据页面变化）===
    if algorithm_name != '':
        st.sidebar.markdown("### 当前算法")
        st.sidebar.subheader(algorithm_name)
        st.sidebar.write(description)

        st.sidebar.markdown("---")
        st.sidebar.info("请在主界面输入明文和密钥进行加密演示。")