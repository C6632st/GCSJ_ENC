import streamlit as st
import pandas as pd

from AESUtils import AESKeyExpansion
from sidebar_utils import pub_render_sidebar

def init_session_state():
    """初始化所有状态变量"""
    if 'aesPhase' not in st.session_state:
        st.session_state.aesPhase = 1  # 1:密钥阶段, 2:明文阶段, 3:加密阶段

    # st.session_state.aes_obj = None
    # st.session_state.show_round_details = False

init_session_state()
def main():
    st.set_page_config(page_title="AES 算法分步演示", layout="wide")
    st.title("AES 加密算法分步演示系统")

    # # AES 版本选择器
    # aes_versions = ["AES-128", "AES-192", "AES-256"]
    # selected_aes_version = st.selectbox("请选择 AES 版本:", aes_versions)
    # textLen = 0
    # if selected_aes_version == "AES-128":
    #     textLen = 16
    # elif selected_aes_version == "AES-192":
    #     textLen = 24
    # else:
    #     textLen = 32

    # 显示当前阶段
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"<h3 style='text-align: center; {'color: green' if st.session_state.aesPhase >= 1 else 'color: gray'}'> 阶段一：选择</h3>",
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"<h3 style='text-align: center; {'color: green' if st.session_state.aesPhase >= 2 else 'color: gray'}'> 阶段二：密钥</h3>",
            unsafe_allow_html=True)
    with col3:
        st.markdown(
            f"<h3 style='text-align: center; {'color: green' if st.session_state.aesPhase >= 3 else 'color: gray'}'> 阶段三：加密</h3>",
            unsafe_allow_html=True)

    st.divider()

    # 第一阶段：选择算法
    if st.session_state.aesPhase == 1:
        render_phase1()

    # 第二阶段：密钥输入和生成
    elif st.session_state.aesPhase == 2:
        render_phase2()
    #
    # # 第三阶段：加密流程
    elif st.session_state.aesPhase == 3:
        render_phase3()

    # 侧边栏说明
    render_sidebar()


def render_phase1():
    st.subheader("1️⃣ 选择 AES 密钥长度")
    key_option = st.radio(
        "请选择 AES 版本：",
        options=[128, 192, 256],
        format_func=lambda x: f"AES-{x}",
        horizontal=True
    )
    st.session_state.selected_key_size = key_option

    expected_bytes = {128: 16, 192: 24, 256: 32}[key_option]
    st.info(f"🔹 请在下一步输入 **{expected_bytes} 字节** 的 ASCII 字符串作为密钥")

    if st.button("下一步：输入密钥", type="primary"):
        st.session_state.aesPhase = 2
        st.rerun()
