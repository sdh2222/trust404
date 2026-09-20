# BAYBENCH report — baseline_keyword

## Summary

| metric | value |
| --- | --- |
| weighted_score | 0.4269 |
| tier0_exact | 3/5 |
| mean_verdict_score | 0.3513 |
| n_cases | 859 |
| determinism | - |
| runtime_p50 | 0.3795 |
| runtime_p95 | 0.3795 |
| compile_fail_count | 0 |

## Per-tier

| tier | n | mean_score | family_recall | rule_recall | high_fp_rate | evidence_hit_rate | uncertain_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tier0_judge | 5 | 0.6 | 0.6667 | 0.6667 | 0.5 | 0.0 | 0.0 |
| tier1_pairs | 67 | 0.597 | 0.4667 | 0.3333 | 0.3429 | 0.0 | 0.0 |
| tier2_realworld | 779 | 0.3299 | 0.1709 | - | - | - | 0.0 |
| tier3_benign_risky | 8 | 0.2188 | 0.3333 | - | 1.0 | - | 0.0 |

## Per-family

| family | n_cases | mean_score |
| --- | --- | --- |
| A | 105 | 0.6667 |
| B | 107 | 0.5304 |
| C | 8 | 0.3438 |
| D | 4 | 1.0 |
| E | 5 | 0.8 |
| F | 324 | 0.3981 |
| G | 1 | 0.0 |

## Coverage

families_zero_cases (0): -
rules_zero_cases (0): -
rules_missing_pair (BB-6): PASS
unknown_rule_ids: -
extra_results: tier1/_harness/multi_file/Helper.sol

## Gaps

