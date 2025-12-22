import streamlit as st
import pandas as pd

# ----------标准DES表----------
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

IP_INV_TABLE = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

E_TABLE = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P_TABLE = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

PC1_TABLE = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2_TABLE = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]


# ---------- 初始化状态 ----------
def init_session_state():
    """初始化所有状态变量"""
    if 'phase' not in st.session_state:
        st.session_state.phase = 1  # 1:密钥阶段, 2:明文阶段, 3:加密阶段

    if 'keys_generated' not in st.session_state:
        st.session_state.keys_generated = False

    if 'encryptor' not in st.session_state:
        st.session_state.encryptor = None

    if 'current_view_round' not in st.session_state:
        st.session_state.current_view_round = 0

    if 'show_key_matrices' not in st.session_state:
        st.session_state.show_key_matrices = False

    if 'key_64' not in st.session_state:
        st.session_state.key_64 = None

    if 'key_text' not in st.session_state:
        st.session_state.key_text = ""

    if 'plaintext_64' not in st.session_state:
        st.session_state.plaintext_64 = None

    if 'plain_text' not in st.session_state:
        st.session_state.plain_text = ""

    if 'subkeys' not in st.session_state:
        st.session_state.subkeys = None

    if 'key_details' not in st.session_state:
        st.session_state.key_details = None

    if 'current_key_display' not in st.session_state:
        st.session_state.current_key_display = None

    if 'pc1_result' not in st.session_state:
        st.session_state.pc1_result = None

    if 'cd_pairs' not in st.session_state:
        st.session_state.cd_pairs = None



init_session_state()


# ---------- 工具函数 ----------
def permute(bits_str, table):
    """通用置换函数"""
    if not bits_str:
        return ""
    bits = [''] + list(bits_str)
    return ''.join(bits[i] for i in table)


def bin_to_hex(s):
    """二进制转十六进制"""
    if not s:
        return ""
    return f"{int(s, 2):0{len(s) // 4}X}"


def hex_to_bin(hex_str, length=None):
    """十六进制转二进制"""
    if not hex_str:
        return ""
    n = int(hex_str, 16)
    b = bin(n)[2:]
    if length:
        b = b.zfill(length)
    return b


def left_rotate(bits, n):
    """循环左移"""
    if not bits:
        return ""
    n = n % len(bits)
    return bits[n:] + bits[:n]


def binary_to_matrix(binary_str, rows=8, cols=8):
    """将二进制字符串转换为矩阵"""
    if not binary_str:
        return [[0] * cols for _ in range(rows)]

    if len(binary_str) != rows * cols:
        # 如果不是完整矩阵，按行x列自动填充
        padded = binary_str.ljust(rows * cols, '0')
        binary_str = padded[:rows * cols]

    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            try:
                row.append(int(binary_str[i * cols + j]))
            except:
                row.append(0)
        matrix.append(row)
    return matrix


def display_matrix(matrix, title="矩阵展示"):
    """使用DataFrame展示矩阵"""
    if not matrix:
        st.write(f"**{title}** (无数据)")
        return None

    df = pd.DataFrame(matrix)

    # 设置样式
    styled_df = df.style \
        .set_properties(**{
        'background-color': '#f8f9fa',
        'color': '#212529',
        'border': '1px solid #dee2e6',
        'text-align': 'center',
        'font-family': 'monospace',
        'font-size': '14px',
        'width': '35px',
        'height': '35px'
    }) \
        .format(lambda x: str(int(x)))

    st.write(f"**{title}**")
    st.dataframe(styled_df, use_container_width=True)
    # st.table(styled_df)
    return df