def render_phase2():
    """渲染第一阶段：密钥设置"""
    st.header("阶段一：密钥设置与生成")

    textLen = int(st.session_state.selected_key_size / 8)
    current_key = None
    custom_key = st.text_input(f"输入{textLen}字符ASCII密钥:", value="", max_chars=textLen, key="custom_key_input")
    if len(custom_key) == textLen:
        current_key_text = custom_key
        # current_key = ''.join(f"{ord(c):08b}" for c in current_key_text)
        current_key = ''.join(f"{ord(c):02X}" for c in current_key_text)
    else:
        current_key = None

    # 控制是否已生成轮密钥
    if 'aes_obj' not in st.session_state:
        st.session_state.aes_obj = None
        st.session_state.show_round_details = False


    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("上一步：选择", type="primary"):
            st.session_state.aesPhase = 1
            st.rerun()
    with col_btn2:
        if st.button("生成轮密钥", type="primary"):
            if current_key is not None:
                try:
                    aes = AESKeyExpansion(current_key)
                    st.session_state.aes_obj = aes
                    st.session_state.show_round_details = True
                    st.session_state.current_round_index = 0  # 默认从第0轮开始
                except Exception as e:
                    st.error(f"轮密钥生成失败: {e}")
            else:
                st.warning("请先输入合法长度的密钥")
    with col_btn3:
        if st.button("下一步：加密", type="primary"):
            aes = AESKeyExpansion(current_key)
            st.session_state.aes_obj = aes
            st.session_state.aesPhase = 3
            st.rerun()

        # ==============================
        # 轮密钥详情展示区（仅在生成后显示）
        # ==============================
    if st.session_state.show_round_details and st.session_state.aes_obj is not None:
        aes = st.session_state.aes_obj
        total_rounds = len(aes.roundKeys)  # 假设 round_keys 是轮密钥列表

        st.divider()
        st.subheader("🔑 轮密钥扩展详情")

        # 显示/隐藏 S盒 和 Rcon 表格（可折叠）
        with st.expander("查看 S盒 与 轮常量表 (Rcon)", expanded=False):
            col_sbox, col_rcon = st.columns([4,1])
            with col_sbox:
                st.markdown("**S盒 (16x16)**")
                # 假设 aes.s_box 是 256 字节的 list
                sbox_2d = [aes.s_box[i:i + 16] for i in range(0, 256, 16)]
                st.table([[f"{b:02X}" for b in row] for row in sbox_2d])
            with col_rcon:
                st.markdown("**轮常量 Rcon**")
                # 假设 aes.rcon 是 list，长度 >= total_rounds
                rcon_display = {i: f"0x{aes.Rcon[i]:02X}" for i in range(1, min(len(aes.Rcon), total_rounds))}
                st.write(rcon_display)

        # 轮次导航
        current_idx = st.session_state.get("current_round_index", 0)
        current_idx = max(0, min(current_idx, total_rounds - 1))

        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if st.button("◀ 上一轮", disabled=(current_idx <= 0)):
                st.session_state.current_round_index -= 1
                st.rerun()
        with nav_col2:
            target_round = st.number_input(
                "跳转到轮次:",
                min_value=0,
                max_value=total_rounds - 1,
                value=current_idx,
                step=1
            )
            if target_round != current_idx:
                st.session_state.current_round_index = target_round
                st.rerun()
        with nav_col3:
            if st.button("下一轮 ▶", disabled=(current_idx >= total_rounds - 1)):
                st.session_state.current_round_index += 1
                st.rerun()

        # 显示当前轮详情
        idx = st.session_state.current_round_index
        st.markdown(f"### 第 {idx} 轮")

        # 显示轮密钥（十六进制）
        round_key = aes.roundKeys[idx]
        display_matrix(round_key,"轮密钥")

        # # todo 显示中间状态（假设 aes.round_states 是 list，每个元素是该轮的完整状态）
        # if hasattr(aes, 'round_states') and idx < len(aes.round_states):
        #     state = aes.round_states[idx]
        #     st.write("**中间状态 (字节矩阵)**:")
        #     # 假设状态是 4x4 矩阵（列优先），格式为 list of lists 或 flat list
        #     if isinstance(state, (list, tuple)) and len(state) == 16:
        #         # 转为 4x4 列优先 → 行优先显示
        #         matrix = [[state[r + 4 * c] for c in range(4)] for r in range(4)]
        #         st.table([[f"{b:02X}" for b in row] for row in matrix])
        #     else:
        #         st.write(state)  # fallback

        st.divider()


