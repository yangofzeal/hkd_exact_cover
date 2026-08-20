# -*- coding: utf-8 -*-
# HKD OBFUSCATE v4 - portable source payload, no marshal/code-object dependency.
# Protection is import-time only; protected functions have no per-call wrapper.
def _hkd_v4_bootstrap(_g):
    import binascii as _hb
    import hashlib as _hh
    import struct as _hs
    import zlib as _hz

    _b = (
        _hb.unhexlify('3bd314f51c231d952fdb19a6675457c2f865a3bba184e1d5323100de943471895b64205f529fb756427ddcf9260efe2940546217b63461a6b5f6a49c794e8de0547daab1af205b0b31b2cd20e8775d28b77260112626c98114dc7f560ad2e54a8bb53e2cd5fcce0a67d31e7d1876f8c5e392135bbd141f52801b184e15e92125'),
        _hb.unhexlify('32816d1e6afeab44a838970c998081de6682c2bcdc13045e292c97ef7813de587f5be7f90a11f951a8979ff5b96c244212067cc6527d25672e57e29866539496aeabd693b00ad1ae084eabbdb04e7797eb76d88bba852472c23fa9ffbf3874eeb61795cd67640440cd90d828398b10ab14b4ab956e08bac9585ec15f44fd6260'),
        _hb.unhexlify('b94098f6a14612fa7aa4b6abf6da09fe7c98f570194faf44b4111901c6f8bf525adfb83886a2f5d78dca775e78cdfde37a6fef0800ab49efbd00d266fe93a41b01e1622cb8280ac13f756404122526a8ee8c2f34ebf5ad1851b0fc4178cfd65a4684c38aae23f10a57561d4efd2e631fc8217fea9dea6c9242148905e8804e36'),
        _hb.unhexlify('86df701d6ab6affb729c90ab79f015bae84fe5762bd4981f7f1cd2cfae3b0bc6a88a432a069c634d034222476d5dd5605812d59e464d2b00abf602a2595119d154f19c9d84b95822fe3955d9a59f44767c413101625b97b6afa654db676a712680cc3b44a1e6dac1d501871a3009b74e02f49a104b23c6b5b789491dd7a85684'),
        _hb.unhexlify('ba1dcba7d9fb387f6e2747b0883f863b33da51f5d19de478c62bb5cf08f76c7eb2d3964293b02d55582b331d2511f108700b8d3414b8553e3e04bae89ed9caf60cf03324ebf7a6893b47f6640eb4a70eb1fc7d9b36fcde8f51f22044114c1e36b6ffa8fc43820299531de62a7b1f31f7d1b66ae64110c1ed940b1f2be715856c'),
        _hb.unhexlify('ef8ca04214cde54150fc555e94364b5e7a12d1f6c0192016dc9f61113f14480cc04d087b374883a9019b241fcad4325c7ca83bcc41f897b9f06278617bb5a2bc5aef39afa980268875859a09926fa34959174ecb736a7f9fc48cf866f0dfcac2b3992e8fdfa979d52a9077906b2da17b0c661e7840cbda5a6da8087355e383a1'),
        _hb.unhexlify('6dd38712a9493abd9a1612e61df47de5795b47a3f8c26c76a7aa4e33237d0e17966c507ad33f91b92782acc729bff78dc2367bd2a82dc789045c430ac7770e4c2c09e6dd05690b441d3719f71c2f6422e9d7a97df0d7957dc9cf2a89947481455a39bababfe1b01e0ce4989819aa55ee46ea09fa56637f7f1af1d5ff249a3f1a'),
        _hb.unhexlify('56f291e235bb925a7aad53c974bc8e1e95fa6fb78fabf9bae581b8420e3c385fedd79173d8761398a1d97e547c7e92715cbefae1b25b67c36436f4b56595ce4333ec78e0bb79706bf0a0ed36b972a08e941ac063e804cd33bd90de3262420871db3ae995fdccdbbf948dcac977dd309785d218e0639ec084e48eb5d78a146ee8'),
        _hb.unhexlify('2ea8525d858d2548f15a754099789fc41541a7ee303f3b8a30343966ffa25e49fab220bdd28e818a435709b5045089e16a13b2af6015388008c8e005f779ede041e21a04bbde265f5c888b7007bda9990253dc24403fbb3fdaa526e1e6def87510ec48839445322d8ccb21da0876262f480c3789b0ef7ff695dcc9833954adbe'),
        _hb.unhexlify('482d4c7aab4b65ddf49a2a84d2020d6fb79b0ccdf2dff7bb18191b60cc16477e858d7007ece66f0cd903c076427b629acb2cf5968a8cfcddcffb2ae7e34293d404219381fc51f1f2745132f4070b8d4bbdae832091b8b94a4f93b64f261fcec328d48b0ef44cbe44071b4cba9f0f343fbb17758a093f0fbf008fb9cd12e2f1ec'),
        _hb.unhexlify('fb2a280847969f4efc8b648a270401c860483484f078ae4e973ec2ae6f1ad1084251421a702be24ee5f63662cb0f2095f68b5d8c347803464a5a9a87631eca55906ac7b5c008ce1210260e6c2219f23a1621edcbe4c872b5512e73d51026c3eca33bec31c3e67256a65f092b8da2fc0501bd29453478b98c67a646469db38d04'),
        _hb.unhexlify('753dd9a4358643175381c4ced20bceb933cb9f19ae5f874cd8d6e413ed6750018c845be64bbf533c4d376ea1e8c5c2efa97f55cfb60defdc85e41ccf75cddc83160e3f1caf652e885fb34836ed675dca4ae3c58c8355f482b9df7480a866cc3fb06e6a05cfdae516ce0f5f7b1870925513488f01716ffce09c2fcc1e32406ab3'),
        _hb.unhexlify('b6a1f8721b367887c74306345f4fae35ce8d3dbbbf72ae0bb76dccd3df292f621e99ec30963758fb5898b7b2dd24aa33264103366aade7d2d7811b78b70f5644b8fa76a41a9c3d50a11967e189dee6d1c2b0332d794ad348a660a5a0727ef79d26ad7dfff9b3b5132a828e8aa1efcfdee03f4cb262520db2bcaf28adcdf336c1'),
        _hb.unhexlify('16a9c91b769a1a27c99a4c46f9eb0922501c0019add3bfba8765a04f9069e5bb87c06904211eeb17198a2a037d04feb0036c7df3d1d185f040f937594835d6e96ae27be6cb3878476d395eb3c67d4e5bd365c9b9ff6d65c8b19f4370184534cf5db4b13b40eaeef1f726075c3ed46ba8500b5496c388e49a7414e47ec8c3898c'),
        _hb.unhexlify('3fbd847c24b97fae85b1997fe00b4c254d420ad8f8d50dcc3e4f5e3587a17e862f0904e742cb93994ba1047684644616f42ace310ba04d85db2962854e91d9dadd008b9b7ae46f031195c743557c369190e15a6e835aff17960602446b3a909ddeb3f688903c04f48be89c187d4fbfe38e0976ddbbc84a41dd65f9ef25ce998c'),
        _hb.unhexlify('3a560b56266a0eeb5d4e381108d0e27163ba7b4cdb29985fd6076fb831cf6ba0c525b5a23f4fdae6a45269a54f7fe30fa90f46bbc537264ae30eae77b0859c86dd38bde5c333c362ff3b30ee04d88286da11ca1afb292ce4610147977d28db0672c0f9368feca3c3562f944be04c79d2ed7369332175c0f4bd61ab406f5f4d95'),
        _hb.unhexlify('20d250fd3501ffc0c176b338b99319b49b5d5b29a60ede8c9d4731f0683a9876886a8544c8cfc137d89fef84cf2392d486b2980035f4eb6728148759037fe265d5117e08dfa1075c1aad72757020299df4a47b777da83393d92f49c89ec8f75d43184fe659e12cd46662d40fc8465453177f00c561d4f7f4e04c9e3f44de717b'),
        _hb.unhexlify('8a57d70044f4460f0fab7a0785655b7142ce32a4ffdd58a4f49b40f642b3e97c1da61f68c6728582dea270968bb6d4f55d3c4b'),
        _hb.unhexlify('05b74006e0785a50549de9f866ee995de3425c94d6aacc6558d52957c3ecd6b264b0513bf2ea8b260b291422ebf5ca3b52f4c49164f788d3611661e14212c5d272c96ffdcd00121a62aa737d0be15073cfd0df10c408256dbfe625d1c42b624d66a5e74cb803254e7d999c298be659a12455a7bc605c81b314ea0770d307e183'),
        _hb.unhexlify('f3dff2d8c47789beb554d4ce692618599a8391beb5ea036af30fe2e3589ce35fce887cdee59239394f8c36f93b808d601775cf2fb901a0fcad760b23925af13c30d0bfd63df6caddf4fd0d8735c7b12e8ba53874ece329546512868b0fa27ca214cfb0fb5004ee606c5ee5cc977c3423c67e3e1b8bf85cfbed3175fa9592ac31'),
        _hb.unhexlify('5cc6ea886080f09e5ba972c8679aaf9c15e5a04c235f0c3484dd8f9ba1a670b14baa3959a4b8a4a98dd45cc62207c660b478d27e3cba212cadd4a730f6410506fe1879783b5e7be50ce0f14c5b34054fa386b388291e9315be942d0267d1a150c5b0cbf89b10af9662a383d0e55d7a6db69684abc4f5969239006e6fff8268e1'),
        _hb.unhexlify('a19447d0a782af4244c08568519cb4df411c74735b6c6318f148b47d8c8e9a48bb8052e2f7aacf96fdbff3c5754e94833e67af983a31e4fe5837af5821af2e2918f215ce1639e752c01c9f2230a9c5f91c8d628a680b8083756b3ed4a164958a33f6b0c9da7211e6f625155bf2e4f295c72461cd881b8e534eea1c6849e2c643'),
        _hb.unhexlify('61f97afea61db996da0fa7d080747826252df3c29973f40b53a0114a0f97b0b38080bfa4c0eb12d5014a7abba51dec650c1df47d633c28e2925c6e522208d9e59b6eaa694dc3fe8379ee80f44925f95cd22ce67370e39d27e72c4d717d47470657d5c5423e236bc45155cf76d9e9a91331dc4910003f8bb36d72587f1fd04ac4'),
        _hb.unhexlify('dcc4d07e1540c3a55c485b5be4801c4b9eb919fe6d9e1d1b1e456a3b2ccabedb9e102c47e06a6053ebbbb47bb9a177452b79c4b2fc8b02578450f86addb2f2efbc2373e7730b7dd47192f636e5774f7ecfa441ca0f702d57338588d0433d6c621d8f33858dc06af474ef6b6f9d3ac1e3fae0e9fd4cd84ae9e61e0ab18ede287f'),
        _hb.unhexlify('aa724d66568adfc979b21d51e664c7a6f4868821be523d99783f7b4c63f87f51670ffff4b0f54bbf621303c27b922b301fca363c911aafe31fb414b6b5cab63fbf609ba19b628679d47e2ad86f9ea4fc10ea00096d673d43ce114541b633e8a506447b15caccb8ac91448bf53ed13f43aece03afcdd38d56e45e8f0cbdd2185c'),
        _hb.unhexlify('69250eecae2245b9731287d2dcf8c950f98546bd7906a6fc8cdacad8d027ba21c110e330155bfeee72077835f476d061d829832e1c9d907a2d45d098c1d31dbcb46ad11cd6fa83f23354d8fbb02136469cc4240758a6f026b67042746049c0e686f589038aa729972025bde36371149b57b5476f9ec897cda0cc1c6e976bb134'),
        _hb.unhexlify('cfc5786bfc41848bf2163b381a9f603946ec7df1b285ed93d1a330351f2cf1e8761c5fdf00db3a0b6e18f6c25b9caf3a3c0edaca1a5b06db679aefa88721691bb542f5e4e376db48a30977621cf71cc95fcec7efaf45f4307638e6c46e84707827eeb76f5843ca9e2f607ba9207282f4c97278352e309b36856c7d62f592ecf9'),
        _hb.unhexlify('494d5f1570546c15aacb052088d20017dc6b092590cb162a896700637f4378be87f6eb85738fa2f6f87e67bdab6083523bcb2d4a574e0c781caae9b9e3eeb38caed7b92db7dea6e387eec8be01b946080221adc2a6d1dd0dfeb7b0b5c3cf0a9280ba4160310c5a1d57cc91a74c75d0e3e9dfa7bff5229b46ed8b48d86a09ff23'),
        _hb.unhexlify('707cde634407ef152105c6857ac4be49201b0146470508d4221e2ce2eb881601219248fae22f52543da013cd63b8a43467937b1605320b88b3cb4dfae8c0ae32fe2c7541829bdf3f927fa714aa9b89635da06020cc8e99ff3d72147dc5ecfce57bdea50606d6c33e220468a074380d9df4e08c411b44385d2a120bb04c55b84f'),
        _hb.unhexlify('6343623ac78fa7798d3ecf2d837c3bc3474693bc9db990f020431032005a746abd775df9ab0cd3e4df4314b91fb97b9af7de459697ba410acd48d8ed347c63cf20b70e6847de9296c5f8bc674165371fbb994e3c20810b70d84d7a85559b6132359c79c56caf6ee8316f16e0a6640ec3551cf9f8ebc54a3edbc2555caa3978a3'),
        _hb.unhexlify('2266789c40255ea471f607c1810cbd5875ed69a3d382ca10304abe67c49942676c4a95d32ca731b7c73ac14480639e9fb47242d698e6cd8f81c72365a129e6aea59a01e4ac08df1293126f153d74d52f470113c5915fcbcb5542385017aa1b05692dd15a34cdb7716fbbe6fd6e97e228a8185d040f6efba824d33284b4720e82'),
    )
    _inv = (24, 12, 9, 14, 16, 28, 4, 21, 11, 22, 6, 10, 13, 25, 26, 8, 23, 20, 2, 18, 19, 5, 30, 15, 29, 7, 1, 3, 27, 0, 17)
    _leaves = (
        _hb.unhexlify('799d9491a8d6645d6eb6c788528224923c819cb9157161d53b7b11a49aae7f38'),
        _hb.unhexlify('a13b3cf36d88d03513c56fc00eb17131582168b6bf56efc093fe9b19a61ad13c'),
        _hb.unhexlify('5c286825c7663ac4e2d887dccb96b30811cd432389db92a1170f14ec9ededbbf'),
        _hb.unhexlify('b3fb167332538c125bdb9a47d75cfecf08e195f85b7fb3525d7f924eef91601f'),
        _hb.unhexlify('19e0a15b0fa8009ca210475f4b84d187a97b5b31f37f5880179caa8738bd7db5'),
        _hb.unhexlify('ca80580e0af55cea612ed0b3819b2740d03eab7946c78f346683c40dfd674aad'),
        _hb.unhexlify('dfa5f7f143e024a744b4666a7ed21af5d4e5b5e20d06ea4c1b879215e6d74894'),
        _hb.unhexlify('1175da7b62b2288d3e1c54e23dd97596ee65e2eece62cd4e241b08a76d6b61cf'),
        _hb.unhexlify('ec171075631ef33e3ec7eda2b2a00a5885f31c97e10fdcda27a8252da1b8db5a'),
        _hb.unhexlify('718eacc70624299b4461569e11d2f9105f5bd59fb1db2647127adf4a0c9ea880'),
        _hb.unhexlify('a6b80061ce2d75865fa1af7bf6b43e95f4c075dab50b7ede9ec77df173064aa1'),
        _hb.unhexlify('e85da010f0f60e2bea77edd3910eade4233f537e28a0260b3939d3071dbc9c6d'),
        _hb.unhexlify('7c594d6cc4cdbf4e483c682f95f12e33492be8692ca33bf1415d7ea0e1f92c45'),
        _hb.unhexlify('793c27dddb7b26a177621509b994460ddd4d20512b7436ffc533b7c4000610e8'),
        _hb.unhexlify('fe493b05d667b67d20c6ae5c1561a16b40493c2813db3629434b114df21a5c36'),
        _hb.unhexlify('56ba5fbb32c6395c5501973bd11592c6cc894230a9b92255c8fd1fbe3ddad3f1'),
        _hb.unhexlify('b7b369415afc9ba97153700baefddcd89bba86b9666d88d9496520f9c5db795f'),
        _hb.unhexlify('5d8bc957a1f2e732f7f10ef010347a190521daa8eb2cdf3ffb8239dbade69774'),
        _hb.unhexlify('0d14b334dd073406f73ccdd864529b9e506c0587b2dc34144e382e011eba179c'),
        _hb.unhexlify('dee00a4dbe191a5d2791a2d1071df15d7ac93727199f4d31b767f68b89313b53'),
        _hb.unhexlify('53c3e0a4dd77ecfebec2be32c861bcd3658e69e4b0b0e032f176ec64c9647f80'),
        _hb.unhexlify('15057f2a0f3ced471388608b0ed83cdd5b81aa252dbd491087b57b12f1f9fb41'),
        _hb.unhexlify('5729c42e9088a321d09e716a734d8abb911718f1544a028be4eadbec8005623b'),
        _hb.unhexlify('3024c75b11c76c9920dc0fd15d9fe47e7fea87a537ca76d4b34cf6822a49b249'),
        _hb.unhexlify('61b0600043aa68f2badbed3db6e7254b077a9e885c70cb874f493a21340ad17d'),
        _hb.unhexlify('37791bf9890e4492d5a21a459550c8b763b025a0793092bced71a80fb5f70f18'),
        _hb.unhexlify('682a4abed268ef042973618f984c1f35335608e03f1f8d4fc3b53a30af81bf79'),
        _hb.unhexlify('0fc18d0475241aac845575643c0e7c1c1e921053e795ef7a299132c0d4909bde'),
        _hb.unhexlify('23cbbfd2c38b415a1d4eeb78ee4ee12cc5e567ab7da1242731d7835542278392'),
        _hb.unhexlify('cf601f2808ddcf2af532a2f6eeaf9e2323e1b72660d684578740cbf2cb274c79'),
        _hb.unhexlify('05291f5fc7e80235aabae0b719c87b686e32704c97ad59c03daee59c38fddb7c'),
    )
    _root = _hb.unhexlify('5725f4987c8534b73fdfeeefeb9c47c7c757b5276852fd609791a9aabd9df68b')
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