# ---------- 密钥调度 ----------
def generate_subkeys(key_64):
    """生成16个子密钥"""
    if not key_64 or len(key_64) != 64:
        return [], []

    # PC-1置换
    key_56 = permute(key_64, PC1_TABLE)
    st.session_state.pc1_result = key_56  # 保存PC-1结果

    C = key_56[:28]
    D = key_56[28:]

    subkeys = [] #存储每一轮的子密钥
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]#指定轮次的左移位数

    # 存储每一轮的C、D和K值，用于后续展示
    key_schedule_details = []

    # 保存初始C0和D0
    cd_pairs = [{'round': 0, 'C': C, 'D': D, 'shifts': 0}]

    for round_num in range(16):
        shifts = shift_table[round_num]
        C = left_rotate(C, shifts)
        D = left_rotate(D, shifts)
        CD = C + D

        # PC-2置换
        K = permute(CD, PC2_TABLE)
        subkeys.append(K)

        # 保存详细信息
        key_schedule_details.append({
            'round': round_num + 1,
            'C': C,
            'D': D,
            'K': K,
            'K_hex': bin_to_hex(K),
            'shifts': shifts
        })

        # 保存C和D对
        cd_pairs.append({'round': round_num + 1, 'C': C, 'D': D, 'shifts': shifts})

    st.session_state.cd_pairs = cd_pairs  # 保存所有C/D对
    return subkeys, key_schedule_details


def display_key_matrices():
    """展示密钥矩阵"""
    if not st.session_state.subkeys:
        st.warning("没有可显示的密钥数据")
        return

    st.subheader("子密钥矩阵展示")

    # 使用选项卡展示不同轮次的密钥
    tab_names = [f"K{i + 1}" for i in range(min(16, len(st.session_state.subkeys)))]
    tabs = st.tabs(tab_names)

    for idx, tab in enumerate(tabs):
        with tab:
            col1, col2 = st.columns([2, 1])

            with col1:
                # 显示48位密钥矩阵 (6×8)
                k_matrix = binary_to_matrix(st.session_state.subkeys[idx], 6, 8)
                display_matrix(k_matrix, f"K{idx + 1} 矩阵 (6×8)")

            with col2:
                st.write("**密钥信息:**")
                st.write(f"十六进制: {st.session_state.key_details[idx]['K_hex']}")
                st.write(f"长度: 48位")
                st.write(f"左移位数: {st.session_state.key_details[idx]['shifts']}")

                st.write("**C/D 部分:**")
                st.write(f"C{idx + 1} (28位):")
                st.code(st.session_state.key_details[idx]['C'][:20] + "...")
                st.write(f"D{idx + 1} (28位):")
                st.code(st.session_state.key_details[idx]['D'][:20] + "...")

    # 汇总表格
    with st.expander(" 子密钥汇总表"):
        summary_data = []
        for i, detail in enumerate(st.session_state.key_details):
            summary_data.append({
                '轮次': f"{i + 1:02d}",
                '子密钥 (Hex)': detail['K_hex'],
                '左移位数': detail['shifts'],
                'C长度': len(detail['C']),
                'D长度': len(detail['D'])
            })
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)


def display_pc1_details(key_64):
    """显示PC-1置换的详细过程"""
    if not key_64 or len(key_64) != 64:
        return

    st.subheader("PC-1置换详情")

    # 原始64位密钥
    st.write("**原始64位密钥:**")
    st.code(key_64)

    # 显示PC-1置换表的作用
    st.write("**PC-1置换表（56位）：**")
    pc1_df = pd.DataFrame({
        '位置': list(range(1, 57)),
        '原密钥位': [PC1_TABLE[i] for i in range(56)],
        '比特值': [key_64[PC1_TABLE[i] - 1] for i in range(56)]
    })
    st.dataframe(pc1_df.head(56), use_container_width=True)
    # if len(pc1_df) > 20:
    #     st.write(f"... 共{len(pc1_df)}行")

    # PC-1置换结果
    pc1_result = permute(key_64, PC1_TABLE)
    st.write("**PC-1置换结果（56位）：**")
    st.code(pc1_result)

    # 显示C0和D0矩阵
    C0 = pc1_result[:28]
    D0 = pc1_result[28:]

    col1, col2 = st.columns(2)
    with col1:
        st.write("**C₀ (前28位):**")
        st.code(C0)
        c0_matrix = binary_to_matrix(C0.ljust(32, '0'), 4, 8)
        display_matrix(c0_matrix, "C₀ 矩阵 (4×8)")

    with col2:
        st.write("**D₀ (后28位):**")
        st.code(D0)
        d0_matrix = binary_to_matrix(D0.ljust(32, '0'), 4, 8)
        display_matrix(d0_matrix, "D₀ 矩阵 (4×8)")


