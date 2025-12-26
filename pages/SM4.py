# sm4_demo.py
import streamlit as st
import pandas as pd
from sidebar_utils import pub_render_sidebar


def sm4Sbox(x):
    SboxTable = [
        0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
        0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
        0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
        0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
        0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
        0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
        0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
        0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
        0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
        0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
        0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
        0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
        0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
        0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
        0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48
    ]
    return SboxTable[x]

def ROTL(x, n):
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

def XOR(a, b):
    return a ^ b

class SM4WithAnimation:
    def __init__(self):
        self.steps = []
        self.rk = []
        self.FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
        self.CK = [
            0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,
            0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
            0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,
            0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
            0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229,
            0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
            0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,
            0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279
        ]

    def T(self, x):
        # 非线性tau
        x0 = (x >> 24) & 0xFF
        x1 = (x >> 16) & 0xFF
        x2 = (x >> 8) & 0xFF
        x3 = x & 0xFF
        y0 = sm4Sbox(x0)
        y1 = sm4Sbox(x1)
        y2 = sm4Sbox(x2)
        y3 = sm4Sbox(x3)
        y = (y0 << 24) | (y1 << 16) | (y2 << 8) | y3

        # 线性 L
        z = y ^ ROTL(y, 2) ^ ROTL(y, 10) ^ ROTL(y, 18) ^ ROTL(y, 24)
        return z

    def sm4_setkey_with_animation(self, key_bytes):
        self.steps = []
        key = [int.from_bytes(key_bytes[i:i+4], 'big') for i in range(0, 16, 4)]
        MK = [key[0] ^ self.FK[0], key[1] ^ self.FK[1],
              key[2] ^ self.FK[2], key[3] ^ self.FK[3]]
        k = MK[:]
        self.rk = []

        for i in range(32):
            step_info = {
                'round': i,
                'K': k.copy(),
                'CK': self.CK[i],
                'before_tau': None,
                'after_tau': None,
                'after_L': None,
                'RK': None
            }

            tmp = k[1] ^ k[2] ^ k[3] ^ self.CK[i]
            step_info['before_tau'] = tmp
            after_tau = (
                (sm4Sbox((tmp >> 24) & 0xFF) << 24) |
                (sm4Sbox((tmp >> 16) & 0xFF) << 16) |
                (sm4Sbox((tmp >> 8) & 0xFF) << 8) |
                sm4Sbox(tmp & 0xFF)
            )
            step_info['after_tau'] = after_tau

            after_L = after_tau ^ ROTL(after_tau, 13) ^ ROTL(after_tau, 23)
            step_info['after_L'] = after_L

            rk_i = after_L ^ k[0]
            self.rk.append(rk_i)
            step_info['RK'] = rk_i

            # Update k
            k = [k[1], k[2], k[3], rk_i]
            self.steps.append(step_info)

        return self.steps

    def sm4_crypt_ecb_with_animation(self, plain_bytes):
        self.encrypt_steps = []
        X = [int.from_bytes(plain_bytes[i:i+4], 'big') for i in range(0, 16, 4)]
        state = X[:]

        for i in range(32):
            step = {
                'round': i,
                'input': state.copy(),
                'XOR_input': None,
                'T_output': None,
                'output': None
            }
            xor_val = state[1] ^ state[2] ^ state[3] ^ self.rk[i]
            step['XOR_input'] = xor_val
            t_out = self.T(xor_val)
            step['T_output'] = t_out
            new_state = [state[1], state[2], state[3], state[0] ^ t_out]
            step['output'] = new_state.copy()
            state = new_state
            self.encrypt_steps.append(step)

        # 最终输出
        cipher = [state[3], state[2], state[1], state[0]]
        ciphertext = b''.join(c.to_bytes(4, 'big') for c in cipher)
        return self.encrypt_steps, ciphertext

# streamlit

def init_session_state():
    if 'sm4Phase' not in st.session_state:
        st.session_state.sm4Phase = 1  # 1:密钥, 2:轮密钥, 3:加密
    if 'sm4_obj' not in st.session_state:
        st.session_state.sm4_obj = None
