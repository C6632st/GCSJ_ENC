
class AESKeyExpansion:

    # 密钥扩展
    PARAMS = {
        16:{'Nk': 4, "Nr": 10, "total_words": 44},#aes-128 密钥长度(字节):{密钥长度(字)，轮次，扩展密钥总字数【(轮次+1)*轮密钥长度(字)】}
        24:{'Nk': 6, "Nr": 12, "total_words": 52},#aes-192
        32:{'Nk': 8, "Nr": 14, "total_words": 60},#aes-256
    }
    # 轮常量
    Rcon = [
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a,
        0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
    ]
    # AES S盒（正向）- 16×16矩阵
    s_box = [
        # 0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,  # 0
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,  # 1
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,  # 2
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,  # 3
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,  # 4
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,  # 5
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,  # 6
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,  # 7
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,  # 8
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,  # 9
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,  # A
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,  # B
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,  # C
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,  # D
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,  # E
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16  # F
    ]

    # 逆S盒（解密用）
    Inv_s_box = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]

    # 列混淆矩阵
    MixColumns_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    # 逆列混淆矩阵
    Inv_MixColumns_matrix = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e]
    ]


    def __init__(self,key):
        key = hex_str_to_byte_list(key)
        self.key = key
        self.key_len = len(key)
        if self.key_len not in self.PARAMS:
            raise ValueError(f"无效密钥长度: {self.key_len}字节")

        params = self.PARAMS[self.key_len]
        self.Nk = params['Nk']
        self.Nr = params['Nr']
        self.total_words = params['total_words']

        # 用于可视化的状态记录
        self.steps = []
        # 用于可视化的状态记录
        self.encryption_steps = []
        self.decryption_steps = []
        # todo 将字组合成每一轮的密钥
        # self.expanded_key = self.key_expansion()
        self.expanded_key = self.key_expansion()
        self.roundKeys =[]
        for i in range(self.Nr+1):
            self.roundKeys.append(self._get_round_key(i))




    def key_expansion(self):
        '''
        key 16字节主密钥
        :return: 44个字（176字节）扩展密钥
        '''
        w = [0] * self.total_words #存放字的数组，后续用来组合成每一轮的轮密钥
        # 1初始填充，前4个字节直接来自主密钥
        self._record_step("初始化", f"从{self.key_len}字节密钥创建前{self.Nk}个字")
        # 每4个字节分为一组，每组32bit
        for i in range(self.Nk):
            w[i] = self.key[i*4:(i+1)*4]
        # 2扩展循环 ：生成后续字
        for i in range(self.Nk,self.total_words):
            temp = w[i-1]#前一个字
            # 判断变换类型
            if  i % self.Nk == 0:
                transform_type ="完全变换"
                temp = self._full_transform(temp, i)#完全变换
                # temp = SubWord(RotWord(temp))#循环左移，字节替换
                # temp[0] ^=  Rcon[i//4]# 与轮常数异或
            elif self.Nk == 8 and i % self.Nk ==4:
                transform_type = "中间变换(AES-256特有)"
                temp = self._mid_transform(temp)#中间变换
            else:
                transform_type = "直接传递"
                pass

            # 记录步骤状态（用于可视化）
            self._record_step(
                f"生成字 w[{i}]",
                f"变换类型: {transform_type}, 结果: {temp}",
                w[i - self.Nk], temp, xor_words(w[i - self.Nk], temp)
            )
            #新字
            w[i] = xor_words(w[i-self.Nk],temp) #w[i] = w[i-4] xor temp
        return w

    def _full_transform(self, word, index):
        """完全变换: RotWord + SubWord + 异或Rcon"""
        temp = RotWord(word)
        temp = SubWord(temp,self.s_box)
        # 将 bytes 转为 bytearray 以便修改
        temp = bytearray(temp)
        rcon_val = self.Rcon[index // self.Nk]
        temp[0] ^= rcon_val  #
        return bytes(temp)  # 转回 bytes 返回
        # temp[0] ^= self.Rcon[index // self.Nk]
        # return temp
    def _mid_transform(self, word):
        """中间变换: 仅SubWord (AES-256特有)"""
        return SubWord(word)
    def _record_step(self, title, description, *data):
        """记录步骤用于可视化"""
        self.steps.append({
            'title': title,
            'description': description,
            'data': data,
            'Nk': self.Nk,
            'current_index': len(self.steps)
        })

# ECB模式
    def encrypt(self,plaintext):
        plaintext = hex_str_to_byte_list(plaintext)
        if len(plaintext) % 16 != 0:
            # 填充（PKCS#7）
            padding_len = 16 - (len(plaintext) % 16)
            plaintext = plaintext + bytes([padding_len] * padding_len)

        # 分块加密
        ciphertext = b''

        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i + 16]

            # 加密当前块
            encrypted_block = self._encrypt_block(block)
            ciphertext += encrypted_block
        self.ciphertext = ciphertext
        # return ciphertext

    def _encrypt_block(self, block):
        """
        加密单个16字节块
        """
        # 初始化状态矩阵（4x4字节矩阵）
        state = bytesToState(block)

        self._record_encryption_step("初始状态", "从明文块创建初始状态矩阵", state)

        # 每一轮展示的状态
        self.state_round =[]

        # 初始轮密钥加
        round_key = self._get_round_key(0)
        state = self._add_round_key(state, round_key)
        self._record_encryption_step("初始轮密钥加", f"与第0轮轮密钥异或", state, round_key)

        self.state_round.append(state)#初始轮密钥加之后

        # 主循环（Nr-1轮）
        for round_num in range(1, self.Nr):
            # 字节替换
            state = SubBytes(state,self.s_box)
            self._record_encryption_step(f"第{round_num}轮-字节替换", "使用S盒替换每个字节", state)

            # 行移位
            state = self._shift_rows(state)
            self._record_encryption_step(f"第{round_num}轮-行移位", "对每行进行循环移位", state)

            # 列混淆
            state = self._mix_columns(state)
            self._record_encryption_step(f"第{round_num}轮-列混淆", "对每列进行混合", state)

            # 轮密钥加
            round_key = self._get_round_key(round_num)
            state = self._add_round_key(state, round_key)
            self.state_round.append(state)
            self._record_encryption_step(f"第{round_num}轮-轮密钥加", f"与第{round_num}轮轮密钥异或", state,
                                         round_key)

        # 最后一轮（无列混淆）
        # 字节替换
        state = SubBytes(state,self.s_box)
        self._record_encryption_step(f"第{self.Nr}轮-字节替换", "最后一轮的字节替换", state)

        # 行移位
        state = self._shift_rows(state)
        self._record_encryption_step(f"第{self.Nr}轮-行移位", "最后一轮的行移位", state)

        # 轮密钥加
        round_key = self._get_round_key(self.Nr)
        state = self._add_round_key(state, round_key)
        self.state_round.append(state)
        self._record_encryption_step(f"第{self.Nr}轮-轮密钥加", f"与第{self.Nr}轮轮密钥异或", state, round_key)

        # 转换为字节输出
        ciphertext = stateToBytes(state)
        self._record_encryption_step("最终密文", "将状态矩阵转换为字节输出", state, None, ciphertext)

        return ciphertext

    def decrypt(self, ciphertext, iv=None):
        """
        AES解密主函数
        """
        if len(ciphertext) % 16 != 0:
            raise ValueError("密文长度必须是16的倍数")

        # 分块解密
        plaintext = b''

        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i + 16]

            # 解密当前块
            decrypted_block = self._decrypt_block(block)

            # 移除填充（如果是最后一块）
            if i + 16 >= len(ciphertext):
                padding_len = decrypted_block[-1]
                if 1 <= padding_len <= 16:
                    # 验证填充
                    if all(decrypted_block[-j] == padding_len for j in range(1, padding_len + 1)):
                        decrypted_block = decrypted_block[:-padding_len]

            plaintext += decrypted_block

        return plaintext


    def _decrypt_block(self, block):
        """
        解密单个16字节块
        """
        state = bytesToState(block)

        self._record_decryption_step("初始状态", "从密文块创建初始状态矩阵", state)

        # 初始轮密钥加（使用最后一轮密钥）
        round_key = self._get_round_key(self.Nr)
        state = self._add_round_key(state, round_key)
        self._record_decryption_step("初始轮密钥加", f"与第{self.Nr}轮轮密钥异或", state, round_key)

        # 主循环（Nr-1轮）
        for round_num in range(self.Nr - 1, 0, -1):
            # 逆行移位
            state = self._inv_shift_rows(state)
            self._record_decryption_step(f"第{round_num}轮-逆行移位", "反向行移位", state)

            # 逆字节替换
            state = invSubBytes(state,self.Inv_s_box)
            self._record_decryption_step(f"第{round_num}轮-逆字节替换", "使用逆S盒替换每个字节", state)

            # 轮密钥加
            round_key = self._get_round_key(round_num)
            state = self._add_round_key(state, round_key)
            self._record_decryption_step(f"第{round_num}轮-轮密钥加", f"与第{round_num}轮轮密钥异或", state, round_key)

            # 逆列混淆
            state = self._inv_mix_columns(state)
            self._record_decryption_step(f"第{round_num}轮-逆列混淆", "反向列混淆", state)

        # 最后一轮
        # 逆行移位
        state = self._inv_shift_rows(state)
        self._record_decryption_step("第0轮-逆行移位", "最后一轮的逆行移位", state)

        # 逆字节替换
        state = invSubBytes(state,self.Inv_s_box)
        self._record_decryption_step("第0轮-逆字节替换", "最后一轮的逆字节替换", state)

        # 轮密钥加（使用第0轮密钥）
        round_key = self._get_round_key(0)
        state = self._add_round_key(state, round_key)
        self._record_decryption_step("第0轮-轮密钥加", f"与第0轮轮密钥异或", state, round_key)

        # 转换为字节输出
        plaintext = stateToBytes(state)
        self._record_decryption_step("最终明文", "将状态矩阵转换为字节输出", state, None, plaintext)

        return plaintext

    def _shift_rows(self, state):
        """行移位"""
        result = [row[:] for row in state]  # 深拷贝
        # 第0行不移位，第1行左移1字节，第2行左移2字节，第3行左移3字节
        for i in range(1, 4):
            result[i] = result[i][i:] + result[i][:i]
        return result
    def _inv_shift_rows(self, state):
        """逆行移位"""
        result = [row[:] for row in state]  # 深拷贝
        # 第0行不移位，第1行右移1字节，第2行右移2字节，第3行右移3字节
        for i in range(1, 4):
            result[i] = result[i][-i:] + result[i][:-i]
        return result

    # def _mix_columns(self, state):
    #     """列混淆"""
    #     result = [[0]*4 for _ in range(4)] #结果矩阵
    #     for i in range(4):#输出行
    #         for j in range(4):#遍历列
    #             val = 0
    #             for k in range(4):#列上4个元素
    #                 # GF(2^8)上的乘法
    #                 if self.MixColumns_matrix[i][k] == 1:
    #                     val ^= state[k][j]
    #                 elif self.MixColumns_matrix[i][k] == 2:
    #                     val ^= self._gmul(state[k][j], 2)
    #                 elif self.MixColumns_matrix[i][k] == 3:
    #                     val ^= self._gmul(state[k][j], 3)
    #             result[i][j] = val & 0xFF
    #     return result
    def _mix_columns(self, state):
        """列混淆 - 输入输出都是十六进制字符串"""
        result = [[0] * 4 for _ in range(4)]

        # 首先将整个状态矩阵转换为整数
        int_state = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                val = state[i][j]
                if isinstance(val, str):
                    if val.startswith('0x'):
                        int_state[i][j] = int(val, 16)
                    else:
                        try:
                            int_state[i][j] = int(val, 16)
                        except ValueError:
                            int_state[i][j] = int(val)
                else:
                    int_state[i][j] = val

        # 执行列混淆
        for i in range(4):
            for j in range(4):
                val = 0
                for k in range(4):
                    state_val = int_state[k][j]

                    # GF(2^8)上的乘法
                    if self.MixColumns_matrix[i][k] == 1:
                        val ^= state_val
                    elif self.MixColumns_matrix[i][k] == 2:
                        val ^= self._gmul(state_val, 2)
                    elif self.MixColumns_matrix[i][k] == 3:
                        val ^= self._gmul(state_val, 3)

                # 转换为小写十六进制字符串
                result[i][j] = f"{val & 0xFF:02x}"

        return result
    def _inv_mix_columns(self, state):
        """逆列混淆"""
        result = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                val = 0
                for k in range(4):
                    val ^= self._gmul(state[k][j], self.Inv_MixColumns_matrix[i][k])
                result[i][j] = val & 0xFF
        return result

    def _add_round_key(self, state, round_key):
        """轮密钥加"""
        result = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                s_val = int(state[i][j], 16)
                k_val = int(round_key[i][j], 16)
                xor_val = s_val ^ k_val  # 异或结果是整数
                result[i][j] = f"{xor_val:02x}"  # 转回2位小写hex字符串
        return result

    def _gmul(self, a, b):
        """GF(2^8)上的有限域乘法"""
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            if hi_bit_set:
                a ^= 0x1b  # AES多项式 x^8 + x^4 + x^3 + x + 1
            a &= 0xFF
            b >>= 1
        return p
    def _get_round_key(self, round_num):
        """获取指定轮数的轮密钥"""
        round_key = [[0]*4 for _ in range(4)]
        for i in range(4):
            word = self.expanded_key[round_num*4 + i]
            for j in range(4):
                round_key[j][i] = word[j]
        return round_key

    def _record_encryption_step(self, title, description, state, round_key=None, output=None):
        """记录加密步骤用于可视化"""
        self.encryption_steps.append({
            'title': title,
            'description': description,
            'state': [row[:] for row in state],  # 深拷贝
            'round_key': [row[:] for row in round_key] if round_key else None,
            'output': output,
            'round': len(self.encryption_steps)
        })

    def _record_decryption_step(self, title, description, state, round_key=None, output=None):
        """记录解密步骤用于可视化"""
        self.decryption_steps.append({
            'title': title,
            'description': description,
            'state': [row[:] for row in state],  # 深拷贝
            'round_key': [row[:] for row in round_key] if round_key else None,
            'output': output,
            'round': len(self.decryption_steps)
        })
