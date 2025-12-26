class SM4KeyExpansion:
    # SM4固定参数表
    # 系统参数FK，用于消除对称性
    FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
 # 固定常数CK，32个32位常数
    CK = [
        0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,
        0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
        0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,
        0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
        0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229,
        0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
        0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,
        0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279
    ]
    # SM4的S盒（8位输入，8位输出）
    S_BOX = [
        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,
        0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,
        0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,
        0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,
        0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,
        0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87,
        0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E,
        0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1,
        0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3,
        0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29, 0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F,
        0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 0x5B, 0x51,
        0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8,
        0x0A, 0xC1, 0x31, 0x88, 0xA8, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0,
        0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84,
        0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48
    ]

    def __init__(self, key):
        """
        初始化SM4密钥扩展器

        Args:
            key: 字节数组，必须为16字节（128位）

        Raises:
            ValueError: 如果密钥长度不是16字节
        """
        if len(key) != 16:
            raise ValueError("SM4密钥长度必须为16字节（128位）")

        self.master_key = key
        self.round_keys = []  # 存储32个轮密钥
        self.expansion_steps = []  # 存储扩展过程的每一步，用于可视化

    def expand(self):
        """
        执行密钥扩展，生成32个轮密钥

        Returns:
            list: 32个轮密钥，每个为4字节的bytes对象
        """
        self.round_keys = []
        self.expansion_steps = []

        # 步骤1: 将主密钥分为4个32位字
        MK = [
            self._bytes_to_word(self.master_key[0:4]),
            self._bytes_to_word(self.master_key[4:8]),
            self._bytes_to_word(self.master_key[8:12]),
            self._bytes_to_word(self.master_key[12:16])
        ]

        self._record_step("初始化", "将128位主密钥分为4个32位字",
                          f"MK0={MK[0]:08X}, MK1={MK[1]:08X}, MK2={MK[2]:08X}, MK3={MK[3]:08X}")

        # 步骤2: 与系统参数FK异或，得到K[0..3]
        K = [
            MK[0] ^ self.FK[0],
            MK[1] ^ self.FK[1],
            MK[2] ^ self.FK[2],
            MK[3] ^ self.FK[3]
        ]

        self._record_step("系统参数异或", "主密钥与固定系统参数FK异或",
                          f"FK={[f'{x:08X}' for x in self.FK]}",
                          f"K0={K[0]:08X}, K1={K[1]:08X}, K2={K[2]:08X}, K3={K[3]:08X}")

        # 步骤3: 32轮扩展循环，生成轮密钥rk[0..31]
        for i in range(32):
            # 计算中间值
            xor_result = K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ self.CK[i]

            # T'变换：非线性τ变换 + 线性变换L'
            t_prime_output = self._tau_transform(xor_result)
            l_prime_output = self._linear_transform_lprime(t_prime_output)

            # 生成新的K值
            K_next = K[i] ^ l_prime_output

            # 生成轮密钥
            rk_i = K_next
            self.round_keys.append(self._word_to_bytes(rk_i))

            # 记录步骤
            self._record_step(
                f"生成轮密钥rk[{i}]",
                f"第{i}轮扩展",
                {
                    "输入": f"K[{i}]={K[i]:08X}, K[{i + 1}]={K[i + 1]:08X}, "
                            f"K[{i + 2}]={K[i + 2]:08X}, K[{i + 3}]={K[i + 3]:08X}",
                    "CK": f"{self.CK[i]:08X}",
                    "异或结果": f"{xor_result:08X}",
                    "τ变换输出": f"{t_prime_output:08X}",
                    "L'变换输出": f"{l_prime_output:08X}",
                    "新K值": f"K[{i + 4}]={K_next:08X}",
                    "轮密钥": f"rk[{i}]={rk_i:08X}"
                }
            )

            # 将新生成的K值加入数组，用于下一轮计算
            K.append(K_next)

        return self.round_keys

    def get_round_key(self, round_num):
        """
        获取指定轮数的轮密钥

        Args:
            round_num: 轮数（0-31）

        Returns:
            bytes: 4字节的轮密钥
        """
        if not 0 <= round_num < 32:
            raise ValueError("轮数必须在0-31之间")

        if not self.round_keys:
            self.expand()

        return self.round_keys[round_num]

    def get_all_round_keys(self):
        """获取所有32个轮密钥"""
        if not self.round_keys:
            self.expand()

        return self.round_keys

    def get_expansion_steps(self):
        """获取扩展过程的详细步骤（用于可视化）"""
        if not self.expansion_steps:
            self.expand()

        return self.expansion_steps

    def _tau_transform(self, word):
        """
        非线性τ变换：对32位字的4个字节分别进行S盒替换

        Args:
            word: 32位整数

        Returns:
            int: 变换后的32位整数
        """
        bytes_list = [
            (word >> 24) & 0xFF,
            (word >> 16) & 0xFF,
            (word >> 8) & 0xFF,
            word & 0xFF
        ]

        transformed_bytes = [
            self.S_BOX[b] for b in bytes_list
        ]

        result = (transformed_bytes[0] << 24) | \
                 (transformed_bytes[1] << 16) | \
                 (transformed_bytes[2] << 8) | \
                 transformed_bytes[3]

        return result

    def _linear_transform_lprime(self, word):
        """
        线性变换L'：用于密钥扩展

        L'(B) = B ⊕ (B <<< 13) ⊕ (B <<< 23)

        Args:
            word: 32位整数

        Returns:
            int: 变换后的32位整数
        """
        # 循环左移13位
        left_rotate_13 = ((word << 13) | (word >> (32 - 13))) & 0xFFFFFFFF

        # 循环左移23位
        left_rotate_23 = ((word << 23) | (word >> (32 - 23))) & 0xFFFFFFFF

        # 异或操作
        result = word ^ left_rotate_13 ^ left_rotate_23

        return result

    def _linear_transform_l(self, word):
        """
        线性变换L：用于加密轮函数（这里列出以供对比）

        L(B) = B ⊕ (B <<< 2) ⊕ (B <<< 10) ⊕ (B <<< 18) ⊕ (B <<< 24)
        """
        # 循环左移2位
        left_rotate_2 = ((word << 2) | (word >> (32 - 2))) & 0xFFFFFFFF

        # 循环左移10位
        left_rotate_10 = ((word << 10) | (word >> (32 - 10))) & 0xFFFFFFFF

        # 循环左移18位
        left_rotate_18 = ((word << 18) | (word >> (32 - 18))) & 0xFFFFFFFF

        # 循环左移24位
        left_rotate_24 = ((word << 24) | (word >> (32 - 24))) & 0xFFFFFFFF

        # 异或操作
        result = word ^ left_rotate_2 ^ left_rotate_10 ^ left_rotate_18 ^ left_rotate_24

        return result

    def _bytes_to_word(self, byte_data):
        """将4字节转换为32位整数"""
        if len(byte_data) != 4:
            raise ValueError("需要4字节数据")

        return (byte_data[0] << 24) | (byte_data[1] << 16) | (byte_data[2] << 8) | byte_data[3]

    def _word_to_bytes(self, word):
        """将32位整数转换为4字节"""
        return bytes([
            (word >> 24) & 0xFF,
            (word >> 16) & 0xFF,
            (word >> 8) & 0xFF,
            word & 0xFF
        ])

    def _record_step(self, title, description, *data):
        """记录扩展步骤（用于可视化）"""
        step_info = {
            'step': len(self.expansion_steps),
            'title': title,
            'description': description,
            'data': data if data else None,
            'round_keys_generated': len(self.round_keys)
        }
        self.expansion_steps.append(step_info)