def display_cd_shifts():
    """显示C和D的循环移位过程"""
    if not st.session_state.cd_pairs:
        return

    st.subheader("C/D循环移位过程")

    # 创建表格显示所有轮的C和D值
    shift_data = []
    for cd in st.session_state.cd_pairs:
        shift_data.append({
            '轮次': cd['round'],
            '左移位数': cd['shifts'],
            # 'C值': cd['C'][:10] + "..." if len(cd['C']) > 10 else cd['C'],
            # 'D值': cd['D'][:10] + "..." if len(cd['D']) > 10 else cd['D'],
            'C值': cd['C'],
            'D值': cd['D'],
            'C长度': len(cd['C']),
            'D长度': len(cd['D'])
        })

    shift_df = pd.DataFrame(shift_data)
    st.dataframe(shift_df, use_container_width=True, hide_index=True)

    # 显示移位细节
    with st.expander("查看详细移位过程"):
        for i in range(min(16, len(st.session_state.cd_pairs) - 1)):
            cd_before = st.session_state.cd_pairs[i]
            cd_after = st.session_state.cd_pairs[i + 1]

            st.write(f"**第{i + 1}轮移位:**")
            st.write(f"移位前 C{i}: {cd_before['C']}")
            st.write(f"移位前 D{i}: {cd_before['D']}")
            st.write(f"左移 {cd_after['shifts']} 位")
            st.write(f"移位后 C{i + 1}: {cd_after['C']}")
            st.write(f"移位后 D{i + 1}: {cd_after['D']}")
            st.divider()


def display_pc2_details():
    """显示PC-2置换的详细过程"""
    if not st.session_state.key_details:
        return

    st.subheader("PC-2置换详情")

    # 选择轮次
    round_num = st.selectbox("选择轮次查看PC-2置换", list(range(1, 17)))

    if round_num:
        idx = round_num - 1
        detail = st.session_state.key_details[idx]
        C = detail['C']
        D = detail['D']
        CD = C + D

        st.write(f"**第{round_num}轮 PC-2输入 (C{round_num}+D{round_num}，56位):**")
        st.code(CD)

        st.write("**PC-2置换表（48位）：**")
        # 显示PC-2置换表的作用
        pc2_positions = []
        for i in range(48):
            pos = PC2_TABLE[i]
            bit_value = CD[pos - 1]  # PC2_TABLE是1-based
            pc2_positions.append({
                '输出位置': i + 1,
                '输入位置': pos,
                '来自': 'C' if pos <= 28 else 'D',
                '比特值': bit_value
            })

        pc2_df = pd.DataFrame(pc2_positions)
        st.dataframe(pc2_df, use_container_width=True)

        st.write(f"**第{round_num}轮子密钥 K{round_num} (48位):**")
        st.code(detail['K'])
        st.write(f"**十六进制:** {detail['K_hex']}")


# ---------- F 函数 ----------
def f_function(r_32, k_48, round_num=None):
    """F函数"""
    if not r_32 or not k_48:
        return {
            'e_out': '',
            'xor_out': '',
            's_out': '',
            'p_out': '',
            'sbox_details': []
        }

    # 1. E扩展
    e_out = permute(r_32, E_TABLE)

    # 2. 异或子密钥
    xor_out = ''.join(str(int(a) ^ int(b)) for a, b in zip(e_out, k_48))

    # 3. S盒替换
    s_out = ''
    sbox_details = []
    for i in range(8):
        block = xor_out[i * 6:(i + 1) * 6]
        row = (int(block[0]) << 1) | int(block[5])
        col = int(block[1:5], 2)
        val = S_BOXES[i][row][col]
        s_out += f"{val:04b}"
        sbox_details.append({
            'S盒': i + 1,
            '输入': block,
            '行': row,
            '列': col,
            '输出': f"{val:04b} ({val})"
        })

    # 4. P置换
    p_out = permute(s_out, P_TABLE)

    return {
        'e_out': e_out,
        'xor_out': xor_out,
        's_out': s_out,
        'p_out': p_out,
        'sbox_details': sbox_details
    }


