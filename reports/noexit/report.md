# BAYBENCH report — noexit

## Summary

| metric | value |
| --- | --- |
| weighted_score | 0.9413 |
| tier0_exact | 5/5 |
| mean_verdict_score | 0.8595 |
| n_cases | 863 |
| determinism | fail |
| runtime_p50 | 63.6372 |
| runtime_p95 | 63.6372 |
| compile_fail_count | 0 |

## Per-tier

| tier | n | mean_score | family_recall | rule_recall | high_fp_rate | evidence_hit_rate | uncertain_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tier0_judge | 5 | 1.0 | 1.0 | 1.0 | 0.0 | 1.0 | 0.0 |
| tier1_pairs | 71 | 0.9296 | 0.9688 | 0.875 | 0.0 | 0.9688 | 0.0704 |
| tier2_realworld | 779 | 0.8511 | 0.732 | - | - | - | 0.2246 |
| tier3_benign_risky | 8 | 0.9688 | 1.0 | - | 0.0 | - | 0.0 |

## Per-family

| family | n_cases | mean_score |
| --- | --- | --- |
| A | 105 | 0.8357 |
| B | 108 | 0.956 |
| C | 8 | 0.9375 |
| D | 4 | 0.875 |
| E | 6 | 0.9167 |
| F | 324 | 0.9707 |
| G | 1 | 0.5 |

## Coverage

families_zero_cases (0): -
rules_zero_cases (0): -
rules_missing_pair (BB-6): PASS
unknown_rule_ids: -
extra_results: -

## Gaps