def render_sidebar():
    pub_render_sidebar(
        algorithm_name="SM4",
        description="中国国家密码标准（GB/T 32907-2016），分组128位，密钥128位，共32轮Feistel结构。"
    )
    """渲染侧边栏说明"""
    with st.sidebar:
        st.header("使用说明")
        st.markdown("""
        **三步流程:**

        1. **密钥阶段**
           - 输入16字节ASCII主密钥
           - 执行密钥扩展（生成32个轮密钥）
           - 查看每轮 CK、S盒变换、线性变换细节

        2. **明文阶段**
           - 输入16字节ASCII明文
           - 准备进入32轮加密流程

        3. **加密阶段**
           - 执行SM4 ECB模式加密
           - 逐轮展示 Feistel 轮函数（T函数）计算过程
           - 查看每轮输入/输出状态及T函数结果

        **当前阶段:** 
        """)

        phase = st.session_state.get('phase', 1)
        if phase == 1:
            st.info(" **阶段一：密钥设置**")
            st.markdown("- 输入16字符ASCII主密钥")
            st.markdown("- 基于FK和CK生成32个轮密钥（RK[0]~RK[31]）")
            st.markdown("- 可查看S盒、线性变换L'等中间步骤")
            st.markdown("- 支持展开查看完整S盒表")
        elif phase == 2:
            st.info(" **阶段二：明文输入**")
            st.markdown("- 输入16字符ASCII明文")
            st.markdown("- 明文将被分为4个32位字（X0~X3）")
            st.markdown("- 准备进入32轮加密演示")
        elif phase == 3:
            st.info(" **阶段三：加密流程**")
            st.markdown("- 点击“开始加密”执行32轮Feistel结构")
            st.markdown("- 每轮展示：异或输入 → S盒 → 线性变换 → 新状态")
            st.markdown("- 使用导航按钮逐轮查看加密过程")
            st.markdown("- 最终输出为密文（16字节）")
def main():
    st.set_page_config(page_title="SM4 算法分步演示", layout="wide")
    st.title("🔐 SM4 国密分组密码算法分步演示")
    init_session_state()
    render_sidebar()

    # 阶段指示器
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<h4 style='text-align:center; color:{'green' if st.session_state.sm4Phase >= 1 else 'gray'}'>阶段一：密钥</h4>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4 style='text-align:center; color:{'green' if st.session_state.sm4Phase >= 2 else 'gray'}'>阶段二：轮密钥</h4>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h4 style='text-align:center; color:{'green' if st.session_state.sm4Phase >= 3 else 'gray'}'>阶段三：加密</h4>", unsafe_allow_html=True)

    st.divider()

    if st.session_state.sm4Phase == 1:
        render_phase1()
    elif st.session_state.sm4Phase == 2:
        render_phase2()
    elif st.session_state.sm4Phase == 3:
        render_phase3()

def render_phase1():
    st.subheader("1️⃣ 输入 16 字节 ASCII 密钥")
    key_input = st.text_input("密钥（16字符）:", max_chars=16, key="key_input")
    if len(key_input) == 16:
        st.success("✅ 密钥长度正确")
        if st.button("下一步：生成轮密钥", type="primary"):
            st.session_state.key_bytes = key_input.encode('latin1')
            st.session_state.sm4Phase = 2
            st.rerun()
    else:
        st.warning("请输入恰好 16 个 ASCII 字符")

def render_phase2():
    st.subheader("2️⃣ 轮密钥生成（32 轮）")

    if st.button("上一步：密钥", type="secondary"):
        st.session_state.sm4Phase = 1
        st.rerun()

    if st.button("生成轮密钥", type="primary"):
        try:
            sm4 = SM4WithAnimation()
            steps = sm4.sm4_setkey_with_animation(st.session_state.key_bytes)
            st.session_state.sm4_obj = sm4
            st.session_state.key_schedule_steps = steps
            st.session_state.current_key_round = 0
        except Exception as e:
            st.error(f"密钥扩展失败: {e}")

    if 'key_schedule_steps' in st.session_state:
        steps = st.session_state.key_schedule_steps
        total = len(steps)  # 32
        idx = st.session_state.get('current_key_round', 0)
        idx = max(1, min(idx, total))

        # S盒展示（可折叠）
        with st.expander("查看 S 盒", expanded=False):
            sbox_2d = [[f"{sm4Sbox(i):02X}" for i in range(j, j+16)] for j in range(0, 256, 16)]
            st.table(sbox_2d)

        # 导航
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button("◀ 上一轮", disabled=(idx <= 0)):
                st.session_state.current_key_round -= 1
                st.rerun()
        with nav2:
            target = st.number_input("轮次:", 1, total, idx)
            if target != idx:
                st.session_state.current_key_round = target
                st.rerun()
        with nav3:
            if st.button("下一轮 ▶", disabled=(idx >= total)):
                st.session_state.current_key_round += 1
                st.rerun()

        # 显示当前轮
        step = steps[idx-1]
        st.markdown(f"### 第 {idx} 轮密钥扩展")
        st.write(f"**CK[{idx}]**: `0x{step['CK']:08X}`")
        st.write(f"**RK[{idx}]**: `0x{step['RK']:08X}`")
        st.write("**中间步骤**:")
        st.write(f"- 异或输入: `0x{step['before_tau']:08X}`")
        st.write(f"- S盒输出: `0x{step['after_tau']:08X}`")
        st.write(f"- 线性变换后: `0x{step['after_L']:08X}`")

        if st.button("下一步：加密", type="primary"):
            st.session_state.sm4Phase = 3
            st.rerun()