# ---------- DES 加密器 ----------
class DESEncryptor:
    """DES加密器，支持分步执行"""

    def __init__(self, plaintext_64, key_64, subkeys, key_details):
        self.plaintext = plaintext_64
        self.key = key_64
        self.subkeys = subkeys
        self.key_details = key_details
        self.round_results = []
        self.current_round = 0
        self.max_rounds = 16

        # 初始化
        self._init_encryption()

    def _init_encryption(self):
        """初始化加密状态"""
        # 初始置换
        ip_out = permute(self.plaintext, IP_TABLE)
        L = ip_out[:32]
        R = ip_out[32:]

        # 保存初始状态
        self.round_results.append({
            'round': 0,
            'L': L,
            'R': R,
            'description': '初始置换后',
            'f_result': None,
            'key_used': None
        })

    def get_round(self, round_num):
        """获取指定轮次的状态，如果未计算则计算到该轮次"""
        if round_num < 0 or round_num > self.max_rounds:
            return None

        # 如果请求的轮次已经计算过，直接返回
        if round_num <= len(self.round_results) - 1:
            return self.round_results[round_num]

        # 否则从当前轮次计算到目标轮次
        self.compute_to_round(round_num)
        return self.round_results[round_num] if round_num < len(self.round_results) else None

    def compute_to_round(self, target_round):
        """计算到指定轮次"""
        if target_round <= self.current_round:
            return

        # 从当前轮次开始计算
        current_state = self.round_results[self.current_round]
        L = current_state['L']
        R = current_state['R']

        for round_num in range(self.current_round + 1, target_round + 1):
            if round_num > self.max_rounds:
                break

            # 执行一轮加密
            f_result = f_function(R, self.subkeys[round_num - 1], round_num)
            L_new = R
            R_new = bin(int(L, 2) ^ int(f_result['p_out'], 2))[2:].zfill(32)

            self.round_results.append({
                'round': round_num,
                'L': L_new,
                'R': R_new,
                'description': f'第{round_num}轮后',
                'f_result': f_result,
                'key_used': self.subkeys[round_num - 1]
            })

            L, R = L_new, R_new

        self.current_round = min(target_round, self.max_rounds)

    def get_final_cipher(self):
        """获取最终密文"""
        if self.current_round < self.max_rounds:
            self.compute_to_round(self.max_rounds)

        # 获取最后一轮的结果
        if not self.round_results:
            return ""

        last_round = self.round_results[-1]

        # 注意：最后一轮后不交换，但DES标准要求拼成 R||L
        final_block = last_round['R'] + last_round['L']
        ciphertext = permute(final_block, IP_INV_TABLE)

        return ciphertext


# ---------- Streamlit 应用主程序 ----------
def main():
    st.set_page_config(page_title="DES 加密分步演示", layout="wide")
    st.title("DES 加密算法分步演示系统")

    # 显示当前阶段
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"<h3 style='text-align: center; {'color: green' if st.session_state.phase >= 1 else 'color: gray'}'> 阶段一：密钥</h3>",
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"<h3 style='text-align: center; {'color: green' if st.session_state.phase >= 2 else 'color: gray'}'> 阶段二：明文</h3>",
            unsafe_allow_html=True)
    with col3:
        st.markdown(
            f"<h3 style='text-align: center; {'color: green' if st.session_state.phase >= 3 else 'color: gray'}'> 阶段三：加密</h3>",
            unsafe_allow_html=True)

    st.divider()

    # 第一阶段：密钥输入和生成
    if st.session_state.phase == 1:
        render_phase1()

    # 第二阶段：明文输入
    elif st.session_state.phase == 2:
        render_phase2()

    # 第三阶段：加密流程
    elif st.session_state.phase == 3:
        render_phase3()

    # 侧边栏说明
    render_sidebar()