def render_phase3():
    """渲染第三阶段：AES 加密过程可视化"""
    st.header("阶段三：AES 加密过程演示")

   # 获取上一阶段生成的 AES 对象
    if 'aes_obj' not in st.session_state or st.session_state.aes_obj is None:
        st.error("❌ 未检测到有效的 AES 密钥对象，请先完成密钥生成阶段。")
        if st.button("返回上一阶段"):
            st.session_state.aesPhase = 2
            st.rerun()
        return

    aes = st.session_state.aes_obj
    block_size = 16  # AES 固定分组长度 128 位 = 16 字节

    # 上一步按钮（始终显示在顶部）
    if st.button("上一步：密钥设置", type="secondary"):
        st.session_state.aesPhase = 2
        st.rerun()
    st.subheader("1️⃣ 输入明文")
    plaintext_input = st.text_input(
        f"请输入 {block_size} 字符 ASCII 明文（不足将自动填充）:",
        max_chars=block_size,
        key="plaintext_input"
    )
    # 动态展示明文矩阵（列优先 → 转为行优先显示）
    if plaintext_input:
        padded = plaintext_input.ljust(block_size, '\x00')[:block_size]  # 简单填充（实际应使用 PKCS#7）
        plain_bytes = padded.encode('latin1')  # 确保每个字符为 1 字节

        # 显示明文十六进制和矩阵
        col_text, col_matrix = st.columns([1, 2])
        with col_text:
            st.write("**明文 (Hex)**:", plain_bytes.hex().upper())
        with col_matrix:
            st.write("**明文状态矩阵 (4×4, 列优先)**")
            # 转为 4x4 列优先 → 显示为行优先表格
            state = list(plain_bytes)
            matrix = [[state[r + 4 * c] for c in range(4)] for r in range(4)]
            hex_matrix = [[f"{b:02X}" for b in row] for row in matrix]
            st.table(hex_matrix)

    # 控制是否已加密
    if 'encryption_states' not in st.session_state:
        st.session_state.encryption_trace = None

    # 加密按钮
    if st.button("开始加密", type="primary"):
        ciphertext = ''
        if not plaintext_input:
            st.warning("请输入明文")
        else:
            try:
                textInput = ''.join(f"{ord(c):02X}" for c in plaintext_input)
                # padded = plaintext_input.ljust(block_size, '\x00')[:block_size]
                # plain_bytes = padded.encode('latin1')
                # 调用你的加密函数（需返回每轮状态）
                # ciphertext = aes.encrypt(textInput)  # 返回的是最终的密文
                aes.encrypt(textInput)  # 返回的是最终的密文
                st.session_state.encryption_states =  aes.state_round#每一轮的状态
                st.session_state.current_enc_round = 0
            except Exception as e:
                st.error(f"加密失败: {e}")
        # ==============================
        # 加密结果展示区
        # ==============================
    if 'encryption_states' in st.session_state :
        # total_rounds = len(trace['rounds'])  # 假设 trace = {'rounds': [...], 'ciphertext': ...}
        total_rounds = aes.Nr

        st.divider()
        st.subheader("2️⃣ 加密过程详情")

        # 显示当前轮详情
        # 轮次导航
        current_idx = st.session_state.get("current_enc_round", 0)
        current_idx = max(0, min(current_idx, total_rounds ))
        # 轮密钥展示（可折叠）
        with st.expander("查看本轮使用的轮密钥", expanded=False):
            # 显示轮密钥（十六进制）
            st.markdown(f"### 第 {current_idx} 轮")
            round_key = aes.roundKeys[current_idx]
            display_matrix(round_key, "轮密钥")


        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button("◀ 上一轮", disabled=(current_idx <= 0)):
                st.session_state.current_enc_round -= 1
                st.rerun()
        with nav2:
            target = st.number_input(
                "跳转到轮次:",
                min_value=0,
                max_value=total_rounds ,
                value=current_idx,
                step=1
            )
            if target != current_idx:
                st.session_state.current_enc_round = target
                st.rerun()
        with nav3:
            if st.button("下一轮 ▶", disabled=(current_idx >= total_rounds )):
                st.session_state.current_enc_round += 1
                st.rerun()

        # 显示当前轮状态
        idx = st.session_state.current_enc_round
        state = st.session_state.encryption_states[idx]
        if idx != 0:
            st.markdown(f"### 第 {idx} 轮加密结果")
        else:
            st.markdown(f"### 初始轮密钥加结果")

        st.write("**状态矩阵 (4×4)**")
        matrix = state
        # hex_matrix = [[f"{b:02X}" for b in row] for row in matrix]
        st.table(matrix)

        # 显示最终密文（最后一轮后）
        if idx == total_rounds :
            st.success(f"✅ 最终密文 (Hex): `{aes.ciphertext.hex().upper()}`")

        st.divider()
def render_sidebar():
    pub_render_sidebar(
        algorithm_name="AES",
        description="高级加密标准（Advanced Encryption Standard），分组128位，支持128/192/256位密钥，安全高效。"
    )

    with st.sidebar:
        st.header("使用说明")
        st.markdown("""
        **三步流程:**

        1. **密钥阶段**
           - 输入16字节ASCII密钥
           - 执行密钥扩展（Key Expansion）
           - 查看每轮轮密钥（Round Key）

        2. **明文阶段**
           - 输入16字节ASCII明文
           - 动态显示状态矩阵（4×4 列优先）

        3. **加密阶段**
           - 执行AES加密（10/12/14轮）
           - 使用轮次导航查看每轮中间状态
           - 观察 SubBytes、ShiftRows、MixColumns、AddRoundKey 效果

        **当前阶段:** 
        """)

        phase = st.session_state.get('aesPhase', 1)
        if phase == 1:
            st.info(" **阶段一：密钥设置**")
            st.markdown("- 输入16字符ASCII密钥（对应AES-128）")
            st.markdown("- 自动生成11个轮密钥（含初始轮）")
            st.markdown("- 可展开查看轮密钥十六进制值")
        elif phase == 2:
            st.info(" **阶段二：明文输入**")
            st.markdown("- 输入16字符ASCII明文")
            st.markdown("- 实时显示明文状态矩阵（4×4）")
            st.markdown("- 准备进入加密演示")
        elif phase == 3:
            st.info(" **阶段三：加密流程**")
            st.markdown("- 点击“开始加密”启动过程")
            st.markdown("- 使用“上一轮/下一轮”或跳转控制轮次")
            st.markdown("- 查看每轮加密后的状态矩阵")
            st.markdown("- 最终轮无 MixColumns 操作")
def display_matrix(matrix, title="矩阵展示"):
    df = pd.DataFrame(
        matrix,
        columns=["Byte 0", "Byte 1", "Byte 2", "Byte 3"],
        index=[f"Row {i}" for i in range(4)])
    # 显示为交互式表格（支持排序等）
    st.subheader(title)
    st.dataframe(df, use_container_width=True)
# 运行主程序
if __name__ == "__main__":
    main()