def render_phase3():
    st.subheader("3️⃣ SM4 加密过程（32 轮）")

    if st.button("上一步：轮密钥", type="secondary"):
        st.session_state.sm4Phase = 2
        st.rerun()

    plaintext = st.text_input("明文（16字符）:", max_chars=16, key="plain_input")
    if len(plaintext) != 16:
        st.warning("请输入恰好 16 个 ASCII 字符")
        return

    if st.button("开始加密", type="primary"):
        try:
            plain_bytes = plaintext.encode('latin1')
            sm4 = st.session_state.sm4_obj
            encrypt_steps, ciphertext = sm4.sm4_crypt_ecb_with_animation(plain_bytes)
            st.session_state.encrypt_steps = encrypt_steps
            st.session_state.ciphertext = ciphertext.hex().upper()
            st.session_state.current_encrypt_round = 0
        except Exception as e:
            st.error(f"加密失败: {e}")

    if 'encrypt_steps' in st.session_state:
        steps = st.session_state.encrypt_steps
        total = len(steps)  # 32
        idx = st.session_state.get('current_encrypt_round', 0)
        idx = max(1, min(idx, total ))

        # 导航
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button("◀ 上一轮", disabled=(idx <= 0)):
                st.session_state.current_encrypt_round -= 1
                st.rerun()
        with nav2:
            target = st.number_input("轮次:", 0, total, idx)
            if target != idx:
                st.session_state.current_encrypt_round = target
                st.rerun()
        with nav3:
            if st.button("下一轮 ▶", disabled=(idx >= total)):
                st.session_state.current_encrypt_round += 1
                st.rerun()

        # 显示当前轮
        step = steps[idx-1]
        st.markdown(f"### 第 {idx} 轮加密")
        # st.write(f"**输入状态**: {[f'0x{x:08X}' for x in step['input']]}")
        display_matrix(hex_list_to_4x4_hex_matrix([f'0x{x:08X}' for x in step['input']]),'输入状态')
        st.write(f"**T 函数输出**: `0x{step['T_output']:08X}`")
        # st.write(f"**输出状态**: {[f'0x{x:08X}' for x in step['output']]}")
        display_matrix(hex_list_to_4x4_hex_matrix([f'0x{x:08X}' for x in step['output']]),'输出状态')

        if idx == total :
            st.success(f"✅ 最终密文: `{st.session_state.ciphertext}`")
def display_matrix(matrix, title="矩阵展示"):
    df = pd.DataFrame(
        matrix,
        columns=["Byte 0", "Byte 1", "Byte 2", "Byte 3"],
        index=[f"Row {i}" for i in range(4)])
    # 显示为交互式表格（支持排序等）
    st.subheader(title)
    st.dataframe(df, use_container_width=True)


def hex_list_to_4x4_hex_matrix(hex_list):
    """将4个32位十六进制字符串列表转换为4x4十六进制字符串矩阵"""
    matrix = []
    for hex_str in hex_list:
        # 去掉'0x'前缀，确保是8位十六进制
        hex_val = hex_str[2:] if hex_str.startswith('0x') else hex_str
        # 补齐8位
        hex_val = hex_val.zfill(8)

        # 每2个十六进制字符为一个字节，保持为十六进制字符串
        row = [hex_val[i:i + 2].upper() for i in range(0, 8, 2)]
        matrix.append(row)

    return matrix
if __name__ == "__main__":
    main()