def render_phase1():
    """渲染第一阶段：密钥设置"""
    st.header("阶段一：密钥设置与生成")

    col1, col2 = st.columns([2, 1])

    current_key_text = ""
    current_key_64 = None

    with col1:
        key_option = st.radio(
            "密钥输入方式:",
            ["使用默认密钥 (ABCDEFGH)", "自定义ASCII密钥", "自定义十六进制密钥"],
            index=0,
            key="key_option"
        )

        if key_option == "使用默认密钥 (ABCDEFGH)":
            current_key_text = "ABCDEFGH"
            current_key_64 = ''.join(f"{ord(c):08b}" for c in current_key_text)
        elif key_option == "自定义ASCII密钥":
            custom_key = st.text_input("输入8字符ASCII密钥:", value="ABCDEFGH", max_chars=8, key="custom_key_input")
            if len(custom_key) == 8:
                current_key_text = custom_key
                current_key_64 = ''.join(f"{ord(c):08b}" for c in current_key_text)
            else:
                st.warning("请输入8个字符")
                current_key_64 = None
        else:  # 十六进制密钥
            hex_key = st.text_input("输入16字符十六进制密钥:", value="4142434445464748", max_chars=16,
                                    key="hex_key_input")
            if len(hex_key) == 16:
                current_key_text = hex_key
                current_key_64 = hex_to_bin(hex_key, 64)
            else:
                st.warning("请输入16个十六进制字符")
                current_key_64 = None

    with col2:
        if current_key_64 and len(current_key_64) == 64:
            st.success("密钥有效")
            st.write(f"密钥文本: `{current_key_text}`")
            st.write(f"密钥长度: {len(current_key_64)} 位")

            # 显示密钥矩阵
            st.write("**主密钥矩阵 (8×8):**")
            key_matrix = binary_to_matrix(current_key_64)
            display_matrix(key_matrix)

            # 保存当前密钥用于显示
            st.session_state.current_key_display = current_key_64

    # 密钥生成按钮 - 修复了按钮位置问题
    if current_key_64 and len(current_key_64) == 64:
        # 将生成密钥按钮放在主区域
        if st.button("生成子密钥", type="primary", key="gen_keys"):
            with st.spinner("正在生成16个子密钥..."):
                subkeys, key_details = generate_subkeys(current_key_64)

                if subkeys:
                    # 保存到session state
                    st.session_state.subkeys = subkeys
                    st.session_state.key_details = key_details
                    st.session_state.key_64 = current_key_64
                    st.session_state.key_text = current_key_text
                    st.session_state.keys_generated = True
                    st.session_state.current_key_display = current_key_64

                    st.success(f"成功生成16个子密钥")
                    st.rerun()

    # 如果已经生成了子密钥，显示详细信息和进入下一阶段的按钮
    if st.session_state.get('keys_generated'):
        st.subheader("密钥调度结果")

        # 显示密钥生成细节的选项卡
        tab1, tab2, tab3, tab4 = st.tabs(["PC-1置换", "C/D循环移位", "PC-2置换", "子密钥矩阵"])

        with tab1:
            display_pc1_details(st.session_state.key_64)

        with tab2:
            display_cd_shifts()

        with tab3:
            display_pc2_details()

        with tab4:
            display_key_matrices()

        # 进入下一阶段按钮 - 修复：将按钮放在最后，确保在显示所有信息之后
        st.divider()
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("进入第二阶段（输入明文）", type="secondary", key="next_to_phase2"):
                st.session_state.phase = 2
                st.rerun()