# 循环左移1字节
def RotWord(word):
    '''
    将4字节循环左移1字节
    '''
    return word[1:]+word[:1]
    # 字节替换
def SubWord(word,s_box):
    result = []
    for i in range(4):
        result.append(s_box[int(word[i],16)])
    return bytes(result)
    # return bytes(s_box[b] for b in word)
def SubBytes(state,s_box):
    """字节替换"""
    result = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = f"{s_box[int(state[i][j],16)]:02x}"
    return result

def invSubBytes(state, inv_s_box):
    """逆字节替换"""
    result = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = inv_s_box[state[i][j]]
    return result
def xor_words(word1, word2):
    """
    对两个字（4字节数组）进行逐字节异或
    word1: 4字节数组，如 [0x2b, 0x7e, 0x15, 0x16]
    word2: 4字节数组，如 [0x8b, 0x84, 0xeb, 0x01]
    返回: 4字节数组，如 [0xa0, 0xfa, 0xfe, 0x17]
    """
    def to_int_list(w):
        if isinstance(w, (bytes, bytearray)):
            return list(w)
        elif isinstance(w, list) and len(w) == 4:
            return [int(x, 16) for x in w]
        else:
            raise TypeError("输入必须是 bytes、bytearray 或 4 个十六进制字符串的列表")

    int1 = to_int_list(word1)
    int2 = to_int_list(word2)
    xored = [a ^ b for a, b in zip(int1, int2)]
    return [f"{b:02x}" for b in xored]
    # result = bytearray(4)  # 创建4字节的数组
    # for j in range(4):
    #     result[j] = word1[j] ^ word2[j]  # 逐字节异或
    # return result
    # return bytes(a ^ b for a, b in zip(word1, word2))