| case | verdict | reason | expected | fired |
| --- | --- | --- | --- | --- |
| tier0/P3_Honeypot_sol | Benign | no_expected_rule | EXIT_ADDR_GATE | - |
| tier1/BAL_DIRECT_SET/mal | Benign | no_expected_rule | BAL_DIRECT_SET | - |
| tier1/BAL_TRANSFER_HIDDEN_MINT/mal | Malicious | no_expected_rule | BAL_TRANSFER_HIDDEN_MINT | BAL_PRIV_MINT |
| tier1/DRAIN_APPROVAL_PULL/mal | Benign | no_expected_rule | DRAIN_APPROVAL_PULL | - |
| tier1/EXIT_AMOUNT_LIMIT/mal | Malicious | no_expected_rule | EXIT_AMOUNT_LIMIT | FEE_UNBOUNDED |
| tier1/EXIT_CALLBACK_CYCLE/mal | Benign | no_expected_rule | EXIT_CALLBACK_CYCLE | - |
| tier1/EXIT_SELL_ONLY/mal | Benign | no_expected_rule | EXIT_SELL_ONLY | - |
| tier1/EXIT_TIME_GATE/mal | Benign | no_expected_rule | EXIT_TIME_GATE | - |
| tier1/HONEYPOT_LEGACY/mal | Benign | no_expected_rule | HONEYPOT_LEGACY | - |
| tier1/LEAK_ARBITRARY_TRANSFERFROM/mal | Benign | no_expected_rule | LEAK_ARBITRARY_TRANSFERFROM | - |
| tier1/LEAK_EXEMPT_PATH/mal | Benign | no_expected_rule | LEAK_EXEMPT_PATH | - |
| tier1/LEAK_PRIV_SWEEP/mal | Benign | no_expected_rule | LEAK_PRIV_SWEEP | - |
| tier1/OWN_FAKE_RENOUNCE/mal | Malicious | no_expected_rule | OWN_FAKE_RENOUNCE | EXIT_ADDR_GATE |
| tier1/OWN_HIDDEN_ROLE/mal | Malicious | no_expected_rule | OWN_HIDDEN_ROLE | EXIT_ADDR_GATE |
| tier1/OWN_REASSIGN_NONSTD/mal | Malicious | no_expected_rule | OWN_REASSIGN_NONSTD | EXIT_ADDR_GATE |
| tier1/PONZI_SHAPE/mal | Benign | no_expected_rule | PONZI_SHAPE | - |
| tier1/PRIV_ROLE/mal | Malicious | no_expected_rule | PRIV_ROLE | BAL_PRIV_MINT, EXIT_ADDR_GATE |
| tier1/SLITHER_HIGH_OVERLAY/mal | Benign | no_expected_rule | SLITHER_HIGH_OVERLAY | - |
| tier1/STRUCT_PROXY_EOA_ADMIN/mal | Malicious | no_expected_rule | STRUCT_PROXY_EOA_ADMIN | STRUCT_DELEGATECALL_SETTABLE |
| tier1/VIEW_CALLER_DEPENDENT/mal | Benign | no_expected_rule | VIEW_CALLER_DEPENDENT | - |
| tier1/_harness/trading_switch_owner_bypass | Benign | no_expected_rule | EXIT_GLOBAL_SWITCH | - |
| tier2/crpwarner/0x186ED770eEcEA82Def7C92DCC077C4Ba27acD5BD_sol | Malicious | no_expected_family | B | EXIT_ADDR_GATE, EXIT_GLOBAL_SWITCH, FEE_UNBOUNDED |
| tier2/crpwarner/0x198376f921570e3cc547Fd5C16e482Cded8B4D1D_sol | Malicious | no_expected_family | A | BAL_PRIV_MINT |
| tier2/crpwarner/0x28c748535cC0c774d7bB046aDba0C9d77E3b4c92_sol | Malicious | no_expected_family | A | BAL_PRIV_MINT |
| tier2/crpwarner/0x42269AC712372AC89A158ad5a32806c6b6782d66_sol | Malicious | no_expected_family | C | EXIT_ADDR_GATE |
| tier2/crpwarner/0x50C6eC50a89a946C5886Aeb54a22fe732558F7D1_sol | Malicious | no_expected_family | C | BAL_PRIV_MINT, EXIT_ADDR_GATE, EXIT_GLOBAL_SWITCH, STRUCT_DELEGATECALL_SETTABLE |
| tier2/crpwarner/0x548c9731aE163A73A28916EEB11717FE446dAb54_sol | Benign | no_expected_family | B | - |
| tier2/crpwarner/0xD00736F864Ecd5BEF5996c735F98769aE0d10c7c_sol | Malicious | no_expected_family | A | BAL_PRIV_MINT |
| tier2/honeybadger/balance_disorder_0x0bf0f154b176c5d90f24e506f10f7f583eb5334d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x0e77cb9d68b8bf3cc41561f8eda6c71e4a4b9ef7_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x15d0e6cedd8ecc39daa60c63a3a5830eeca7d720_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x35c3034556b81132e682db2f879e6f30721b847c_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x3bafb3af16203c817ee9208c6b8a748398dae689_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x3e013fc32a54c4c5b6991ba539dcd0ec4355c859_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x5aa88d2901c68fda244f1d0584400368d2c8e739_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x5bb52e85c21ca3df3c71da6d03be19cff89e7cf9_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/balance_disorder_0x69bfbf000bd39444af2efba733829b04211252bc_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x92e63be3a88df80f64ba4f829dd7ddf97e8b750b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x9efc7a38552e63534a8e9b9558adabd73297f91d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0x9f54d912a029380f2743aaf4ddd28c3f207cd719_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/balance_disorder_0xc7e4a9147601fdbc7d1c2fb8b6c2ffcb2469f293_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0xc9c8ef2588647e6f5acb6aaee637264d2632609d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0xdf77e4a81fba17e0cc39dba521aa4167f388ed7c_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0xe26e90598190a98c92c75204c9a4ecfe5983f8e0_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/balance_disorder_0xfd1e3d3e641f224ce8e1117866cf3f01ed2d5d9f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x03209bde47da583547c17c47e7ca74bfa3dfb404_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0x0595d187cac88f04466371eff3a6b6d1b12fb013_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x062e659a3c8991bc1739e72c68edb9ac7b5a8ca7_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x064656852581472f9b315fea4730fe18fb7c579a_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x0684a256b8a6434cf10ee81bc1bcdcbba3365daa_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x07ec6c3159c2336ba36ab41f73411f8fee430470_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT |
| tier2/honeybadger/hidden_state_update_0x0cfa149c0a843e1f8d9bc5c6e6bebf901845cebe_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x0e35f4f608d4a8fa560595db79cfda02d790777b_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x0e8f2803fa16492b948bc470c69e99460942db2b_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x0ffb3f4605dd9f01de1a06052b7687418a9d82ee_sol | Malicious | no_expected_family | F | EXIT_ADDR_GATE |
| tier2/honeybadger/hidden_state_update_0x11f4306f9812b80e75c1411c1cf296b04917b2f0_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x1237b26652eebf1cb8f59e07e07101c0df4f60f6_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x129e719c424a7a6fbdeb7ca3d65186892d54ea8c_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x137e531680b5d1f5645cd73a450323f1645d5034_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x13c547ff0888a0a876e6f1304eaefe9e6e06fc4b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x159d2829613b0fe363e462b218c695c6eae0a5e1_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x16aae4b322501c339ed31a41fb915ae305528585_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x175744fb0849584129fa3d0e6350c00206d95d2f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x197803b104641fbf6e206a425d9dc35dadc4f62f_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0x19d0321ba91ed5edec4afe1da158a6b06bba03f0_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x1dabd43e0f8a684a02712bcd767056e25026061c_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x1efd5dc066eb56d4db7e2ff38843c8bf8aa59168_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT, EXIT_ADDR_GATE, EXIT_GLOBAL_SWITCH |
| tier2/honeybadger/hidden_state_update_0x1fbf025ad94dde79f88732f79966a9a435f2772f_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x24cad91c063686c49f2ef26a24bf80329fb131c7_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x2634baad203cba4aa4114c132b2e50a3a6027ff9_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x265c91539255a96e1005a0fd11ca776c183d04f5_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x26ae986bfab33f4cbadec30ea55b5eed9e883ecf_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x286bbee3f20f1702e707e58d33dc28a69e7efd4e_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x2b98b39d39914b3aad05dd06a46868507156400d_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x2cc8e271f11934f5fa15942dfda2b59432c2e0f3_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x2e0794073ec7b08e40d80a41599bb31df042e4e5_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x2e4eb4585cb949e53212e796cef13d562c24374b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x2fe321bbb468d71cc392dd95082efef181df2038_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x34bc4f174c027a68f94a7ea6a3b4930e0211b19d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x3597f78c7872db259ce023acc34511c7a79f42e3_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x3668eba58190c7bb2d63cb484467ff0a42fb3367_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x36d5d7262784130de564e99f5c2eab2aa0484bce_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x377f64e05c29309c8527022dbe5fbbfa8e40f6dd_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x38321bbb97a3541bb3913c12201b35d504f7af39_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x3b048ab84ddd61c2ffe89ede66d68ef27661c0f2_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x3c3f481950fa627bb9f39a04bccdc88f4130795b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x3caf97b4d97276d75185aaf1dcf3a2a8755afe27_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x40ef62929748b3e045fd2036322880ef486e4454_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x448fcea60482c0ea5d02fa44648c3749c46c4a29_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x4876bca6feab4243e4370bddc92f5a8364de9df9_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x4a73d9fe078fa67601047f88c3e6c270602e5709_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x4aec37ae465e1d78649aff117bab737c5fb4f214_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x4bc53ead2ae82e0c723ee8e3d7bacfb1fafea1ce_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x4c4757b23526ba13876f8ef3efe973618266e3e8_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x4ca675d62a05c451555c93e456f902bd3e423586_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x4d200a0a7066af311baba7a647b1cce54ae2f9a5_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x52682a037a8deab04e708055c751556a0840897a_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x53018f93f9240cf7e01301cdc4b3e45d25481f73_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x57684f9059afbf7bb11b07263500292ac9d78e7b_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x590d1d5ba0feb249d42c527ae21d12f2e5768a87_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x59434a7b9aeebe94045d3715aa020f6a1d7875ad_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x5ccfcdc1c88134993f48a898ae8e9e35853b2068_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x611ae0be21a9c0ab284a4a68c8c44843330072a7_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x64669148bca4f3d1216127a46380a67b37bbf63e_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x6594ac0a2ba54885ff7d314eb27c9694cb25698b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x686847351a61eb1cae8ac0efa4208ff689fd53f2_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x68af0f18c974a9603ec863fefcebb4ceb2589070_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x6ce3fef99a6a4a8d1cc55d980966459854b3b021_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x6f905e47d3e6a9cc286b8250181ee5a0441acc81_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x704079e823e42a936bbaac5163434c2515473836_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x70bf9df6967dc96156e76cc43b928a7ef02e159a_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x735906d7ab237eeea06f4af86795bb4e0ec199e0_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x7409bac00c479b0003651cc157a72d1a227eccfb_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x75041597d8f6e869092d78b9814b7bcdeeb393b4_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x75658ed3dba1e12644d2cd9272ba9ee888f4c417_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x75890afea0658ed67e145df17948c8fceed0affa_sol | Malicious | no_expected_family | F | EXIT_ADDR_GATE |
| tier2/honeybadger/hidden_state_update_0x7a2ac9691ce2fcffb9777311c14a82a6aec7e639_sol | Malicious | no_expected_family | F | EXIT_ADDR_GATE |
| tier2/honeybadger/hidden_state_update_0x7b3c3a05fcbf18db060ef29250769cee961d75ac_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x7c05c837f7a84dced69ae94f8649bbc3897d2b31_sol | Malicious | no_expected_family | F | EXIT_ADDR_GATE |
| tier2/honeybadger/hidden_state_update_0x7fefc8bf6e44784ed016d08557e209169095f0f3_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x7ffc2bd9431b059c509b45b33e77852d47de827d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x807a3ef8a8dbdd7fc9863df695bbe8691e450e8e_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT |
| tier2/honeybadger/hidden_state_update_0x85044611b5954739dbde0ccb9aae6bb18e38e38b_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x85bc00724203d53536072b000c44a2cc16cd12c5_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x878e6c6f9a86a1e5d313e7b872ccd109135e91b4_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x8a36f3e0da7b36fd22fcf2844c21e812279372ac_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x8bbf2d91e3c601df2c71c4ee98e87351922f8aa7_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x8bce9d720745b93c58c505fc0d842a7d9cd59697_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x8cc5d9de2c8df87f2d40d84aa78049ea6e61f973_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x8d056569b215c8b56e4b3a615dac425d8d2352a4_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x8d4eb49f0ed7ee6d6e00fc76ea3e9c3898bf219d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x930dfbdc5e9f1984a8d87de29d6a79fbb2bb7b32_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x95be22039da3114d17a38b9e7cd9b3576de83924_sol | Malicious | no_expected_family | F | EXIT_GLOBAL_SWITCH, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0x96fa4b2bebbbc9ffdb7d64ed18058de27680752c_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x99bab102c0a03438bcfd70119f07ee646db26ddf_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0x9bdb9d9bd3e348d93453400e46e71dd519c60503_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xa0f9e5283fbf6d735e1e3a0f724ea6cccc13c27a_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xa379eda47d90fb4bc2dfa54556421ff0f198ca47_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xa48a36d94024f861b453267468b9096e4a3eb8be_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xa630823bd70ab8e8e2d6e62089d3837db1887bf6_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xa9aebbf67433e3e8206af6fc2ddd99ff8e7cc137_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xaa3a6f5bddd02a08c8651f7e285e2bec33ea5e53_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xaa4fd1781246f0b9a63921f7aee292311ea05bf7_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xabcdd0dbc5ba15804f5de963bd60491e48c3ef0b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xacfc9577583ded00ae53ae79a0346cca4655c0bb_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xaded0438139b495db87d3f70f0991336df97136f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xae3bf0f077ed66dda9fb1b5475942c919ef3bb0d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xaea5418057d0e37a6e69e588e7f393e946846d62_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xaec8162438b83646518f3bf3a70b048979f81fab_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xaf531dc0b3b1151af48f3d638eeb6fe6acdfd59f_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0xb19117892e2b2aaa418e75f61d7d1c05f86b66bd_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xb389327f8325d9568826b0f3ca63ef613687cfab_sol | Malicious | no_expected_family | F | EXIT_ADDR_GATE |
| tier2/honeybadger/hidden_state_update_0xb38beba95e0e21a97466c452454debe2658527f7_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xb49b1dddf1b3d6e878fd9b73874da7ab0da7e004_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xb5c424cd005cd1ccc155654b551c4453346e0718_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xb620cee6b52f96f3c6b253e6eea556aa2d214a99_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xb6f6f6f47e92e517876d30c04198f45a3bc1b281_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xb85a54944b58342b07887942e6f530f616479efd_sol | Malicious | no_expected_family | F | EXIT_ADDR_GATE |
| tier2/honeybadger/hidden_state_update_0xb919b2903e07293bc84372471a7081ecb69e8d36_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT |
| tier2/honeybadger/hidden_state_update_0xb91a6c5c6362b10db6440d690e5391bb1eabe591_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xbae339b730cb3a58eff2f2f2fa4af579332c3e1c_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0xbb51397fb8d3b91a08eff3c34d5c869c1d149ec5_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xbc272b58e7cd0a6002c95afd1f208898d756c580_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xbd53a4db4003c59070abbfa4e6c31afbf0b26843_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xbf5fb038c28df2b8821988da78c3ebdbf7aa5ac7_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xc034cf94f7ced9c968cc75210d1b5ddaccacfbf4_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xc1574ab95106621686d6e480f378d79c0442fe33_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xc1d73e148590b60ce9dd42d141f9b27bbad07879_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xc304349d7cc07407b7844d54218d29d1a449b854_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xc5ce9c06a0caf0e4cbd90572b6550feafd69b740_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xc6389ef3d79cf17a5d103bd0f06f83cf76b14258_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xc77081641129a028d622f85671ea172ac5595938_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xc78f0fdfb708689cbe6629175b66958eaa89e7d0_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xc7e454770433c071dd1863eeb27fb7e1adbd3361_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xc8b2c33a45ce83d19da15a58d1d1ddb2738506bf_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xcaa7b8aa3bc78dda98af8fee1390f34e756a5f55_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xcb71b51d9159a49050d56516737b4b497e98bb99_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xce6b1aff0fe66da643d7a9a64d4747293628d667_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xcea86636608bacb632dfd1606a0dc1728b625387_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xd0981f1e922be67f2d0bb4f0c86f98f039dd24cc_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xd6bc92a0f5a2bc17207283679c5ddcc108fd3710_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xd87eaad7afb256c69526a490f402a658f12246fd_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0xd8993f49f372bb014fb088eabec95cfdc795cbf6_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xdda2044b39fdb4db77ac085866179c548e5d0f15_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xde82658c23f034d71827c215fdfbce0d4e248ccd_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xdfe06d5a4534fbe955eebe8a4908ef596763c2a4_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT |
| tier2/honeybadger/hidden_state_update_0xe1ccb3a5bae6fecdb9b60c0acf94989f48c10742_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xe35a91f2acceccf1ce6bae792274da6100b639af_sol | Malicious | no_expected_family | F | EXIT_ADDR_GATE |
| tier2/honeybadger/hidden_state_update_0xe3b0fe57f7de3281579a504dcc3af491afbb23e5_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xe3d085b7bdf97c6d003abcec2003b9c5b120d616_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xe830d955cbe549d9bcf55e3960b86ffac6ef83f1_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xed4fd2e53153b8bfd866e11fb015a1bc4a0e9655_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xed55fb58ea9de1f484addcc970463218b4d89cfe_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xed710216da4b1416a78768790ca9aa3633ca110f_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xef75f477126d05519d965d116fc9606e60fc70a8_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xefbfc3f373c9cc5c0375403177d71bcc387d3597_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xf0344800bd3ffa687e4d780357961b28995a5f46_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xf331f7887d31714dce936d9a9846e6afbe82e0a0_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT, EXIT_GLOBAL_SWITCH |
| tier2/honeybadger/hidden_state_update_0xf3f3dd2b5d9f3de1b1ceb6ad84683bf31adf29d1_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xf6b55acbbc49f4524aa48d19281a9a77c54de10f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xfac1c7270bc5b0664e27e7f2e82281d564aedf4e_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_state_update_0xfb0513602b08ede66c28c128ece6a2f11161f17f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xff45211ebdfc7ebcc458e584bcec4eac19d6a624_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/hidden_transfer_0x3f2ef511aa6e75231e4deafc7a3d2ecab3741de2_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0x55654a38372617aedd583009f76e28700e48fdad_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0x78c2a1e91b52bca4130b6ed9edd9fbcfd4671c37_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0x7a4349a749e59a5736efb7826ee3496a2dfd5489_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0x806a6bd219f162442d992bdc4ee6eba1f2c5a707_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0xc7f4ade4874e06a20fab9c5dc4f1dd8b6d85faf2_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0xd2018bfaa266a9ec0a1a84b061640faa009def76_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0xdb1c55f6926e7d847ddf8678905ad871a68199d2_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0xe4eabdca81e31d9acbc4af76b30f532b6ed7f3bf_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0xe82f0742a71a02b9e9ffc142fdcb6eb1ed06fb87_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_transfer_0xf70d589d76eebdd7c12cc5eec99f8f6fa4233b9e_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x017bcaee2456d8bd0e181f94165919a4a2ecc2d9_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x038e20839aebfe12b7956adcbc2511f6f7085164_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x07f06a75ddf49de735d51dbf5c0a9062c034e7c6_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x0bcccba050c2ce6439c57bd203378b113cc3cfd6_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x11f3081cd6b2ac5a263e65e206f806bea7fa9c56_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x1767856bc75cf070de5e6ba3d0c718440f008c66_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x2d05359a51ca13c4ac5f4437585afaf5bf2050f9_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT, EXIT_ADDR_GATE, EXIT_GLOBAL_SWITCH, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x33685492a20234101b553d2a429ae8a6bf202e18_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x33b44a1d150f3feaa40503ad20a75634adc39b18_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x340844b39aacbdb4e7718fa14a95758f87a09a9a_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x3526cf7d12c95b11a680678cc1f705cba667578d_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x3e7840b88396acd80bac66021e1354064461a498_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x4ba0d338a7c41cc12778e0a2fa6df2361e8d8465_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x4c7c98c4d64c29ef8103b005eeccf5145cfdf8c1_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x4dc76cfc65b14b3fd83c8bc8b895482f3cbc150a_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x4fed7f5f0314bd156a8486fc41dc8bd4737c24fb_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x50abfc76b637b70571c301071f7ce660c1c3d847_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x50ddfe3722fc303cace413df41db23d55025e2e6_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x52c2d09acf0ef12c487ae0c20a92d4f9a4abbfd1_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x5b2028602af2693d50b4157f4acf84d632ec8208_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x5c8546a7b86ba30202c09a84f5a72644a2a4f7ba_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x641074844a0dd00042347161f830346bdfe348bc_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x68563d2a5fc58f88db8140a981170989f001b746_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x6e843aefc1f2887e5b0aeb4002c1924c433d9a13_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x70c01853e4430cae353c9a7ae232a6a95f6cafd9_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x7704442e1005b9ab403463ed85e2fb24761a8738_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x787080326e1f7e0eae490efdb18e90cfd0ae2692_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x78faf034c61f4158a4a12bfa372187a21405ae33_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x7e97c48497a8d650dc030744b74c81e29816f8e3_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x81edefc64aabdce71f68347774bd4673d1d31419_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x849019a489c3c26c7a7668e468be81a4d132781f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x9168fdc9f9db7b71865fe4bfd6f78b3610ebc704_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x96050da7c01bbd4891ed766720a5c1c79b824163_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x98fe1d52649a3a13863647c6789f16e46e090377_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0x9c0c5a14fde1306686a8a270f271165acda670c2_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xa16cdcba1d6cb6874ff9fd8a6c8b82a3f834f512_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xb31820c1d84e183377030b6d3f0e1ee5c1cff643_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xc0c7d89e4968775931e53e9510ebad43644b0866_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xcacf9396a56e9ff1e3f6533be83a043c36ce0436_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xe65c53087e1a40b7c53b9a0ea3c2562ae2dfeb24_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xf1aab4171ceb49b6a276975347e3c1d4d5650e5a_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xf5615138a7f2605e382375fa33ab368661e017ff_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xfae0300c03a1ea898176bcb39f919c559f64f4ff_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xfdc39e06a7297268a0f6d5bd1692ae5fa9026152_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xff41067fe843f190482d998a9976c7b19cd7c8b7_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT, EXIT_ADDR_GATE |
| tier2/honeybadger/named_CryptoRoulette_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_DividendDistributor_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/named_EtherBet_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_For_Test_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_G_GAME_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/named_Gift_1_Eth_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_GuessNumber_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/named_ICO_Hold_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_IFYKRYGE_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/named_KingOfTheHill_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_MultiplicatorX3_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_NEW_YEARS_GIFT_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_OpenAddressLottery_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/named_PINCODE_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_PrivateBank_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_RACEFORETH_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_RichestTakeAll_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_TerrionFund_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_Test1_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_TestBank_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_TransferReg_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE |
| tier2/honeybadger/named_TrustFund_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_TwelHourTrains_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_WhaleGiveaway1_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/named_X2_FLASH_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/named_firstTest_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/named_testBank2_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/skip_empty_string_literal_0x7bc51b19abe2cfb15d58f845dad027feab01bfa0_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/skip_empty_string_literal_0x858c9eaf3ace37d2bedb4a1eb6b8805ffe801bba_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/skip_empty_string_literal_0xa0174f796d3b901adaa16cfbb589330462be0329_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/skip_empty_string_literal_0xa395480a4a90c7066c8ddb5db83e2718e750641c_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/skip_empty_string_literal_0xaa12936a79848938770bdbc5da0d49fe986678cc_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/skip_empty_string_literal_0xd022969da8a1ace11e2974b3e7ee476c3f9f99c6_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/skip_empty_string_literal_0xe63760e74ffd44ce7abdb7ca2e7fa01b357df460_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/straw_man_contract_0x01f8c4e3fa3edeb29e514cba738d87ce8c091d3f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x23a91059fdc9579a9fbd0edc5f2ea0bfdb70deb4_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x4320e6f8c05b27ab4707cd1f6d5ce6f3e4b3a5a1_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x463f235748bc7862deaa04d85b4b16ac8fafef39_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x477d1ee2f953a2f85dbecbcb371c2613809ea452_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/straw_man_contract_0x4e73b32ed6c35f570686b89848e5f39f20ecc106_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x561eac93c92360949ab1f1403323e6db345cbf31_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x62d5c4a317b93085697cfb1c775be4398df0678c_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE |
| tier2/honeybadger/straw_man_contract_0x7a7d08bcb2faf27414e86ecf9a0351d928054b6b_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE |
| tier2/honeybadger/straw_man_contract_0x7a8721a9d64c74da899424c1b52acbf58ddc9782_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/straw_man_contract_0x8c7777c45481dba411450c228cb692ac3d550344_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x941d225236464a25eb18076df7da6a91d0f95e9e_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0x95d34980095380851902ccd9a1fb4c813c2cb639_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xa5d6accc5695327f65cbf38da29198df53efdcf0_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xa91a453abde404a303fb118c46e00c8f630216a9_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE |
| tier2/honeybadger/straw_man_contract_0xaae1f51cf3339f18b6d3f3bdc75a5facd744b0b8_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xb4c05e6e4cdb07c15095300d96a5735046eef999_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xb5e1b1ee15c6fa0e48fce100125569d430f1bd12_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xb93430ce38ac4a6bb47fb1fc085ea669353fd89e_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xbabfe0ae175b847543724c386700065137d30e3b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xbaf51e761510c1a11bf48dd87c0307ac8a8c8a4f_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xbe4041d55db380c5ae9d4a9b9703f1ed4e7e3888_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xbf64a825e602a4f1c31480a470e99e1d896c88a7_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/straw_man_contract_0xd116d1349c1382b0b302086a4e4219ae4f8634ff_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xd518db222f37f9109db8e86e2789186c7e340f12_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xdad02644b70cbb20dec56d25282ddc65bb7805a1_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE |
| tier2/honeybadger/straw_man_contract_0xdd17afae8a3dd1936d1113998900447ab9aa9bc0_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xe610af01f92f19679327715b426c35849c47c657_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/straw_man_contract_0xff5a11c0442028ee2a60d31e6ebb3cbac121ffe5_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE |
| tier2/honeybadger/type_deduction_overflow_0x2ecf8d1f46dd3c2098de9352683444a0b69eb229_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/type_deduction_overflow_0x752406cbfd32593fc422da69cdd702d1eaadc121_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/type_deduction_overflow_0x791d0463b8813b827807a36852e4778be01b704e_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/type_deduction_overflow_0xf5b1d75f4415f853fef2466a5ab8e412d593dd44_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0x2075d158924f5030aece55179848c2bd7ec5833f_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0x29d6cf436c893c7e44ea926411d5fd4dd763d9b3_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/uninitialised_struct_0x2f069a1d7a052052458e8b5511e91221eb337c52_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0x3268ecb4fcba1ca9f43da8ed05ffc80382cef1da_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0x4fdc2078d8bc92e1ee594759d7362f94b60b1a3d_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/uninitialised_struct_0x559be9a89db88794645abb93e3bfc1af2ee0be40_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0x559cc6564ef51bd1ad9fbe752c9455cb6fb7feb1_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/uninitialised_struct_0x6324d9d0a23f5ddba165bf8cc61da455350895f2_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0x650734bfd0465b7c6cd2932ea555e721308fd0b3_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0x6a2e025f43ca4d0d3c61bdee85a8e37e81880528_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0x741f1923974464efd0aa70e77800ba5d9ed18902_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/uninitialised_struct_0x74808c86c6f0bc6f59a3a1430ddfcd2e29952eac_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0x783cf9c6754bf826f1727620b4baa19714fedf8d_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0x787b9a8978b21476abb78876f24c49c0e513065e_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0x8685631276cfcf17a973d92f6dc11645e5158c0c_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0x96830139e44251ddbe3d1c4c4110262b47cf6d34_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0xad1aa68300588aa5842751ddcab2afd4a69e9016_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0xb1f4ca3c6256f415e420de511504af8ea8a9c8e0_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0xc57fc2c9fd3130933bd29f01ff940dc52bc4115b_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0xe19ca313512e0231340e778abe7110401c737c23_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0xe6f245bb5268b16c5d79a349ec57673e477bd015_sol | Malicious | no_expected_family | F | OWN_TX_ORIGIN |
| tier2/honeybadger/uninitialised_struct_0xefba96262f277cc8073da87e564955666d30a03b_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/uninitialised_struct_0xf6c61cb3b0add944ac53c9c2decaf2954f0515cb_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/uninitialised_struct_0xfb6e71e0800bccc0db8a9cf326fe3213ca1a0ea0_sol | Benign | no_expected_family | F | - |
| tier2/pied-piper/injected_DestroyToken_10_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_12_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_13_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_15_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_16_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_17_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_18_sol | Malicious | no_expected_family | B | OWN_TX_ORIGIN |
| tier2/pied-piper/injected_DestroyToken_19_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_20_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_21_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_22_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_23_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_24_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_25_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_26_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_27_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_28_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_29_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_2_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_30_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_31_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_32_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_33_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_34_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_35_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_36_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_37_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_38_sol | Malicious | no_expected_family | B | EXIT_GLOBAL_SWITCH, STRUCT_SELFDESTRUCT |
| tier2/pied-piper/injected_DestroyToken_39_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_3_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_40_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_4_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_5_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_6_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_7_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_8_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_DestroyToken_9_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/injected_FreezeAccount_8_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x01f2acf2914860331c1cb1a9acecda7475e06af8_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x031e0c6a7c91df1bc171d33cccc6988fd2ddeb6f_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x08a2246dcb48db6a5a9e1f6bc082752fceddd106_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x0b6e701cd51a9e1b5829a4c4fe2130d60c0c4f6c_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x123ab195dd38b1b40510d467a6a359b201af056f_sol | Malicious | no_expected_family | B | EXIT_ADDR_GATE |
| tier2/pied-piper/real_0x1354c8c1a66c2573ce9cc3e92e98d17869501a46_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x17d30c85376bc2c39edc1da179162d308559a3c4_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x1829aa045e21e0d59580024a951db48096e01782_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0x1f10822c753a1f587923d9916e64738ee7c27419_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x21f15966e07a10554c364b988e91dab01d32794a_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x24df76b88a2ea9ae3c3af5402ba4493226a82143_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x2bba3cf6de6058cc1b4457ce00deb359e2703d7f_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x2dcfce5df534b5bd27d3f1cf78e17d67addd0bce_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x378903a03fb2c3ac76bb52773e3ce11340377a32_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x381beac50b9a5ea06a320a72592f7460c49a2b48_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x386cabc0b14a507a4e024dea15554342865b20de_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0x4689a4e169eb39cc9078c0940e21ff1aa8a39b9c_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x46bf6e3e2d51bc587de0e2121748fd15dec991d1_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x48c1b2f3efa85fbafb2ab951bf4ba860a08cdbb7_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0x4c1cdef065c27dd08037d693c512bb7ed4c38f17_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0x521a0d4917b1dec2c21b4807a3dd41c5325aa637_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x55f93985431fc9304077687a35a1ba103dc1e081_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x589891a198195061cb8ad1a75357a3b7dbadd7bc_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER, BAL_PRIV_MINT |
| tier2/pied-piper/real_0x5d64d850c8368008afb39224e92ad0dceff3cf38_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x67fe8dbf5ed0aa9d7a127e5e061d715a1eff3712_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER, BAL_PRIV_MINT |
| tier2/pied-piper/real_0x6e8b6f2d02eacbe33b4c45154cbfa53df1b542ea_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x6f7a4bac3315b5082f793161a22e26666d22717f_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x6ff869d8727ef71369dd33d7e6fd63da31ae203f_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x765f0c16d1ddc279295c1a7c24b0883f62d33f75_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0x7d5902d64e4ed8c60f7c3e2ad1a0aaddd54a6e3f_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0x7e0d051ec68668d603c4e33255d1aed342a691b7_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x7fa4f8d1b089d79b65bc35805726a380e0ef4c1b_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x93ed3fbe21207ec2e8f2d3c3de6e058cb73bc04d_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0x98c0a763de628863f0afb9d75eeee9ad06b18c8e_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0x98f777fb9139576902bf7f35956ca015ddc1569f_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER, BAL_PRIV_MINT |
| tier2/pied-piper/real_0x9954ff0295443c01f562dccb1f893be464e01986_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x9e7ce36dbd1a9a6c6e80d08e38077745855edd3a_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x9eec65e5b998db6845321baa915ec3338b1a469b_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER, BAL_PRIV_MINT |
| tier2/pied-piper/real_0xa370d750995d198834df49191893aa4aa44742af_sol | Malicious | no_expected_family | A | STRUCT_SELFDESTRUCT |
| tier2/pied-piper/real_0xa66daa57432024023db65477ba87d4e7f5f95213_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xa88fc5e2b9aa4e3bb40d67fa553517a1569c8e72_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xb0fe24dc6222e9d9d0e43ab67f40c578af810d21_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xb9e7f8568e08d5659f5d29c4997173d84cdf2607_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0xbae94d28610c8cfd2168f7b97bc7cb0589803c6b_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0xbc2faad1ec407571249b0e874a9abd840111389b_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xc5b106f17246b2f5c0c658dbd6e8d168695806ab_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xcbeaec699431857fdb4d37addbbdc20e132d4903_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0xcf9fbffec9e0e5bbc62e79bf1965f5db76955661_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xd29decbfd29766d8aba8215587f915162c5bd8d8_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0xd4c435f5b09f855c3317c8524cb1f586e42795fa_sol | Benign | no_expected_family | B | - |
| tier2/pied-piper/real_0xd50649aab1d39d68bc965e0f6d1cfe0010e4908b_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xd65960facb8e4a2dfcb2c2212cb2e44a02e2a57e_sol | Benign | no_expected_family | C | - |
| tier2/pied-piper/real_0xd7394087e1dbbe477fe4f1cf373b9ac9459565ff_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0xda2e0aa8f697db190c32034894cf9731f6619960_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xe1aee98495365fc179699c1bb3e761fa716bee62_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0xe4ffee3b33360e21ea2aec37a39901cb720eb84c_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xf336496011891a6f905cde1242285e9953c94d0b_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier2/pied-piper/real_0xfa456cf55250a839088b27ee32a424d7dacb54ff_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xfb5fb992b64c86fbcb33ba151abd8ecbcc611bde_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0xfc87d4f82fc5fe80a2d1692ffee872b2517c34c7_sol | Malicious | no_expected_family | A | BAL_PRIV_BURN_OTHER |
| tier3/bancor_smarttoken | Benign | no_expected_family | B, C | - |
| tier3/lido_ldo_minime | Benign | no_expected_family | B, E | - |