def render_phase2():
    """渲染第二阶段：明文输入"""
    st.header("阶段二：明文输入")

    # 显示已生成的密钥信息
    with st.expander("已生成密钥信息", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**主密钥:** {st.session_state.get('key_text', 'N/A')}")
            st.write(f"**密钥长度:** {len(st.session_state.get('key_64', ''))}位")
        with col2:
            if st.button("返回第一阶段", key="back_to_phase1"):
                st.session_state.phase = 1
                st.rerun()

    plain_option = st.radio(
        "明文输入方式:",
        ["使用默认明文 (Hello123)", "自定义ASCII明文", "自定义十六进制明文"],
        index=0,
        key="plain_option"
    )

    plaintext_64 = None
    plain_text = ""

    if plain_option == "使用默认明文 (Hello123)":
        plain_text = "Hello123"
        plaintext_64 = ''.join(f"{ord(c):08b}" for c in plain_text)
    elif plain_option == "自定义ASCII明文":
        custom_plain = st.text_input("输入8字符ASCII明文:", value="Hello123", max_chars=8, key="custom_plain_input")
        if len(custom_plain) == 8:
            plain_text = custom_plain
            plaintext_64 = ''.join(f"{ord(c):08b}" for c in plain_text)
        else:
            st.warning("请输入8个字符")
    else:  # 十六进制明文
        hex_plain = st.text_input("输入16字符十六进制明文:", value="48656C6C6F313233", max_chars=16,
                                  key="hex_plain_input")
        if len(hex_plain) == 16:
            plain_text = hex_plain
            plaintext_64 = hex_to_bin(hex_plain, 64)
        else:
            st.warning("请输入16个十六进制字符")

    if plaintext_64 and len(plaintext_64) == 64:
        # 保存明文到session state
        st.session_state.plaintext_64 = plaintext_64
        st.session_state.plain_text = plain_text

        st.success("明文有效")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"明文文本: `{plain_text}`")
            st.write(f"明文长度: {len(plaintext_64)} 位")
            st.write(f"十六进制: {bin_to_hex(plaintext_64)}")

        with col2:
            # 显示明文矩阵
            plain_matrix = binary_to_matrix(plaintext_64)
            display_matrix(plain_matrix, "明文矩阵 (8×8)")

        # 进入加密阶段按钮
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("返回第一阶段", key="back_to_keys_from_plain"):
                st.session_state.phase = 1
                st.rerun()
        with col2:
            if st.button("开始第三阶段（加密）", type="primary", key="start_encryption"):
                st.session_state.phase = 3
                st.rerun()