# ================== 辅助函数 ==================

def bytesToState(data):
    """将16字节转换为4x4状态矩阵"""
    state = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state[j][i] = data[i * 4 + j]  # 按列填充
    return state
# def stateToBytes( state):
#     """将4x4状态矩阵转换为16字节"""
#     data = bytearray(16)
#     for i in range(4):
#         for j in range(4):
#             data[i*4 + j] = state[j][i]  # 按列取出
#     return bytes(data)
def stateToBytes(state):
    """将4x4状态矩阵转换为16字节 - 支持十六进制字符串"""
    data = bytearray(16)
    for i in range(4):
        for j in range(4):
            val = state[j][i]  # 按列取出

            # 如果值是字符串，转换为整数
            if isinstance(val, str):
                # 移除可能的'0x'前缀
                if val.startswith('0x'):
                    val = val[2:]

                # 转换为整数（十六进制）
                int_val = int(val, 16)
            else:
                int_val = int(val)

            data[i * 4 + j] = int_val & 0xFF  # 确保在0-255范围内

    return bytes(data)
# ================== 测试代码 ==================
def test_aes():
    """测试AES加密解密"""
    print("=" * 60)
    print("AES加密测试")
    print("=" * 60)

    # 测试密钥和明文
    key = b'\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c'  # 128位密钥
    plaintext = b'\x32\x43\xf6\xa8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x37\x07\x34'
    iv = b'\x00' * 16  # CBC模式初始向量

    # 创建AES实例
    aes = AESKeyExpansion(key)

    # 加密
    print("\n1. 加密过程:")
    ciphertext = aes.encrypt(plaintext)
    print(f"明文: {plaintext.hex()}")
    print(f"密文: {ciphertext.hex()}")

    # # 打印加密步骤
    # aes.print_encryption_steps()

    # 解密
    print("\n2. 解密过程:")
    decrypted = aes.decrypt(ciphertext)
    print(f"解密结果: {decrypted.hex()}")

    # # 打印解密步骤
    # aes.print_decryption_steps()

    # 验证
    if decrypted[:len(plaintext)] == plaintext:
        print("\n✓ 加密解密成功！")
    else:
        print("\n✗ 加密解密失败！")


def hex_str_to_byte_list(hex_str):
    """
    将十六进制字符串按字节（每2字符）分割为列表
    """
    # 清理：去空格、转小写
    clean = hex_str.replace(' ', '').strip().lower()

    # 检查长度是否为偶数
    if len(clean) % 2 != 0:
        raise ValueError("十六进制字符串长度必须为偶数（每个字节占2字符）")
    # 每2个字符切片
    return [clean[i:i + 2] for i in range(0, len(clean), 2)]

if __name__ == "__main__":
    test_aes()