| case | verdict | reason | expected | fired |
| --- | --- | --- | --- | --- |
| tier1/BAL_PRIV_BURN_OTHER/mal | Malicious | no_expected_rule | BAL_PRIV_BURN_OTHER | BAL_DIRECT_SET |
| tier1/EXIT_CALLBACK_CYCLE/mal | Malicious | no_expected_rule | EXIT_CALLBACK_CYCLE | EXIT_AMOUNT_LIMIT, EXIT_SELL_ONLY, STRUCT_EXTERNAL_GATE |
| tier1/LEAK_ARBITRARY_TRANSFERFROM/mal | Malicious | no_expected_rule | LEAK_ARBITRARY_TRANSFERFROM | BAL_DIRECT_SET |
| tier1/PRIV_ROLE/mal | Malicious | no_expected_rule | PRIV_ROLE | EXIT_ADDR_GATE |
| tier2/crpwarner/0x2753dcE37A7eDB052a77832039bcc9aA49Ad8b25_sol | Malicious | no_expected_family | A | LEAK_ARBITRARY_TRANSFERFROM |
| tier2/crpwarner/0x50C6eC50a89a946C5886Aeb54a22fe732558F7D1_sol | Malicious | no_expected_family | C | BAL_PRIV_MINT, OWN_FAKE_RENOUNCE |
| tier2/crpwarner/0x90F75ca026adD95aE15ECBf48EFc77ED272945bE_sol | Benign | no_expected_family | B | - |
| tier2/crpwarner/0x9372b371196751dd2F603729Ae8D8014BbeB07f6_sol | Malicious | no_expected_family | B | LEAK_ARBITRARY_TRANSFERFROM |
| tier2/crpwarner/0xEe45E37e2B73E86c709d9edD1c8eA3B0ec72DaD3_sol | Malicious | no_expected_family | A | STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/hidden_state_update_0x03209bde47da583547c17c47e7ca74bfa3dfb404_sol | Malicious | no_expected_family | F | EXIT_GLOBAL_SWITCH, FEE_ADDR_MUTABLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0x07ec6c3159c2336ba36ab41f73411f8fee430470_sol | Benign | no_expected_family | F | EXIT_GLOBAL_SWITCH |
| tier2/honeybadger/hidden_state_update_0x0ffb3f4605dd9f01de1a06052b7687418a9d82ee_sol | Malicious | no_expected_family | F | EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x11f4306f9812b80e75c1411c1cf296b04917b2f0_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD |
| tier2/honeybadger/hidden_state_update_0x175744fb0849584129fa3d0e6350c00206d95d2f_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x1efd5dc066eb56d4db7e2ff38843c8bf8aa59168_sol | Uncertain | no_expected_family | F | BAL_DIRECT_SET, EXIT_GLOBAL_SWITCH, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x286bbee3f20f1702e707e58d33dc28a69e7efd4e_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x38321bbb97a3541bb3913c12201b35d504f7af39_sol | Benign | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x3c3f481950fa627bb9f39a04bccdc88f4130795b_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD |
| tier2/honeybadger/hidden_state_update_0x53018f93f9240cf7e01301cdc4b3e45d25481f73_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x7409bac00c479b0003651cc157a72d1a227eccfb_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x75890afea0658ed67e145df17948c8fceed0affa_sol | Malicious | no_expected_family | F | EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x7a2ac9691ce2fcffb9777311c14a82a6aec7e639_sol | Malicious | no_expected_family | F | EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x7c05c837f7a84dced69ae94f8649bbc3897d2b31_sol | Malicious | no_expected_family | F | EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x7ffc2bd9431b059c509b45b33e77852d47de827d_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0x807a3ef8a8dbdd7fc9863df695bbe8691e450e8e_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0x85bc00724203d53536072b000c44a2cc16cd12c5_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0x95be22039da3114d17a38b9e7cd9b3576de83924_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0xaa3a6f5bddd02a08c8651f7e285e2bec33ea5e53_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xabcdd0dbc5ba15804f5de963bd60491e48c3ef0b_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xae3bf0f077ed66dda9fb1b5475942c919ef3bb0d_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xb389327f8325d9568826b0f3ca63ef613687cfab_sol | Malicious | no_expected_family | F | EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xb620cee6b52f96f3c6b253e6eea556aa2d214a99_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/hidden_state_update_0xb85a54944b58342b07887942e6f530f616479efd_sol | Malicious | no_expected_family | F | EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xb919b2903e07293bc84372471a7081ecb69e8d36_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/hidden_state_update_0xb91a6c5c6362b10db6440d690e5391bb1eabe591_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xc1d73e148590b60ce9dd42d141f9b27bbad07879_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xc8b2c33a45ce83d19da15a58d1d1ddb2738506bf_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/hidden_state_update_0xcb71b51d9159a49050d56516737b4b497e98bb99_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xdfe06d5a4534fbe955eebe8a4908ef596763c2a4_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/hidden_state_update_0xe35a91f2acceccf1ce6bae792274da6100b639af_sol | Malicious | no_expected_family | F | EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xed4fd2e53153b8bfd866e11fb015a1bc4a0e9655_sol | Benign | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xf331f7887d31714dce936d9a9846e6afbe82e0a0_sol | Malicious | no_expected_family | F | FEE_UNBOUNDED, LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE |
| tier2/honeybadger/hidden_state_update_0xf6b55acbbc49f4524aa48d19281a9a77c54de10f_sol | Malicious | no_expected_family | F | BAL_DIRECT_SET, EXIT_GLOBAL_SWITCH, EXIT_TIME_GATE, LEAK_PRIV_SWEEP |
| tier2/honeybadger/hidden_state_update_0xfb0513602b08ede66c28c128ece6a2f11161f17f_sol | Benign | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/inheritance_disorder_0x017bcaee2456d8bd0e181f94165919a4a2ecc2d9_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x038e20839aebfe12b7956adcbc2511f6f7085164_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x07f06a75ddf49de735d51dbf5c0a9062c034e7c6_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x0bcccba050c2ce6439c57bd203378b113cc3cfd6_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x11f3081cd6b2ac5a263e65e206f806bea7fa9c56_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x1767856bc75cf070de5e6ba3d0c718440f008c66_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x2d05359a51ca13c4ac5f4437585afaf5bf2050f9_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x33685492a20234101b553d2a429ae8a6bf202e18_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE |
| tier2/honeybadger/inheritance_disorder_0x33b44a1d150f3feaa40503ad20a75634adc39b18_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x340844b39aacbdb4e7718fa14a95758f87a09a9a_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x3526cf7d12c95b11a680678cc1f705cba667578d_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x3e7840b88396acd80bac66021e1354064461a498_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x4ba0d338a7c41cc12778e0a2fa6df2361e8d8465_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x4c7c98c4d64c29ef8103b005eeccf5145cfdf8c1_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x4dc76cfc65b14b3fd83c8bc8b895482f3cbc150a_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x4fed7f5f0314bd156a8486fc41dc8bd4737c24fb_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x50abfc76b637b70571c301071f7ce660c1c3d847_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x50ddfe3722fc303cace413df41db23d55025e2e6_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE |
| tier2/honeybadger/inheritance_disorder_0x52c2d09acf0ef12c487ae0c20a92d4f9a4abbfd1_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x5b2028602af2693d50b4157f4acf84d632ec8208_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x5c8546a7b86ba30202c09a84f5a72644a2a4f7ba_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x641074844a0dd00042347161f830346bdfe348bc_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x68563d2a5fc58f88db8140a981170989f001b746_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x6e843aefc1f2887e5b0aeb4002c1924c433d9a13_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x70c01853e4430cae353c9a7ae232a6a95f6cafd9_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x7704442e1005b9ab403463ed85e2fb24761a8738_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x787080326e1f7e0eae490efdb18e90cfd0ae2692_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x78faf034c61f4158a4a12bfa372187a21405ae33_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x7e97c48497a8d650dc030744b74c81e29816f8e3_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x81edefc64aabdce71f68347774bd4673d1d31419_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x849019a489c3c26c7a7668e468be81a4d132781f_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x9168fdc9f9db7b71865fe4bfd6f78b3610ebc704_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x96050da7c01bbd4891ed766720a5c1c79b824163_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0x98fe1d52649a3a13863647c6789f16e46e090377_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0x9c0c5a14fde1306686a8a270f271165acda670c2_sol | Benign | no_expected_family | F | - |
| tier2/honeybadger/inheritance_disorder_0xa16cdcba1d6cb6874ff9fd8a6c8b82a3f834f512_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xb31820c1d84e183377030b6d3f0e1ee5c1cff643_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xc0c7d89e4968775931e53e9510ebad43644b0866_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE |
| tier2/honeybadger/inheritance_disorder_0xcacf9396a56e9ff1e3f6533be83a043c36ce0436_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xe65c53087e1a40b7c53b9a0ea3c2562ae2dfeb24_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0xf1aab4171ceb49b6a276975347e3c1d4d5650e5a_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xf5615138a7f2605e382375fa33ab368661e017ff_sol | Benign | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/inheritance_disorder_0xfae0300c03a1ea898176bcb39f919c559f64f4ff_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/inheritance_disorder_0xfdc39e06a7297268a0f6d5bd1692ae5fa9026152_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/inheritance_disorder_0xff41067fe843f190482d998a9976c7b19cd7c8b7_sol | Malicious | no_expected_family | F | BAL_PRIV_MINT, LEAK_ARBITRARY_TRANSFERFROM, LEAK_PRIV_SWEEP |
| tier2/honeybadger/named_EtherBet_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD |
| tier2/honeybadger/named_ICO_Hold_sol | Malicious | no_expected_family | F | OWN_REASSIGN_NONSTD |
| tier2/honeybadger/named_KingOfTheHill_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/named_PrivateBank_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/named_RACEFORETH_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/named_RichestTakeAll_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/named_TerrionFund_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE |
| tier2/honeybadger/named_TestBank_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, OWN_REASSIGN_NONSTD |
| tier2/honeybadger/named_TrustFund_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/named_TwelHourTrains_sol | Malicious | no_expected_family | F | LEAK_PRIV_SWEEP |
| tier2/honeybadger/named_X2_FLASH_sol | Malicious | no_expected_family | F | STRUCT_SELFDESTRUCT |
| tier2/honeybadger/named_firstTest_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/named_testBank2_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/straw_man_contract_0x01f8c4e3fa3edeb29e514cba738d87ce8c091d3f_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x23a91059fdc9579a9fbd0edc5f2ea0bfdb70deb4_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x4320e6f8c05b27ab4707cd1f6d5ce6f3e4b3a5a1_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x463f235748bc7862deaa04d85b4b16ac8fafef39_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x477d1ee2f953a2f85dbecbcb371c2613809ea452_sol | Malicious | no_expected_family | F | STRUCT_DELEGATECALL_SETTABLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/straw_man_contract_0x4e73b32ed6c35f570686b89848e5f39f20ecc106_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x561eac93c92360949ab1f1403323e6db345cbf31_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x7a8721a9d64c74da899424c1b52acbf58ddc9782_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x8c7777c45481dba411450c228cb692ac3d550344_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x941d225236464a25eb18076df7da6a91d0f95e9e_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0x95d34980095380851902ccd9a1fb4c813c2cb639_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xa5d6accc5695327f65cbf38da29198df53efdcf0_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xaae1f51cf3339f18b6d3f3bdc75a5facd744b0b8_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xb4c05e6e4cdb07c15095300d96a5735046eef999_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xb5e1b1ee15c6fa0e48fce100125569d430f1bd12_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xb93430ce38ac4a6bb47fb1fc085ea669353fd89e_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xbabfe0ae175b847543724c386700065137d30e3b_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xbaf51e761510c1a11bf48dd87c0307ac8a8c8a4f_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xbe4041d55db380c5ae9d4a9b9703f1ed4e7e3888_sol | Malicious | no_expected_family | F | STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xbf64a825e602a4f1c31480a470e99e1d896c88a7_sol | Malicious | no_expected_family | F | BAL_DIRECT_SET, LEAK_PRIV_SWEEP, OWN_HIDDEN_ROLE, STRUCT_SELFDESTRUCT |
| tier2/honeybadger/straw_man_contract_0xd116d1349c1382b0b302086a4e4219ae4f8634ff_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xd518db222f37f9109db8e86e2789186c7e340f12_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xdd17afae8a3dd1936d1113998900447ab9aa9bc0_sol | Malicious | no_expected_family | F | STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/straw_man_contract_0xe610af01f92f19679327715b426c35849c47c657_sol | Malicious | no_expected_family | F | SLITHER_HIGH_OVERLAY, STRUCT_EXTERNAL_GATE |
| tier2/honeybadger/uninitialised_struct_0xad1aa68300588aa5842751ddcab2afd4a69e9016_sol | Benign | no_expected_family | F | - |
| tier2/pied-piper/injected_FreezeAccount_8_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x17280da053596e097604839c61a2ef5efb7d493f_sol | Malicious | no_expected_family | A | BAL_PRIV_MINT, OWN_FAKE_RENOUNCE |
| tier2/pied-piper/real_0x1829aa045e21e0d59580024a951db48096e01782_sol | Benign | no_expected_family | B | LEAK_PRIV_SWEEP |
| tier2/pied-piper/real_0x46b9ad944d1059450da1163511069c718f699d31_sol | Malicious | no_expected_family | B | EXIT_ADDR_GATE, EXIT_GLOBAL_SWITCH, EXIT_SELL_ONLY, EXIT_TIME_GATE, OWN_REASSIGN_NONSTD |
| tier2/pied-piper/real_0x6e8b6f2d02eacbe33b4c45154cbfa53df1b542ea_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x6f7a4bac3315b5082f793161a22e26666d22717f_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x744d70fdbe2ba4cf95131626614a1763df805b9e_sol | Malicious | no_expected_family | B | EXIT_GLOBAL_SWITCH, EXIT_SELL_ONLY, LEAK_ARBITRARY_TRANSFERFROM, LEAK_PRIV_SWEEP, STRUCT_EXTERNAL_GATE |
| tier2/pied-piper/real_0x765f0c16d1ddc279295c1a7c24b0883f62d33f75_sol | Malicious | no_expected_family | B | EXIT_GLOBAL_SWITCH, LEAK_ARBITRARY_TRANSFERFROM, LEAK_PRIV_SWEEP, STRUCT_EXTERNAL_GATE |
| tier2/pied-piper/real_0x814f67fa286f7572b041d041b1d99b432c9155ee_sol | Uncertain | no_expected_family | B | EXIT_AMOUNT_LIMIT |
| tier2/pied-piper/real_0x8bcb64bfda77905398b67af0af084c744e777a20_sol | Benign | no_expected_family | A | - |
| tier2/pied-piper/real_0x93ed3fbe21207ec2e8f2d3c3de6e058cb73bc04d_sol | Malicious | no_expected_family | B | EXIT_GLOBAL_SWITCH, LEAK_ARBITRARY_TRANSFERFROM, LEAK_PRIV_SWEEP, STRUCT_EXTERNAL_GATE |
| tier2/pied-piper/real_0xb9e7f8568e08d5659f5d29c4997173d84cdf2607_sol | Malicious | no_expected_family | B | EXIT_GLOBAL_SWITCH, EXIT_SELL_ONLY, LEAK_ARBITRARY_TRANSFERFROM, STRUCT_EXTERNAL_GATE |
| tier2/pied-piper/real_0xcbeaec699431857fdb4d37addbbdc20e132d4903_sol | Malicious | no_expected_family | B | EXIT_GLOBAL_SWITCH, EXIT_SELL_ONLY, LEAK_ARBITRARY_TRANSFERFROM, LEAK_PRIV_SWEEP, STRUCT_EXTERNAL_GATE |
| tier2/pied-piper/real_0xd4c435f5b09f855c3317c8524cb1f586e42795fa_sol | Malicious | no_expected_family | B | EXIT_GLOBAL_SWITCH, LEAK_ARBITRARY_TRANSFERFROM, LEAK_PRIV_SWEEP, STRUCT_EXTERNAL_GATE |
| tier2/pied-piper/real_0xfa456cf55250a839088b27ee32a424d7dacb54ff_sol | Uncertain | no_expected_family | A | BAL_DIRECT_SET |