def render_phase3():
    """渲染第三阶段：加密流程"""
    # 检查必要数据
    if not (st.session_state.get('keys_generated') and st.session_state.get('plaintext_64')):
        st.error("缺少必要数据，请返回前两个阶段")
        if st.button("返回第一阶段"):
            st.session_state.phase = 1
            st.rerun()
        return

    st.header("阶段三：加密流程")

    # 显示摘要信息
    with st.expander("加密配置摘要", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**密钥信息:**")
            st.write(f"主密钥: {st.session_state.get('key_text', 'N/A')}")
            st.write(f"子密钥数: 16个")
        with col2:
            st.write("**明文信息:**")
            st.write(f"明文: {st.session_state.get('plain_text', 'N/A')}")
            st.write(f"长度: 64位")

    # 初始化加密器按钮
    if st.session_state.encryptor is None:
        if st.button("开始加密", type="primary", key="init_encryptor"):
            with st.spinner("正在初始化加密器..."):
                encryptor = DESEncryptor(
                    st.session_state.plaintext_64,
                    st.session_state.key_64,
                    st.session_state.subkeys,
                    st.session_state.key_details
                )
                st.session_state.encryptor = encryptor
                st.session_state.current_view_round = 0
                st.rerun()

    # 如果加密器已初始化，显示控制界面
    if st.session_state.encryptor is not None:
        encryptor = st.session_state.encryptor

        # 阶段导航
        st.subheader("操作导航")
        nav_cols = st.columns(4)
        with nav_cols[0]:
            if st.button("返回第一阶段", key="back_to_phase1_from_encrypt"):
                st.session_state.phase = 1
                st.rerun()
        with nav_cols[1]:
            if st.button("返回第二阶段", key="back_to_phase2_from_encrypt"):
                st.session_state.phase = 2
                st.rerun()
        with nav_cols[2]:
            if st.button("重新初始化", key="reset_encryptor"):
                st.session_state.encryptor = None
                st.session_state.current_view_round = 0
                st.rerun()

        # 轮次导航控制
        st.subheader("轮次导航")

        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

        with col1:
            if st.button("初始轮", use_container_width=True, key="to_round_0"):
                st.session_state.current_view_round = 0
                st.rerun()

        with col2:
            if st.button("上一轮", use_container_width=True,
                         key="prev_round") and st.session_state.current_view_round > 0:
                st.session_state.current_view_round -= 1
                st.rerun()

        with col3:
            target_round = st.slider(
                "跳转到轮次:",
                0, 16,
                st.session_state.current_view_round,
                key="round_slider"
            )
            if target_round != st.session_state.current_view_round:
                st.session_state.current_view_round = target_round
                st.rerun()

        with col4:
            if st.button("下一轮", use_container_width=True,
                         key="next_round") and st.session_state.current_view_round < 16:
                st.session_state.current_view_round += 1
                st.rerun()

        with col5:
            if st.button("最终轮", use_container_width=True, key="to_final_round"):
                st.session_state.current_view_round = 16
                st.rerun()

        # 显示当前轮次信息
        current_round = st.session_state.current_view_round
        round_data = encryptor.get_round(current_round)

        if round_data:
            render_round_details(current_round, round_data, encryptor)

        # 显示轮次进度
        st.divider()
        st.write("**加密进度:**")
        progress = current_round / 16
        st.progress(progress, text=f"已完成 {current_round}/16 轮")

        # 轮次状态表格
        render_round_status_table(current_round)


def render_round_details(current_round, round_data, encryptor):
    """渲染轮次详细信息"""
    if current_round == 0:
        # 显示初始置换
        st.write("**初始置换 IP 结果:**")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"L₀ (左32位):")
            st.code(round_data['L'])
            L_matrix = binary_to_matrix(round_data['L'], 4, 8)
            display_matrix(L_matrix, "L₀ 矩阵 (4×8)")

        with col2:
            st.write(f"R₀ (右32位):")
            st.code(round_data['R'])
            R_matrix = binary_to_matrix(round_data['R'], 4, 8)
            display_matrix(R_matrix, "R₀ 矩阵 (4×8)")

    elif current_round <= 16:
        # 显示加密轮次
        st.write(f"**第 {current_round} 轮加密结果:**")

        # 显示L和R
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"L{current_round}:")
            st.code(round_data['L'])
            L_matrix = binary_to_matrix(round_data['L'], 4, 8)
            display_matrix(L_matrix, f"L{current_round} 矩阵 (4×8)")

        with col2:
            st.write(f"R{current_round}:")
            st.code(round_data['R'])
            R_matrix = binary_to_matrix(round_data['R'], 4, 8)
            display_matrix(R_matrix, f"R{current_round} 矩阵 (4×8)")

        # 显示F函数详情
        if round_data['f_result']:
            with st.expander("查看F函数详情", expanded=False):
                render_f_function_details(current_round, round_data)

    # 如果到达最终轮，显示密文
    if current_round == 16:
        st.subheader("加密完成！")

        # 获取最终密文
        ciphertext = encryptor.get_final_cipher()

        col1, col2 = st.columns(2)

        with col1:
            st.write("**最终密文:**")
            st.write(f"二进制: `{ciphertext}`")
            st.write(f"十六进制: `{bin_to_hex(ciphertext)}`")

            # 尝试解码为ASCII
            try:
                ascii_text = ''.join(chr(int(ciphertext[i:i + 8], 2)) for i in range(0, 64, 8))
                if all(32 <= ord(c) <= 126 for c in ascii_text):
                    st.write(f"ASCII: `{ascii_text}`")
            except:
                pass

        with col2:
            # 显示密文矩阵
            cipher_matrix = binary_to_matrix(ciphertext)
            display_matrix(cipher_matrix, "密文矩阵 (8×8)")