# 测试代码和示例使用
if __name__ == "__main__":
    # 测试用例1: 全零密钥
    print("=== 测试1: 全零密钥 ===")
    zero_key = bytes(16)  # 16个0x00
    sm4_expander = SM4KeyExpansion(zero_key)
    round_keys = sm4_expander.expand()

    print(f"生成的轮密钥数量: {len(round_keys)}")
    print(f"第一个轮密钥 (rk[0]): {round_keys[0].hex()}")
    print(f"最后一个轮密钥 (rk[31]): {round_keys[31].hex()}")

    # 测试用例2: 标准测试向量
    print("\n=== 测试2: 标准测试向量 ===")
    test_key = bytes.fromhex("0123456789ABCDEFFEDCBA9876543210")
    sm4_expander2 = SM4KeyExpansion(test_key)
    round_keys2 = sm4_expander2.expand()

    # 验证前几个轮密钥（标准测试值）
    expected_rk0 = bytes.fromhex("F12186F9")
    expected_rk1 = bytes.fromhex("41662B61")

    print(f"测试密钥: {test_key.hex()}")
    print(f"rk[0] 计算值: {round_keys2[0].hex()}, 期望值: {expected_rk0.hex()}, "
          f"匹配: {round_keys2[0] == expected_rk0}")
    print(f"rk[1] 计算值: {round_keys2[1].hex()}, 期望值: {expected_rk1.hex()}, "
          f"匹配: {round_keys2[1] == expected_rk1}")

    # 演示可视化数据获取
    print("\n=== 扩展过程步骤示例 ===")
    steps = sm4_expander2.get_expansion_steps()
    for i, step in enumerate(steps[:3]):  # 只显示前3步
        print(f"步骤{i}: {step['title']}")
        print(f"  描述: {step['description']}")
        if step['data']:
            print(f"  数据: {step['data']}")

    # 演示按需获取轮密钥
    print("\n=== 按需获取轮密钥 ===")
    specific_key = sm4_expander2.get_round_key(15)
    print(f"轮密钥15: {specific_key.hex()}")