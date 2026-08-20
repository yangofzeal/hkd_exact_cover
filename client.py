# -*- coding: utf-8 -*-
# HKD OBFUSCATE v4 - portable source payload, no marshal/code-object dependency.
# Protection is import-time only; protected functions have no per-call wrapper.
def _hkd_v4_bootstrap(_g):
    import binascii as _hb
    import hashlib as _hh
    import struct as _hs
    import zlib as _hz

    _b = (
        _hb.unhexlify('d111ab2e086a2226224c40a0b989ab89d166221f9eb0d5a64bb14b689368998181db21717aab719d5684d49e6b1c45e249513f0215b2f957daf75409c5b36361b318d154e46f9ec60bf659ac7a87f4f24f8d15b533aa23620983690ee052ef6030e101aa7977ac3dcea7cf3fe29bacb6825c37d43794d4a40504894ab3e43f8d'),
        _hb.unhexlify('f252ca96c21eb4ebde5f018ac3da26dd17ecd5a13bcbcfb663541f875bee160e4bb0d4778127451d93caa7ab8ccd7f090b470003707bacbdd7b43d3a35503d9260ae9e2328c4ffc6493418f3868bf492b501c7903036374d2b67a4d6fedfb8d2e421d6d45e0d863911863fbcc198e26c14010416cfb636f91848efbd97b7fb40'),
        _hb.unhexlify('beeb7c7bc39fb09a854dd6bf8ebe812ac0d4e7f02bda19f24b6160fffef6936134ada2c536c44383b5e388a3dc2f024bbe4512c3c5de48dc8c517ccf5c9ed1f292450a169e991970398d16811fdfc1d33f7d83073ced9cb2b60d9041b8591ea6534dfa0a4aa0fa9d80f85b1d47a755b64b529a6dc886ce86eb83ac11020c53ef'),
        _hb.unhexlify('737bd0938cd9cd80385676674a64146b40f65215f9bb953c123873ebe8780921346590bda2d88ea1261e3f2cda50817c6495791d8b2b7d9d41b901deac19055588c21df3c8684bd2928a8698f833a9d1eed9c03b6e7f7d299fcd873c00c7625100bd6f60a5dd28da42d7751a6cf04008fe9d5ea2316caf4ddbeef601b2ee6ff7'),
        _hb.unhexlify('85b96d7f54c3b5ef663d29f95f71bbe627d8928ba7e59d8e46275baf7b3e80eb62ce20e1b7f29ecc3ee3f18ee9cfc4fbfe3cd7340893fe80666e820eac42239a51428227ed921a6a06fee1311240ef46d9bcad47003b9f1af109fb390932e4ad8835a4ab5642e33155566fdefd6da055ebcbfc0c28d0750901e8c97f9b72fa2e'),
        _hb.unhexlify('eda28eb32b40547f0e4d4b037882037dc57a030381353b308ca58fd02f1374fdd3e0bd9bbe5b70d63e5f4904e96e700fbf7686dce2305ed681d90a81621206818d24e973d9f8cfe630a7f98e5fbd8966ab8b6cf745443c2c56b8c891d9d5edf4f369cb4cfc3604956ad9ca71167505b454581d3a4eb67e8d6ccbf5cb19ec470e'),
        _hb.unhexlify('00ec78b37c066eef31124696a59d96d33ae7067ebf3f2e4d248a79ce7fe0dba7de4c4aa14ec2f3abce08d3fedfe4cda88dc40dc0286ece68d2d375cc586adf9cf0bb3847bf1afaede408b5915a44c60b849ccb6e278c05c186ff4f2b5b721be01007781532e8b3874b16c233da4e42e1d4a6407f17ccf1c604bbcbfd0001a1c2'),
        _hb.unhexlify('6af19c590beb43db5a0a4ec974e8d2933be51893f77350ba5e32205c27ae29ab74f8e31d4daa014dce56705088ec80612ae6da1ab13e0b7f429cedc4be3d064f3cd7d725ddbbc6b9136402d1c1361ba5c1354893dafeafa843f49c30dbf49ed727970cc21d7c11a7e8ba769687980f0a1bae05e392e4834b40892ff3b23f19fc'),
        _hb.unhexlify('aa725d65768adfc77f333561849b86374d8b6b1e3f04d56e4d6faa56648fd4b257b8591a54406192070724ca87733aa36e553912ccfef9e104ab015801a9c33cbeaef9a92e12716516b029c753d8fd62a34410448d71c28c7ad9d8c8cb592cdabb18f0ad25b8442b6ca7d666d7598353a85a412e6e89964ae58025bf068d9139'),
        _hb.unhexlify('dd8057e48e16f189fdf4'),
        _hb.unhexlify('770e1aa65fc459535f5bd5370e1f9f77ebc6084e963c4c6a597b8d889c48407dec204872298218a5e4086dbdbcf8fe8f55dedc73ace589667ed50be16f3ee498165d3d4bad247d9cf428a06386bc14d8865af8062b8a167a2b2573c902c61a2d8baf0ecf0ae4630b450dd4f74830784a1aa99a00c80d9ad6d5ba1a77f6d8ff7d'),
        _hb.unhexlify('56bfff8621442cff93cac8e5e25532a15ef294aac85d5e26fd99502c66afe03531754a9c1b0451dcf9cb6fd266c5dcea6b6c5b8ef75704308a50a799feaaf07f7e4a738cf0a74fb494725c45727f3c0320c3d6d9f91f4c243b5993ecc2c07a8ffc521c5f437d12991007cc2f761a0bd5719a167f41a81b9dcf5e311aaf8ef590'),
        _hb.unhexlify('35a9d2224d0a417525c7d39ecb1cab586d3b8dc6e40ffc54bd672bbd4a1080db6cb3cb82f58f788f240370dff434427faae72d3e382439debc103fba9a7c62b7d01233cfcdb55df850e2cfa060383d888145247c3e4539fd749c70457010d1d11abb2a44f49eab14aad1cf4c21f5c4a10a4f39f7d151692d259597fb32845ac4'),
        _hb.unhexlify('09c28c5ba1aa4fd2aebfebb68c7528496b5a37fbfefa90d7da307ebcca606f0241673defa79e771fe6a57add419092a41bb726c65bc8597b4afda62ead54a56f32dfe2ab5d5db5e813562d0dc620b9462d59adc75ac01b14ff00a5aee3a8fa6a7fb2d3ef98cad335c570424d70f2d98db6b9b9fef0cfbffb6fa600e0ed0f02fa'),
        _hb.unhexlify('e99028c39c73c22c1e2b244f850b9f68b0f8655a7780e7c089f290ffc68d6dc5410a19342c66211fe8bd6811cbcbe63d166311b731f53847d6d4db9fc977a43e03ac7783430cdb9e17ce13b496ee513ac11a0d970868ca264753ae7d4de5b3806ae05540945326d6d71ae42392906f0b5c2fc434521b81858df637829bca5d98'),
    )
    _inv = (8, 10, 14, 5, 13, 11, 2, 7, 6, 12, 4, 3, 0, 1, 9)
    _leaves = (
        _hb.unhexlify('a0323b69aea0048966f863e75b2268a1cfa2b0b83c7a31c9bdfd99079a1e7802'),
        _hb.unhexlify('7f04534420c194b6352adeaac2bfb60cbef4545f86847bc750d1d5acf289225b'),
        _hb.unhexlify('0b1af978c611a4270bfe6fff096ee5a4046d41ec9ad5c5f52060862bd2ee5a73'),
        _hb.unhexlify('467aeef50c3e6a515e55ba9ad924f7eb9ac9717517c9f5d741906d5168332c66'),
        _hb.unhexlify('de1ef7a31ac359da387f1ff7a0f1e400e4527d2fb97651883ca47d8753714d24'),
        _hb.unhexlify('8c8c94c9c1556bb6699a7d52f06800d37d75a73384cbb5da2a123c3178b6a496'),
        _hb.unhexlify('91fee248d51746eb8027c17effb269f438e07ca2a282c017b3d204b1ce9aec40'),
        _hb.unhexlify('0a423f7d15a8c23bce6bd4615981b9e2022ba7fa02abcd2758e19cc7cfab23cf'),
        _hb.unhexlify('38132be6d43960713fc3ccb32e5b25a14ca8eddc7fc7a37373d33d85b80d814b'),
        _hb.unhexlify('ff1fe75150a4f2697a1dbfb4c10954d62b93558617a4cea91f80dad76553a4c7'),
        _hb.unhexlify('1884f6b20c777d2cbc7df0fcdb37a0ff289bb00914c843d7f99ff71fe9d0356e'),
        _hb.unhexlify('a7bc7f61fb0762348f2993172352564ce64bba98c99763504e4b6da335743c66'),
        _hb.unhexlify('eb86c4f73438338ed14751b53c90d884a72ef975f6f4539946454630ec73d190'),
        _hb.unhexlify('dfae41bc05783d0a5be88930b5457eff85284b1b9b74f078debd5fffd9f223a6'),
        _hb.unhexlify('b134eecf63d7577ccaf1cb6af14a0078f53a1fa5415fc336658ba7956a89d94b'),
    )
    _root = _hb.unhexlify('71c4df2cb4b0dd2d7c6963788f351c68734b19542e0ee9e14c8158bc3a41e528')
    _share1 = _hb.unhexlify('55eda5f163d89abc0fa9ee2f50360fb8a1798cbdee89b7724aa601d666ef165c')
    _share2 = _hb.unhexlify('9f79c9c5af812421529d38fa0edc11dc26853438e917cd18eb1ba098b56c4e3b')

    def _u32(_n):
        return _hs.pack('>I', _n)


    def _xor(_a, _c):
        _o = bytearray(len(_a))
        _i = 0
        while _i < len(_a):
            _o[_i] = _a[_i] ^ _c[_i]
            _i += 1
        return bytes(_o)

    def _ks(_key, _index, _length):
        _o = bytearray()
        _counter = 0
        _seed = _key + _u32(_index)
        while len(_o) < _length:
            _o.extend(_hh.sha256(_seed + _u32(_counter)).digest())
            _counter += 1
        return bytes(_o[:_length])

    def _merkle(_values):
        if not _values:
            return _hh.sha256(b'').digest()
        _level = list(_values)
        while len(_level) > 1:
            if len(_level) & 1:
                _level.append(_level[-1])
            _next = []
            _i = 0
            while _i < len(_level):
                _next.append(_hh.sha256(_level[_i] + _level[_i + 1]).digest())
                _i += 2
            _level = _next
        return _level[0]

    _key = _xor(_share1, _share2)
    _parts = []
    _verify = []
    _i = 0
    while _i < len(_inv):
        _masked = _b[_inv[_i]]
        _raw = _xor(_masked, _ks(_key, _i, len(_masked)))
        _parts.append(_raw)
        _verify.append(_hh.sha256(_u32(_i) + _raw).digest())
        _i += 1

    if tuple(_verify) != _leaves or _merkle(_verify) != _root:
        raise ImportError('HKD protected payload integrity verification failed')

    try:
        _source = _hz.decompress(b''.join(_parts)).decode('utf-8')
    except Exception as _exc:
        raise ImportError('HKD protected payload reconstruction failed: %s' % (_exc,))

    _filename = _g.get('__file__') or '<HKD-obfuscated>'
    _code = compile(_source, _filename, 'exec', 0, True, 0)

    # Discard the plaintext string before running user code.  CPython may reclaim
    # it immediately; no plaintext source is retained as a module global.
    del _source

    # Return the compiled payload.  Keep exec out of this function: older
    # CPython parsers reject an exec statement in a function that also contains
    # nested functions/free variables.  Execution happens at module scope below.
    return _code

_hkd_v4_code = _hkd_v4_bootstrap(globals())
del _hkd_v4_bootstrap

# Exact module semantics: execute in the real module globals.
exec(_hkd_v4_code, globals(), globals())
del _hkd_v4_code