def render_f_function_details(round_num, round_data):
    """渲染F函数详细信息"""
    f_result = round_data['f_result']

    st.write(f"**使用的子密钥 K{round_num}:**")
    st.code(round_data['key_used'])
    st.write(f"十六进制: {bin_to_hex(round_data['key_used'])}")

    # 显示F函数各步骤
    tabs = st.tabs(["1. E扩展", "2. 异或", "3. S盒", "4. P置换"])

    with tabs[0]:
        st.write(f"E(R{round_num - 1}):")
        st.code(f_result['e_out'])
        e_matrix = binary_to_matrix(f_result['e_out'], 6, 8)
        display_matrix(e_matrix, "E扩展结果 (6×8)")

    with tabs[1]:
        st.write(f"E(R) ⊕ K{round_num}:")
        st.code(f_result['xor_out'])
        xor_matrix = binary_to_matrix(f_result['xor_out'], 6, 8)
        display_matrix(xor_matrix, "异或结果 (6×8)")

    with tabs[2]:
        st.write("S盒替换结果:")
        st.code(f_result['s_out'])
        s_matrix = binary_to_matrix(f_result['s_out'], 4, 8)
        display_matrix(s_matrix, "S盒输出 (4×8)")

        # S盒详情表格
        sbox_df = pd.DataFrame(f_result['sbox_details'])
        st.dataframe(sbox_df, use_container_width=True, hide_index=True)

    with tabs[3]:
        st.write("P置换结果 (F函数输出):")
        st.code(f_result['p_out'])
        p_matrix = binary_to_matrix(f_result['p_out'], 4, 8)
        display_matrix(p_matrix, "P置换结果 (4×8)")


def render_round_status_table(current_round):
    """渲染轮次状态表格"""
    status_data = []
    for i in range(0, 17):
        status = "✅" if i <= current_round else "⏳"
        if i == 0:
            desc = "初始置换"
        elif i == 16:
            desc = "完成"
        else:
            desc = f"第{i}轮"
        status_data.append({
            '状态': status,
            '轮次': i,
            '描述': desc,
            '当前': "📍" if i == current_round else ""
        })

    status_df = pd.DataFrame(status_data)
    st.dataframe(status_df, use_container_width=True, hide_index=True)


def render_sidebar():
    """渲染侧边栏说明"""
    with st.sidebar:
        st.header("使用说明")
        st.markdown("""
        **三步流程:**

        1. **密钥阶段**
           - 输入或选择密钥
           - 生成16个子密钥
           - 查看PC-1、循环移位、PC-2等详细过程

        2. **明文阶段**
           - 输入明文
           - 查看明文矩阵

        3. **加密阶段**
           - 初始化加密器
           - 使用导航控制轮次
           - 查看每轮详细结果

        **当前阶段:** 
        """)

        # 显示当前阶段状态
        phase = st.session_state.phase
        if phase == 1:
            st.info(" **阶段一：密钥设置**")
            st.markdown("- 选择密钥输入方式")
            st.markdown("- 点击生成子密钥")
            st.markdown("- 查看详细的密钥调度过程")
            st.markdown("- 包括PC-1置换、循环移位、PC-2置换")
        elif phase == 2:
            st.info(" **阶段二：明文输入**")
            st.markdown("- 选择明文输入方式")
            st.markdown("- 查看明文矩阵")
            st.markdown("- 准备进入加密阶段")
        elif phase == 3:
            st.info(" **阶段三：加密流程**")
            st.markdown("- 初始化加密器")
            st.markdown("- 使用轮次导航")
            st.markdown("- 查看详细结果")



# 运行主程序
if __name__ == "__main__":
    main()