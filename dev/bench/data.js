window.BENCHMARK_DATA = {
  "lastUpdate": 1778724860545,
  "repoUrl": "https://github.com/endavis/pynetappfoundry",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "0dfdf9cb3b309ddcf6b3e892f3417628cffcd8dc",
          "message": "fix: untrack _version.py so builds produce PyPI-compliant versions (merges PR #662, addresses #661)\n\n_version.py's own header says \"don't change, don't track in version\ncontrol\", but the file was committed long ago. .gitignore already lists\n**/_version.py but gitignore has no effect on tracked files. At build\ntime hatch-vcs overwrites _version.py with the computed version; git\nsees it as modified; setuptools-scm flags the tree dirty and appends a\n+d<date> local-version suffix to the wheel. PyPI and TestPyPI reject\nlocal-version strings with HTTP 400.\n\ngit rm --cached src/pynetappfoundry/_version.py untracks the file. It\nstays on disk, hatch-vcs keeps overwriting it, and setuptools-scm stops\nflagging the tree as dirty. Regression test asserts the file stays\nuntracked via git ls-files --error-unmatch.\n\nAlso removes the now-obsolete\n\"git update-index --assume-unchanged src/pynetappfoundry/_version.py\"\nstep from task_install_dev. That was a workaround for the tracked-file\nproblem this PR fixes at the root; after untracking, the command itself\nfails on untracked files and would break doit install_dev for every\ndeveloper on a fresh clone. Syncs the matching doc entry.\n\nAddresses #661.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T02:42:25+01:00",
          "tree_id": "fe42e4a58a34369a3267ec9171b142b5d88efcb9",
          "url": "https://github.com/endavis/pynetappfoundry/commit/0dfdf9cb3b309ddcf6b3e892f3417628cffcd8dc"
        },
        "date": 1776735816650,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 817831.780326593,
            "unit": "iter/sec",
            "range": "stddev: 2.8433701921816313e-7",
            "extra": "mean: 1.2227453420808128 usec\nrounds: 52062"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 547314.09943874,
            "unit": "iter/sec",
            "range": "stddev: 3.202682495704069e-7",
            "extra": "mean: 1.8271044013400723 usec\nrounds: 127211"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 369235.9075274643,
            "unit": "iter/sec",
            "range": "stddev: 3.8688853168495596e-7",
            "extra": "mean: 2.7082956440947403 usec\nrounds: 125898"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 367956.44987936824,
            "unit": "iter/sec",
            "range": "stddev: 3.6515631029392936e-7",
            "extra": "mean: 2.7177129258852304 usec\nrounds: 134157"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 379760.2723399851,
            "unit": "iter/sec",
            "range": "stddev: 3.922578412372077e-7",
            "extra": "mean: 2.6332401592148047 usec\nrounds: 66077"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 122398.69632446734,
            "unit": "iter/sec",
            "range": "stddev: 6.647920620521164e-7",
            "extra": "mean: 8.170021658965181 usec\nrounds: 46909"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 109771.09536941988,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013511742985511307",
            "extra": "mean: 9.109866277954449 usec\nrounds: 57627"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 59773.919615296756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012034304115333047",
            "extra": "mean: 16.72970429973426 usec\nrounds: 35979"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 184075.8495070622,
            "unit": "iter/sec",
            "range": "stddev: 6.187849380885857e-7",
            "extra": "mean: 5.432543175424184 usec\nrounds: 37614"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 25919.859469623356,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019849069681600106",
            "extra": "mean: 38.58045608510898 usec\nrounds: 2539"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 72.11831544635908,
            "unit": "iter/sec",
            "range": "stddev: 0.0003368080527318343",
            "extra": "mean: 13.866103136363337 msec\nrounds: 66"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 70.30113402117216,
            "unit": "iter/sec",
            "range": "stddev: 0.00037136867633723205",
            "extra": "mean: 14.224521608696044 msec\nrounds: 69"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 82.89679498350766,
            "unit": "iter/sec",
            "range": "stddev: 0.00019370670721669458",
            "extra": "mean: 12.063192554054114 msec\nrounds: 74"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 13.46581352068593,
            "unit": "iter/sec",
            "range": "stddev: 0.00023569762583162498",
            "extra": "mean: 74.26213042857148 msec\nrounds: 14"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 269.8788898185196,
            "unit": "iter/sec",
            "range": "stddev: 0.00008487429149384485",
            "extra": "mean: 3.7053657685951324 msec\nrounds: 242"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 73.70840331295943,
            "unit": "iter/sec",
            "range": "stddev: 0.0005155142646240456",
            "extra": "mean: 13.566974117646906 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.4036668498368576,
            "unit": "iter/sec",
            "range": "stddev: 0.10838486455096619",
            "extra": "mean: 712.4197598000023 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.411295752427231,
            "unit": "iter/sec",
            "range": "stddev: 0.10484130850809556",
            "extra": "mean: 708.5687024000038 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 313628.91891082196,
            "unit": "iter/sec",
            "range": "stddev: 3.743138695955583e-7",
            "extra": "mean: 3.188481481468048 usec\nrounds: 12015"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 303650.4198478457,
            "unit": "iter/sec",
            "range": "stddev: 8.535002018350021e-7",
            "extra": "mean: 3.293260719023816 usec\nrounds: 53130"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 299263.894645733,
            "unit": "iter/sec",
            "range": "stddev: 3.780899769404011e-7",
            "extra": "mean: 3.3415323996360953 usec\nrounds: 49908"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 142228.6763333245,
            "unit": "iter/sec",
            "range": "stddev: 5.908756385414813e-7",
            "extra": "mean: 7.030930933058947 usec\nrounds: 37413"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 163255.14008453864,
            "unit": "iter/sec",
            "range": "stddev: 6.379444334445284e-7",
            "extra": "mean: 6.125381409015168 usec\nrounds: 48077"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 327160.535672127,
            "unit": "iter/sec",
            "range": "stddev: 7.633102036630442e-7",
            "extra": "mean: 3.056603382634689 usec\nrounds: 70892"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 333549.84670184064,
            "unit": "iter/sec",
            "range": "stddev: 3.6097460887030943e-7",
            "extra": "mean: 2.9980526445688866 usec\nrounds: 64793"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 27720.893568818417,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015621558332237065",
            "extra": "mean: 36.07387321470908 usec\nrounds: 14284"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 406800.73074536707,
            "unit": "iter/sec",
            "range": "stddev: 3.244069164912339e-7",
            "extra": "mean: 2.4582060070731293 usec\nrounds: 51406"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 185948.31271446368,
            "unit": "iter/sec",
            "range": "stddev: 9.492069887655388e-7",
            "extra": "mean: 5.377838526212218 usec\nrounds: 48175"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 272804.35597171413,
            "unit": "iter/sec",
            "range": "stddev: 4.452519376855242e-7",
            "extra": "mean: 3.6656306180964555 usec\nrounds: 54556"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 165884.0124318541,
            "unit": "iter/sec",
            "range": "stddev: 5.312985481262251e-7",
            "extra": "mean: 6.028308486996627 usec\nrounds: 42783"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 153863.34151470865,
            "unit": "iter/sec",
            "range": "stddev: 6.512913927356407e-7",
            "extra": "mean: 6.499273902123102 usec\nrounds: 54242"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 38770.27688465584,
            "unit": "iter/sec",
            "range": "stddev: 0.000001329090881282758",
            "extra": "mean: 25.792954818844 usec\nrounds: 19123"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 19669.6607898336,
            "unit": "iter/sec",
            "range": "stddev: 0.000043804713729612144",
            "extra": "mean: 50.83971760798523 usec\nrounds: 9632"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 28104.14545765751,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020014529095168303",
            "extra": "mean: 35.58193937996186 usec\nrounds: 8611"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 270.5616865816428,
            "unit": "iter/sec",
            "range": "stddev: 0.000034770346719490853",
            "extra": "mean: 3.696014807692467 msec\nrounds: 260"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 26.53807988004534,
            "unit": "iter/sec",
            "range": "stddev: 0.0001911626524602972",
            "extra": "mean: 37.68170133333292 msec\nrounds: 27"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 22867.10279702159,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019358264763266685",
            "extra": "mean: 43.7309443560226 usec\nrounds: 13820"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 179.66395336156287,
            "unit": "iter/sec",
            "range": "stddev: 0.011367628627081265",
            "extra": "mean: 5.565946765000547 msec\nrounds: 200"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.495944165119615,
            "unit": "iter/sec",
            "range": "stddev: 0.05882911404905541",
            "extra": "mean: 74.09633500000012 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 11937.94451664516,
            "unit": "iter/sec",
            "range": "stddev: 0.000003358892506270275",
            "extra": "mean: 83.76651429445772 usec\nrounds: 6436"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1f8a87909d4336b0661f8ad05374114acdcca2d1",
          "message": "release: v0.1.0a1 (merges PR #663)\n\nchore: update changelog for v0.1.0a1",
          "timestamp": "2026-04-21T02:59:39+01:00",
          "tree_id": "2cd612b2ad41238cef7ee00f5ca29945d58eeabb",
          "url": "https://github.com/endavis/pynetappfoundry/commit/1f8a87909d4336b0661f8ad05374114acdcca2d1"
        },
        "date": 1776736849775,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 833231.824032036,
            "unit": "iter/sec",
            "range": "stddev: 3.3422416916864026e-7",
            "extra": "mean: 1.2001461912015883 usec\nrounds: 43833"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 539882.0605008589,
            "unit": "iter/sec",
            "range": "stddev: 5.455187949715362e-7",
            "extra": "mean: 1.8522563966513 usec\nrounds: 137533"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 367917.0389182615,
            "unit": "iter/sec",
            "range": "stddev: 6.531099748118581e-7",
            "extra": "mean: 2.7180040449884295 usec\nrounds: 130532"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 367170.826978434,
            "unit": "iter/sec",
            "range": "stddev: 6.372254505290235e-7",
            "extra": "mean: 2.7235279235807464 usec\nrounds: 136408"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 359352.25045960664,
            "unit": "iter/sec",
            "range": "stddev: 6.082644951617219e-7",
            "extra": "mean: 2.782784854473608 usec\nrounds: 66792"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 111409.21177695382,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010316065852711395",
            "extra": "mean: 8.975918454589234 usec\nrounds: 24796"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 98555.34402811452,
            "unit": "iter/sec",
            "range": "stddev: 0.000001190477348707193",
            "extra": "mean: 10.146583220436364 usec\nrounds: 55353"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 57873.463326019504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014759853633555007",
            "extra": "mean: 17.279076497749653 usec\nrounds: 35086"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 173501.75349705567,
            "unit": "iter/sec",
            "range": "stddev: 8.367711026669269e-7",
            "extra": "mean: 5.7636305100338365 usec\nrounds: 37568"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23613.339450114603,
            "unit": "iter/sec",
            "range": "stddev: 0.000002312708384085329",
            "extra": "mean: 42.34894442239286 usec\nrounds: 2519"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 68.03462791502619,
            "unit": "iter/sec",
            "range": "stddev: 0.0006876927897520766",
            "extra": "mean: 14.698397428570916 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 65.8271925418037,
            "unit": "iter/sec",
            "range": "stddev: 0.0010295356784044438",
            "extra": "mean: 15.191290428570957 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 76.34927950182504,
            "unit": "iter/sec",
            "range": "stddev: 0.0005429996918521294",
            "extra": "mean: 13.097700548386921 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.360250852678472,
            "unit": "iter/sec",
            "range": "stddev: 0.0006579181378255099",
            "extra": "mean: 96.52275936363708 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 268.0175376759549,
            "unit": "iter/sec",
            "range": "stddev: 0.00007031989487940943",
            "extra": "mean: 3.7310991238530242 msec\nrounds: 218"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 68.48637548047272,
            "unit": "iter/sec",
            "range": "stddev: 0.000937893406172922",
            "extra": "mean: 14.60144434545418 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2239686404624996,
            "unit": "iter/sec",
            "range": "stddev: 0.15314068590227342",
            "extra": "mean: 817.0143964000018 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2465468362107173,
            "unit": "iter/sec",
            "range": "stddev: 0.14442401873088426",
            "extra": "mean: 802.2161469999986 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 292725.5071692917,
            "unit": "iter/sec",
            "range": "stddev: 6.236823062081429e-7",
            "extra": "mean: 3.416169672640351 usec\nrounds: 10479"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 285293.21610033355,
            "unit": "iter/sec",
            "range": "stddev: 6.602780523548793e-7",
            "extra": "mean: 3.5051657157116356 usec\nrounds: 60115"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 276310.3625282818,
            "unit": "iter/sec",
            "range": "stddev: 7.717737267917694e-7",
            "extra": "mean: 3.6191186998918465 usec\nrounds: 73530"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 135123.47304108617,
            "unit": "iter/sec",
            "range": "stddev: 9.056645655826535e-7",
            "extra": "mean: 7.40063867138714 usec\nrounds: 38054"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 157268.1065331192,
            "unit": "iter/sec",
            "range": "stddev: 9.504501622343707e-7",
            "extra": "mean: 6.35856832033143 usec\nrounds: 50051"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 304878.4542173116,
            "unit": "iter/sec",
            "range": "stddev: 5.737192047106919e-7",
            "extra": "mean: 3.2799956381542756 usec\nrounds: 74739"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 311093.8280167981,
            "unit": "iter/sec",
            "range": "stddev: 5.540033411186654e-7",
            "extra": "mean: 3.214464286787467 usec\nrounds: 67286"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 25863.915826585868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023086607426064063",
            "extra": "mean: 38.66390560133537 usec\nrounds: 13104"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 376442.6063866309,
            "unit": "iter/sec",
            "range": "stddev: 5.362514610799649e-7",
            "extra": "mean: 2.656447445199482 usec\nrounds: 46989"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 170643.296808951,
            "unit": "iter/sec",
            "range": "stddev: 9.8001953787684e-7",
            "extra": "mean: 5.860177450272664 usec\nrounds: 50076"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 247807.32885678162,
            "unit": "iter/sec",
            "range": "stddev: 7.735419062027234e-7",
            "extra": "mean: 4.035393160538615 usec\nrounds: 50969"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 149859.9045188207,
            "unit": "iter/sec",
            "range": "stddev: 7.980150013268247e-7",
            "extra": "mean: 6.672898953264789 usec\nrounds: 43564"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 138060.6821155929,
            "unit": "iter/sec",
            "range": "stddev: 9.077213152459372e-7",
            "extra": "mean: 7.243191795639097 usec\nrounds: 28619"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 35432.479651208654,
            "unit": "iter/sec",
            "range": "stddev: 0.000001920394385199882",
            "extra": "mean: 28.222693129124213 usec\nrounds: 17698"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 17889.253943837914,
            "unit": "iter/sec",
            "range": "stddev: 0.00003819355452173815",
            "extra": "mean: 55.89948038858587 usec\nrounds: 11014"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 25540.01916342111,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024106052683081585",
            "extra": "mean: 39.154238436603 usec\nrounds: 8929"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 243.98351535178784,
            "unit": "iter/sec",
            "range": "stddev: 0.000039228027385055674",
            "extra": "mean: 4.098637559829192 msec\nrounds: 234"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 23.648181557116978,
            "unit": "iter/sec",
            "range": "stddev: 0.0011010014670477623",
            "extra": "mean: 42.2865494999994 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 21423.787990165507,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036950403096722894",
            "extra": "mean: 46.67708625846398 usec\nrounds: 12706"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 161.9908052067749,
            "unit": "iter/sec",
            "range": "stddev: 0.01493153713621084",
            "extra": "mean: 6.173189883978534 msec\nrounds: 181"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 10.834412038494705,
            "unit": "iter/sec",
            "range": "stddev: 0.08800586656351204",
            "extra": "mean: 92.29850188888851 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 11405.744513219428,
            "unit": "iter/sec",
            "range": "stddev: 0.000004856123726960153",
            "extra": "mean: 87.67511834418043 usec\nrounds: 5653"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "751e0a7b5357519108e445faddda4fdc22a1a06c",
          "message": "release: v0.1.0 (merges PR #664)\n\nchore: update changelog for v0.1.0",
          "timestamp": "2026-04-21T03:18:27+01:00",
          "tree_id": "40f6ac7426657e4d1c8c05f8e73e52b58a4201f0",
          "url": "https://github.com/endavis/pynetappfoundry/commit/751e0a7b5357519108e445faddda4fdc22a1a06c"
        },
        "date": 1776737977127,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 841891.9659543559,
            "unit": "iter/sec",
            "range": "stddev: 3.1016183038484634e-7",
            "extra": "mean: 1.187800858589279 usec\nrounds: 44260"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 534566.8337464641,
            "unit": "iter/sec",
            "range": "stddev: 5.402247950868278e-7",
            "extra": "mean: 1.8706734815394155 usec\nrounds: 144488"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 363549.23055143026,
            "unit": "iter/sec",
            "range": "stddev: 6.57431689360252e-7",
            "extra": "mean: 2.7506591018861553 usec\nrounds: 120294"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 365698.54287248495,
            "unit": "iter/sec",
            "range": "stddev: 5.980851951445812e-7",
            "extra": "mean: 2.7344927112512147 usec\nrounds: 114903"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 370205.17137169675,
            "unit": "iter/sec",
            "range": "stddev: 5.841832619732645e-7",
            "extra": "mean: 2.7012048381030604 usec\nrounds: 62132"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 116403.47240590081,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010434524571507317",
            "extra": "mean: 8.590809013952638 usec\nrounds: 45019"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 106133.28682287996,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011466520830440367",
            "extra": "mean: 9.422114681785416 usec\nrounds: 57350"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 58698.98240201199,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015077944008827767",
            "extra": "mean: 17.03607045776868 usec\nrounds: 35610"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 177015.36655123727,
            "unit": "iter/sec",
            "range": "stddev: 8.119459397644967e-7",
            "extra": "mean: 5.649227067021603 usec\nrounds: 36901"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23932.034578379364,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026534707030603",
            "extra": "mean: 41.784997289926125 usec\nrounds: 2583"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 67.20226124857237,
            "unit": "iter/sec",
            "range": "stddev: 0.0007565266766999135",
            "extra": "mean: 14.880451660713183 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 64.6212175343497,
            "unit": "iter/sec",
            "range": "stddev: 0.0008523441527859997",
            "extra": "mean: 15.474793545455027 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 75.61048564653241,
            "unit": "iter/sec",
            "range": "stddev: 0.0006118138396397499",
            "extra": "mean: 13.225678838710929 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.715407624422058,
            "unit": "iter/sec",
            "range": "stddev: 0.0003648244212213104",
            "extra": "mean: 93.32356127272719 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 266.7478843142928,
            "unit": "iter/sec",
            "range": "stddev: 0.00006230667640457098",
            "extra": "mean: 3.7488582245764355 msec\nrounds: 236"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 65.47943155214706,
            "unit": "iter/sec",
            "range": "stddev: 0.0008796144108566725",
            "extra": "mean: 15.271971309091338 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2089140107280996,
            "unit": "iter/sec",
            "range": "stddev: 0.14369727722272746",
            "extra": "mean: 827.1886926000008 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.196194279669064,
            "unit": "iter/sec",
            "range": "stddev: 0.15145756083861311",
            "extra": "mean: 835.9846029999886 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 287105.67986494716,
            "unit": "iter/sec",
            "range": "stddev: 6.984788116171897e-7",
            "extra": "mean: 3.4830380244319588 usec\nrounds: 8889"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 277360.05388219387,
            "unit": "iter/sec",
            "range": "stddev: 8.008222298535075e-7",
            "extra": "mean: 3.6054218551051367 usec\nrounds: 59684"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 273884.0856757051,
            "unit": "iter/sec",
            "range": "stddev: 9.466137320657796e-7",
            "extra": "mean: 3.6511796497152416 usec\nrounds: 62132"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 131221.5657749259,
            "unit": "iter/sec",
            "range": "stddev: 9.149412592772729e-7",
            "extra": "mean: 7.620698580256404 usec\nrounds: 35711"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 149124.67200207958,
            "unit": "iter/sec",
            "range": "stddev: 9.9627446797762e-7",
            "extra": "mean: 6.705798487765021 usec\nrounds: 50126"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 301856.7333840901,
            "unit": "iter/sec",
            "range": "stddev: 5.945799063311147e-7",
            "extra": "mean: 3.3128298606729265 usec\nrounds: 71271"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 305593.75470693246,
            "unit": "iter/sec",
            "range": "stddev: 6.080892930131353e-7",
            "extra": "mean: 3.272318182546009 usec\nrounds: 67191"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 25713.438381016804,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025366197816370633",
            "extra": "mean: 38.890170391924705 usec\nrounds: 11990"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 372939.7444940061,
            "unit": "iter/sec",
            "range": "stddev: 4.928942729442188e-7",
            "extra": "mean: 2.681398308342736 usec\nrounds: 45992"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 167322.02023514864,
            "unit": "iter/sec",
            "range": "stddev: 7.699420646156063e-7",
            "extra": "mean: 5.976499677655305 usec\nrounds: 49628"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 246956.69578519772,
            "unit": "iter/sec",
            "range": "stddev: 6.472924710936107e-7",
            "extra": "mean: 4.049292920851991 usec\nrounds: 52888"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 150815.09120337217,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010142251897587767",
            "extra": "mean: 6.6306361785208425 usec\nrounds: 44695"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 135706.22229764867,
            "unit": "iter/sec",
            "range": "stddev: 9.199640504469713e-7",
            "extra": "mean: 7.368858870794215 usec\nrounds: 52087"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 35352.35113208155,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023381638842969166",
            "extra": "mean: 28.286661791286633 usec\nrounds: 13264"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 17818.991352591634,
            "unit": "iter/sec",
            "range": "stddev: 0.000036398405141257015",
            "extra": "mean: 56.11989928119909 usec\nrounds: 11130"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 25222.440755885254,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026630718869045866",
            "extra": "mean: 39.64723357578572 usec\nrounds: 8798"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 244.1178310610849,
            "unit": "iter/sec",
            "range": "stddev: 0.00012788666060789628",
            "extra": "mean: 4.096382454544146 msec\nrounds: 231"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 23.307707299031055,
            "unit": "iter/sec",
            "range": "stddev: 0.0010670371080069218",
            "extra": "mean: 42.90426283333204 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 21602.90269915686,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026832645733863655",
            "extra": "mean: 46.29007564057717 usec\nrounds: 12176"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 160.94236481499806,
            "unit": "iter/sec",
            "range": "stddev: 0.01636708730265831",
            "extra": "mean: 6.213404414365925 msec\nrounds: 181"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.759798701465613,
            "unit": "iter/sec",
            "range": "stddev: 0.08382068267799489",
            "extra": "mean: 85.03546917647246 msec\nrounds: 17"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 11577.664610389085,
            "unit": "iter/sec",
            "range": "stddev: 0.000005330552443819676",
            "extra": "mean: 86.37320510240566 usec\nrounds: 4978"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "24c86cc8323a86b1cc37b401ada0413f0862dbc1",
          "message": "fix: split SBOMs into separate release artifact so twine accepts dist (merges PR #666, addresses #665)\n\nrelease.yml's build job generated SBOMs (sbom.json, sbom.xml) into\ndist/ alongside the wheels and sdist, then uploaded the whole directory\nas a single dist artifact. publish-testpypi and publish handed\npackages-dir: dist to pypa/gh-action-pypi-publish, which calls twine.\nTwine inspects every file in packages-dir and rejected sbom.json with\n\"InvalidDistribution: Unknown distribution format\". publish-testpypi\nfailed; publish and github-release were skipped (both needs: upstream).\n\nSplit the build output into two artifacts: dist (wheels + sdist only,\nconsumed by the publish jobs) and sbom (the SBOM files, consumed by\ngithub-release). github-release's download-artifact now grabs sbom into\ndist/ so the existing gh release upload line is unchanged. publish jobs\nare unchanged — they already only download the dist artifact and now\nget a twine-clean payload. New tests/test_release_workflow.py pins the\nartifact split via 3 structural YAML asserts. Synced\ndocs/development/release-and-automation.md SBOM bullet.\n\nPost-merge: re-run the failed release.yml run for v0.1.0 via Actions\n→ Release → Re-run failed jobs. skip-existing: true tolerates already-\nuploaded files and gh release upload --clobber handles re-upload.\n\nAddresses #665.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T03:50:45+01:00",
          "tree_id": "fffbf59bd88f5f943012f6c920c6778f1eff6b79",
          "url": "https://github.com/endavis/pynetappfoundry/commit/24c86cc8323a86b1cc37b401ada0413f0862dbc1"
        },
        "date": 1776739917178,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 841568.9213196117,
            "unit": "iter/sec",
            "range": "stddev: 3.627427374020869e-7",
            "extra": "mean: 1.188256807810776 usec\nrounds: 50824"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 535537.0851867399,
            "unit": "iter/sec",
            "range": "stddev: 5.021504775701053e-7",
            "extra": "mean: 1.8672843163630832 usec\nrounds: 155232"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 354556.9792319889,
            "unit": "iter/sec",
            "range": "stddev: 6.428031469764198e-7",
            "extra": "mean: 2.820421141239737 usec\nrounds: 81348"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 351210.72856617626,
            "unit": "iter/sec",
            "range": "stddev: 6.171106136402543e-7",
            "extra": "mean: 2.847293430022815 usec\nrounds: 127976"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 349743.81482709816,
            "unit": "iter/sec",
            "range": "stddev: 8.775752720422603e-7",
            "extra": "mean: 2.859235696546534 usec\nrounds: 67536"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 114841.89644678782,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012250986035551802",
            "extra": "mean: 8.707623532352164 usec\nrounds: 47781"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 104813.43982927524,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011572700784365134",
            "extra": "mean: 9.540761200365566 usec\nrounds: 54485"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 56103.122439317594,
            "unit": "iter/sec",
            "range": "stddev: 0.000001608790964043093",
            "extra": "mean: 17.824319868856186 usec\nrounds: 29584"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 176532.88801735197,
            "unit": "iter/sec",
            "range": "stddev: 0.000001275285509766766",
            "extra": "mean: 5.6646668574396575 usec\nrounds: 38434"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23130.477588490296,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037797523817572578",
            "extra": "mean: 43.23300269846564 usec\nrounds: 2594"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 55.33349674797261,
            "unit": "iter/sec",
            "range": "stddev: 0.0010654008914436084",
            "extra": "mean: 18.072235784315207 msec\nrounds: 51"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 54.36849582403033,
            "unit": "iter/sec",
            "range": "stddev: 0.001136354200726852",
            "extra": "mean: 18.393004714285475 msec\nrounds: 49"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 63.378361324248196,
            "unit": "iter/sec",
            "range": "stddev: 0.0005369268740034047",
            "extra": "mean: 15.778255844828948 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.652070800055139,
            "unit": "iter/sec",
            "range": "stddev: 0.0003718656464468145",
            "extra": "mean: 103.60471039999908 msec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 256.9392449470002,
            "unit": "iter/sec",
            "range": "stddev: 0.00009800833755193416",
            "extra": "mean: 3.8919706493504864 msec\nrounds: 231"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 51.45624286852462,
            "unit": "iter/sec",
            "range": "stddev: 0.002514589160426452",
            "extra": "mean: 19.433987875000724 msec\nrounds: 48"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2889789576283694,
            "unit": "iter/sec",
            "range": "stddev: 0.12787894218979887",
            "extra": "mean: 775.8078547999958 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2779112127797374,
            "unit": "iter/sec",
            "range": "stddev: 0.12431073668326152",
            "extra": "mean: 782.5269783999943 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 284464.1893167545,
            "unit": "iter/sec",
            "range": "stddev: 7.940441012993372e-7",
            "extra": "mean: 3.515380977837204 usec\nrounds: 11208"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 276589.544696239,
            "unit": "iter/sec",
            "range": "stddev: 6.610087169824339e-7",
            "extra": "mean: 3.615465657236746 usec\nrounds: 67627"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 276289.83785756206,
            "unit": "iter/sec",
            "range": "stddev: 7.11029167938443e-7",
            "extra": "mean: 3.619387552413484 usec\nrounds: 75902"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 127819.39922543439,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011130836713131196",
            "extra": "mean: 7.823538571295469 usec\nrounds: 39252"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 148642.10824789706,
            "unit": "iter/sec",
            "range": "stddev: 9.88448574989297e-7",
            "extra": "mean: 6.727568733970426 usec\nrounds: 50259"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 299055.78476006066,
            "unit": "iter/sec",
            "range": "stddev: 7.048315445988154e-7",
            "extra": "mean: 3.3438577381217454 usec\nrounds: 73449"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 304575.72164465516,
            "unit": "iter/sec",
            "range": "stddev: 6.746854089473183e-7",
            "extra": "mean: 3.2832557848018102 usec\nrounds: 69363"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 23371.150029734352,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035000893094592336",
            "extra": "mean: 42.78779601036887 usec\nrounds: 12633"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 372190.0545479354,
            "unit": "iter/sec",
            "range": "stddev: 5.490828078994221e-7",
            "extra": "mean: 2.6867993590387766 usec\nrounds: 52726"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 168669.35012203336,
            "unit": "iter/sec",
            "range": "stddev: 9.488342505171882e-7",
            "extra": "mean: 5.928759429478406 usec\nrounds: 50692"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 245585.68755177472,
            "unit": "iter/sec",
            "range": "stddev: 7.547261520525461e-7",
            "extra": "mean: 4.07189852946613 usec\nrounds: 47738"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 147368.70059723582,
            "unit": "iter/sec",
            "range": "stddev: 9.562555902908562e-7",
            "extra": "mean: 6.785701413850675 usec\nrounds: 44560"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 135987.52108740425,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014035675333729891",
            "extra": "mean: 7.353615920075951 usec\nrounds: 53291"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 34164.51633441383,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025832154208566228",
            "extra": "mean: 29.270134844341484 usec\nrounds: 18221"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 16824.015648837532,
            "unit": "iter/sec",
            "range": "stddev: 0.00003119585287170643",
            "extra": "mean: 59.43884152705812 usec\nrounds: 10740"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 23864.456142158644,
            "unit": "iter/sec",
            "range": "stddev: 0.000003528683361578389",
            "extra": "mean: 41.90332241569138 usec\nrounds: 8793"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 230.1325921118658,
            "unit": "iter/sec",
            "range": "stddev: 0.000053725238965648035",
            "extra": "mean: 4.3453210639278215 msec\nrounds: 219"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 22.368901876528753,
            "unit": "iter/sec",
            "range": "stddev: 0.000614375223287943",
            "extra": "mean: 44.704921391303536 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 19981.139279165523,
            "unit": "iter/sec",
            "range": "stddev: 0.000008920868262399903",
            "extra": "mean: 50.04719630990748 usec\nrounds: 12791"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 153.33341798082074,
            "unit": "iter/sec",
            "range": "stddev: 0.015895209242166967",
            "extra": "mean: 6.521735530118308 msec\nrounds: 166"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.049683946841013,
            "unit": "iter/sec",
            "range": "stddev: 0.08022161555631442",
            "extra": "mean: 90.50032605556011 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 9990.541724277657,
            "unit": "iter/sec",
            "range": "stddev: 0.000007914071110201087",
            "extra": "mean: 100.09467230089595 usec\nrounds: 5798"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "6aee3f627ac1c175554e573df460c6bfaf79d5de",
          "message": "fix: bump lxml to 6.1.0 in uv.lock to resolve CVE-2026-41066 (merges PR #670, addresses #669)\n\npip-audit flags lxml 6.0.2 for CVE-2026-41066 with a fix in 6.1.0.\nlxml is a transitive dependency via cyclonedx-python-lib, pulled in\nthrough both cyclonedx-bom[validation] and pip-audit under the\nsecurity extra. Since pip-audit --skip-editable inspects the\nresolved lockfile, the CVE blocks CI on every branch until the lock\nis regenerated.\n\nRegenerated via: uv lock --upgrade-package lxml\n\nNo pyproject.toml change — the bump is lock-only, matching the\nupstream pyproject-template fix (#460).\n\nAddresses #669.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T18:45:25+01:00",
          "tree_id": "612923f9d6b0ecef2bd8a0e90cbf1e0b391e6daf",
          "url": "https://github.com/endavis/pynetappfoundry/commit/6aee3f627ac1c175554e573df460c6bfaf79d5de"
        },
        "date": 1776966408592,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 823852.1660369227,
            "unit": "iter/sec",
            "range": "stddev: 3.437252941903449e-7",
            "extra": "mean: 1.2138100028436205 usec\nrounds: 49906"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 536707.1817547256,
            "unit": "iter/sec",
            "range": "stddev: 4.961433165682658e-7",
            "extra": "mean: 1.8632133759242269 usec\nrounds: 161499"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 352305.17455518834,
            "unit": "iter/sec",
            "range": "stddev: 6.989862557230774e-7",
            "extra": "mean: 2.8384482324523757 usec\nrounds: 130294"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 351454.0643267123,
            "unit": "iter/sec",
            "range": "stddev: 6.08221000718657e-7",
            "extra": "mean: 2.8453220534402424 usec\nrounds: 131857"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 363492.5842975752,
            "unit": "iter/sec",
            "range": "stddev: 6.291919582737168e-7",
            "extra": "mean: 2.751087761343006 usec\nrounds: 27928"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 115399.87849212805,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012165368631909012",
            "extra": "mean: 8.665520389332253 usec\nrounds: 49315"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 104964.54007776809,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010866476303876845",
            "extra": "mean: 9.52702692984794 usec\nrounds: 53955"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 55971.30005638263,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019116449214058574",
            "extra": "mean: 17.86629931755473 usec\nrounds: 36777"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 175496.82594335964,
            "unit": "iter/sec",
            "range": "stddev: 9.46283132895066e-7",
            "extra": "mean: 5.698108752820082 usec\nrounds: 40330"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23442.343874260376,
            "unit": "iter/sec",
            "range": "stddev: 0.000004200195648451418",
            "extra": "mean: 42.65785048473745 usec\nrounds: 2682"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 58.05840603128424,
            "unit": "iter/sec",
            "range": "stddev: 0.0012662934192737426",
            "extra": "mean: 17.224034698113467 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 59.08609571732535,
            "unit": "iter/sec",
            "range": "stddev: 0.001014930991438993",
            "extra": "mean: 16.92445553999903 msec\nrounds: 50"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 64.66495716948596,
            "unit": "iter/sec",
            "range": "stddev: 0.0013979365600419393",
            "extra": "mean: 15.464326333334046 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.477917672105798,
            "unit": "iter/sec",
            "range": "stddev: 0.0007952341844976062",
            "extra": "mean: 105.50840750000106 msec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 256.4933676183724,
            "unit": "iter/sec",
            "range": "stddev: 0.000025952023608268967",
            "extra": "mean: 3.8987362881361727 msec\nrounds: 236"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 55.83166332513265,
            "unit": "iter/sec",
            "range": "stddev: 0.001998873789810574",
            "extra": "mean: 17.910983489360767 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.3038451493377792,
            "unit": "iter/sec",
            "range": "stddev: 0.12273113810459947",
            "extra": "mean: 766.9622427999968 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2967024140792862,
            "unit": "iter/sec",
            "range": "stddev: 0.12295972519648177",
            "extra": "mean: 771.1869656000005 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 286621.7122617913,
            "unit": "iter/sec",
            "range": "stddev: 7.336186192235906e-7",
            "extra": "mean: 3.488919217280481 usec\nrounds: 9148"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 280528.61841420544,
            "unit": "iter/sec",
            "range": "stddev: 8.582891330229272e-7",
            "extra": "mean: 3.56469869510241 usec\nrounds: 67669"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 277513.8342009786,
            "unit": "iter/sec",
            "range": "stddev: 6.940806481658127e-7",
            "extra": "mean: 3.603423962193499 usec\nrounds: 79158"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 131494.97022959046,
            "unit": "iter/sec",
            "range": "stddev: 0.000001047349343403469",
            "extra": "mean: 7.604853617244813 usec\nrounds: 39547"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 151371.15103304636,
            "unit": "iter/sec",
            "range": "stddev: 0.000001044220494213719",
            "extra": "mean: 6.606278628228747 usec\nrounds: 48929"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 302894.603270785,
            "unit": "iter/sec",
            "range": "stddev: 6.151829217598028e-7",
            "extra": "mean: 3.301478432436808 usec\nrounds: 76782"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 306485.8590772765,
            "unit": "iter/sec",
            "range": "stddev: 6.255052735022241e-7",
            "extra": "mean: 3.2627932753917457 usec\nrounds: 72807"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 23966.680971147085,
            "unit": "iter/sec",
            "range": "stddev: 0.000003235794658736778",
            "extra": "mean: 41.724592621059045 usec\nrounds: 12983"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 343646.9245884981,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010914033357734935",
            "extra": "mean: 2.9099634783505066 usec\nrounds: 53749"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 172322.06139556284,
            "unit": "iter/sec",
            "range": "stddev: 8.554591416558738e-7",
            "extra": "mean: 5.803087497337409 usec\nrounds: 51293"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 243221.16496721853,
            "unit": "iter/sec",
            "range": "stddev: 9.807306076385122e-7",
            "extra": "mean: 4.11148429510557 usec\nrounds: 57498"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 148303.72565684674,
            "unit": "iter/sec",
            "range": "stddev: 9.213341120995391e-7",
            "extra": "mean: 6.742918935926496 usec\nrounds: 44582"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 137065.3053118019,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012366904320182315",
            "extra": "mean: 7.295792306631924 usec\nrounds: 57166"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 34257.66983028462,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022951572080036196",
            "extra": "mean: 29.19054345943797 usec\nrounds: 18546"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 16308.783339906708,
            "unit": "iter/sec",
            "range": "stddev: 0.0000382466583398318",
            "extra": "mean: 61.31665245396046 usec\nrounds: 8537"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 24217.339242120164,
            "unit": "iter/sec",
            "range": "stddev: 0.000003504111346616863",
            "extra": "mean: 41.292727908801126 usec\nrounds: 9291"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 233.09460449429622,
            "unit": "iter/sec",
            "range": "stddev: 0.00019740169095618413",
            "extra": "mean: 4.290103591927928 msec\nrounds: 223"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 22.602323265095094,
            "unit": "iter/sec",
            "range": "stddev: 0.0008099741394254131",
            "extra": "mean: 44.243239434784385 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 20427.388120910084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045200398529727895",
            "extra": "mean: 48.953884563262896 usec\nrounds: 12535"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 158.41831889407584,
            "unit": "iter/sec",
            "range": "stddev: 0.013958114577061233",
            "extra": "mean: 6.312401286549669 msec\nrounds: 171"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.244034863816301,
            "unit": "iter/sec",
            "range": "stddev: 0.07691511291461403",
            "extra": "mean: 88.9360458333365 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 10132.638885130264,
            "unit": "iter/sec",
            "range": "stddev: 0.000006807019174940315",
            "extra": "mean: 98.69097392462183 usec\nrounds: 6021"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "36c322f3902781b45079298f2d0e7faa69e90fe1",
          "message": "chore: sync with pyproject-template (64c7aca0 → 0cdab3e) (merges PR #668, addresses #667)\n\n* chore: sync with pyproject-template (64c7aca0 → 0cdab3e)\n\nSyncs to upstream pyproject-template commit 0cdab3e (2026-04-22),\ncovering ~30 upstream commits touching 136 files. Key changes:\n\nTooling (tools/doit/, tools/pyproject_template/, tools/hooks/ai/):\nUTF-8 encoding hardening, new PyPI environment helper tasks,\nplaceholder marker tokens (upstream #464/#468), refreshed hooks.\n\nWorkflows (.github/): refreshed 7 workflows (dedupe, App-token\nready-to-merge, concurrency, codecov gating, python-versions\nextraction). Added composite action python-versions/action.yml,\nnew workflows ci-full-matrix.yml and dependabot-blocked-label.yml.\n\nPre-commit: added actionlint hook (upstream #415/#416).\n\nDocs: refreshed 11 template-owned development docs, updated ADR\nREADME as a two-series index (9XXX template-meta + 0001+ project),\nregenerated TABLE_OF_CONTENTS.md.\n\nADRs: added 16 template-meta ADRs (9001-9016) documenting\ninherited tooling decisions (uv, doit, ruff, mypy, pytest, mkdocs,\nconventional commits, merge gate, etc.). Project ADRs 0001-0016\nleft untouched.\n\nContributor instructions: renamed issue type doc → docs across\nAGENTS.md, .github/CONTRIBUTING.md, tools/doit/github.py,\ntools/doit/templates.py. Unblocks docs-typed PRs that were\nfailing the Validate PR Title Format check. Cache-schema\npitfalls and other project-specific content preserved.\n\nDependencies: bumped mkdocstrings[python] >=1.0.4, regenerated\nuv.lock. Ruff/pyproject-fmt/hypothesis bumps deferred to open\ndependabot PRs #623-#629.\n\nSettings pointer (.config/pyproject_template/settings.toml):\nbumped to 0cdab3e349b2bfd8007acb713b136b134bf0700e, 2026-04-22.\n\nDeleted tests/test_doit_github.py and tests/test_doit_release.py\nper upstream #463 strip-on-spawn behavior. bootstrap.py addition\nskipped per project memory.\n\nAddresses #667.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* fix: restore SOPS install tasks stripped by template sync\n\nThe template sync replaced tools/doit/install_tools.py with the\nupstream framework-only version, stripping this project's SOPS-\nspecific task_install_age / task_install_sops / task_install_tools\ndefinitions. CI on ubuntu-latest and windows-latest failed at the\n\"Install SOPS tools\" step with:\n\n  ERROR: Invalid parameter: \"install_tools\". Must be a command,\n  task, or a target.\n\nRestoring the tasks in a dedicated tools/doit/install_sops.py\nso future template refreshes do not overwrite them. The module\nimports create_install_task / get_install_dir /\nget_latest_github_release from the template-owned install_tools\nframework.\n\ndoit auto-discovery picks up the three tasks from any tools/doit/\nfile, so ci.yml's `uv run doit install_tools` invocation works\nunchanged.\n\nAddresses #667.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* docs: reference upstream issue #477 in install_sops.py\n\nPoints future readers to\nhttps://github.com/endavis/pyproject-template/issues/477, which\ntracks adding per-platform extract_binaries support to the\ninstall_tool framework. Once that lands, _install_age can collapse\nto a single create_install_task call.\n\nAddresses #667.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T19:22:04+01:00",
          "tree_id": "f2fe32dcc67102c487c80ee1a1bea9535deaa1e6",
          "url": "https://github.com/endavis/pynetappfoundry/commit/36c322f3902781b45079298f2d0e7faa69e90fe1"
        },
        "date": 1776968595602,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1114591.8362235911,
            "unit": "iter/sec",
            "range": "stddev: 3.2343366681490725e-7",
            "extra": "mean: 897.1894172382907 nsec\nrounds: 67903"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 724768.8415213726,
            "unit": "iter/sec",
            "range": "stddev: 4.6519215865379153e-7",
            "extra": "mean: 1.3797502634093457 usec\nrounds: 194553"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 425352.6965662378,
            "unit": "iter/sec",
            "range": "stddev: 6.333774387245801e-7",
            "extra": "mean: 2.350990150227661 usec\nrounds: 147211"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 442375.3184025443,
            "unit": "iter/sec",
            "range": "stddev: 5.734568316697132e-7",
            "extra": "mean: 2.26052394516739 usec\nrounds: 167758"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 499915.7975244451,
            "unit": "iter/sec",
            "range": "stddev: 5.406525699177118e-7",
            "extra": "mean: 2.000336866632228 usec\nrounds: 82359"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 157798.38024328038,
            "unit": "iter/sec",
            "range": "stddev: 9.42876690585413e-7",
            "extra": "mean: 6.337200663646126 usec\nrounds: 56358"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 138288.21727657955,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010635156837200027",
            "extra": "mean: 7.231274071600601 usec\nrounds: 70737"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 69553.01846875196,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014015653302360015",
            "extra": "mean: 14.377521235103108 usec\nrounds: 45891"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 231465.98012260924,
            "unit": "iter/sec",
            "range": "stddev: 9.80117418265649e-7",
            "extra": "mean: 4.320289311933843 usec\nrounds: 47015"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31480.457661588414,
            "unit": "iter/sec",
            "range": "stddev: 0.000002574757364999802",
            "extra": "mean: 31.76573894667905 usec\nrounds: 3076"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 83.52990524734024,
            "unit": "iter/sec",
            "range": "stddev: 0.0008146675963981116",
            "extra": "mean: 11.971760258064487 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 81.01544622572817,
            "unit": "iter/sec",
            "range": "stddev: 0.00103738128664532",
            "extra": "mean: 12.343325212500389 msec\nrounds: 80"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 91.48575344691861,
            "unit": "iter/sec",
            "range": "stddev: 0.00073828346471133",
            "extra": "mean: 10.93066365333281 msec\nrounds: 75"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 12.250585026923346,
            "unit": "iter/sec",
            "range": "stddev: 0.0009634832961499388",
            "extra": "mean: 81.62875469230904 msec\nrounds: 13"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 335.1694675425698,
            "unit": "iter/sec",
            "range": "stddev: 0.00008602163088227",
            "extra": "mean: 2.9835653209461572 msec\nrounds: 296"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 84.24270247083133,
            "unit": "iter/sec",
            "range": "stddev: 0.0007200700996885576",
            "extra": "mean: 11.870464392405331 msec\nrounds: 79"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.4064411589113832,
            "unit": "iter/sec",
            "range": "stddev: 0.1475826054451738",
            "extra": "mean: 711.0144592000012 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.352289440383876,
            "unit": "iter/sec",
            "range": "stddev: 0.14926057162816025",
            "extra": "mean: 739.4866588000042 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 411680.5147804233,
            "unit": "iter/sec",
            "range": "stddev: 7.154050848239209e-7",
            "extra": "mean: 2.4290680858028137 usec\nrounds: 11603"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 384312.7455138633,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013196183980095908",
            "extra": "mean: 2.60204745138729 usec\nrounds: 80103"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 388098.2969995254,
            "unit": "iter/sec",
            "range": "stddev: 7.538518319075378e-7",
            "extra": "mean: 2.576666807690792 usec\nrounds: 89840"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 172223.66927127694,
            "unit": "iter/sec",
            "range": "stddev: 8.830723715113946e-7",
            "extra": "mean: 5.806402826227426 usec\nrounds: 44441"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 202065.78686324478,
            "unit": "iter/sec",
            "range": "stddev: 8.019072201539487e-7",
            "extra": "mean: 4.948883309358974 usec\nrounds: 61196"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 436728.6945938012,
            "unit": "iter/sec",
            "range": "stddev: 6.055703428412255e-7",
            "extra": "mean: 2.2897510797409226 usec\nrounds: 102575"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 445035.57377182564,
            "unit": "iter/sec",
            "range": "stddev: 5.466991334937037e-7",
            "extra": "mean: 2.2470113827635503 usec\nrounds: 77310"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34413.025256509296,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024022709859002206",
            "extra": "mean: 29.058764597013973 usec\nrounds: 17281"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 566910.7578666434,
            "unit": "iter/sec",
            "range": "stddev: 4.7268980224670904e-7",
            "extra": "mean: 1.7639460640385907 usec\nrounds: 57661"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262319.7847038481,
            "unit": "iter/sec",
            "range": "stddev: 7.195246304141898e-7",
            "extra": "mean: 3.812140975675825 usec\nrounds: 84660"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 371457.48432655085,
            "unit": "iter/sec",
            "range": "stddev: 6.022297206990052e-7",
            "extra": "mean: 2.6920981328805134 usec\nrounds: 77018"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 226300.9514449565,
            "unit": "iter/sec",
            "range": "stddev: 7.663933284046113e-7",
            "extra": "mean: 4.418894368825628 usec\nrounds: 60787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 210550.67854735767,
            "unit": "iter/sec",
            "range": "stddev: 8.223756840563299e-7",
            "extra": "mean: 4.749450378879103 usec\nrounds: 82082"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52264.26661309554,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020141216002698786",
            "extra": "mean: 19.13353166137102 usec\nrounds: 25678"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26221.331099373325,
            "unit": "iter/sec",
            "range": "stddev: 0.00004448843497217277",
            "extra": "mean: 38.136889245256484 usec\nrounds: 14031"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35773.47449072354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027190181974519026",
            "extra": "mean: 27.953672776719273 usec\nrounds: 11020"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 334.69319742547276,
            "unit": "iter/sec",
            "range": "stddev: 0.00017875218556010364",
            "extra": "mean: 2.987810949526912 msec\nrounds: 317"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 34.06664508878836,
            "unit": "iter/sec",
            "range": "stddev: 0.0004106522670622652",
            "extra": "mean: 29.35422602941048 msec\nrounds: 34"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 29176.422184446186,
            "unit": "iter/sec",
            "range": "stddev: 0.000003323627567179073",
            "extra": "mean: 34.2742504093972 usec\nrounds: 16485"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 225.67527434204948,
            "unit": "iter/sec",
            "range": "stddev: 0.011602992345633419",
            "extra": "mean: 4.431145604743251 msec\nrounds: 253"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 15.516154469345542,
            "unit": "iter/sec",
            "range": "stddev: 0.0698885681600611",
            "extra": "mean: 64.44895879166761 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 15345.138180363034,
            "unit": "iter/sec",
            "range": "stddev: 0.0000073406987652837285",
            "extra": "mean: 65.16722027825638 usec\nrounds: 7259"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "49699333+dependabot[bot]@users.noreply.github.com",
            "name": "dependabot[bot]",
            "username": "dependabot[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bff2eb8110f5b9083c430d9d021157e9cf4df5db",
          "message": "chore(deps): Bump cryptography from 46.0.7 to 47.0.0 (merges PR #674)\n\nBumps [cryptography](https://github.com/pyca/cryptography) from 46.0.7 to 47.0.0.\n- [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst)\n- [Commits](https://github.com/pyca/cryptography/compare/46.0.7...47.0.0)\n\n---\nupdated-dependencies:\n- dependency-name: cryptography\n  dependency-version: 47.0.0\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-28T14:06:53+01:00",
          "tree_id": "146dc55dd46d30b9f262350cdf5e74475124c6ea",
          "url": "https://github.com/endavis/pynetappfoundry/commit/bff2eb8110f5b9083c430d9d021157e9cf4df5db"
        },
        "date": 1777381946252,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1108063.5487523025,
            "unit": "iter/sec",
            "range": "stddev: 3.7220719775053527e-7",
            "extra": "mean: 902.4753148192775 nsec\nrounds: 50739"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 504077.6184437156,
            "unit": "iter/sec",
            "range": "stddev: 9.547309599740518e-7",
            "extra": "mean: 1.9838214660023794 usec\nrounds: 53396"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 466370.2641148955,
            "unit": "iter/sec",
            "range": "stddev: 5.982133793838892e-7",
            "extra": "mean: 2.1442190399893057 usec\nrounds: 134391"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 466797.09941113763,
            "unit": "iter/sec",
            "range": "stddev: 5.485453175668039e-7",
            "extra": "mean: 2.1422583843419236 usec\nrounds: 101678"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 519331.71583444317,
            "unit": "iter/sec",
            "range": "stddev: 5.352346935045441e-7",
            "extra": "mean: 1.9255515685061457 usec\nrounds: 71119"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 159100.69213103564,
            "unit": "iter/sec",
            "range": "stddev: 9.101506155616431e-7",
            "extra": "mean: 6.285327779569922 usec\nrounds: 27009"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141320.70666073475,
            "unit": "iter/sec",
            "range": "stddev: 9.156897021130293e-7",
            "extra": "mean: 7.076103874860151 usec\nrounds: 67331"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 75397.78107043184,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013157757624192118",
            "extra": "mean: 13.262989783026415 usec\nrounds: 41989"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 225441.4995949901,
            "unit": "iter/sec",
            "range": "stddev: 7.553186851892928e-7",
            "extra": "mean: 4.435740543761991 usec\nrounds: 40053"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32937.66393105198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018087855955561765",
            "extra": "mean: 30.360380204658348 usec\nrounds: 2738"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 47.684241835703126,
            "unit": "iter/sec",
            "range": "stddev: 0.0026175291783970206",
            "extra": "mean: 20.971288658536654 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 45.296870445785856,
            "unit": "iter/sec",
            "range": "stddev: 0.001982330407578445",
            "extra": "mean: 22.076580350001507 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 53.181556651623424,
            "unit": "iter/sec",
            "range": "stddev: 0.0024783486766806295",
            "extra": "mean: 18.803511272727555 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.435687054860937,
            "unit": "iter/sec",
            "range": "stddev: 0.000827958260147074",
            "extra": "mean: 118.54398977778165 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 306.69595107854866,
            "unit": "iter/sec",
            "range": "stddev: 0.00006404358108314731",
            "extra": "mean: 3.2605582058821754 msec\nrounds: 170"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 56.90617679317815,
            "unit": "iter/sec",
            "range": "stddev: 0.0011393744635381283",
            "extra": "mean: 17.572784825001264 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.0734550989705129,
            "unit": "iter/sec",
            "range": "stddev: 0.2105418393778912",
            "extra": "mean: 13.613758799800001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07543284196517562,
            "unit": "iter/sec",
            "range": "stddev: 0.10213461573200995",
            "extra": "mean: 13.256825196400007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 417754.06773222267,
            "unit": "iter/sec",
            "range": "stddev: 4.940117162098951e-7",
            "extra": "mean: 2.393752873379542 usec\nrounds: 12095"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 392802.35045045946,
            "unit": "iter/sec",
            "range": "stddev: 5.161132039249954e-7",
            "extra": "mean: 2.5458096135453774 usec\nrounds: 65262"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 391836.4190787085,
            "unit": "iter/sec",
            "range": "stddev: 4.773971549057838e-7",
            "extra": "mean: 2.5520853889774067 usec\nrounds: 83348"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177214.87369237436,
            "unit": "iter/sec",
            "range": "stddev: 7.85953700991543e-7",
            "extra": "mean: 5.642867210660268 usec\nrounds: 43264"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 208113.75410305746,
            "unit": "iter/sec",
            "range": "stddev: 6.611166209484225e-7",
            "extra": "mean: 4.805064443289041 usec\nrounds: 60332"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 437305.10711936926,
            "unit": "iter/sec",
            "range": "stddev: 4.661341079581056e-7",
            "extra": "mean: 2.2867329553666393 usec\nrounds: 80979"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 447426.6145713148,
            "unit": "iter/sec",
            "range": "stddev: 4.6660362847353535e-7",
            "extra": "mean: 2.2350033892331433 usec\nrounds: 90286"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35862.61633314373,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021005451871695956",
            "extra": "mean: 27.88418978444174 usec\nrounds: 15486"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 576017.509263623,
            "unit": "iter/sec",
            "range": "stddev: 4.458865996606629e-7",
            "extra": "mean: 1.7360583383626538 usec\nrounds: 57955"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262296.60914308764,
            "unit": "iter/sec",
            "range": "stddev: 6.423760209822741e-7",
            "extra": "mean: 3.812477802389285 usec\nrounds: 61448"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 373977.1115666101,
            "unit": "iter/sec",
            "range": "stddev: 4.847750143133769e-7",
            "extra": "mean: 2.673960435201359 usec\nrounds: 56161"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 230065.7894702361,
            "unit": "iter/sec",
            "range": "stddev: 7.114955299629279e-7",
            "extra": "mean: 4.346582785309639 usec\nrounds: 40907"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209385.00793155876,
            "unit": "iter/sec",
            "range": "stddev: 6.76105021062721e-7",
            "extra": "mean: 4.775891119801986 usec\nrounds: 71069"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54165.64938582753,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014152844943392078",
            "extra": "mean: 18.461885186253312 usec\nrounds: 19867"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26988.23984216652,
            "unit": "iter/sec",
            "range": "stddev: 0.0000725531599167939",
            "extra": "mean: 37.05317597028304 usec\nrounds: 13991"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36207.16807853084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018910977850707564",
            "extra": "mean: 27.61884049675107 usec\nrounds: 9097"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 338.33925025977925,
            "unit": "iter/sec",
            "range": "stddev: 0.00007898847583200307",
            "extra": "mean: 2.955613335526969 msec\nrounds: 304"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.224513022716827,
            "unit": "iter/sec",
            "range": "stddev: 0.0008052306841520986",
            "extra": "mean: 32.02611996774676 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 975.2216147609238,
            "unit": "iter/sec",
            "range": "stddev: 0.0010830601361856013",
            "extra": "mean: 1.0254079532939295 msec\nrounds: 1199"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.878275055073164,
            "unit": "iter/sec",
            "range": "stddev: 0.0027426309136602766",
            "extra": "mean: 126.93133877777679 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7851762198290769,
            "unit": "iter/sec",
            "range": "stddev: 0.1179975731156025",
            "extra": "mean: 1.2735994477999952 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 946.6241375730007,
            "unit": "iter/sec",
            "range": "stddev: 0.001048562738760636",
            "extra": "mean: 1.056385486391512 msec\nrounds: 1139"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d4973b8bb9a495f878a630a74469fb0d11069d50",
          "message": "feat: validate where expressions before query execution (merges PR #682, addresses #618)\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-05T16:11:51+01:00",
          "tree_id": "b5b07591f2304bd6b5fc203c9d3cc242849b487f",
          "url": "https://github.com/endavis/pynetappfoundry/commit/d4973b8bb9a495f878a630a74469fb0d11069d50"
        },
        "date": 1777994255428,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1202998.2036865363,
            "unit": "iter/sec",
            "range": "stddev: 2.7730671571658504e-7",
            "extra": "mean: 831.2564365728418 nsec\nrounds: 50687"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 746318.985233784,
            "unit": "iter/sec",
            "range": "stddev: 5.046956233231054e-7",
            "extra": "mean: 1.3399096362083711 usec\nrounds: 181555"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 477469.494725125,
            "unit": "iter/sec",
            "range": "stddev: 5.227229670045067e-7",
            "extra": "mean: 2.094374637641911 usec\nrounds: 164204"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 475718.02697111364,
            "unit": "iter/sec",
            "range": "stddev: 5.572017057693868e-7",
            "extra": "mean: 2.1020855702420578 usec\nrounds: 126551"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 516656.28993886494,
            "unit": "iter/sec",
            "range": "stddev: 4.818850099867774e-7",
            "extra": "mean: 1.93552274398581 usec\nrounds: 72041"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 164887.92958429342,
            "unit": "iter/sec",
            "range": "stddev: 9.278346858528746e-7",
            "extra": "mean: 6.064725310828671 usec\nrounds: 54771"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 144018.57640468894,
            "unit": "iter/sec",
            "range": "stddev: 9.929097651673741e-7",
            "extra": "mean: 6.9435487071474915 usec\nrounds: 67331"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 78637.40846018643,
            "unit": "iter/sec",
            "range": "stddev: 0.000001672967050158036",
            "extra": "mean: 12.716594043231892 usec\nrounds: 44655"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 240606.7814615903,
            "unit": "iter/sec",
            "range": "stddev: 7.038029647820741e-7",
            "extra": "mean: 4.156158832786834 usec\nrounds: 40508"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32537.074585716535,
            "unit": "iter/sec",
            "range": "stddev: 0.000002211431768566947",
            "extra": "mean: 30.73417056489124 usec\nrounds: 2779"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 49.4647957388137,
            "unit": "iter/sec",
            "range": "stddev: 0.0017954381557863028",
            "extra": "mean: 20.216398047618476 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 50.139816345389676,
            "unit": "iter/sec",
            "range": "stddev: 0.002045770956067758",
            "extra": "mean: 19.944229414632655 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 77.51914091252306,
            "unit": "iter/sec",
            "range": "stddev: 0.001059606947593027",
            "extra": "mean: 12.90003976086959 msec\nrounds: 46"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.476155406074792,
            "unit": "iter/sec",
            "range": "stddev: 0.0012603836798925285",
            "extra": "mean: 117.97801622222595 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 292.6748451691527,
            "unit": "iter/sec",
            "range": "stddev: 0.0003122423310049274",
            "extra": "mean: 3.4167610114290676 msec\nrounds: 175"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 65.6619120586047,
            "unit": "iter/sec",
            "range": "stddev: 0.0016653155215679422",
            "extra": "mean: 15.229529093022421 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07129310122988654,
            "unit": "iter/sec",
            "range": "stddev: 0.3141994168668526",
            "extra": "mean: 14.026602613 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07451103357464275,
            "unit": "iter/sec",
            "range": "stddev: 0.21102986510983532",
            "extra": "mean: 13.420831144400006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 403568.4865248838,
            "unit": "iter/sec",
            "range": "stddev: 5.291976046025706e-7",
            "extra": "mean: 2.477894170109689 usec\nrounds: 11509"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 385514.0209528876,
            "unit": "iter/sec",
            "range": "stddev: 5.559936489969856e-7",
            "extra": "mean: 2.593939378724196 usec\nrounds: 48168"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 383163.39053135476,
            "unit": "iter/sec",
            "range": "stddev: 5.761517339537722e-7",
            "extra": "mean: 2.609852675677711 usec\nrounds: 62135"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 173558.00714940345,
            "unit": "iter/sec",
            "range": "stddev: 7.306952175943111e-7",
            "extra": "mean: 5.761762401081113 usec\nrounds: 36469"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 205825.6751761196,
            "unit": "iter/sec",
            "range": "stddev: 7.313915181402075e-7",
            "extra": "mean: 4.858480357925834 usec\nrounds: 41467"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 416288.01472937345,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014263006360462266",
            "extra": "mean: 2.4021830190093136 usec\nrounds: 60043"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 430681.2542428668,
            "unit": "iter/sec",
            "range": "stddev: 4.784727366023498e-7",
            "extra": "mean: 2.3219027764697806 usec\nrounds: 67422"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35751.272508788585,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020955699810624612",
            "extra": "mean: 27.971032352881263 usec\nrounds: 14682"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 597269.0887843375,
            "unit": "iter/sec",
            "range": "stddev: 4.0133321304438433e-7",
            "extra": "mean: 1.6742872162283973 usec\nrounds: 55164"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263193.45560504467,
            "unit": "iter/sec",
            "range": "stddev: 6.345257833507348e-7",
            "extra": "mean: 3.799486570443558 usec\nrounds: 55289"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 361946.0420942333,
            "unit": "iter/sec",
            "range": "stddev: 5.37719783306956e-7",
            "extra": "mean: 2.7628427547210155 usec\nrounds: 51709"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 230255.0768550125,
            "unit": "iter/sec",
            "range": "stddev: 7.606436806745052e-7",
            "extra": "mean: 4.3430095599137735 usec\nrounds: 46549"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 205144.5352020511,
            "unit": "iter/sec",
            "range": "stddev: 6.639335656903312e-7",
            "extra": "mean: 4.874611936482146 usec\nrounds: 62799"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53025.19641697545,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015078566941858558",
            "extra": "mean: 18.85895890203361 usec\nrounds: 20512"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26481.510127608988,
            "unit": "iter/sec",
            "range": "stddev: 0.00006691390227285229",
            "extra": "mean: 37.76219691328796 usec\nrounds: 13087"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36670.09463807649,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018366775682183014",
            "extra": "mean: 27.270177780278956 usec\nrounds: 9028"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 341.9105656053709,
            "unit": "iter/sec",
            "range": "stddev: 0.00003403824948616155",
            "extra": "mean: 2.924741440000389 msec\nrounds: 300"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.88015148155104,
            "unit": "iter/sec",
            "range": "stddev: 0.0007481547016643131",
            "extra": "mean: 32.38326083333618 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 968.6992601845539,
            "unit": "iter/sec",
            "range": "stddev: 0.0011052627695848703",
            "extra": "mean: 1.0323121334989798 msec\nrounds: 1206"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.671075571325032,
            "unit": "iter/sec",
            "range": "stddev: 0.0027379881003430423",
            "extra": "mean: 130.3598159999966 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7596701057874777,
            "unit": "iter/sec",
            "range": "stddev: 0.13222325827668327",
            "extra": "mean: 1.3163608682000132 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 917.0913722670729,
            "unit": "iter/sec",
            "range": "stddev: 0.0011033892920540233",
            "extra": "mean: 1.0904038902121334 msec\nrounds: 1175"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e7a91ed1fd62add94ade0ee3e39afe8287b60f93",
          "message": "fix: QueryBuilder.filter() leaves partial state on early-validation rejection (merges PR #684, addresses #683)\n\nfix: address review feedback for early where validation\n\n- Hoist filter() validation above state mutation so a rejected call\n  leaves the QueryBuilder in its prior state instead of with partially\n  applied equality filters.\n- Switch _validate_where_expressions to a class-attribute lookup\n  against _BACKENDS, avoiding eager backend instantiation at chain\n  time and removing the type(backend).__name__ fragility in error\n  messages.\n- Add ModelRegistry.unregister_mapping() and use it in the new DII\n  test fixture instead of poking the private _mappings indexes.\n- Make the codegen tomli ignore portable across mypy environments\n  via unused-ignore so doit check passes whether or not tomli is\n  installed.\n\nAddresses #683.",
          "timestamp": "2026-05-05T16:53:53+01:00",
          "tree_id": "f273b741748cd1ac46ffdee9546ddd9260542d23",
          "url": "https://github.com/endavis/pynetappfoundry/commit/e7a91ed1fd62add94ade0ee3e39afe8287b60f93"
        },
        "date": 1777996831108,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1180577.137578954,
            "unit": "iter/sec",
            "range": "stddev: 2.8806384983250955e-7",
            "extra": "mean: 847.0433385240129 nsec\nrounds: 125708"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 739731.6431731152,
            "unit": "iter/sec",
            "range": "stddev: 4.2806425960436666e-7",
            "extra": "mean: 1.3518415890801305 usec\nrounds: 190877"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 471979.34448689147,
            "unit": "iter/sec",
            "range": "stddev: 5.27998467235683e-7",
            "extra": "mean: 2.118736787278566 usec\nrounds: 161265"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 468138.84640932817,
            "unit": "iter/sec",
            "range": "stddev: 5.047905802537811e-7",
            "extra": "mean: 2.136118392374613 usec\nrounds: 166058"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 507770.9507080355,
            "unit": "iter/sec",
            "range": "stddev: 5.14624253909285e-7",
            "extra": "mean: 1.969391905160389 usec\nrounds: 64189"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 163314.93304560165,
            "unit": "iter/sec",
            "range": "stddev: 8.892720497000043e-7",
            "extra": "mean: 6.123138780706445 usec\nrounds: 60347"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 140903.85242268714,
            "unit": "iter/sec",
            "range": "stddev: 9.42040917896276e-7",
            "extra": "mean: 7.097038035554722 usec\nrounds: 71144"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74906.62939211297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018159267176509612",
            "extra": "mean: 13.349953243327906 usec\nrounds: 38155"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 234405.4469155017,
            "unit": "iter/sec",
            "range": "stddev: 7.768791511420712e-7",
            "extra": "mean: 4.266112469478917 usec\nrounds: 51534"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31773.558611718265,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028087894417376694",
            "extra": "mean: 31.47271013046661 usec\nrounds: 2991"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 77.02961939073461,
            "unit": "iter/sec",
            "range": "stddev: 0.0014322669229969113",
            "extra": "mean: 12.982019227272511 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 76.29678318011258,
            "unit": "iter/sec",
            "range": "stddev: 0.0015626029241843323",
            "extra": "mean: 13.106712476190722 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 85.06272629402552,
            "unit": "iter/sec",
            "range": "stddev: 0.0014160081089313649",
            "extra": "mean: 11.75603044444434 msec\nrounds: 45"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.493922404916798,
            "unit": "iter/sec",
            "range": "stddev: 0.0011917837772053963",
            "extra": "mean: 105.33054277777865 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 304.7115748297007,
            "unit": "iter/sec",
            "range": "stddev: 0.00009056766963280343",
            "extra": "mean: 3.281791971830696 msec\nrounds: 213"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 79.13835921906856,
            "unit": "iter/sec",
            "range": "stddev: 0.0011414699910086005",
            "extra": "mean: 12.636097208331401 msec\nrounds: 48"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.0614676980513077,
            "unit": "iter/sec",
            "range": "stddev: 0.14975732229197875",
            "extra": "mean: 16.268707495199997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06605660638836859,
            "unit": "iter/sec",
            "range": "stddev: 0.14484705059874795",
            "extra": "mean: 15.138531248800007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 423798.8255837565,
            "unit": "iter/sec",
            "range": "stddev: 5.46338256627273e-7",
            "extra": "mean: 2.3596101254470496 usec\nrounds: 12740"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 404551.0492583041,
            "unit": "iter/sec",
            "range": "stddev: 5.804909314538368e-7",
            "extra": "mean: 2.4718759272368227 usec\nrounds: 86949"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 396154.9772746027,
            "unit": "iter/sec",
            "range": "stddev: 5.297797022909343e-7",
            "extra": "mean: 2.52426463723774 usec\nrounds: 106304"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176005.56747266502,
            "unit": "iter/sec",
            "range": "stddev: 8.044832065647201e-7",
            "extra": "mean: 5.681638452461496 usec\nrounds: 49266"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 207716.04794443204,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010087115595489236",
            "extra": "mean: 4.814264520705299 usec\nrounds: 66543"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 446086.5173742109,
            "unit": "iter/sec",
            "range": "stddev: 5.212978162910418e-7",
            "extra": "mean: 2.2417176064550834 usec\nrounds: 107205"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 451174.01318478683,
            "unit": "iter/sec",
            "range": "stddev: 5.026288729507688e-7",
            "extra": "mean: 2.2164397123431643 usec\nrounds: 98146"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35616.87704040923,
            "unit": "iter/sec",
            "range": "stddev: 0.000002408033610507973",
            "extra": "mean: 28.076577260421995 usec\nrounds: 15286"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 598011.5726029463,
            "unit": "iter/sec",
            "range": "stddev: 4.241721912925847e-7",
            "extra": "mean: 1.672208441798762 usec\nrounds: 66455"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262306.4403898792,
            "unit": "iter/sec",
            "range": "stddev: 6.578849128466979e-7",
            "extra": "mean: 3.8123349107008195 usec\nrounds: 91075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 390192.2601352506,
            "unit": "iter/sec",
            "range": "stddev: 5.275534906891634e-7",
            "extra": "mean: 2.562839149227036 usec\nrounds: 79981"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 240746.63902821537,
            "unit": "iter/sec",
            "range": "stddev: 7.371635542258172e-7",
            "extra": "mean: 4.153744384704787 usec\nrounds: 45412"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209427.23212007183,
            "unit": "iter/sec",
            "range": "stddev: 7.595726038187673e-7",
            "extra": "mean: 4.774928216721432 usec\nrounds: 84797"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54581.92387089412,
            "unit": "iter/sec",
            "range": "stddev: 0.000001782457657857886",
            "extra": "mean: 18.32108377794377 usec\nrounds: 25496"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26484.63741322381,
            "unit": "iter/sec",
            "range": "stddev: 0.00006476361601361368",
            "extra": "mean: 37.757737982121625 usec\nrounds: 15789"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36006.07740092426,
            "unit": "iter/sec",
            "range": "stddev: 0.000002487401419313171",
            "extra": "mean: 27.77308921672013 usec\nrounds: 7734"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 338.71326112267354,
            "unit": "iter/sec",
            "range": "stddev: 0.000033562731063690956",
            "extra": "mean: 2.9523497151705103 msec\nrounds: 323"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 34.12258708368057,
            "unit": "iter/sec",
            "range": "stddev: 0.00012366264203108826",
            "extra": "mean: 29.306101484850743 msec\nrounds: 33"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 821.1285863639216,
            "unit": "iter/sec",
            "range": "stddev: 0.0011360979385529777",
            "extra": "mean: 1.2178360571127447 msec\nrounds: 928"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.731962322211087,
            "unit": "iter/sec",
            "range": "stddev: 0.0027798150919698754",
            "extra": "mean: 148.54509757142458 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6640008435169232,
            "unit": "iter/sec",
            "range": "stddev: 0.1016732575459304",
            "extra": "mean: 1.5060221832000025 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 788.2223382566524,
            "unit": "iter/sec",
            "range": "stddev: 0.0011300655892295074",
            "extra": "mean: 1.268677569087608 msec\nrounds: 977"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "93281e4f672f04c29eb52f5d2204c4f50209d16a",
          "message": "fix: correct nf events get EMS field mapping (merges PR #685, addresses #108)\n\n- Default --output to ems_output.csv (matches sysadmin script behaviour)\n- Remove console/Rich table output path; always write CSV\n- Add fields=\"*\" to API query so log_message, node, message.severity are returned\n- Replace .to_dict() with direct bracket access (matches azevents.py pattern)\n- Fix severity: event[\"message\"][\"severity\"] (was top-level, doesn't exist)\n- Fix message: event[\"log_message\"] (was message.text, doesn't exist)\n- Add node column to CSV output (cluster, node, time, name, severity, message)\n- Remove output_to_file parameter from _get_cluster_events\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T11:54:05+01:00",
          "tree_id": "f2dd0a9db8b76a4bddd48507318b35ed44ddcaf7",
          "url": "https://github.com/endavis/pynetappfoundry/commit/93281e4f672f04c29eb52f5d2204c4f50209d16a"
        },
        "date": 1778065240594,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1170314.7791792287,
            "unit": "iter/sec",
            "range": "stddev: 2.6652969912800225e-7",
            "extra": "mean: 854.4709660945452 nsec\nrounds: 68644"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 737358.3425756228,
            "unit": "iter/sec",
            "range": "stddev: 5.059352497296106e-7",
            "extra": "mean: 1.3561926979858385 usec\nrounds: 194932"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 463846.42448380834,
            "unit": "iter/sec",
            "range": "stddev: 4.97143246344138e-7",
            "extra": "mean: 2.1558859726316753 usec\nrounds: 163908"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 445963.8148660615,
            "unit": "iter/sec",
            "range": "stddev: 7.074689633801723e-7",
            "extra": "mean: 2.2423343927586026 usec\nrounds: 171792"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 392407.79058830335,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013224219760186982",
            "extra": "mean: 2.5483693850746074 usec\nrounds: 86866"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 153121.84698129902,
            "unit": "iter/sec",
            "range": "stddev: 0.000002008822753859628",
            "extra": "mean: 6.530746720434553 usec\nrounds: 55267"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 129906.75549663688,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023119239748587616",
            "extra": "mean: 7.6978290788417745 usec\nrounds: 68985"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 73022.33201210886,
            "unit": "iter/sec",
            "range": "stddev: 0.000002562016959824839",
            "extra": "mean: 13.694440761412219 usec\nrounds: 45494"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232434.593983185,
            "unit": "iter/sec",
            "range": "stddev: 7.56821540854646e-7",
            "extra": "mean: 4.302285571451308 usec\nrounds: 45999"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31626.1232760704,
            "unit": "iter/sec",
            "range": "stddev: 0.00000232906595575003",
            "extra": "mean: 31.619430281442064 usec\nrounds: 3091"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 70.53857432717679,
            "unit": "iter/sec",
            "range": "stddev: 0.0013909523346930085",
            "extra": "mean: 14.176640363636105 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 65.88601268269281,
            "unit": "iter/sec",
            "range": "stddev: 0.0016283448143070028",
            "extra": "mean: 15.177728311106067 msec\nrounds: 45"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 71.57299539977281,
            "unit": "iter/sec",
            "range": "stddev: 0.0014808335621162537",
            "extra": "mean: 13.97175002128211 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.092381321946364,
            "unit": "iter/sec",
            "range": "stddev: 0.0009796029475872925",
            "extra": "mean: 109.98218888887676 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 301.80924020858583,
            "unit": "iter/sec",
            "range": "stddev: 0.00012444627978120694",
            "extra": "mean: 3.3133511727768235 msec\nrounds: 191"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 69.79897464875626,
            "unit": "iter/sec",
            "range": "stddev: 0.00228445543684208",
            "extra": "mean: 14.3268580238065 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.060803533965719365,
            "unit": "iter/sec",
            "range": "stddev: 0.187708285741466",
            "extra": "mean: 16.4464124826 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06512676879051071,
            "unit": "iter/sec",
            "range": "stddev: 0.24171463007058616",
            "extra": "mean: 15.354669340600003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 437226.27261253557,
            "unit": "iter/sec",
            "range": "stddev: 5.039951336937485e-7",
            "extra": "mean: 2.287145266968409 usec\nrounds: 9424"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 415004.2040166367,
            "unit": "iter/sec",
            "range": "stddev: 5.445307758631984e-7",
            "extra": "mean: 2.4096141444386716 usec\nrounds: 85602"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 406201.71003616037,
            "unit": "iter/sec",
            "range": "stddev: 5.126317922412464e-7",
            "extra": "mean: 2.461831093500269 usec\nrounds: 32219"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 180431.2244666086,
            "unit": "iter/sec",
            "range": "stddev: 8.805025900784989e-7",
            "extra": "mean: 5.542277967442739 usec\nrounds: 46340"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 212661.0580796775,
            "unit": "iter/sec",
            "range": "stddev: 7.26938965143474e-7",
            "extra": "mean: 4.702318370039008 usec\nrounds: 61573"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 462474.2896170681,
            "unit": "iter/sec",
            "range": "stddev: 5.263787008242988e-7",
            "extra": "mean: 2.162282363475831 usec\nrounds: 94697"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 471102.37827267253,
            "unit": "iter/sec",
            "range": "stddev: 4.658742306144018e-7",
            "extra": "mean: 2.1226808569011366 usec\nrounds: 86491"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 36339.99018205792,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021498955218039458",
            "extra": "mean: 27.51789406078949 usec\nrounds: 17189"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 592033.0097190929,
            "unit": "iter/sec",
            "range": "stddev: 4.318560677861309e-7",
            "extra": "mean: 1.6890950058248928 usec\nrounds: 68743"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 265551.78710055473,
            "unit": "iter/sec",
            "range": "stddev: 6.54716444871356e-7",
            "extra": "mean: 3.7657438156171645 usec\nrounds: 77979"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 387767.3570881184,
            "unit": "iter/sec",
            "range": "stddev: 5.426624635674757e-7",
            "extra": "mean: 2.5788658630508565 usec\nrounds: 74767"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 237397.88602521786,
            "unit": "iter/sec",
            "range": "stddev: 7.113381424152581e-7",
            "extra": "mean: 4.212337425337367 usec\nrounds: 57598"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 211684.01726173374,
            "unit": "iter/sec",
            "range": "stddev: 8.124706720951821e-7",
            "extra": "mean: 4.724022214504575 usec\nrounds: 78778"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54149.48239262173,
            "unit": "iter/sec",
            "range": "stddev: 0.00000163596477898885",
            "extra": "mean: 18.46739720888371 usec\nrounds: 24652"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 27013.8678689542,
            "unit": "iter/sec",
            "range": "stddev: 0.00006262889038609557",
            "extra": "mean: 37.01802366292219 usec\nrounds: 15594"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35870.61453981317,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025149496493378436",
            "extra": "mean: 27.877972341123105 usec\nrounds: 10449"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 335.3906531036324,
            "unit": "iter/sec",
            "range": "stddev: 0.000032805303543833496",
            "extra": "mean: 2.9815977003122085 msec\nrounds: 317"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 33.34328085300183,
            "unit": "iter/sec",
            "range": "stddev: 0.00039736672155231276",
            "extra": "mean: 29.991049903236263 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 817.9326219204742,
            "unit": "iter/sec",
            "range": "stddev: 0.0011576287878844803",
            "extra": "mean: 1.2225945917795022 msec\nrounds: 1046"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.775054426141006,
            "unit": "iter/sec",
            "range": "stddev: 0.0025719015175991256",
            "extra": "mean: 147.6002902857252 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6719178280360553,
            "unit": "iter/sec",
            "range": "stddev: 0.08998056943246846",
            "extra": "mean: 1.4882772242000102 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 793.6425396386068,
            "unit": "iter/sec",
            "range": "stddev: 0.0011404974492946842",
            "extra": "mean: 1.2600131042060323 msec\nrounds: 1046"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "eb2489f41d348d1cb16ffa136bde127d38761b6f",
          "message": "fix: use message.severity filter and default to wildcard (merges PR #686)\n\n- Change severity API param key from 'severity' to 'message.severity'\n  (matches ONTAP EMS API and sysadmin script pattern)\n- Default message.severity to '*' when no --severity given so debug\n  events are included, matching sysadmin get_event.py behaviour\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T12:39:25+01:00",
          "tree_id": "b3ab5f8b9686fb92b43df2461dfcfa2690f23b1a",
          "url": "https://github.com/endavis/pynetappfoundry/commit/eb2489f41d348d1cb16ffa136bde127d38761b6f"
        },
        "date": 1778067970510,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1148062.2225480562,
            "unit": "iter/sec",
            "range": "stddev: 3.2012899796540946e-7",
            "extra": "mean: 871.0329286687607 nsec\nrounds: 57731"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 741122.0038435844,
            "unit": "iter/sec",
            "range": "stddev: 4.142995360588182e-7",
            "extra": "mean: 1.3493055054550134 usec\nrounds: 194553"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 469422.8460731993,
            "unit": "iter/sec",
            "range": "stddev: 5.143173588766582e-7",
            "extra": "mean: 2.130275525286354 usec\nrounds: 168039"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 465613.9034859372,
            "unit": "iter/sec",
            "range": "stddev: 5.32292571023242e-7",
            "extra": "mean: 2.147702189546414 usec\nrounds: 158705"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 506537.66917229764,
            "unit": "iter/sec",
            "range": "stddev: 5.956070672490982e-7",
            "extra": "mean: 1.9741868391230195 usec\nrounds: 82563"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 160801.18720126478,
            "unit": "iter/sec",
            "range": "stddev: 8.471531401608033e-7",
            "extra": "mean: 6.218859558221809 usec\nrounds: 57134"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141079.69356468908,
            "unit": "iter/sec",
            "range": "stddev: 9.205381118578251e-7",
            "extra": "mean: 7.088192316929519 usec\nrounds: 70493"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74856.20071482948,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012811308306608686",
            "extra": "mean: 13.358946759929452 usec\nrounds: 46018"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232851.5426128037,
            "unit": "iter/sec",
            "range": "stddev: 7.879902144601755e-7",
            "extra": "mean: 4.294581812854237 usec\nrounds: 44779"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30762.004216388617,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027860158079863944",
            "extra": "mean: 32.507634839580604 usec\nrounds: 2922"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 48.673843731768365,
            "unit": "iter/sec",
            "range": "stddev: 0.0014577256288696692",
            "extra": "mean: 20.544915365854322 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 58.33643663730936,
            "unit": "iter/sec",
            "range": "stddev: 0.002260412221199254",
            "extra": "mean: 17.141945199999498 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 51.42559522233293,
            "unit": "iter/sec",
            "range": "stddev: 0.0014306992740262074",
            "extra": "mean: 19.44556977272911 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.597490512884702,
            "unit": "iter/sec",
            "range": "stddev: 0.0006445739165901279",
            "extra": "mean: 116.31300999999263 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 297.47408999023725,
            "unit": "iter/sec",
            "range": "stddev: 0.00020927951021178624",
            "extra": "mean: 3.361637311111091 msec\nrounds: 180"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 49.7882410886305,
            "unit": "iter/sec",
            "range": "stddev: 0.0018241872034398304",
            "extra": "mean: 20.08506382500741 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.05853513473957843,
            "unit": "iter/sec",
            "range": "stddev: 0.419825749290076",
            "extra": "mean: 17.083756694999998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06519893203246972,
            "unit": "iter/sec",
            "range": "stddev: 0.14214723544235014",
            "extra": "mean: 15.337674542000013 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 428310.2209039919,
            "unit": "iter/sec",
            "range": "stddev: 5.355928297039204e-7",
            "extra": "mean: 2.334756331262418 usec\nrounds: 11688"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 408987.16470514523,
            "unit": "iter/sec",
            "range": "stddev: 5.344000849127156e-7",
            "extra": "mean: 2.445064506415352 usec\nrounds: 81480"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 404936.09911320196,
            "unit": "iter/sec",
            "range": "stddev: 5.284214559847171e-7",
            "extra": "mean: 2.469525444113208 usec\nrounds: 96722"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176139.2391976858,
            "unit": "iter/sec",
            "range": "stddev: 8.804486082002672e-7",
            "extra": "mean: 5.6773266681234675 usec\nrounds: 47461"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 207362.5944200358,
            "unit": "iter/sec",
            "range": "stddev: 7.695865276555122e-7",
            "extra": "mean: 4.8224705270343495 usec\nrounds: 62345"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 453153.4822589046,
            "unit": "iter/sec",
            "range": "stddev: 4.940851902412333e-7",
            "extra": "mean: 2.206757840666135 usec\nrounds: 95239"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 457463.15167888784,
            "unit": "iter/sec",
            "range": "stddev: 5.072196006326308e-7",
            "extra": "mean: 2.185968413696282 usec\nrounds: 90736"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35461.14347337909,
            "unit": "iter/sec",
            "range": "stddev: 0.000002226132153118363",
            "extra": "mean: 28.199880264738404 usec\nrounds: 16620"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 600354.7283938541,
            "unit": "iter/sec",
            "range": "stddev: 4.0087474638795017e-7",
            "extra": "mean: 1.6656818922294958 usec\nrounds: 59659"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262324.91227791895,
            "unit": "iter/sec",
            "range": "stddev: 6.336904828671032e-7",
            "extra": "mean: 3.812066461078445 usec\nrounds: 74600"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 385891.8533159059,
            "unit": "iter/sec",
            "range": "stddev: 5.094405897724954e-7",
            "extra": "mean: 2.5913996147033496 usec\nrounds: 75330"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 233481.42839646208,
            "unit": "iter/sec",
            "range": "stddev: 7.16578105281204e-7",
            "extra": "mean: 4.282995897652101 usec\nrounds: 46318"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 206766.3630583188,
            "unit": "iter/sec",
            "range": "stddev: 7.658297010666606e-7",
            "extra": "mean: 4.836376600182054 usec\nrounds: 77018"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53478.811420682665,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017490184180499354",
            "extra": "mean: 18.698994488371422 usec\nrounds: 24671"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26426.31250745556,
            "unit": "iter/sec",
            "range": "stddev: 0.00006741292181577673",
            "extra": "mean: 37.84107221610558 usec\nrounds: 15149"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35876.10549646126,
            "unit": "iter/sec",
            "range": "stddev: 0.000002617979495407616",
            "extra": "mean: 27.873705525217552 usec\nrounds: 9882"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 337.0531670400645,
            "unit": "iter/sec",
            "range": "stddev: 0.000027658096520499924",
            "extra": "mean: 2.9668909768206775 msec\nrounds: 302"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.78485816730891,
            "unit": "iter/sec",
            "range": "stddev: 0.0008932926552403143",
            "extra": "mean: 30.501885806452556 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 803.7421652370062,
            "unit": "iter/sec",
            "range": "stddev: 0.0011784387169482904",
            "extra": "mean: 1.244180090645265 msec\nrounds: 1026"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.603813039574536,
            "unit": "iter/sec",
            "range": "stddev: 0.0027839838644892296",
            "extra": "mean: 151.42766671426347 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6583463787433309,
            "unit": "iter/sec",
            "range": "stddev: 0.1083410482660321",
            "extra": "mean: 1.5189572424000062 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 782.6251170663851,
            "unit": "iter/sec",
            "range": "stddev: 0.0011631381500552419",
            "extra": "mean: 1.2777509668338136 msec\nrounds: 995"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "18d724a239c52ffdc6365549765ea8611d86ae0b",
          "message": "fix: use bracket access for HA detection in azevents (merges PR #687, addresses #92)\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T14:49:48+01:00",
          "tree_id": "05418bf6db711777a53c2c325f906c84a1c327bd",
          "url": "https://github.com/endavis/pynetappfoundry/commit/18d724a239c52ffdc6365549765ea8611d86ae0b"
        },
        "date": 1778075824272,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1167812.6023508355,
            "unit": "iter/sec",
            "range": "stddev: 3.2724626655650936e-7",
            "extra": "mean: 856.3017713518209 nsec\nrounds: 51317"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 727552.0603705834,
            "unit": "iter/sec",
            "range": "stddev: 4.779685834735034e-7",
            "extra": "mean: 1.3744720886236559 usec\nrounds: 185874"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 467869.6706954972,
            "unit": "iter/sec",
            "range": "stddev: 5.95332924768674e-7",
            "extra": "mean: 2.1373473482764567 usec\nrounds: 140588"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 469771.7555948957,
            "unit": "iter/sec",
            "range": "stddev: 5.527525472639695e-7",
            "extra": "mean: 2.128693324130672 usec\nrounds: 154991"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 506551.35245954397,
            "unit": "iter/sec",
            "range": "stddev: 5.979917961620866e-7",
            "extra": "mean: 1.974133511132745 usec\nrounds: 76488"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162142.5269087819,
            "unit": "iter/sec",
            "range": "stddev: 9.909358781724274e-7",
            "extra": "mean: 6.16741344214143 usec\nrounds: 53548"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 142722.14723765457,
            "unit": "iter/sec",
            "range": "stddev: 0.000001063751731391595",
            "extra": "mean: 7.006621042036626 usec\nrounds: 68691"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74532.99907841354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014798215836248033",
            "extra": "mean: 13.416875912210848 usec\nrounds: 33573"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232255.11669721047,
            "unit": "iter/sec",
            "range": "stddev: 9.120655192419144e-7",
            "extra": "mean: 4.305610202352156 usec\nrounds: 44441"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31196.614003301067,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030265345642463555",
            "extra": "mean: 32.05476081135552 usec\nrounds: 2613"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 40.534983605856915,
            "unit": "iter/sec",
            "range": "stddev: 0.0009393228573139479",
            "extra": "mean: 24.670048216215626 msec\nrounds: 37"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 38.790745803319865,
            "unit": "iter/sec",
            "range": "stddev: 0.0006518508935297166",
            "extra": "mean: 25.779344513515802 msec\nrounds: 37"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 42.08658030256699,
            "unit": "iter/sec",
            "range": "stddev: 0.001235519356100157",
            "extra": "mean: 23.76054297618965 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.007613198210224,
            "unit": "iter/sec",
            "range": "stddev: 0.001777186024602673",
            "extra": "mean: 124.88115687499857 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 172.07321953965518,
            "unit": "iter/sec",
            "range": "stddev: 0.00022391115138169397",
            "extra": "mean: 5.811479570587942 msec\nrounds: 170"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 38.49646507867347,
            "unit": "iter/sec",
            "range": "stddev: 0.0004125503474119682",
            "extra": "mean: 25.976411027774777 msec\nrounds: 36"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.05444913928853181,
            "unit": "iter/sec",
            "range": "stddev: 0.6263374366741524",
            "extra": "mean: 18.365763225400002 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.05916302940236506,
            "unit": "iter/sec",
            "range": "stddev: 0.17201551289158365",
            "extra": "mean: 16.902447526799982 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 426030.1026726853,
            "unit": "iter/sec",
            "range": "stddev: 5.380395999099634e-7",
            "extra": "mean: 2.347251975216151 usec\nrounds: 10378"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 403747.48557878565,
            "unit": "iter/sec",
            "range": "stddev: 5.461490218639779e-7",
            "extra": "mean: 2.4767956104208704 usec\nrounds: 70938"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 398140.09973922337,
            "unit": "iter/sec",
            "range": "stddev: 5.947874777433736e-7",
            "extra": "mean: 2.5116786795778347 usec\nrounds: 90819"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176047.7052461378,
            "unit": "iter/sec",
            "range": "stddev: 8.864169793810751e-7",
            "extra": "mean: 5.680278527924398 usec\nrounds: 47690"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 201546.39947064628,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012543443141087309",
            "extra": "mean: 4.961636638642322 usec\nrounds: 62819"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 451724.84743943485,
            "unit": "iter/sec",
            "range": "stddev: 5.033266581701181e-7",
            "extra": "mean: 2.2137369809706455 usec\nrounds: 96628"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 461224.3600039596,
            "unit": "iter/sec",
            "range": "stddev: 5.631496476489229e-7",
            "extra": "mean: 2.168142203051493 usec\nrounds: 97192"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35104.79838225959,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023288288165461943",
            "extra": "mean: 28.486134263211028 usec\nrounds: 15060"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 598764.2397255469,
            "unit": "iter/sec",
            "range": "stddev: 4.499779698457273e-7",
            "extra": "mean: 1.6701064186103798 usec\nrounds: 59482"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 258391.95748637803,
            "unit": "iter/sec",
            "range": "stddev: 6.651295735410998e-7",
            "extra": "mean: 3.8700894939917716 usec\nrounds: 54663"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 387395.3394067767,
            "unit": "iter/sec",
            "range": "stddev: 6.043597871711772e-7",
            "extra": "mean: 2.581342360833025 usec\nrounds: 66944"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 238280.75311299166,
            "unit": "iter/sec",
            "range": "stddev: 7.513048117750947e-7",
            "extra": "mean: 4.196730062901071 usec\nrounds: 56202"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 207922.8583176016,
            "unit": "iter/sec",
            "range": "stddev: 8.312570056350455e-7",
            "extra": "mean: 4.809476014765546 usec\nrounds: 74212"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53122.98290350031,
            "unit": "iter/sec",
            "range": "stddev: 0.000001940530598532643",
            "extra": "mean: 18.824244147143123 usec\nrounds: 23834"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26466.42478533343,
            "unit": "iter/sec",
            "range": "stddev: 0.00007642389912738844",
            "extra": "mean: 37.78372062380551 usec\nrounds: 14876"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35546.10973268443,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028663310396215867",
            "extra": "mean: 28.13247377899433 usec\nrounds: 8886"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 325.41838354966245,
            "unit": "iter/sec",
            "range": "stddev: 0.00006657038577034924",
            "extra": "mean: 3.0729671418436904 msec\nrounds: 282"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 29.713465044188286,
            "unit": "iter/sec",
            "range": "stddev: 0.00024707424680855126",
            "extra": "mean: 33.654775655173616 msec\nrounds: 29"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 749.2615736003845,
            "unit": "iter/sec",
            "range": "stddev: 0.0013388424517499684",
            "extra": "mean: 1.3346473851511644 msec\nrounds: 862"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 5.971104905518009,
            "unit": "iter/sec",
            "range": "stddev: 0.005061540040473783",
            "extra": "mean: 167.47319228571607 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6167645254682489,
            "unit": "iter/sec",
            "range": "stddev: 0.10767080476382233",
            "extra": "mean: 1.6213643273999878 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 738.2369562921941,
            "unit": "iter/sec",
            "range": "stddev: 0.0012938725499887908",
            "extra": "mean: 1.3545786234036759 msec\nrounds: 940"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "de1b6aad35b5b6e0c23407987336e69412cb27ae",
          "message": "feat: add Query for RPC-style POST endpoints (merges PR #689, addresses #688)\n\n* feat: add Query for RPC-style POST endpoints\n\nAdd Query class to pynetappfoundry.query as a lightweight wrapper for\nPOST-for-data RPC endpoints (e.g. /lake/query/timeseries). Completes\nthe consistent API interface trilogy alongside QuerySet (GET) and\nMutation (POST/PATCH/DELETE resource lifecycle).\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n\n* refactor: simplify Query.invoke kwargs forwarding\n\nAlways forward query_params to call_endpoint instead of conditionally\nbuilding a kwargs dict. Behavior is unchanged (call_endpoint defaults\nquery_params to None) but the code path is more direct.\n\nDrop tests that pinned the previous over-specified behavior:\n- test_invoke_without_query_params_omits_kwarg (assertion no longer holds)\n- test_works_with_any_mock_client (redundant — other tests already cover\n  duck-typed clients via spec'd MagicMock)\n\nUpdate test_calls_post_on_correct_path and test_invoke_with_no_body to\ninclude query_params=None in the expected call signature.\n\n---------\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T17:13:07+01:00",
          "tree_id": "30d3cd5da9933087206ff568994f98494e5ab1e3",
          "url": "https://github.com/endavis/pynetappfoundry/commit/de1b6aad35b5b6e0c23407987336e69412cb27ae"
        },
        "date": 1778084411922,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1081680.087263138,
            "unit": "iter/sec",
            "range": "stddev: 4.0134135793523636e-7",
            "extra": "mean: 924.4877591582512 nsec\nrounds: 57104"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 700477.6616464731,
            "unit": "iter/sec",
            "range": "stddev: 5.110585827541276e-7",
            "extra": "mean: 1.4275972736225442 usec\nrounds: 159185"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 445342.36275214516,
            "unit": "iter/sec",
            "range": "stddev: 5.540968632590304e-7",
            "extra": "mean: 2.2454634538249594 usec\nrounds: 157431"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 444649.6003311619,
            "unit": "iter/sec",
            "range": "stddev: 5.876906281365548e-7",
            "extra": "mean: 2.2489618775216025 usec\nrounds: 142593"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 482416.9913372874,
            "unit": "iter/sec",
            "range": "stddev: 7.859602921412302e-7",
            "extra": "mean: 2.0728954783038276 usec\nrounds: 78223"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 155459.87867180473,
            "unit": "iter/sec",
            "range": "stddev: 9.727877200839498e-7",
            "extra": "mean: 6.432527855699188 usec\nrounds: 49559"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 136591.67516650003,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010584032541527408",
            "extra": "mean: 7.321090386958342 usec\nrounds: 67034"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 71657.81764665898,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013758919847501813",
            "extra": "mean: 13.955211487613935 usec\nrounds: 41993"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 220743.94405835116,
            "unit": "iter/sec",
            "range": "stddev: 8.634713342587231e-7",
            "extra": "mean: 4.530135602432025 usec\nrounds: 31290"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31302.52499929102,
            "unit": "iter/sec",
            "range": "stddev: 0.000002515873707006191",
            "extra": "mean: 31.94630465186592 usec\nrounds: 2859"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 40.81105850848091,
            "unit": "iter/sec",
            "range": "stddev: 0.0008415074771727769",
            "extra": "mean: 24.503162538462238 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 39.29705290693685,
            "unit": "iter/sec",
            "range": "stddev: 0.0027419473876646875",
            "extra": "mean: 25.44720089743617 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 44.03165295448926,
            "unit": "iter/sec",
            "range": "stddev: 0.00048498010162212704",
            "extra": "mean: 22.710934813952846 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.443099735506694,
            "unit": "iter/sec",
            "range": "stddev: 0.001408191027606409",
            "extra": "mean: 118.43991322222456 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 272.6739511828676,
            "unit": "iter/sec",
            "range": "stddev: 0.0003858884939962946",
            "extra": "mean: 3.667383685394115 msec\nrounds: 178"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 43.80473551596589,
            "unit": "iter/sec",
            "range": "stddev: 0.001424557980581043",
            "extra": "mean: 22.8285820750024 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.055495295426664176,
            "unit": "iter/sec",
            "range": "stddev: 0.6083077349566828",
            "extra": "mean: 18.0195454824 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06337152997295974,
            "unit": "iter/sec",
            "range": "stddev: 0.20410778009478986",
            "extra": "mean: 15.779956715999981 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 411935.7094924794,
            "unit": "iter/sec",
            "range": "stddev: 5.954199533565129e-7",
            "extra": "mean: 2.427563274939282 usec\nrounds: 11213"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 391749.18526085746,
            "unit": "iter/sec",
            "range": "stddev: 6.418566085319771e-7",
            "extra": "mean: 2.55265368154913 usec\nrounds: 80296"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 387268.4183761507,
            "unit": "iter/sec",
            "range": "stddev: 5.689107933476054e-7",
            "extra": "mean: 2.5821883545089594 usec\nrounds: 91158"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 171713.38381179923,
            "unit": "iter/sec",
            "range": "stddev: 9.307198087082313e-7",
            "extra": "mean: 5.823657875707679 usec\nrounds: 45577"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 201059.67475746642,
            "unit": "iter/sec",
            "range": "stddev: 8.122112722393311e-7",
            "extra": "mean: 4.973647755106918 usec\nrounds: 26703"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 431096.78038054734,
            "unit": "iter/sec",
            "range": "stddev: 5.925964469896738e-7",
            "extra": "mean: 2.319664737735359 usec\nrounds: 91075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 442784.1294052803,
            "unit": "iter/sec",
            "range": "stddev: 5.140819644773296e-7",
            "extra": "mean: 2.258436862547754 usec\nrounds: 92251"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34259.7025587097,
            "unit": "iter/sec",
            "range": "stddev: 0.000002472214088372309",
            "extra": "mean: 29.188811499058804 usec\nrounds: 16175"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 592662.1693648284,
            "unit": "iter/sec",
            "range": "stddev: 4.23200641558809e-7",
            "extra": "mean: 1.6873018925296452 usec\nrounds: 62933"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 255840.1404244149,
            "unit": "iter/sec",
            "range": "stddev: 6.819997891866421e-7",
            "extra": "mean: 3.908690787696932 usec\nrounds: 72067"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 379304.34558418,
            "unit": "iter/sec",
            "range": "stddev: 5.786774734452267e-7",
            "extra": "mean: 2.6364053342438374 usec\nrounds: 69513"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 232630.71487519683,
            "unit": "iter/sec",
            "range": "stddev: 7.548363560253117e-7",
            "extra": "mean: 4.2986585006046445 usec\nrounds: 57432"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 204769.26635048626,
            "unit": "iter/sec",
            "range": "stddev: 9.032097107692967e-7",
            "extra": "mean: 4.883545357282204 usec\nrounds: 75787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53339.90274238028,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018240262915037409",
            "extra": "mean: 18.747690726579965 usec\nrounds: 23788"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25991.58072961953,
            "unit": "iter/sec",
            "range": "stddev: 0.00007306897017448933",
            "extra": "mean: 38.4739970378338 usec\nrounds: 14854"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35207.58814773252,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028506186344652586",
            "extra": "mean: 28.402968013712215 usec\nrounds: 9379"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 332.85767217204767,
            "unit": "iter/sec",
            "range": "stddev: 0.00006894921207417663",
            "extra": "mean: 3.0042870680268394 msec\nrounds: 294"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.94978575635434,
            "unit": "iter/sec",
            "range": "stddev: 0.0007700688795097238",
            "extra": "mean: 32.31040136666176 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 781.199251452647,
            "unit": "iter/sec",
            "range": "stddev: 0.0012078691027573511",
            "extra": "mean: 1.280083151821371 msec\nrounds: 988"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.2802864853165925,
            "unit": "iter/sec",
            "range": "stddev: 0.0035066964327081034",
            "extra": "mean: 159.2284049999973 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6409592564645822,
            "unit": "iter/sec",
            "range": "stddev: 0.09546980241478913",
            "extra": "mean: 1.560161570199989 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 747.8329521142032,
            "unit": "iter/sec",
            "range": "stddev: 0.001209560588953308",
            "extra": "mean: 1.3371970266526687 msec\nrounds: 938"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "7ab66a86f1a942da3838735ea1c4207211eef4ca",
          "message": "refactor(codegen): remove dead datamodel-code-generator call (merges PR #693, addresses #692)\n\nrefactor: remove dead datamodel-code-generator call from parse_openapi_spec\n\n`parse_openapi_spec` invoked `_parse_with_datamodel_codegen(spec_path)`\nand discarded the return value. The function ran datamodel-code-generator's\nOpenAPIParser, which internally formats every generated Pydantic model\nwith `black` — costing ~20s per call on the ONTAP spec — and produced\na dict that was never read by any caller, test, or downstream tool.\n\nThe original intent (per the docstring and call-site comment) was to\n\"cross-reference type information when our own flattening logic needs\nconfirmation.\" That cross-reference was scoped but never implemented;\nno production code path depends on the result. `test_codegen_round_trip`\nremains the canonical safety net for parser correctness — it exercises\nthe full pipeline end-to-end and asserts byte-identical output against\nthe on-disk fixtures.\n\nRemoves:\n- the call site in `parse_openapi_spec`\n- the `_parse_with_datamodel_codegen` function (~40 lines)\n- the now-unused `OpenAPIParser` import\n- the docstring reference to datamodel-code-generator\n\n`tests/unit/codegen/test_roundtrip.py` runtime drops from ~33s to ~3s\nlocally. Equivalent CI savings compound across the matrix.\n\nNote: this leaves `datamodel-code-generator` as an unused project\ndependency. Removing it from `pyproject.toml` is a separate decision\nleft to the maintainer.\n\nAddresses #692",
          "timestamp": "2026-05-07T14:04:56+01:00",
          "tree_id": "a84563ec9ed1614a39647b6bed6cc1399bfb6d7c",
          "url": "https://github.com/endavis/pynetappfoundry/commit/7ab66a86f1a942da3838735ea1c4207211eef4ca"
        },
        "date": 1778159433386,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1196704.221033984,
            "unit": "iter/sec",
            "range": "stddev: 3.551810328679703e-7",
            "extra": "mean: 835.6283720098968 nsec\nrounds: 44558"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 751159.4895381808,
            "unit": "iter/sec",
            "range": "stddev: 4.805491327952266e-7",
            "extra": "mean: 1.3312752004435284 usec\nrounds: 170999"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 486601.1685547927,
            "unit": "iter/sec",
            "range": "stddev: 5.677404535141957e-7",
            "extra": "mean: 2.055071102623949 usec\nrounds: 163693"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 482109.6961355528,
            "unit": "iter/sec",
            "range": "stddev: 5.326710905830956e-7",
            "extra": "mean: 2.074216735352351 usec\nrounds: 156495"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 521901.14567901334,
            "unit": "iter/sec",
            "range": "stddev: 4.927938226264025e-7",
            "extra": "mean: 1.916071670429008 usec\nrounds: 72945"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162953.11945686844,
            "unit": "iter/sec",
            "range": "stddev: 0.000001149158180618219",
            "extra": "mean: 6.136734315569129 usec\nrounds: 53891"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 144150.086231583,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012716290702283627",
            "extra": "mean: 6.9372140256195145 usec\nrounds: 73052"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 78547.49157112486,
            "unit": "iter/sec",
            "range": "stddev: 0.000001403606335473056",
            "extra": "mean: 12.731151307289025 usec\nrounds: 46508"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 242501.18727719176,
            "unit": "iter/sec",
            "range": "stddev: 7.060165104223788e-7",
            "extra": "mean: 4.123691150662066 usec\nrounds: 42150"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31632.05121820976,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019543104590192565",
            "extra": "mean: 31.61350470450445 usec\nrounds: 2657"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 58.84329556701968,
            "unit": "iter/sec",
            "range": "stddev: 0.001284775011166041",
            "extra": "mean: 16.994289500000015 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 45.05313129636449,
            "unit": "iter/sec",
            "range": "stddev: 0.0026462389055493902",
            "extra": "mean: 22.196015487178666 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 64.10457129289647,
            "unit": "iter/sec",
            "range": "stddev: 0.001505687895651516",
            "extra": "mean: 15.599511545455286 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 7.754627156944585,
            "unit": "iter/sec",
            "range": "stddev: 0.0020105391718444263",
            "extra": "mean: 128.95526500000187 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 298.830829454267,
            "unit": "iter/sec",
            "range": "stddev: 0.00006076466262825649",
            "extra": "mean: 3.346374943395991 msec\nrounds: 159"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 52.59703762770947,
            "unit": "iter/sec",
            "range": "stddev: 0.0022266520531266467",
            "extra": "mean: 19.01247760526297 msec\nrounds: 38"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07297244231863466,
            "unit": "iter/sec",
            "range": "stddev: 0.16958792835912556",
            "extra": "mean: 13.7038033568 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07480755207244241,
            "unit": "iter/sec",
            "range": "stddev: 0.18837728862766856",
            "extra": "mean: 13.367634313600002 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 404809.54216155974,
            "unit": "iter/sec",
            "range": "stddev: 4.536074718750394e-7",
            "extra": "mean: 2.470297500054728 usec\nrounds: 10800"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 383470.2349260538,
            "unit": "iter/sec",
            "range": "stddev: 4.740151369984672e-7",
            "extra": "mean: 2.607764329330109 usec\nrounds: 77167"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 384432.99702888686,
            "unit": "iter/sec",
            "range": "stddev: 5.06792717222575e-7",
            "extra": "mean: 2.6012335250318235 usec\nrounds: 92200"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 175375.35781581272,
            "unit": "iter/sec",
            "range": "stddev: 7.057982651683671e-7",
            "extra": "mean: 5.702055365442197 usec\nrounds: 43547"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 204942.0950554601,
            "unit": "iter/sec",
            "range": "stddev: 7.158881263559755e-7",
            "extra": "mean: 4.879427038790574 usec\nrounds: 58634"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 421215.729133945,
            "unit": "iter/sec",
            "range": "stddev: 4.6113888704313293e-7",
            "extra": "mean: 2.374080384073226 usec\nrounds: 95193"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 433233.395895522,
            "unit": "iter/sec",
            "range": "stddev: 4.812864080944158e-7",
            "extra": "mean: 2.308224641669034 usec\nrounds: 91025"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35276.4399469633,
            "unit": "iter/sec",
            "range": "stddev: 0.000001824716616314418",
            "extra": "mean: 28.347531709646994 usec\nrounds: 15153"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 591353.5967247093,
            "unit": "iter/sec",
            "range": "stddev: 4.129199451198774e-7",
            "extra": "mean: 1.6910356266346116 usec\nrounds: 59899"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263224.0415295191,
            "unit": "iter/sec",
            "range": "stddev: 7.676077818834989e-7",
            "extra": "mean: 3.7990450803402607 usec\nrounds: 66437"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 372915.7099895251,
            "unit": "iter/sec",
            "range": "stddev: 4.662069004811253e-7",
            "extra": "mean: 2.6815711250890693 usec\nrounds: 61638"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 233785.8542180129,
            "unit": "iter/sec",
            "range": "stddev: 6.678190190396977e-7",
            "extra": "mean: 4.277418765754183 usec\nrounds: 38869"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209305.87151002657,
            "unit": "iter/sec",
            "range": "stddev: 6.682940554858331e-7",
            "extra": "mean: 4.777696835667107 usec\nrounds: 66525"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53713.49126121716,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013659583892987943",
            "extra": "mean: 18.61729663292305 usec\nrounds: 21889"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26514.879426126943,
            "unit": "iter/sec",
            "range": "stddev: 0.0000738841606059732",
            "extra": "mean: 37.71467272880113 usec\nrounds: 13472"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36480.62867014407,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016848063818936885",
            "extra": "mean: 27.41180830631916 usec\nrounds: 8451"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 343.8706223863991,
            "unit": "iter/sec",
            "range": "stddev: 0.00003462144144396798",
            "extra": "mean: 2.908070462839144 msec\nrounds: 296"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.454766846590864,
            "unit": "iter/sec",
            "range": "stddev: 0.0002839644847070943",
            "extra": "mean: 30.812114741937904 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 985.2619171585991,
            "unit": "iter/sec",
            "range": "stddev: 0.0010544377510361054",
            "extra": "mean: 1.0149585430886277 msec\nrounds: 1230"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.816730398207032,
            "unit": "iter/sec",
            "range": "stddev: 0.004465498519712378",
            "extra": "mean: 127.93072666666048 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.78069372181183,
            "unit": "iter/sec",
            "range": "stddev: 0.12604385741074037",
            "extra": "mean: 1.2809120555999924 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 939.8016482272874,
            "unit": "iter/sec",
            "range": "stddev: 0.0010278316276209683",
            "extra": "mean: 1.0640543160211118 msec\nrounds: 1136"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "cf4e3d8afb096d49a7a067fab10a5aefc9cc2545",
          "message": "feat: rewrite dump-dii for DII timeseries (merges PR #691, addresses #96)\n\n* feat: rewrite dump-dii for DII timeseries\n\nBREAKING CHANGE: `nf metrics dump-dii` now requires `--date YYYY-MM-DD`\ninstead of `--days` and writes per-volume tables to `{cluster}_{date}_metrics.db`.\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n\n* feat: add --interval/--window-days options and harden dump-dii\n\nAligns the dump-dii rewrite with the refreshed implementation plan on\nissue #96:\n\n* Add `--interval` (default `60s`) and `--window-days` (default `3`,\n  centered on `--date`) CLI options. `_compute_window` now accepts an\n  arbitrary window length; `_build_body` takes the interval as a\n  parameter and forwards it as `timeAggregationInterval`.\n* Drop optional spec fields (`maxNumberOfDataPoints`, `detectAnomalies`,\n  `interpolationType`) from the timeseries body so DII server defaults\n  apply.\n* Validate `{vserver}-{volume}` against\n  `MetricDB._TABLE_NAME_PATTERN` at the top of `_dump_volume`, skipping\n  the 6 wasted POSTs when the table name is illegal.\n* Extract `_dump_cluster` from the click command so per-cluster\n  orchestration is independently testable.\n* Update tests, CLI reference, the DII access-patterns example, and\n  CHANGELOG.\n\nAddresses #96\n\n---------\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-07T14:18:19+01:00",
          "tree_id": "d35d8c1e469062383623ce10ba7f30dbf2a487d4",
          "url": "https://github.com/endavis/pynetappfoundry/commit/cf4e3d8afb096d49a7a067fab10a5aefc9cc2545"
        },
        "date": 1778160241761,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1180441.0209379594,
            "unit": "iter/sec",
            "range": "stddev: 3.5550060334404e-7",
            "extra": "mean: 847.1410110819564 nsec\nrounds: 47592"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 743851.846839643,
            "unit": "iter/sec",
            "range": "stddev: 4.88790748500247e-7",
            "extra": "mean: 1.3443537234580216 usec\nrounds: 182883"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 481909.2911548046,
            "unit": "iter/sec",
            "range": "stddev: 6.280844001267036e-7",
            "extra": "mean: 2.0750793113029404 usec\nrounds: 157506"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 481791.9355849169,
            "unit": "iter/sec",
            "range": "stddev: 6.485569572796174e-7",
            "extra": "mean: 2.075584762094358 usec\nrounds: 109123"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 522685.4792370261,
            "unit": "iter/sec",
            "range": "stddev: 5.527552351907628e-7",
            "extra": "mean: 1.9131964436045152 usec\nrounds: 72041"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 165103.13483895484,
            "unit": "iter/sec",
            "range": "stddev: 9.750696052111388e-7",
            "extra": "mean: 6.056820186820932 usec\nrounds: 52777"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 143524.9241960553,
            "unit": "iter/sec",
            "range": "stddev: 9.223411424948136e-7",
            "extra": "mean: 6.96743095738548 usec\nrounds: 70413"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 78801.25359839416,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013674045918043813",
            "extra": "mean: 12.690153447259096 usec\nrounds: 44556"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 231029.94150738674,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011055612622861355",
            "extra": "mean: 4.328443289537979 usec\nrounds: 41465"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32942.00544252097,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020972746241711075",
            "extra": "mean: 30.35637893220725 usec\nrounds: 2829"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 44.03789797129149,
            "unit": "iter/sec",
            "range": "stddev: 0.0011258299835304843",
            "extra": "mean: 22.70771417500228 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 50.710113878658554,
            "unit": "iter/sec",
            "range": "stddev: 0.003970890551554733",
            "extra": "mean: 19.7199320512836 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 58.49788369690132,
            "unit": "iter/sec",
            "range": "stddev: 0.0015651891089291643",
            "extra": "mean: 17.09463551162571 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.534847240743774,
            "unit": "iter/sec",
            "range": "stddev: 0.0009272640508294039",
            "extra": "mean: 117.16671333333137 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 293.54965742055657,
            "unit": "iter/sec",
            "range": "stddev: 0.0001313362939057856",
            "extra": "mean: 3.406578664703876 msec\nrounds: 170"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 46.739125000086744,
            "unit": "iter/sec",
            "range": "stddev: 0.001295264649114503",
            "extra": "mean: 21.395351325001144 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07356743392234091,
            "unit": "iter/sec",
            "range": "stddev: 0.21938203645854878",
            "extra": "mean: 13.592971056400007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07689882732507626,
            "unit": "iter/sec",
            "range": "stddev: 0.14723060270427277",
            "extra": "mean: 13.004099474399993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 410437.17953384464,
            "unit": "iter/sec",
            "range": "stddev: 5.459712039265567e-7",
            "extra": "mean: 2.4364264493186343 usec\nrounds: 11441"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 391152.6146875008,
            "unit": "iter/sec",
            "range": "stddev: 4.741840017383125e-7",
            "extra": "mean: 2.5565468884796254 usec\nrounds: 80457"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 392301.5500413653,
            "unit": "iter/sec",
            "range": "stddev: 4.7609927004957364e-7",
            "extra": "mean: 2.549059517849362 usec\nrounds: 82933"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177760.21173287608,
            "unit": "iter/sec",
            "range": "stddev: 7.544104851759761e-7",
            "extra": "mean: 5.625555855563001 usec\nrounds: 41849"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 209146.63800361528,
            "unit": "iter/sec",
            "range": "stddev: 6.920205406008544e-7",
            "extra": "mean: 4.781334328609739 usec\nrounds: 58942"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 433352.6104943395,
            "unit": "iter/sec",
            "range": "stddev: 5.010344085450626e-7",
            "extra": "mean: 2.3075896528216764 usec\nrounds: 84119"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 436261.1996371597,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010082655934627146",
            "extra": "mean: 2.2922047636409206 usec\nrounds: 66125"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35143.31139010067,
            "unit": "iter/sec",
            "range": "stddev: 0.0000069251794111084034",
            "extra": "mean: 28.454916752144324 usec\nrounds: 15580"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 604104.5961288845,
            "unit": "iter/sec",
            "range": "stddev: 3.823916179843332e-7",
            "extra": "mean: 1.6553424794448213 usec\nrounds: 53028"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 266059.029608496,
            "unit": "iter/sec",
            "range": "stddev: 6.29054510678607e-7",
            "extra": "mean: 3.758564411331925 usec\nrounds: 63436"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 375392.60369534895,
            "unit": "iter/sec",
            "range": "stddev: 5.15333451431731e-7",
            "extra": "mean: 2.6638777380162586 usec\nrounds: 54236"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 231946.66708243726,
            "unit": "iter/sec",
            "range": "stddev: 6.482091839803878e-7",
            "extra": "mean: 4.311335931568205 usec\nrounds: 37201"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 212309.139359333,
            "unit": "iter/sec",
            "range": "stddev: 6.819483024453772e-7",
            "extra": "mean: 4.710112824241169 usec\nrounds: 51496"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54047.97946389407,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030815502089042857",
            "extra": "mean: 18.50207926214956 usec\nrounds: 22823"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 27155.35739571151,
            "unit": "iter/sec",
            "range": "stddev: 0.00007194459549360882",
            "extra": "mean: 36.825145971303776 usec\nrounds: 13441"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36061.23048342874,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016876425769349209",
            "extra": "mean: 27.730612255716878 usec\nrounds: 8975"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 335.53136237237976,
            "unit": "iter/sec",
            "range": "stddev: 0.000041863276726851234",
            "extra": "mean: 2.98034733006621 msec\nrounds: 306"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.19986299016985,
            "unit": "iter/sec",
            "range": "stddev: 0.0008057688386666355",
            "extra": "mean: 32.051422799999806 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 981.6090130459806,
            "unit": "iter/sec",
            "range": "stddev: 0.0010746553178426154",
            "extra": "mean: 1.0187355522510446 msec\nrounds: 1244"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.89140560982859,
            "unit": "iter/sec",
            "range": "stddev: 0.0027137981133151497",
            "extra": "mean: 126.72013699999398 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7964114812357425,
            "unit": "iter/sec",
            "range": "stddev: 0.10842648931536537",
            "extra": "mean: 1.2556323251999857 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 965.1650631851537,
            "unit": "iter/sec",
            "range": "stddev: 0.0010372972884624683",
            "extra": "mean: 1.0360922065495068 msec\nrounds: 1191"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "9ea4857601d84bdc52d4a3f4b06b1000f58efe62",
          "message": "docs: add ADR-0017 rationale for where-expressions being cache-only (merges PR #694, addresses #619)\n\nCaptures the \"not yet implemented; no fundamental objection\" rationale\nfor `.where()`-expressions and non-equality typed DSL operators being\ncache-only. Cross-links from ADR-0012 §49, ADR-0015 §17, and the\nDataSource user guide. Notes issue #618 (early validation) as the\noperational consequence of this position.\n\nAddresses #619\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-08T11:54:36+01:00",
          "tree_id": "7134addf032fa095312be1c5cad58fa9cb3e4135",
          "url": "https://github.com/endavis/pynetappfoundry/commit/9ea4857601d84bdc52d4a3f4b06b1000f58efe62"
        },
        "date": 1778238044983,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1175177.3402382454,
            "unit": "iter/sec",
            "range": "stddev: 1.5865554488406136e-7",
            "extra": "mean: 850.9353999263366 nsec\nrounds: 71099"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 744889.299584943,
            "unit": "iter/sec",
            "range": "stddev: 2.5684317444663845e-7",
            "extra": "mean: 1.3424813600587446 usec\nrounds: 157431"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 473141.20652179216,
            "unit": "iter/sec",
            "range": "stddev: 3.2308252891896126e-7",
            "extra": "mean: 2.1135339433893536 usec\nrounds: 151149"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 476011.96579464216,
            "unit": "iter/sec",
            "range": "stddev: 3.113544234396516e-7",
            "extra": "mean: 2.100787526066967 usec\nrounds: 135852"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 514647.81283950363,
            "unit": "iter/sec",
            "range": "stddev: 3.45841505890147e-7",
            "extra": "mean: 1.9430763622264857 usec\nrounds: 76805"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 160778.63614531033,
            "unit": "iter/sec",
            "range": "stddev: 5.43111129316671e-7",
            "extra": "mean: 6.219731824918633 usec\nrounds: 52902"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141333.1264538846,
            "unit": "iter/sec",
            "range": "stddev: 8.952224613187044e-7",
            "extra": "mean: 7.075482054989343 usec\nrounds: 71552"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 76625.51963205023,
            "unit": "iter/sec",
            "range": "stddev: 9.754560005356652e-7",
            "extra": "mean: 13.05048246069876 usec\nrounds: 44671"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 231404.676238261,
            "unit": "iter/sec",
            "range": "stddev: 4.4965568957687655e-7",
            "extra": "mean: 4.321433845919219 usec\nrounds: 33747"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 34628.40051273722,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017863473601797696",
            "extra": "mean: 28.87803032173473 usec\nrounds: 3232"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 79.909715377955,
            "unit": "iter/sec",
            "range": "stddev: 0.0005899815558754183",
            "extra": "mean: 12.514122910715233 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 77.65280164916402,
            "unit": "iter/sec",
            "range": "stddev: 0.0012638185302798065",
            "extra": "mean: 12.87783542592588 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 88.51073914074205,
            "unit": "iter/sec",
            "range": "stddev: 0.0005645508259254203",
            "extra": "mean: 11.29806405084797 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.178823439043109,
            "unit": "iter/sec",
            "range": "stddev: 0.0013477000143563552",
            "extra": "mean: 89.45485233333272 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 299.80183889813287,
            "unit": "iter/sec",
            "range": "stddev: 0.00008115140032743019",
            "extra": "mean: 3.335536578679164 msec\nrounds: 197"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 80.15184560212668,
            "unit": "iter/sec",
            "range": "stddev: 0.0007067272785006627",
            "extra": "mean: 12.476319072725966 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.06326940734594115,
            "unit": "iter/sec",
            "range": "stddev: 0.273775775533237",
            "extra": "mean: 15.80542701359999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06995665628609897,
            "unit": "iter/sec",
            "range": "stddev: 0.26839159601345647",
            "extra": "mean: 14.294565422199991 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 442836.390411475,
            "unit": "iter/sec",
            "range": "stddev: 2.9973797411246635e-7",
            "extra": "mean: 2.2581703348065396 usec\nrounds: 12722"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 423964.31577189954,
            "unit": "iter/sec",
            "range": "stddev: 2.7610796366607524e-7",
            "extra": "mean: 2.358689075469309 usec\nrounds: 63874"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 413744.83534755226,
            "unit": "iter/sec",
            "range": "stddev: 2.872893298534308e-7",
            "extra": "mean: 2.416948598669477 usec\nrounds: 81593"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 178475.67375566822,
            "unit": "iter/sec",
            "range": "stddev: 4.366854198653285e-7",
            "extra": "mean: 5.603004482106575 usec\nrounds: 45513"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 213313.05586313145,
            "unit": "iter/sec",
            "range": "stddev: 3.996631093185947e-7",
            "extra": "mean: 4.6879455922361934 usec\nrounds: 53926"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 465207.6507199567,
            "unit": "iter/sec",
            "range": "stddev: 2.5282050976172773e-7",
            "extra": "mean: 2.1495777175039943 usec\nrounds: 85412"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 472395.39730131073,
            "unit": "iter/sec",
            "range": "stddev: 2.94928488613185e-7",
            "extra": "mean: 2.1168707521554535 usec\nrounds: 97371"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 37259.968260486465,
            "unit": "iter/sec",
            "range": "stddev: 0.000001175864554198949",
            "extra": "mean: 26.8384554975717 usec\nrounds: 17089"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 613491.9035493231,
            "unit": "iter/sec",
            "range": "stddev: 2.265988334496687e-7",
            "extra": "mean: 1.6300133615693313 usec\nrounds: 63316"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 283149.0122714759,
            "unit": "iter/sec",
            "range": "stddev: 3.593116984510602e-7",
            "extra": "mean: 3.531709300264929 usec\nrounds: 74245"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 409883.8312194747,
            "unit": "iter/sec",
            "range": "stddev: 2.948115312888025e-7",
            "extra": "mean: 2.439715655591557 usec\nrounds: 67573"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 237847.60834325443,
            "unit": "iter/sec",
            "range": "stddev: 6.328179358242255e-7",
            "extra": "mean: 4.204372736667717 usec\nrounds: 47720"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 227517.88429287862,
            "unit": "iter/sec",
            "range": "stddev: 4.064643382914218e-7",
            "extra": "mean: 4.395258874298965 usec\nrounds: 67921"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 56695.62058467441,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010158234096747144",
            "extra": "mean: 17.638046637244383 usec\nrounds: 24787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 28278.275365006582,
            "unit": "iter/sec",
            "range": "stddev: 0.00007619130246975014",
            "extra": "mean: 35.362835501540744 usec\nrounds: 14529"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 38295.409843909685,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010804371652653306",
            "extra": "mean: 26.11279012487276 usec\nrounds: 8810"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 359.4286684430348,
            "unit": "iter/sec",
            "range": "stddev: 0.00002594803174402979",
            "extra": "mean: 2.782193207714282 msec\nrounds: 337"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 35.8222244734566,
            "unit": "iter/sec",
            "range": "stddev: 0.00014057100907320376",
            "extra": "mean: 27.91563099999487 msec\nrounds: 34"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 878.269207539408,
            "unit": "iter/sec",
            "range": "stddev: 0.0009764740393119495",
            "extra": "mean: 1.1386030517927843 msec\nrounds: 1004"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.2240830818097,
            "unit": "iter/sec",
            "range": "stddev: 0.001192908012728139",
            "extra": "mean: 138.42587200000622 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7186948584738655,
            "unit": "iter/sec",
            "range": "stddev: 0.07801965180207492",
            "extra": "mean: 1.3914110950000123 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 839.1663602040193,
            "unit": "iter/sec",
            "range": "stddev: 0.000966327894917353",
            "extra": "mean: 1.1916588264535277 msec\nrounds: 1066"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "948428003d95c72097c5d663143d9ed47077931e",
          "message": "docs: add ADR-0018 codifying cache-schema versioning and backward-compat policy (merges PR #695, addresses #620)\n\nRecords the contract behind the cache-schema migration mechanism documented\nin ADR-0001 (substrate) and ADR-0003 (mechanism): rebuild-tolerant cache,\ndrop-and-recreate column policy, no-downgrade, internal SCHEMA_VERSION\nvisibility. Cites the v3 -> v4 destructive precedent (ADR-0011, issue #444).\n\nCross-links added from AGENTS.md \"Cache Schema Pitfalls\" and\ndocs/reference/cache.md \"SQLite database schema versioning\" to the ADR,\nplus index updates in docs/decisions/README.md and docs/TABLE_OF_CONTENTS.md\nand reciprocal \"Related Documentation\" links from ADR-0001 and ADR-0003.\ndocs/development/cache-models.md \"Removing a field\" guidance was rewritten\nto align with the ADR's drop-and-recreate policy.\n\nPolicy documentation only -- no code changes.",
          "timestamp": "2026-05-08T15:35:23+01:00",
          "tree_id": "989144854e8219dea6c6e17e55e36d8e156dcdb0",
          "url": "https://github.com/endavis/pynetappfoundry/commit/948428003d95c72097c5d663143d9ed47077931e"
        },
        "date": 1778251254242,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1251678.5815234354,
            "unit": "iter/sec",
            "range": "stddev: 2.9553275607864674e-7",
            "extra": "mean: 798.9271485199387 nsec\nrounds: 53712"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 744372.2552330861,
            "unit": "iter/sec",
            "range": "stddev: 5.44147702433767e-7",
            "extra": "mean: 1.3434138537133802 usec\nrounds: 191645"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 478919.0346106132,
            "unit": "iter/sec",
            "range": "stddev: 5.360966178793558e-7",
            "extra": "mean: 2.0880356129779925 usec\nrounds: 160026"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 476684.3063533262,
            "unit": "iter/sec",
            "range": "stddev: 5.528994276378617e-7",
            "extra": "mean: 2.097824465105809 usec\nrounds: 173071"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 522707.427012901,
            "unit": "iter/sec",
            "range": "stddev: 5.279653938991182e-7",
            "extra": "mean: 1.9131161110808532 usec\nrounds: 78623"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 168504.75020269467,
            "unit": "iter/sec",
            "range": "stddev: 8.351527084649562e-7",
            "extra": "mean: 5.93455079929259 usec\nrounds: 57422"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 146459.56552155092,
            "unit": "iter/sec",
            "range": "stddev: 9.722752637626271e-7",
            "extra": "mean: 6.827823068018415 usec\nrounds: 72412"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 80417.81886456591,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013479575014735803",
            "extra": "mean: 12.435054993024995 usec\nrounds: 45824"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 240695.7440776158,
            "unit": "iter/sec",
            "range": "stddev: 7.329117289649088e-7",
            "extra": "mean: 4.154622691116365 usec\nrounds: 41849"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 28228.373254749436,
            "unit": "iter/sec",
            "range": "stddev: 0.000007017306666299346",
            "extra": "mean: 35.42534991214025 usec\nrounds: 2855"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 57.08666906727289,
            "unit": "iter/sec",
            "range": "stddev: 0.0012364866014756251",
            "extra": "mean: 17.51722453488337 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 54.71374357534226,
            "unit": "iter/sec",
            "range": "stddev: 0.0008065846804112404",
            "extra": "mean: 18.276943499999664 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 55.842861931560776,
            "unit": "iter/sec",
            "range": "stddev: 0.002471756076173505",
            "extra": "mean: 17.90739165957447 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.795603637532853,
            "unit": "iter/sec",
            "range": "stddev: 0.0003272137412186152",
            "extra": "mean: 113.69316322222289 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 309.49375710678527,
            "unit": "iter/sec",
            "range": "stddev: 0.00009719682708108021",
            "extra": "mean: 3.2310829444452023 msec\nrounds: 180"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 56.279823877817186,
            "unit": "iter/sec",
            "range": "stddev: 0.001113109061764058",
            "extra": "mean: 17.76835695454534 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07563201416571867,
            "unit": "iter/sec",
            "range": "stddev: 0.17699215107916663",
            "extra": "mean: 13.221914172600004 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07834310213096146,
            "unit": "iter/sec",
            "range": "stddev: 0.08709102378695599",
            "extra": "mean: 12.76436562759999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 411484.5209834716,
            "unit": "iter/sec",
            "range": "stddev: 5.757119169990231e-7",
            "extra": "mean: 2.4302250728896015 usec\nrounds: 12005"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 389265.86735527846,
            "unit": "iter/sec",
            "range": "stddev: 5.155365311418146e-7",
            "extra": "mean: 2.568938311478801 usec\nrounds: 85267"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 391080.02182260924,
            "unit": "iter/sec",
            "range": "stddev: 5.522190299666631e-7",
            "extra": "mean: 2.5570214385780923 usec\nrounds: 104998"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177529.8870558459,
            "unit": "iter/sec",
            "range": "stddev: 7.996577730169376e-7",
            "extra": "mean: 5.63285436939093 usec\nrounds: 45430"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 208992.96936383037,
            "unit": "iter/sec",
            "range": "stddev: 7.305730517261886e-7",
            "extra": "mean: 4.784849954732813 usec\nrounds: 62961"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 435113.5582875287,
            "unit": "iter/sec",
            "range": "stddev: 4.98206267451128e-7",
            "extra": "mean: 2.2982506082680767 usec\nrounds: 103157"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 444560.29482599825,
            "unit": "iter/sec",
            "range": "stddev: 4.999289851672373e-7",
            "extra": "mean: 2.2494136602806645 usec\nrounds: 97041"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 36205.152795619695,
            "unit": "iter/sec",
            "range": "stddev: 0.000002373815379115829",
            "extra": "mean: 27.620377840830038 usec\nrounds: 16192"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 596280.2446299077,
            "unit": "iter/sec",
            "range": "stddev: 4.1318485704705214e-7",
            "extra": "mean: 1.6770637783256903 usec\nrounds: 58327"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 265006.17624094995,
            "unit": "iter/sec",
            "range": "stddev: 6.84570752976039e-7",
            "extra": "mean: 3.773496958390797 usec\nrounds: 74795"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 364412.84592633205,
            "unit": "iter/sec",
            "range": "stddev: 6.343696467971319e-7",
            "extra": "mean: 2.744140364915004 usec\nrounds: 69248"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 231149.0557808463,
            "unit": "iter/sec",
            "range": "stddev: 6.62118731516602e-7",
            "extra": "mean: 4.326212783443535 usec\nrounds: 54774"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 208109.5686647951,
            "unit": "iter/sec",
            "range": "stddev: 6.896501367304905e-7",
            "extra": "mean: 4.805161081327853 usec\nrounds: 73584"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52774.64839702961,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015726972334398869",
            "extra": "mean: 18.948491944027513 usec\nrounds: 23523"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26335.791402802555,
            "unit": "iter/sec",
            "range": "stddev: 0.00007337253076090051",
            "extra": "mean: 37.97113915071425 usec\nrounds: 14955"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35402.72774088154,
            "unit": "iter/sec",
            "range": "stddev: 0.000002179371050122616",
            "extra": "mean: 28.246411048300192 usec\nrounds: 9359"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 335.4411966885656,
            "unit": "iter/sec",
            "range": "stddev: 0.000028212798697618297",
            "extra": "mean: 2.9811484393445933 msec\nrounds: 305"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.10874126123867,
            "unit": "iter/sec",
            "range": "stddev: 0.0003313942855415902",
            "extra": "mean: 31.14416700000599 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 1000.2234789635277,
            "unit": "iter/sec",
            "range": "stddev: 0.0010385519244825866",
            "extra": "mean: 999.7765709681607 usec\nrounds: 1240"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 8.051860098448554,
            "unit": "iter/sec",
            "range": "stddev: 0.0023949333045915695",
            "extra": "mean: 124.19490499998649 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.8003949112634536,
            "unit": "iter/sec",
            "range": "stddev: 0.09668606992438504",
            "extra": "mean: 1.2493832555999915 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 953.2978015468268,
            "unit": "iter/sec",
            "range": "stddev: 0.0010412878696101772",
            "extra": "mean: 1.0489901459726372 msec\nrounds: 1192"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ea4c6dd33d55b71c6c18053513c55c15ff686313",
          "message": "feat: add BlueXP/Console SaaS docs to OpenAPI 3.1 parser (merges PR #698, addresses #697)\n\n* feat: add BlueXP/Console SaaS docs to OpenAPI 3.1 parser\n\nAdd a build-time tool (`tools/console_openapi/`) that fetches the\n`NetAppDocs/console-automation` AsciiDoc reference docs, parses them, and\nemits a single OpenAPI 3.1 spec for the BlueXP/NetApp Console SaaS layer\n(api.bluexp.netapp.com). NetApp does not publish a machine-readable spec\nfor this surface; this tool fills that gap.\n\nScope (v1):\n- Services: `tenancy` (v3, 50 endpoints) + `tenancyv4` (v4, 172 endpoints).\n  Total 222 endpoints generated and validated against\n  `openapi-spec-validator`.\n- `cm/` (workflow tutorials with curl examples) deliberately excluded\n  per scope decision; documented in info.description.\n\nArchitecture:\n- Pydantic AST in `models.py`; pure-function parser modules\n  (frontmatter, operation line, AsciiDoc tables, type expressions,\n  endpoint orchestrator); builder assembles OpenAPI 3.1 with\n  per-file schema namespacing (`<service>.<file_stem>.<anchor>`)\n  to avoid cross-file false-merging.\n- Bearer auth modeled as a `BearerAuth` security scheme; per-request\n  Authorization headers are stripped at build time. `*Token usage:*`\n  is preserved as `x-token-type` on each operation.\n- Per-operation `servers` blocks encode the verified base URLs:\n  v3 `tenancy` paths at `https://api.bluexp.netapp.com`, v4\n  `tenancyv4` paths at `https://api.bluexp.netapp.com/v1/management`.\n- Final invariant pass enforces unique operationIds, no unresolved\n  $refs, and reconciles path-template variables with declared params\n  (synthesizing missing path params and demoting stray `in: path`\n  declarations to `in: query`, both with `x-` markers).\n- Strict by default; `--lenient` skips malformed files.\n- Lockfile pins repo URL, requested ref, resolved SHA, services, and\n  endpoint count.\n\nValidation:\n- 31 unit tests across parser/builder/types/tables/frontmatter modules.\n- End-to-end smoke-tested against the live SaaS using a user JWT:\n  9 endpoints' response shapes validated cleanly against generated\n  schemas (0 errors); 5 endpoints' upstream docs declare no response\n  schema (correctly recorded as such); no parser-introduced bugs found.\n\nDistribution:\n- Build-time only — `tools/` is not in the wheel package.\n- Generated artifact (`tools/console_openapi/generated/console_openapi.yaml`)\n  and lockfile checked in.\n- Refresh via `doit console_openapi_refresh` or\n  `python -m tools.console_openapi.cli build`.\n\nADR-0008 amended with a new \"Spec acquisition strategies\" section\ndocumenting the three strategies now in use (vendor-published,\nconnector-scraped, parser-derived).\n\nAddresses #697\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n\n* fix(console_openapi): address PR #698 review findings\n\nBugs and correctness:\n- doit console_openapi_refresh --ref param now actually plumbs through\n  to the build CLI (wrap action in a Python callable; doit only forwards\n  params to callables, not list[str] actions).\n- fetcher: add 120s timeout to all subprocess.run calls; surface\n  TimeoutExpired as a clear FetchError.\n- fetcher: unify the initial-clone and cached-clone paths to both use\n  'git fetch --depth=1 origin <ref>' + 'git checkout FETCH_HEAD'. The\n  original initial-clone path cloned 'main' first and could fail on\n  SHAs not reachable from main.\n- builder: requestBody.required now correctly defaults to True whenever\n  the operation has a body section. The previous 'any field is required'\n  heuristic conflated 'some property is required' with 'the body itself\n  is required' and was wrong for endpoints accepting an all-optional\n  body.\n- models.TypeRef: add @model_validator enforcing at most one of\n  {primitive, ref_anchor, array_items, one_of, additional_properties}\n  is set; the docstring has always asserted this but it was unenforced.\n\nStyle and consistency:\n- doit tasks now use 'uv run python' instead of sys.executable, matching\n  docs_serve / docs_build conventions.\n- lockfile: add encoding='utf-8' to read_text/write_text for consistency\n  with walker.py.\n- endpoint._parse_response_blocks: drop unused enumerate index. Add\n  comment documenting same-status-code overwrite semantics.\n- cli._validate: take the in-memory spec dict instead of re-reading\n  from disk after writing.\n\nTests added (13 new):\n- test_lockfile.py: round-trip, sort/format stability, missing-field\n  rejection.\n- test_ensure_path_params.py: unit-level coverage of synthesis and\n  demotion paths in isolation, including combined synthesize+demote.\n- test_walker_lenient.py: --lenient/--strict mode behavior verified\n  with a deliberately malformed fixture\n  (tests/fixtures/console_openapi/malformed_table.adoc).\n- test_types.py: TypeRef validator rejects multiple kinds and allows\n  zero kinds.\n\nTotal: 44 unit tests pass (was 31). doit check passes.\n\nGenerated spec rebuilt: only the requestBody.required flips changed\n(no other behavior shifts).\n\nNote: task_console_openapi_check intentionally not wired into 'doit\ncheck' — it requires a network git-clone and a full rebuild, which\nis heavyweight for local dev. CI should call it directly.\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n\n---------\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-08T17:47:30+01:00",
          "tree_id": "8926b2d36f1984c4ffb826c4fe6689aacae757f4",
          "url": "https://github.com/endavis/pynetappfoundry/commit/ea4c6dd33d55b71c6c18053513c55c15ff686313"
        },
        "date": 1778259233826,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1183815.2637052021,
            "unit": "iter/sec",
            "range": "stddev: 2.7357047712442116e-7",
            "extra": "mean: 844.7263949529743 nsec\nrounds: 64107"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 743621.1845674635,
            "unit": "iter/sec",
            "range": "stddev: 4.573696433573311e-7",
            "extra": "mean: 1.3447707256775672 usec\nrounds: 198413"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 469545.88491665863,
            "unit": "iter/sec",
            "range": "stddev: 5.953181370134044e-7",
            "extra": "mean: 2.1297173122441344 usec\nrounds: 165536"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 465684.70842584316,
            "unit": "iter/sec",
            "range": "stddev: 8.428310716917379e-7",
            "extra": "mean: 2.1473756425893953 usec\nrounds: 169435"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 510461.53487188835,
            "unit": "iter/sec",
            "range": "stddev: 6.168952048713806e-7",
            "extra": "mean: 1.9590114664584322 usec\nrounds: 83112"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162876.03052905388,
            "unit": "iter/sec",
            "range": "stddev: 8.675870117968528e-7",
            "extra": "mean: 6.139638820714136 usec\nrounds: 60787"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 142381.1449341775,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010679580851578354",
            "extra": "mean: 7.023401872925646 usec\nrounds: 74108"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74968.72400584775,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013482167339521265",
            "extra": "mean: 13.338895829706232 usec\nrounds: 45704"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 235219.30608026907,
            "unit": "iter/sec",
            "range": "stddev: 9.366202220217193e-7",
            "extra": "mean: 4.251351713701374 usec\nrounds: 47351"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31188.036231180133,
            "unit": "iter/sec",
            "range": "stddev: 0.00000655865908766079",
            "extra": "mean: 32.06357696225366 usec\nrounds: 2969"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 74.88583625458732,
            "unit": "iter/sec",
            "range": "stddev: 0.0009378357138015122",
            "extra": "mean: 13.353660051285633 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 76.20563260686205,
            "unit": "iter/sec",
            "range": "stddev: 0.0008283795815501813",
            "extra": "mean: 13.122389589742129 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 84.71484913431277,
            "unit": "iter/sec",
            "range": "stddev: 0.0006632910471394796",
            "extra": "mean: 11.804305977273605 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.787052993656053,
            "unit": "iter/sec",
            "range": "stddev: 0.006628281191790192",
            "extra": "mean: 113.80379755555875 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 305.00746501104976,
            "unit": "iter/sec",
            "range": "stddev: 0.00001908530539445936",
            "extra": "mean: 3.278608279190059 msec\nrounds: 197"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 74.12896206918016,
            "unit": "iter/sec",
            "range": "stddev: 0.0011804323600307775",
            "extra": "mean: 13.490004069755614 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.06246285882990092,
            "unit": "iter/sec",
            "range": "stddev: 0.26605524202760156",
            "extra": "mean: 16.00951379319995 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06691137037597167,
            "unit": "iter/sec",
            "range": "stddev: 0.08904044922219019",
            "extra": "mean: 14.945143021000012 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 422135.5260764093,
            "unit": "iter/sec",
            "range": "stddev: 5.230791435562614e-7",
            "extra": "mean: 2.3689074674539317 usec\nrounds: 13325"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 404399.71152581286,
            "unit": "iter/sec",
            "range": "stddev: 5.207209475913575e-7",
            "extra": "mean: 2.472800972648988 usec\nrounds: 69076"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 396023.72587979666,
            "unit": "iter/sec",
            "range": "stddev: 5.10684583427513e-7",
            "extra": "mean: 2.5251012367464205 usec\nrounds: 106987"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 174026.70858630416,
            "unit": "iter/sec",
            "range": "stddev: 7.982170285553695e-7",
            "extra": "mean: 5.746244401927967 usec\nrounds: 48408"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 205551.0415647959,
            "unit": "iter/sec",
            "range": "stddev: 7.451668446728509e-7",
            "extra": "mean: 4.864971699424689 usec\nrounds: 63497"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 445926.2480098755,
            "unit": "iter/sec",
            "range": "stddev: 5.420700198691751e-7",
            "extra": "mean: 2.2425232972109193 usec\nrounds: 100614"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 456922.9102836069,
            "unit": "iter/sec",
            "range": "stddev: 4.488156324325485e-7",
            "extra": "mean: 2.1885529867156612 usec\nrounds: 96071"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35489.7833939143,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022425955515819938",
            "extra": "mean: 28.177123227285673 usec\nrounds: 16782"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 611050.7431907539,
            "unit": "iter/sec",
            "range": "stddev: 3.8504330805481616e-7",
            "extra": "mean: 1.6365252986654604 usec\nrounds: 65241"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 264676.36266204325,
            "unit": "iter/sec",
            "range": "stddev: 5.896480605136883e-7",
            "extra": "mean: 3.778199118131557 usec\nrounds: 92337"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 383303.316274443,
            "unit": "iter/sec",
            "range": "stddev: 5.367994721231994e-7",
            "extra": "mean: 2.6088999430519033 usec\nrounds: 75787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 237111.79292796872,
            "unit": "iter/sec",
            "range": "stddev: 6.69023204874169e-7",
            "extra": "mean: 4.2174199252239895 usec\nrounds: 57003"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 210068.00642099135,
            "unit": "iter/sec",
            "range": "stddev: 7.23618966576852e-7",
            "extra": "mean: 4.760363165421431 usec\nrounds: 80561"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54214.63580280766,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015148317184956817",
            "extra": "mean: 18.445203683323687 usec\nrounds: 25412"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26320.093183728342,
            "unit": "iter/sec",
            "range": "stddev: 0.00006643777614982792",
            "extra": "mean: 37.99378645886489 usec\nrounds: 15435"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36061.1669370968,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025640904234967554",
            "extra": "mean: 27.730661122097 usec\nrounds: 10340"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 337.84374529361,
            "unit": "iter/sec",
            "range": "stddev: 0.000027758405630665003",
            "extra": "mean: 2.9599482421405474 msec\nrounds: 318"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 33.75076760846683,
            "unit": "iter/sec",
            "range": "stddev: 0.00011200934337341899",
            "extra": "mean: 29.628955750006014 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 834.6257197725012,
            "unit": "iter/sec",
            "range": "stddev: 0.0011467655857265576",
            "extra": "mean: 1.1981418452723647 msec\nrounds: 1047"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.861075433470757,
            "unit": "iter/sec",
            "range": "stddev: 0.0021356146184322656",
            "extra": "mean: 145.74974575000965 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6794680877841291,
            "unit": "iter/sec",
            "range": "stddev: 0.08574240852149088",
            "extra": "mean: 1.4717394650000188 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 800.4197786049083,
            "unit": "iter/sec",
            "range": "stddev: 0.001140656966393467",
            "extra": "mean: 1.249344439917452 msec\nrounds: 982"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bac2512b8b86d3fa72b510839e5d5897eeb715a3",
          "message": "chore: suppress paramiko CVE-2026-44405 until upstream 4.0.1 ships (merges PR #702, addresses #701)\n\nparamiko 4.0.0 (latest released) is flagged for CVE-2026-44405 /\nGHSA-r374-rxx8-8654 (rsakey.py accepts SHA-1). All released versions\nare affected; the upstream fix landed in commit a4489456 but no tagged\nrelease exists yet, so pinning past the issue is not currently possible.\n\nAdds --ignore-vuln to both the CI pip-audit step and the local doit\naudit task, with inline comments pointing at the upstream fix and a\nTODO to remove when paramiko 4.0.1+ ships.\n\nAddresses #701\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-09T15:44:38+01:00",
          "tree_id": "58cbbfb1d7ba66835d10c778635770adc9f07e38",
          "url": "https://github.com/endavis/pynetappfoundry/commit/bac2512b8b86d3fa72b510839e5d5897eeb715a3"
        },
        "date": 1778338257627,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1189375.144498965,
            "unit": "iter/sec",
            "range": "stddev: 1.5301831610012486e-7",
            "extra": "mean: 840.7776172430938 nsec\nrounds: 64371"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 749125.7406903482,
            "unit": "iter/sec",
            "range": "stddev: 2.792533694232624e-7",
            "extra": "mean: 1.334889385964046 usec\nrounds: 160052"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 471841.9645436384,
            "unit": "iter/sec",
            "range": "stddev: 3.438337865503538e-7",
            "extra": "mean: 2.1193536716624846 usec\nrounds: 137458"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 472789.8732680644,
            "unit": "iter/sec",
            "range": "stddev: 4.421510036049612e-7",
            "extra": "mean: 2.115104524315849 usec\nrounds: 150807"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 525863.3884417468,
            "unit": "iter/sec",
            "range": "stddev: 3.800292952591422e-7",
            "extra": "mean: 1.9016345727418447 usec\nrounds: 73960"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 161570.73853290032,
            "unit": "iter/sec",
            "range": "stddev: 5.500198918510984e-7",
            "extra": "mean: 6.189239518741025 usec\nrounds: 54192"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141713.34492571047,
            "unit": "iter/sec",
            "range": "stddev: 5.943051138765403e-7",
            "extra": "mean: 7.0564984583789485 usec\nrounds: 64218"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 75433.22805065333,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018608816104634058",
            "extra": "mean: 13.25675734476723 usec\nrounds: 42377"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 210043.89172932698,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016400551583097362",
            "extra": "mean: 4.760909692573445 usec\nrounds: 42001"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 33826.23674136573,
            "unit": "iter/sec",
            "range": "stddev: 0.000001488860390863334",
            "extra": "mean: 29.56285109827518 usec\nrounds: 3096"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 60.61041841165706,
            "unit": "iter/sec",
            "range": "stddev: 0.0006587902749541395",
            "extra": "mean: 16.498813672727795 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 62.002944040163065,
            "unit": "iter/sec",
            "range": "stddev: 0.0008061020578872767",
            "extra": "mean: 16.12826641509538 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 65.78965327058567,
            "unit": "iter/sec",
            "range": "stddev: 0.0008954363186766625",
            "extra": "mean: 15.199958508477147 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.848025818964187,
            "unit": "iter/sec",
            "range": "stddev: 0.00047536186384441613",
            "extra": "mean: 92.18267145454527 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 305.8979513433858,
            "unit": "iter/sec",
            "range": "stddev: 0.00008161498374462074",
            "extra": "mean: 3.2690640640396116 msec\nrounds: 203"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 55.312544067726776,
            "unit": "iter/sec",
            "range": "stddev: 0.0005180750991585132",
            "extra": "mean: 18.079081641509063 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.05986525118061832,
            "unit": "iter/sec",
            "range": "stddev: 0.46561950496128246",
            "extra": "mean: 16.704181144799993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06819270346907655,
            "unit": "iter/sec",
            "range": "stddev: 0.0950542890838605",
            "extra": "mean: 14.6643254942 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 433043.98721244844,
            "unit": "iter/sec",
            "range": "stddev: 3.0683991591901023e-7",
            "extra": "mean: 2.309234233771746 usec\nrounds: 13478"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 418064.33099226933,
            "unit": "iter/sec",
            "range": "stddev: 2.958738999950114e-7",
            "extra": "mean: 2.3919763679109267 usec\nrounds: 70667"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 403756.4273615223,
            "unit": "iter/sec",
            "range": "stddev: 3.0523779619566334e-7",
            "extra": "mean: 2.476740758121983 usec\nrounds: 87482"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 179520.79171637568,
            "unit": "iter/sec",
            "range": "stddev: 4.902590949706498e-7",
            "extra": "mean: 5.570385415745585 usec\nrounds: 42196"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 211285.72081531913,
            "unit": "iter/sec",
            "range": "stddev: 4.2912905704303467e-7",
            "extra": "mean: 4.73292750755306 usec\nrounds: 61234"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 463011.030239096,
            "unit": "iter/sec",
            "range": "stddev: 2.648721085779225e-7",
            "extra": "mean: 2.1597757605982006 usec\nrounds: 98756"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 471904.2956510562,
            "unit": "iter/sec",
            "range": "stddev: 2.949447699748763e-7",
            "extra": "mean: 2.1190737385010747 usec\nrounds: 98795"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 37057.266241777856,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011907290834313588",
            "extra": "mean: 26.985260960038485 usec\nrounds: 13002"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 587819.3796268952,
            "unit": "iter/sec",
            "range": "stddev: 2.3280387972622263e-7",
            "extra": "mean: 1.701202843354241 usec\nrounds: 66051"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 275406.1137828752,
            "unit": "iter/sec",
            "range": "stddev: 3.7402458986750804e-7",
            "extra": "mean: 3.631001455502838 usec\nrounds: 59781"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 403859.1543862411,
            "unit": "iter/sec",
            "range": "stddev: 2.8896872297054533e-7",
            "extra": "mean: 2.4761107656943793 usec\nrounds: 65300"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 234057.20270834333,
            "unit": "iter/sec",
            "range": "stddev: 4.1185322183218643e-7",
            "extra": "mean: 4.272459844981106 usec\nrounds: 50106"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 223494.5204109174,
            "unit": "iter/sec",
            "range": "stddev: 4.2634209091352175e-7",
            "extra": "mean: 4.474382629880134 usec\nrounds: 68335"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 55229.270156617364,
            "unit": "iter/sec",
            "range": "stddev: 0.000004428324194775861",
            "extra": "mean: 18.10634102468189 usec\nrounds: 23576"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 28194.360144917962,
            "unit": "iter/sec",
            "range": "stddev: 0.00007999372725280936",
            "extra": "mean: 35.46808634280179 usec\nrounds: 14095"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 38159.477697150665,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012965467841938448",
            "extra": "mean: 26.205809417424735 usec\nrounds: 9896"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 358.10110066543604,
            "unit": "iter/sec",
            "range": "stddev: 0.00003966205092884165",
            "extra": "mean: 2.7925074738440205 msec\nrounds: 325"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 34.44823303634683,
            "unit": "iter/sec",
            "range": "stddev: 0.00026988333434158063",
            "extra": "mean: 29.029065117647274 msec\nrounds: 34"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 872.1478196734386,
            "unit": "iter/sec",
            "range": "stddev: 0.0009901988479796829",
            "extra": "mean: 1.1465946224281494 msec\nrounds: 972"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.168293878485905,
            "unit": "iter/sec",
            "range": "stddev: 0.002662895169723795",
            "extra": "mean: 139.50320912501724 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7080132424049721,
            "unit": "iter/sec",
            "range": "stddev: 0.08743841954352408",
            "extra": "mean: 1.4124029610000093 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 816.9977392800415,
            "unit": "iter/sec",
            "range": "stddev: 0.0010041548899293819",
            "extra": "mean: 1.2239935949899012 msec\nrounds: 958"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "add278a4dad94a52b19f93f653affd11661a0b32",
          "message": "feat: generate Pydantic models from Console OpenAPI spec (merges PR #700, addresses #699)\n\nAdds a doit task that runs datamodel-code-generator against the Console\nOpenAPI 3.0.3 spec and emits a Pydantic v2 tree under\nsrc/pynetappfoundry/models/console/. Uses a separate pipeline (not\ntools/codegen/) because Console's SaaS control-plane domain is not a\nper-cluster cache entity. ADR-0008 amended with the split-pipeline\nrationale; no new ADR.\n\nAddresses #699\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-09T15:57:02+01:00",
          "tree_id": "a84fb41599aece05ec4d0936c4b77b53f6391489",
          "url": "https://github.com/endavis/pynetappfoundry/commit/add278a4dad94a52b19f93f653affd11661a0b32"
        },
        "date": 1778339017119,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1156926.5117936446,
            "unit": "iter/sec",
            "range": "stddev: 3.0193067715947796e-7",
            "extra": "mean: 864.3591358708229 nsec\nrounds: 62074"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 714769.7305711007,
            "unit": "iter/sec",
            "range": "stddev: 4.4780539385887833e-7",
            "extra": "mean: 1.399051970487055 usec\nrounds: 177620"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 449235.0922312253,
            "unit": "iter/sec",
            "range": "stddev: 5.648769757585244e-7",
            "extra": "mean: 2.2260059761433135 usec\nrounds: 162312"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 449259.61951368005,
            "unit": "iter/sec",
            "range": "stddev: 5.661149931826594e-7",
            "extra": "mean: 2.2258844475773096 usec\nrounds: 163640"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 486160.26862750953,
            "unit": "iter/sec",
            "range": "stddev: 7.887597917147383e-7",
            "extra": "mean: 2.0569348515935357 usec\nrounds: 88567"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 157789.82267283488,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014014171533861269",
            "extra": "mean: 6.33754435527457 usec\nrounds: 54334"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 140779.6430443365,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012447981723685394",
            "extra": "mean: 7.103299726971637 usec\nrounds: 67765"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 70613.40842742973,
            "unit": "iter/sec",
            "range": "stddev: 0.000001643239126050876",
            "extra": "mean: 14.161616359699053 usec\nrounds: 45123"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 234492.8997736062,
            "unit": "iter/sec",
            "range": "stddev: 9.124688325937775e-7",
            "extra": "mean: 4.264521445917814 usec\nrounds: 45370"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32059.937592912676,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028945631823215196",
            "extra": "mean: 31.19157662431211 usec\nrounds: 2832"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 46.43305201585647,
            "unit": "iter/sec",
            "range": "stddev: 0.0012232711848752364",
            "extra": "mean: 21.536383170731682 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 43.70125561947749,
            "unit": "iter/sec",
            "range": "stddev: 0.00367627267053206",
            "extra": "mean: 22.88263771428809 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 57.43509668788992,
            "unit": "iter/sec",
            "range": "stddev: 0.0009236877282933985",
            "extra": "mean: 17.410957022221712 msec\nrounds: 45"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.744334792029893,
            "unit": "iter/sec",
            "range": "stddev: 0.001551153344283654",
            "extra": "mean: 114.35975677777795 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 290.720140284072,
            "unit": "iter/sec",
            "range": "stddev: 0.00023977716127715446",
            "extra": "mean: 3.4397341684785507 msec\nrounds: 184"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 50.82758918764294,
            "unit": "iter/sec",
            "range": "stddev: 0.0013184508704823454",
            "extra": "mean: 19.674354341462987 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.060008651233137436,
            "unit": "iter/sec",
            "range": "stddev: 0.1916677574640839",
            "extra": "mean: 16.664263892799994 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06441969510851946,
            "unit": "iter/sec",
            "range": "stddev: 0.16875484578650157",
            "extra": "mean: 15.523202932200013 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 424138.5426854781,
            "unit": "iter/sec",
            "range": "stddev: 6.160775352906841e-7",
            "extra": "mean: 2.3577201771581384 usec\nrounds: 11954"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 400878.98074578424,
            "unit": "iter/sec",
            "range": "stddev: 5.98111725076759e-7",
            "extra": "mean: 2.4945184158561458 usec\nrounds: 80555"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 401042.2890663425,
            "unit": "iter/sec",
            "range": "stddev: 5.298955317570769e-7",
            "extra": "mean: 2.493502623696063 usec\nrounds: 89759"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 174011.74662816373,
            "unit": "iter/sec",
            "range": "stddev: 9.260279634425257e-7",
            "extra": "mean: 5.746738478160591 usec\nrounds: 42528"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 204955.1110717083,
            "unit": "iter/sec",
            "range": "stddev: 8.310326140866092e-7",
            "extra": "mean: 4.8791171626362955 usec\nrounds: 58645"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 446718.6098519117,
            "unit": "iter/sec",
            "range": "stddev: 5.239410069866089e-7",
            "extra": "mean: 2.238545648079229 usec\nrounds: 96247"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 458740.15427057876,
            "unit": "iter/sec",
            "range": "stddev: 5.120163162873635e-7",
            "extra": "mean: 2.1798832970923443 usec\nrounds: 93888"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35057.52980392514,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023658829289615514",
            "extra": "mean: 28.524542533171775 usec\nrounds: 16681"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 587057.8592630642,
            "unit": "iter/sec",
            "range": "stddev: 4.595781454010012e-7",
            "extra": "mean: 1.7034096115420436 usec\nrounds: 63902"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 264131.3361412667,
            "unit": "iter/sec",
            "range": "stddev: 6.810929446444039e-7",
            "extra": "mean: 3.785995310549464 usec\nrounds: 75273"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 385400.5055633245,
            "unit": "iter/sec",
            "range": "stddev: 5.678923174514026e-7",
            "extra": "mean: 2.594703394429491 usec\nrounds: 77979"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 236548.14318365217,
            "unit": "iter/sec",
            "range": "stddev: 7.503777719025579e-7",
            "extra": "mean: 4.22746924385543 usec\nrounds: 59517"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 208313.27679434756,
            "unit": "iter/sec",
            "range": "stddev: 8.647759601473132e-7",
            "extra": "mean: 4.800462147149779 usec\nrounds: 80496"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52737.961359489804,
            "unit": "iter/sec",
            "range": "stddev: 0.000002321265456398182",
            "extra": "mean: 18.96167341743591 usec\nrounds: 24787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26332.138720492545,
            "unit": "iter/sec",
            "range": "stddev: 0.00010199572590409587",
            "extra": "mean: 37.976406345670924 usec\nrounds: 15349"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36588.650559349,
            "unit": "iter/sec",
            "range": "stddev: 0.000002513666910340868",
            "extra": "mean: 27.330879513524 usec\nrounds: 9860"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 341.3017712311233,
            "unit": "iter/sec",
            "range": "stddev: 0.000044473490443978296",
            "extra": "mean: 2.92995842474787 msec\nrounds: 299"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.89821727500587,
            "unit": "iter/sec",
            "range": "stddev: 0.0003416625090658713",
            "extra": "mean: 31.349714354838223 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 827.3409880724652,
            "unit": "iter/sec",
            "range": "stddev: 0.0011611237063311082",
            "extra": "mean: 1.2086914759654237 msec\nrounds: 1061"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.729708861604237,
            "unit": "iter/sec",
            "range": "stddev: 0.0021320750730493775",
            "extra": "mean: 148.59483828571132 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6720199449326325,
            "unit": "iter/sec",
            "range": "stddev: 0.10025044062251111",
            "extra": "mean: 1.488051072799999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 791.8535105143244,
            "unit": "iter/sec",
            "range": "stddev: 0.0011614146239114856",
            "extra": "mean: 1.2628598430415248 msec\nrounds: 1013"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "0781a6dc920846a6f6c77209fe598282bf573f11",
          "message": "fix: bump urllib3 to 2.7.0 to resolve CVE-2026-44431/44432 (merges PR #722, addresses #721)\n\nurllib3 2.6.3 is affected by two known CVEs (CVE-2026-44431 and\nCVE-2026-44432), both fixed upstream in 2.7.0. The vulnerabilities were\nfailing the `Run dependency audit` step of `.github/workflows/ci.yml`\nacross every OS x Python combination, blocking PR #720 (Phase A of the\npyproject-template sync).\n\nurllib3 is a transitive dependency — no pyproject.toml change is\nrequired. `uv lock --upgrade-package urllib3` cleanly resolves to\n2.7.0 with no other package movement.\n\nAddresses #721\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-13T22:28:59+01:00",
          "tree_id": "920b42cbc674be9960012cf4dd5a7b00a7a1b169",
          "url": "https://github.com/endavis/pynetappfoundry/commit/0781a6dc920846a6f6c77209fe598282bf573f11"
        },
        "date": 1778708074030,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1212357.0994306956,
            "unit": "iter/sec",
            "range": "stddev: 2.968581349192848e-7",
            "extra": "mean: 824.839480438218 nsec\nrounds: 47502"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 732908.3419742808,
            "unit": "iter/sec",
            "range": "stddev: 7.051570491109989e-7",
            "extra": "mean: 1.3644270950801813 usec\nrounds: 177368"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 472300.68548367923,
            "unit": "iter/sec",
            "range": "stddev: 5.497171684222427e-7",
            "extra": "mean: 2.117295254348209 usec\nrounds: 145986"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 468859.81702950597,
            "unit": "iter/sec",
            "range": "stddev: 6.379665837741305e-7",
            "extra": "mean: 2.132833660891585 usec\nrounds: 161291"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 520951.8266222471,
            "unit": "iter/sec",
            "range": "stddev: 7.647829241717231e-7",
            "extra": "mean: 1.9195632856953597 usec\nrounds: 73579"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 165164.19128766053,
            "unit": "iter/sec",
            "range": "stddev: 9.827971301701095e-7",
            "extra": "mean: 6.054581154690704 usec\nrounds: 53626"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 145623.2522652683,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011238456433203049",
            "extra": "mean: 6.867035205190949 usec\nrounds: 71069"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 77899.18758493618,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014553293830427271",
            "extra": "mean: 12.837104352464078 usec\nrounds: 45078"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 242795.5126327839,
            "unit": "iter/sec",
            "range": "stddev: 7.514711793788085e-7",
            "extra": "mean: 4.118692265587503 usec\nrounds: 42007"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31515.134737942717,
            "unit": "iter/sec",
            "range": "stddev: 0.000002477902451468866",
            "extra": "mean: 31.730786122771924 usec\nrounds: 2623"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 54.28964161315921,
            "unit": "iter/sec",
            "range": "stddev: 0.003178478663212049",
            "extra": "mean: 18.419720047619744 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 45.16707825053817,
            "unit": "iter/sec",
            "range": "stddev: 0.0016807393943607887",
            "extra": "mean: 22.140019649999942 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 73.55142687305566,
            "unit": "iter/sec",
            "range": "stddev: 0.0010437589843234427",
            "extra": "mean: 13.595929304348184 msec\nrounds: 46"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.370278891833564,
            "unit": "iter/sec",
            "range": "stddev: 0.0004383663136183396",
            "extra": "mean: 119.47033222222103 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 304.93733271655384,
            "unit": "iter/sec",
            "range": "stddev: 0.00006930212039882898",
            "extra": "mean: 3.279362323699219 msec\nrounds: 173"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 34.99669709708814,
            "unit": "iter/sec",
            "range": "stddev: 0.006563624510554483",
            "extra": "mean: 28.574125073168805 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07472774490393103,
            "unit": "iter/sec",
            "range": "stddev: 0.17531679112905402",
            "extra": "mean: 13.381910577999998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07723775363050087,
            "unit": "iter/sec",
            "range": "stddev: 0.20035429306903801",
            "extra": "mean: 12.947036300200011 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 403840.676584751,
            "unit": "iter/sec",
            "range": "stddev: 6.791291191845768e-7",
            "extra": "mean: 2.476224060579835 usec\nrounds: 10756"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 387698.9820348106,
            "unit": "iter/sec",
            "range": "stddev: 5.272411156549167e-7",
            "extra": "mean: 2.5793206748998183 usec\nrounds: 74075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 385736.1561684625,
            "unit": "iter/sec",
            "range": "stddev: 4.847196184522371e-7",
            "extra": "mean: 2.5924455978746006 usec\nrounds: 36791"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 174588.23348056935,
            "unit": "iter/sec",
            "range": "stddev: 7.835809772734081e-7",
            "extra": "mean: 5.727762862732064 usec\nrounds: 44936"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 204778.4014477625,
            "unit": "iter/sec",
            "range": "stddev: 6.914479860183122e-7",
            "extra": "mean: 4.883327503926691 usec\nrounds: 60442"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 432244.20509894064,
            "unit": "iter/sec",
            "range": "stddev: 5.299287888056311e-7",
            "extra": "mean: 2.3135070134048417 usec\nrounds: 100453"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 440338.2904910108,
            "unit": "iter/sec",
            "range": "stddev: 4.978920365285929e-7",
            "extra": "mean: 2.270981246906608 usec\nrounds: 94118"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35611.10664282894,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019249598455911584",
            "extra": "mean: 28.081126768391837 usec\nrounds: 15619"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 588358.8470925917,
            "unit": "iter/sec",
            "range": "stddev: 5.086568926160596e-7",
            "extra": "mean: 1.6996430068852644 usec\nrounds: 53396"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 265699.16049254325,
            "unit": "iter/sec",
            "range": "stddev: 6.601642269549285e-7",
            "extra": "mean: 3.763655098293262 usec\nrounds: 63882"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 371599.9272182634,
            "unit": "iter/sec",
            "range": "stddev: 5.396544925775104e-7",
            "extra": "mean: 2.69106618907554 usec\nrounds: 58907"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 230048.47746738326,
            "unit": "iter/sec",
            "range": "stddev: 7.190109020097716e-7",
            "extra": "mean: 4.346909881817331 usec\nrounds: 51954"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 210203.22914881795,
            "unit": "iter/sec",
            "range": "stddev: 7.465794518009759e-7",
            "extra": "mean: 4.757300846658394 usec\nrounds: 72512"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53673.9159109253,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014990041174955411",
            "extra": "mean: 18.631023711024792 usec\nrounds: 23871"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26881.231272419118,
            "unit": "iter/sec",
            "range": "stddev: 0.00006428970094625305",
            "extra": "mean: 37.20067692829337 usec\nrounds: 14650"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36893.6779692244,
            "unit": "iter/sec",
            "range": "stddev: 0.000001909185679537286",
            "extra": "mean: 27.104914853817775 usec\nrounds: 7904"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 339.9299786788011,
            "unit": "iter/sec",
            "range": "stddev: 0.00006585459543036828",
            "extra": "mean: 2.94178231613075 msec\nrounds: 310"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.75406747167712,
            "unit": "iter/sec",
            "range": "stddev: 0.001359668796639292",
            "extra": "mean: 30.530559322585304 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 1004.2506722158282,
            "unit": "iter/sec",
            "range": "stddev: 0.0010603219667908639",
            "extra": "mean: 995.7673195214803 usec\nrounds: 1255"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 8.04893854082021,
            "unit": "iter/sec",
            "range": "stddev: 0.0016337510810323112",
            "extra": "mean: 124.2399845555408 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.8009184585604533,
            "unit": "iter/sec",
            "range": "stddev: 0.10303596627326767",
            "extra": "mean: 1.2485665541999993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 960.7158001577076,
            "unit": "iter/sec",
            "range": "stddev: 0.0010544933836624732",
            "extra": "mean: 1.0408905524774794 msec\nrounds: 1191"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e1230bc6b1127b5a984461fb9af7dde5ce2b73ae",
          "message": "chore: pyproject-template sync Phase A — foundation (merges PR #720, addresses #716)\n\n* fix: anchor pr_merge Addresses regex to start of line\n\nMid-sentence \"Addresses #N\" was triggering false matches, causing\nunintended issue closures via `doit pr_merge --auto-close`. The regex\nis now anchored to start-of-line and case-sensitive (\"Addresses\", not\n\"addresses\"). Lowercase, uppercase, and mid-sentence variants are\nignored to prevent misattribution.\n\nPorts upstream pyproject-template PR #544.\n\nAddresses #716\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* feat: support sync-exclude.toml for pyproject-template drift checks\n\nAdds `.config/pyproject_template/sync-exclude.toml` — a hand-managed\nlist of glob patterns for upstream template files the project\nintentionally does not adopt. Patterns are matched via\n`fnmatch.fnmatch` against upstream-relative paths; matched files land\nin a separate \"Skipped per project policy\" bucket instead of crowding\nthe actionable drift list. Pass `--show-excluded` to `manage.py check`\nto list the suppressed paths.\n\nThe file is deliberately separate from `settings.toml` — `manage.py\nsync` rewrites `settings.toml` and would clobber user-managed\nexcludes.\n\nInitial exclude set encodes known project divergences: absent\n`bootstrap.py`, the `src/package_name/{cli,core,logging}.py` template\nscaffold, `examples/**`, top-level `tests/test_*.py`, the example\nbenchmark suites, and the CBM (#717) and context-mode (#718) hook\nplumbing whose adoption is deferred to their own issues. Running\n`manage.py --show-excluded check` against the current upstream HEAD\nmoves 42 files from the drift list into the skipped bucket.\n\nPorts upstream pyproject-template PR #507.\n\nAddresses #716\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-14T01:09:19+01:00",
          "tree_id": "bdb68ab461a0bd4eedcee916a34c4d3b16af0d43",
          "url": "https://github.com/endavis/pynetappfoundry/commit/e1230bc6b1127b5a984461fb9af7dde5ce2b73ae"
        },
        "date": 1778717697112,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1224042.4706931007,
            "unit": "iter/sec",
            "range": "stddev: 2.660060550840997e-7",
            "extra": "mean: 816.9651167689965 nsec\nrounds: 47960"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 769592.3377542055,
            "unit": "iter/sec",
            "range": "stddev: 4.1782378063563816e-7",
            "extra": "mean: 1.299389236278211 usec\nrounds: 184230"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 485113.5662650689,
            "unit": "iter/sec",
            "range": "stddev: 5.480554095618217e-7",
            "extra": "mean: 2.0613729846787963 usec\nrounds: 157481"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 473398.2337893257,
            "unit": "iter/sec",
            "range": "stddev: 5.107555385904332e-7",
            "extra": "mean: 2.112386419348209 usec\nrounds: 165618"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 529547.5745209403,
            "unit": "iter/sec",
            "range": "stddev: 6.253293911268548e-7",
            "extra": "mean: 1.8884044571531813 usec\nrounds: 79064"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 167774.092971923,
            "unit": "iter/sec",
            "range": "stddev: 7.996340040346035e-7",
            "extra": "mean: 5.960395805372347 usec\nrounds: 52114"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 145440.1440795713,
            "unit": "iter/sec",
            "range": "stddev: 9.111545151298825e-7",
            "extra": "mean: 6.8756807573904295 usec\nrounds: 72459"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 79571.57309019029,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013185593384187723",
            "extra": "mean: 12.567302130203602 usec\nrounds: 45348"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 241265.67880136622,
            "unit": "iter/sec",
            "range": "stddev: 7.129912540188421e-7",
            "extra": "mean: 4.1448083497334025 usec\nrounds: 42708"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31643.44952165859,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021709136412210617",
            "extra": "mean: 31.602117187493818 usec\nrounds: 2816"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 63.056068494878474,
            "unit": "iter/sec",
            "range": "stddev: 0.0020419486607210447",
            "extra": "mean: 15.85890182926996 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 56.02906362546984,
            "unit": "iter/sec",
            "range": "stddev: 0.0023852850769443003",
            "extra": "mean: 17.847879926828142 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 51.30478103412255,
            "unit": "iter/sec",
            "range": "stddev: 0.001389649139046863",
            "extra": "mean: 19.49136084091081 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.535613891551247,
            "unit": "iter/sec",
            "range": "stddev: 0.0002576399602974967",
            "extra": "mean: 117.15618966666517 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 294.18346170140563,
            "unit": "iter/sec",
            "range": "stddev: 0.00005715307316667665",
            "extra": "mean: 3.3992393529415796 msec\nrounds: 170"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 74.3582325484109,
            "unit": "iter/sec",
            "range": "stddev: 0.000831957650720406",
            "extra": "mean: 13.448410024390379 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07475919136177496,
            "unit": "iter/sec",
            "range": "stddev: 0.2544127333706279",
            "extra": "mean: 13.376281655599996 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.0759943117937839,
            "unit": "iter/sec",
            "range": "stddev: 0.26145225533393085",
            "extra": "mean: 13.158879610799989 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 396519.1115181507,
            "unit": "iter/sec",
            "range": "stddev: 6.115483606102327e-7",
            "extra": "mean: 2.5219465366279703 usec\nrounds: 11260"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 379092.0235868452,
            "unit": "iter/sec",
            "range": "stddev: 5.618012548770667e-7",
            "extra": "mean: 2.637881933094571 usec\nrounds: 58255"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 372028.40317522944,
            "unit": "iter/sec",
            "range": "stddev: 6.087319959576678e-7",
            "extra": "mean: 2.6879668096980995 usec\nrounds: 88520"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 172175.4823243713,
            "unit": "iter/sec",
            "range": "stddev: 8.99519054646142e-7",
            "extra": "mean: 5.808027870751322 usec\nrounds: 42984"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 199800.52620488117,
            "unit": "iter/sec",
            "range": "stddev: 7.075063929627151e-7",
            "extra": "mean: 5.004991823567929 usec\nrounds: 53568"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 419734.9190056514,
            "unit": "iter/sec",
            "range": "stddev: 5.937145831856619e-7",
            "extra": "mean: 2.382456056715491 usec\nrounds: 85485"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 428415.2853782002,
            "unit": "iter/sec",
            "range": "stddev: 4.637028241380557e-7",
            "extra": "mean: 2.3341837561122762 usec\nrounds: 90778"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34975.25679143329,
            "unit": "iter/sec",
            "range": "stddev: 0.000001875703477156012",
            "extra": "mean: 28.591641398468195 usec\nrounds: 15474"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 556770.6641779601,
            "unit": "iter/sec",
            "range": "stddev: 4.6637029191295515e-7",
            "extra": "mean: 1.7960716401544656 usec\nrounds: 57091"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 258092.6826490105,
            "unit": "iter/sec",
            "range": "stddev: 6.327568005733589e-7",
            "extra": "mean: 3.8745771082550826 usec\nrounds: 71886"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 368470.0820826028,
            "unit": "iter/sec",
            "range": "stddev: 5.498080228929053e-7",
            "extra": "mean: 2.713924545374141 usec\nrounds: 73965"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 228740.3674990614,
            "unit": "iter/sec",
            "range": "stddev: 6.6379823560735e-7",
            "extra": "mean: 4.371768791549674 usec\nrounds: 55504"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 206533.7915516858,
            "unit": "iter/sec",
            "range": "stddev: 7.335594703435597e-7",
            "extra": "mean: 4.841822698779762 usec\nrounds: 78629"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52475.59785916116,
            "unit": "iter/sec",
            "range": "stddev: 0.000001468328587540257",
            "extra": "mean: 19.0564765490408 usec\nrounds: 23645"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26687.325325673235,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021781933924292224",
            "extra": "mean: 37.470971249336806 usec\nrounds: 14817"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35965.96867550988,
            "unit": "iter/sec",
            "range": "stddev: 0.000002150687012935167",
            "extra": "mean: 27.804061362065436 usec\nrounds: 8458"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 336.41926804885594,
            "unit": "iter/sec",
            "range": "stddev: 0.000250793876349356",
            "extra": "mean: 2.972481349833912 msec\nrounds: 303"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.31517117375342,
            "unit": "iter/sec",
            "range": "stddev: 0.00045805828764419835",
            "extra": "mean: 30.945217483861143 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 999.5188615274036,
            "unit": "iter/sec",
            "range": "stddev: 0.0010632590553434453",
            "extra": "mean: 1.0004813700782607 msec\nrounds: 1270"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.94721179359238,
            "unit": "iter/sec",
            "range": "stddev: 0.0008517719783441743",
            "extra": "mean: 125.83029444443305 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7541643594283917,
            "unit": "iter/sec",
            "range": "stddev: 0.12067909068425138",
            "extra": "mean: 1.3259709073999943 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 951.0344582835946,
            "unit": "iter/sec",
            "range": "stddev: 0.001061272495524416",
            "extra": "mean: 1.051486611541686 msec\nrounds: 1161"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "951f31dc87707c1e85c75578d16cacd2aa91554a",
          "message": "chore: pyproject-template sync Phase B (merges PR #723, addresses #716)\n\n* chore: sync template state to 36bcb77fe1df2d644e7ae6a4e2339d786175f388\n\n* chore: sync template framework code and docs from pyproject-template\n\nPulls upstream changes for framework code and docs across 67 files:\n\n- tools/doit/ (5 files): base.py, git.py, install_tools.py, quality.py,\n  release.py — picks up #555 transient gh retries, #545\n  install_check_or_skip pattern, #561 CI parallelization, doit-task\n  wording tweaks.\n- tools/pyproject_template/cleanup.py: cleanup mechanism updates.\n- docs/ (31 files + TOC): all template-shipped doc pages\n  (development/, template/, decisions/9XXX ADRs, examples/, deployment/,\n  etc.). TABLE_OF_CONTENTS.md regenerated to include the new pages from\n  the new-files commit.\n- .github/ (12 files): CONTRIBUTING.md, CODEOWNERS, SECURITY.md,\n  dependabot.yml, python-versions.json, ISSUE_TEMPLATE/config.yml,\n  workflows/breaking-change-detection.yml, workflows/codeql.yml\n  (v3 -> v4 bump per #501), workflows/dependabot-automerge.yml,\n  workflows/pr-checks.yml, workflows/release.yml, workflows/testpypi.yml.\n- .claude/ (4 files): agents/implement-worker.md, lsp-setup.md,\n  settings.json (wires PreCompact + SessionStart hooks per #513),\n  statusline-command.sh.\n- .codex/config.toml, .copilot/README.md, .gemini/settings.json.\n- tests/template/test_doit_github.py: replaces Phase A's minimal stub\n  with the full upstream test suite (now imports cleanly thanks to\n  #555 retry symbols arriving in this same sync).\n- tests/conftest.py: test config sync.\n- .envrc, .envrc.local.example, .gitignore, .python-version, LICENSE,\n  .pre-commit-config.yaml: misc config updates.\n\n.pre-commit-config.yaml: adopts upstream's stage cleanups and adds the\nuv-lock-check hook (#557); the docs/example-config/apis/ exclusions on\ntrailing-whitespace, end-of-file-fixer, check-added-large-files,\ndetect-private-key, and codespell hooks are preserved.\n\nAddresses #716\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* chore: bring in cross-agent delegation skills and new template assets\n\nAdds 117 new files from upstream pyproject-template covering the\ncross-agent delegation matrix and ancillary tooling:\n\n- .agents/skills/ (23 files): codex-* self-action skills,\n  delegate-{claude,gemini,copilot}-* bridges, multi-* orchestrators,\n  ghi-finalize, checkpoint/restore skills.\n- .claude/commands/ (16 files): {claude,gemini,codex,copilot}/* bridge\n  commands plus ghi-finalize, ghi-status, multi-*, checkpoint, restore.\n- .claude/rules/README.md: rule-scaffold pattern doc (loading is opt-in).\n- .gemini/commands/ (19 files): TOML-format equivalents under\n  {claude,gemini,codex,copilot}/, multi-*, checkpoint, restore,\n  ghi-finalize.\n- .gemini/policies/developer.toml: Gemini Policy Engine config.\n- .gemini/rules/README.md: rule-scaffold mirror.\n- .copilot/commands/ (19 files): {claude,gemini,codex,copilot}/* bridges\n  plus multi-*.\n- .github/instructions/README.md: per-stack instruction file doc for\n  Copilot CLI.\n- docs/development/ai/ (4 files): auto-checkpoint-hook,\n  cross-agent-delegation matrix, lsp-tool guide, token-efficiency add-ons\n  walkthrough.\n- tests/template/ (16 files): template framework test coverage\n  (test_doit_* per-module suites, test_ai_agent_assets, test_cleanup,\n  test_repo_settings, test_setup_repo, test_templates, test_utils,\n  test_pyproject_template_main).\n- tools/hooks/ai/ (3 files): bash-ban-raw-tools.py (disabled by\n  default), precompact-checkpoint.py + session-resume-restore.py\n  wired in .claude/settings.json for auto-checkpoint behavior (per\n  #513 — to be evaluated in real session).\n- tools/statusline/claude-usage.sh: Claude Max usage helper.\n\nCBM and context-mode hook files are kept out via sync-exclude rules\n(tracked separately in #717 and #718).\n\nAddresses #716\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* chore: hand-merge customized files for pyproject-template Phase B sync\n\nAdopts upstream's structural changes to 6 customized files while\npreserving project-specific content:\n\n- AGENTS.md: takes upstream's AI Config Directories restructure (per\n  #550/#558 cross-agent delegation) and updated Slash Commands &\n  Workflows reference line. Preserves project's `Cache Schema Pitfalls`\n  section under Common Pitfalls (ADR-0018 contract).\n- .claude/CLAUDE.md: adopts the rule-scaffold opt-in comments at the\n  top. Keeps project's `src/pynetappfoundry/cli.py` example path\n  (upstream generalized to `__PACKAGE_NAME__`).\n- .github/workflows/ci.yml: adopts upstream's restructure (separate\n  `lint` job using doit tasks + parallelized `pytest -n auto` via\n  #561). Preserves SOPS install steps across Linux/macOS/Windows and\n  updates `--cov=package_name` -> `--cov=pynetappfoundry`.\n- tools/doit/security.py: adopts upstream's `install_check_or_skip`\n  pattern. Adds `--ignore-vuln GHSA-r374-rxx8-8654` to the pip-audit\n  invocation to keep `doit audit` clean against the paramiko CVE\n  (matches the existing CI suppression tracked in #701).\n- tools/doit/github.py: takes upstream's full revision (includes #555\n  transient retries, #544 anchored Addresses regex, and other\n  refinements). Drops one unused `noqa: ANN401` directive that this\n  project's ruff config rejects.\n- tests/test_codeql_workflow.py: renames `test_analyze_uses_codeql_*_v3`\n  to `*_v4` and updates assertions to match upstream's CodeQL\n  v3 -> v4 bump (#501). Test failure was a signal that the workflow\n  pin moved, not a regression.\n\nAddresses #716\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* chore: expand sync-exclude.toml for Phase B divergences\n\nAdds 9 new exclude patterns covering project-content files,\npackage-mapping artifacts, and tests whose targets don't exist locally:\n\n- README.md, CHANGELOG.md: 100% project-owned content. Upstream's are\n  template scaffolds.\n- mkdocs.yml: project-specific metadata (site_name, site_url) plus a\n  custom nav structure (ONTAP usage pages, project ADRs). Upstream nav\n  improvements can be pulled in by hand if needed.\n- src/package_name/__init__.py: heavily project-customized (re-exports\n  ONTAP/DII clients, config, logging, DBs). Upstream's is a 6-line\n  scaffold exporting `greet`/`setup_logging`.\n- tests/template/test_properties.py: Hypothesis property tests for\n  upstream's example `package_name.core.greet`, which we exclude.\n- tests/template/test_bootstrap.py: imports the absent `bootstrap.py`\n  module (excluded since Phase A).\n- tests/benchmarks/conftest.py + tests/benchmarks/__init__.py: project\n  owns the benchmark fixtures (QEVolume, QENode) that the bulk-copy\n  initially stripped. Excluding the whole directory keeps upstream from\n  clobbering the project fixtures going forward.\n\nAfter Phase B, `manage.py --show-excluded check` reports 8 different\nfiles (all documented project divergences) and 47 skipped per project\npolicy.\n\nAddresses #716\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* fix: restore project user-facing docs clobbered by Phase B bulk-copy\n\nPhase B's bulk-overwrite stage applied upstream's template versions over\nthe project's user-facing documentation, which references concrete\n`pynetappfoundry.*` modules. The upstream versions reference a fictional\n`package_name` module, which broke mkdocstrings in the docs CI job:\n\n  ERROR -  Could not collect 'package_name'\n\nEight pages restored from main and added to sync-exclude.toml so future\nsyncs leave them alone:\n\n- docs/index.md\n- docs/deployment/{development,production}.md\n- docs/examples/{README,api}.md\n- docs/getting-started/installation.md\n- docs/reference/api.md\n- docs/usage/basics.md\n\n`docs/examples/add-a-feature.md` and `docs/usage/cli.md` carry no\nproject-specific references and remain on the upstream version.\n\nAddresses #716\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-14T02:06:29+01:00",
          "tree_id": "d6bca5eb404c1c27917fe623bb0419cc22ae58ec",
          "url": "https://github.com/endavis/pynetappfoundry/commit/951f31dc87707c1e85c75578d16cacd2aa91554a"
        },
        "date": 1778721128754,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1209244.0681688872,
            "unit": "iter/sec",
            "range": "stddev: 3.1428438618873345e-7",
            "extra": "mean: 826.9629153643585 nsec\nrounds: 47459"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 765445.120074943,
            "unit": "iter/sec",
            "range": "stddev: 4.906506195410894e-7",
            "extra": "mean: 1.3064293883042748 usec\nrounds: 169809"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 485005.5009906884,
            "unit": "iter/sec",
            "range": "stddev: 5.575654574938376e-7",
            "extra": "mean: 2.0618322842882537 usec\nrounds: 163962"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 472091.6293794246,
            "unit": "iter/sec",
            "range": "stddev: 7.161897825005935e-7",
            "extra": "mean: 2.1182328551652634 usec\nrounds: 156986"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 532830.9928663085,
            "unit": "iter/sec",
            "range": "stddev: 5.403840764203119e-7",
            "extra": "mean: 1.876767705685821 usec\nrounds: 71220"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 168310.8687018864,
            "unit": "iter/sec",
            "range": "stddev: 9.343995091126444e-7",
            "extra": "mean: 5.941386956841202 usec\nrounds: 53944"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 147868.13105730427,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012302807098317886",
            "extra": "mean: 6.76278243898588 usec\nrounds: 68914"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 80290.46018442296,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013605541756975334",
            "extra": "mean: 12.454779779603362 usec\nrounds: 44737"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 246323.56005550254,
            "unit": "iter/sec",
            "range": "stddev: 7.50181553060405e-7",
            "extra": "mean: 4.059700987492533 usec\nrounds: 40102"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32893.45153169536,
            "unit": "iter/sec",
            "range": "stddev: 0.000002157232612642137",
            "extra": "mean: 30.401187878882926 usec\nrounds: 2640"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 47.55550494258974,
            "unit": "iter/sec",
            "range": "stddev: 0.0013577199140329542",
            "extra": "mean: 21.028059763159415 msec\nrounds: 38"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 43.506499297178856,
            "unit": "iter/sec",
            "range": "stddev: 0.0008529539543292439",
            "extra": "mean: 22.985071567567935 msec\nrounds: 37"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 57.93739573218351,
            "unit": "iter/sec",
            "range": "stddev: 0.002911535341465097",
            "extra": "mean: 17.26000948718018 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.029044272781515,
            "unit": "iter/sec",
            "range": "stddev: 0.0010991325326710924",
            "extra": "mean: 124.54782487499827 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 299.2286262821382,
            "unit": "iter/sec",
            "range": "stddev: 0.00010279914198113616",
            "extra": "mean: 3.341926246913004 msec\nrounds: 162"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 60.533741225399886,
            "unit": "iter/sec",
            "range": "stddev: 0.0018313739015827675",
            "extra": "mean: 16.519712473684034 msec\nrounds: 38"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07242900594470111,
            "unit": "iter/sec",
            "range": "stddev: 0.3583892068277304",
            "extra": "mean: 13.806623285200004 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07766913188707723,
            "unit": "iter/sec",
            "range": "stddev: 0.2392111087551674",
            "extra": "mean: 12.875127810799984 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 400417.1644653588,
            "unit": "iter/sec",
            "range": "stddev: 6.929852754687254e-7",
            "extra": "mean: 2.497395438417857 usec\nrounds: 11400"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 387522.8826821997,
            "unit": "iter/sec",
            "range": "stddev: 6.452563468484702e-7",
            "extra": "mean: 2.5804927778163784 usec\nrounds: 77400"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 386087.5735220696,
            "unit": "iter/sec",
            "range": "stddev: 5.779589046215207e-7",
            "extra": "mean: 2.5900859509088496 usec\nrounds: 98184"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176069.85926596503,
            "unit": "iter/sec",
            "range": "stddev: 7.555566786476216e-7",
            "extra": "mean: 5.679563805917711 usec\nrounds: 47190"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 205351.66622891533,
            "unit": "iter/sec",
            "range": "stddev: 7.990424568237245e-7",
            "extra": "mean: 4.869695086307467 usec\nrounds: 59935"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 428613.3752331902,
            "unit": "iter/sec",
            "range": "stddev: 4.6547217405326995e-7",
            "extra": "mean: 2.333104979414006 usec\nrounds: 92542"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 437804.80746027565,
            "unit": "iter/sec",
            "range": "stddev: 4.7672248007182606e-7",
            "extra": "mean: 2.2841229309496223 usec\nrounds: 95094"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35372.98637653198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019732653061110244",
            "extra": "mean: 28.270160436989414 usec\nrounds: 15277"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 600459.2126418188,
            "unit": "iter/sec",
            "range": "stddev: 4.1487583010468473e-7",
            "extra": "mean: 1.6653920515272567 usec\nrounds: 51256"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 260307.85417337655,
            "unit": "iter/sec",
            "range": "stddev: 7.437498487497434e-7",
            "extra": "mean: 3.841605176207844 usec\nrounds: 63598"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 376571.45783515146,
            "unit": "iter/sec",
            "range": "stddev: 5.382256126682129e-7",
            "extra": "mean: 2.655538488627998 usec\nrounds: 62720"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 234225.07315373808,
            "unit": "iter/sec",
            "range": "stddev: 8.240979289468691e-7",
            "extra": "mean: 4.26939774865021 usec\nrounds: 52860"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209250.54370945817,
            "unit": "iter/sec",
            "range": "stddev: 7.195818187201936e-7",
            "extra": "mean: 4.778960103389207 usec\nrounds: 67650"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54277.48625594337,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015215637996639727",
            "extra": "mean: 18.423845114796567 usec\nrounds: 23243"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 27612.037577228548,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022383386355411485",
            "extra": "mean: 36.21608862450241 usec\nrounds: 14962"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36451.01343361016,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018819246968410458",
            "extra": "mean: 27.43407948921212 usec\nrounds: 7523"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 340.1139832352835,
            "unit": "iter/sec",
            "range": "stddev: 0.000019936930688148886",
            "extra": "mean: 2.9401907868875288 msec\nrounds: 305"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.08985786264006,
            "unit": "iter/sec",
            "range": "stddev: 0.0014311069123976983",
            "extra": "mean: 31.162493903228814 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 916.397876987094,
            "unit": "iter/sec",
            "range": "stddev: 0.0012653995359834937",
            "extra": "mean: 1.0912290666667308 msec\nrounds: 675"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 8.010161555667032,
            "unit": "iter/sec",
            "range": "stddev: 0.0005529073641450614",
            "extra": "mean: 124.84142711110735 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.77112311163433,
            "unit": "iter/sec",
            "range": "stddev: 0.14649457634707455",
            "extra": "mean: 1.2968097894000152 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 963.0575261536032,
            "unit": "iter/sec",
            "range": "stddev: 0.001065387003267156",
            "extra": "mean: 1.0383595713061327 msec\nrounds: 1164"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "04cb9525ab79e0f7045664d526f563bb2423ba2e",
          "message": "fix: point breaking-change-detection workflow at pynetappfoundry module (merges PR #727, addresses #726)\n\nThe Phase B template sync (#723 / 951f31dc) bulk-overwrote\n.github/workflows/breaking-change-detection.yml from upstream without\napplying the package_name -> pynetappfoundry mapping. The workflow then\ninvoked `griffe check package_name` on every PR and failed with:\n\n  ModuleNotFoundError: package_name\n\nsurfacing as a false-positive \"Breaking changes detected but not\ndocumented!\" gate on every PR. First reproduced on PR #715.\n\nFix: change `griffe check package_name` -> `griffe check pynetappfoundry`\non line 38.\n\nNot adopting a sync-exclude entry for this file — the override is a\nsingle line and upstream may add useful improvements (newer griffe\nflags, better diff handling, security fixes) that we want. Future\ntemplate syncs will flag this file as drift; the one-line module-name\noverride is re-applied as part of the hand-merge pass (same pattern as\nci.yml, AGENTS.md, .pre-commit-config.yaml).\n\nAddresses #726\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-14T02:24:40+01:00",
          "tree_id": "15288b4f0fba4e05d269c138ddf8de4e763fc5fb",
          "url": "https://github.com/endavis/pynetappfoundry/commit/04cb9525ab79e0f7045664d526f563bb2423ba2e"
        },
        "date": 1778722284789,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1165489.2707951674,
            "unit": "iter/sec",
            "range": "stddev: 3.5965490885439704e-7",
            "extra": "mean: 858.0087565437127 nsec\nrounds: 56073"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 693505.7535242026,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019296564623121123",
            "extra": "mean: 1.4419491041253505 usec\nrounds: 180506"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 458572.6571767308,
            "unit": "iter/sec",
            "range": "stddev: 5.72390607952647e-7",
            "extra": "mean: 2.180679515775418 usec\nrounds: 167197"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 463634.71276647947,
            "unit": "iter/sec",
            "range": "stddev: 5.459598632519878e-7",
            "extra": "mean: 2.1568704250660224 usec\nrounds: 153093"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 497057.2756791839,
            "unit": "iter/sec",
            "range": "stddev: 5.485356767827366e-7",
            "extra": "mean: 2.0118405844348426 usec\nrounds: 83599"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 160181.46170252253,
            "unit": "iter/sec",
            "range": "stddev: 9.480625113645916e-7",
            "extra": "mean: 6.242919682285882 usec\nrounds: 54633"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 140849.0693164704,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010453717336444356",
            "extra": "mean: 7.099798421479973 usec\nrounds: 69804"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 73417.66275292824,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013430715997753616",
            "extra": "mean: 13.620700557647693 usec\nrounds: 45204"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 233778.81851324686,
            "unit": "iter/sec",
            "range": "stddev: 8.087106238475865e-7",
            "extra": "mean: 4.277547497072905 usec\nrounds: 43266"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 27169.95674134766,
            "unit": "iter/sec",
            "range": "stddev: 0.000011442520804188278",
            "extra": "mean: 36.80535856276077 usec\nrounds: 2867"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 44.70709065412373,
            "unit": "iter/sec",
            "range": "stddev: 0.0013070842386047295",
            "extra": "mean: 22.36781649999319 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 52.64697495481694,
            "unit": "iter/sec",
            "range": "stddev: 0.0032968137629940746",
            "extra": "mean: 18.99444366667272 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 65.8550493289518,
            "unit": "iter/sec",
            "range": "stddev: 0.002259229054063157",
            "extra": "mean: 15.184864489356187 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.328473661239107,
            "unit": "iter/sec",
            "range": "stddev: 0.0037185950216997057",
            "extra": "mean: 120.07002011113046 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 304.05818946658354,
            "unit": "iter/sec",
            "range": "stddev: 0.00005534352226513893",
            "extra": "mean: 3.28884415760787 msec\nrounds: 184"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 49.78514220390803,
            "unit": "iter/sec",
            "range": "stddev: 0.0028796749239237",
            "extra": "mean: 20.08631402325295 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.058545596194987407,
            "unit": "iter/sec",
            "range": "stddev: 0.42403856151476693",
            "extra": "mean: 17.080704015200013 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06336765985761153,
            "unit": "iter/sec",
            "range": "stddev: 0.17527628115416102",
            "extra": "mean: 15.780920460800052 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 421286.30910344335,
            "unit": "iter/sec",
            "range": "stddev: 5.894081777974037e-7",
            "extra": "mean: 2.3736826438251484 usec\nrounds: 12560"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 402052.63575588306,
            "unit": "iter/sec",
            "range": "stddev: 5.654001740923499e-7",
            "extra": "mean: 2.487236523446588 usec\nrounds: 66099"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 401448.4936974763,
            "unit": "iter/sec",
            "range": "stddev: 5.957419651212215e-7",
            "extra": "mean: 2.490979579446574 usec\nrounds: 88098"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 171820.2321173366,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012745827562183979",
            "extra": "mean: 5.820036369856007 usec\nrounds: 46577"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 205541.44691386775,
            "unit": "iter/sec",
            "range": "stddev: 7.972821574015894e-7",
            "extra": "mean: 4.8651987957399685 usec\nrounds: 61958"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 442374.7717687942,
            "unit": "iter/sec",
            "range": "stddev: 5.305069144193774e-7",
            "extra": "mean: 2.2605267384520897 usec\nrounds: 92507"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 451274.58307663334,
            "unit": "iter/sec",
            "range": "stddev: 5.42263039093828e-7",
            "extra": "mean: 2.2159457622947594 usec\nrounds: 86491"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34644.42302171596,
            "unit": "iter/sec",
            "range": "stddev: 0.000005066729113110546",
            "extra": "mean: 28.86467468005387 usec\nrounds: 16267"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 591731.7026040098,
            "unit": "iter/sec",
            "range": "stddev: 4.343392524469981e-7",
            "extra": "mean: 1.6899550853864016 usec\nrounds: 57465"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 265281.5603131427,
            "unit": "iter/sec",
            "range": "stddev: 7.094223900215153e-7",
            "extra": "mean: 3.769579758274882 usec\nrounds: 64313"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 381398.86069196515,
            "unit": "iter/sec",
            "range": "stddev: 5.804186708574066e-7",
            "extra": "mean: 2.621927077038767 usec\nrounds: 62422"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 233856.02566916312,
            "unit": "iter/sec",
            "range": "stddev: 7.694049237343171e-7",
            "extra": "mean: 4.27613527228374 usec\nrounds: 54660"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 211518.16871423536,
            "unit": "iter/sec",
            "range": "stddev: 7.802439550182994e-7",
            "extra": "mean: 4.727726256702879 usec\nrounds: 69945"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53081.30253351373,
            "unit": "iter/sec",
            "range": "stddev: 0.000001815460249961982",
            "extra": "mean: 18.839025273892517 usec\nrounds: 24651"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26883.147302345587,
            "unit": "iter/sec",
            "range": "stddev: 0.000003040792480603305",
            "extra": "mean: 37.198025541925624 usec\nrounds: 15151"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35750.21391942965,
            "unit": "iter/sec",
            "range": "stddev: 0.000002936109929735909",
            "extra": "mean: 27.97186059511987 usec\nrounds: 8981"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 331.8262340767828,
            "unit": "iter/sec",
            "range": "stddev: 0.0000352149231946776",
            "extra": "mean: 3.013625498243775 msec\nrounds: 283"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.718398498990464,
            "unit": "iter/sec",
            "range": "stddev: 0.0006438143894871236",
            "extra": "mean: 32.55378043334076 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 780.2903852692552,
            "unit": "iter/sec",
            "range": "stddev: 0.0012097253118892575",
            "extra": "mean: 1.281574166334152 msec\nrounds: 998"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.399955277843256,
            "unit": "iter/sec",
            "range": "stddev: 0.0014008099729841638",
            "extra": "mean: 156.2510918571596 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6163761167922908,
            "unit": "iter/sec",
            "range": "stddev: 0.1172395423439732",
            "extra": "mean: 1.622386028200026 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 745.3495337931596,
            "unit": "iter/sec",
            "range": "stddev: 0.0012118799343868035",
            "extra": "mean: 1.3416524122728009 msec\nrounds: 929"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4448a4ed48fb527d6094354a2d8d6fbcbc535c9a",
          "message": "chore: memoize Pydantic takes_validated_data_argument to cut model-batch cost ~17x (merges PR #729, addresses #728)\n\nPydantic 2.13.4's `_internal._fields.takes_validated_data_argument`\ncalls `inspect.signature` on every `model_post_init` call, per\n`default_factory` field. For a model with ~155 default_factory fields\n(e.g., `OntapVolume`), a batch deserialization of 500 instances triggers\n~123k `inspect.signature` calls and burns ~16 of 17.6 seconds total wall\ntime. The function is deterministic for a given factory callable, so a\n`functools.cache` wrapper is safe.\n\nMeasurements (local dev box):\n\n- Single `LazyClusterMetadata.storage` access on a 500-volume DB:\n  17,600 ms -> 671 ms (~26x faster).\n- Two slow lazy benchmarks (5 rounds each): 171s -> 18.5s (~9x faster).\n- `doit check` wall time: 108s -> 23.4s (~4.6x faster).\n- Cache hit rate: 99.7% (617k hits / 1.8k misses) — the work is wildly\n  repetitive across model instances.\n\nImplementation:\n\n- `src/pynetappfoundry/_perf_patches.py` applies the wrapper at import\n  time. The patch is idempotent (re-running is a no-op) and reversible\n  the moment Pydantic ships an upstream fix.\n- `src/pynetappfoundry/__init__.py` imports `_perf_patches` as its\n  first project-level import; Python guarantees `__init__.py` runs\n  before any submodule import, so importing any `pynetappfoundry.*`\n  module also applies the patches first.\n- `tests/unit/test_perf_patches.py` covers patch application, contract\n  correctness, end-to-end Pydantic validation, and common factory\n  shapes.\n\nAddresses #728\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-14T03:00:20+01:00",
          "tree_id": "40f0e67e1895536273e223629d791adaec587305",
          "url": "https://github.com/endavis/pynetappfoundry/commit/4448a4ed48fb527d6094354a2d8d6fbcbc535c9a"
        },
        "date": 1778724089992,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1162965.9815867525,
            "unit": "iter/sec",
            "range": "stddev: 2.7289587638777654e-7",
            "extra": "mean: 859.8703795579631 nsec\nrounds: 56488"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 722436.7586719333,
            "unit": "iter/sec",
            "range": "stddev: 4.377787178451336e-7",
            "extra": "mean: 1.384204206107003 usec\nrounds: 180832"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 450730.54480292526,
            "unit": "iter/sec",
            "range": "stddev: 7.444773612774324e-7",
            "extra": "mean: 2.218620440816218 usec\nrounds: 159211"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 454304.51068296516,
            "unit": "iter/sec",
            "range": "stddev: 6.148213187812151e-7",
            "extra": "mean: 2.2011667867806985 usec\nrounds: 158178"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 497107.86433815793,
            "unit": "iter/sec",
            "range": "stddev: 5.335037536451706e-7",
            "extra": "mean: 2.011635847546659 usec\nrounds: 84374"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 158564.4917234725,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010056783398498816",
            "extra": "mean: 6.306582193344671 usec\nrounds: 56361"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 139619.1659979809,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010510892890830933",
            "extra": "mean: 7.16234044840564 usec\nrounds: 70742"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 72548.04516514232,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015678501270834953",
            "extra": "mean: 13.783968923265723 usec\nrounds: 45082"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 223619.34004312783,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011286963425598174",
            "extra": "mean: 4.471885123205968 usec\nrounds: 44761"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30041.605219784637,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029233725867453133",
            "extra": "mean: 33.28716933346243 usec\nrounds: 3000"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 62.472485965674586,
            "unit": "iter/sec",
            "range": "stddev: 0.0004948442263635947",
            "extra": "mean: 16.0070466949154 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 58.871709496323255,
            "unit": "iter/sec",
            "range": "stddev: 0.0006361478416422486",
            "extra": "mean: 16.986087350876968 msec\nrounds: 57"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 70.0237087515426,
            "unit": "iter/sec",
            "range": "stddev: 0.0006581564514523377",
            "extra": "mean: 14.280877403226238 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.479273070938484,
            "unit": "iter/sec",
            "range": "stddev: 0.0006160096424384678",
            "extra": "mean: 87.11353008333352 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 309.72105730331583,
            "unit": "iter/sec",
            "range": "stddev: 0.00007837551806656699",
            "extra": "mean: 3.2287116953132466 msec\nrounds: 256"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 57.60190292987585,
            "unit": "iter/sec",
            "range": "stddev: 0.0006096884411706246",
            "extra": "mean: 17.36053757143046 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2606770543828751,
            "unit": "iter/sec",
            "range": "stddev: 0.13875617958725084",
            "extra": "mean: 793.2245585999965 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.1656939234527732,
            "unit": "iter/sec",
            "range": "stddev: 0.1622332072788848",
            "extra": "mean: 857.8581219999933 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 412849.00328347844,
            "unit": "iter/sec",
            "range": "stddev: 7.544724637620983e-7",
            "extra": "mean: 2.4221930828142524 usec\nrounds: 12606"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 394446.14630255214,
            "unit": "iter/sec",
            "range": "stddev: 5.877892089781164e-7",
            "extra": "mean: 2.5352003293067282 usec\nrounds: 72276"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 388834.7594572981,
            "unit": "iter/sec",
            "range": "stddev: 6.177062195384663e-7",
            "extra": "mean: 2.571786538311836 usec\nrounds: 82352"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 173651.19411677652,
            "unit": "iter/sec",
            "range": "stddev: 8.868544887214712e-7",
            "extra": "mean: 5.758670449035453 usec\nrounds: 42655"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 203653.85419755426,
            "unit": "iter/sec",
            "range": "stddev: 8.603915408148781e-7",
            "extra": "mean: 4.910292535047978 usec\nrounds: 56906"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 434780.885785168,
            "unit": "iter/sec",
            "range": "stddev: 5.854994460980465e-7",
            "extra": "mean: 2.3000091142325783 usec\nrounds: 82837"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 449118.91560886084,
            "unit": "iter/sec",
            "range": "stddev: 6.464357469283038e-7",
            "extra": "mean: 2.2265817921392186 usec\nrounds: 76835"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 33983.16505972159,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025092468583560206",
            "extra": "mean: 29.426335017430322 usec\nrounds: 15635"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 581976.0790276586,
            "unit": "iter/sec",
            "range": "stddev: 5.303519627361426e-7",
            "extra": "mean: 1.718283682158824 usec\nrounds: 54903"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 258913.5663172448,
            "unit": "iter/sec",
            "range": "stddev: 6.65831157098109e-7",
            "extra": "mean: 3.86229278837675 usec\nrounds: 64521"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 381330.51333850145,
            "unit": "iter/sec",
            "range": "stddev: 7.779775740647065e-7",
            "extra": "mean: 2.622397015243086 usec\nrounds: 67811"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 227478.02089782633,
            "unit": "iter/sec",
            "range": "stddev: 7.421010990632324e-7",
            "extra": "mean: 4.396029102298012 usec\nrounds: 49412"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 208271.52903083523,
            "unit": "iter/sec",
            "range": "stddev: 8.578545118854973e-7",
            "extra": "mean: 4.801424393691117 usec\nrounds: 64730"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52270.92431384395,
            "unit": "iter/sec",
            "range": "stddev: 0.000002468778139259575",
            "extra": "mean: 19.131094640604054 usec\nrounds: 23436"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26188.95203546562,
            "unit": "iter/sec",
            "range": "stddev: 0.00003686637017176583",
            "extra": "mean: 38.18404030240612 usec\nrounds: 14416"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34842.15520077586,
            "unit": "iter/sec",
            "range": "stddev: 0.000003322641251240307",
            "extra": "mean: 28.700865208755292 usec\nrounds: 9511"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 329.6032000515711,
            "unit": "iter/sec",
            "range": "stddev: 0.00022480847339646564",
            "extra": "mean: 3.0339511262133856 msec\nrounds: 309"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.163701987735422,
            "unit": "iter/sec",
            "range": "stddev: 0.0004849670001119522",
            "extra": "mean: 32.088613874999616 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25178.131438378416,
            "unit": "iter/sec",
            "range": "stddev: 0.000003904286507629677",
            "extra": "mean: 39.71700610299159 usec\nrounds: 13272"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 182.02529518010743,
            "unit": "iter/sec",
            "range": "stddev: 0.014565682237967295",
            "extra": "mean: 5.493741949494087 msec\nrounds: 198"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.947850179487052,
            "unit": "iter/sec",
            "range": "stddev: 0.082460112247733",
            "extra": "mean: 83.69706557895022 msec\nrounds: 19"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13493.4398443556,
            "unit": "iter/sec",
            "range": "stddev: 0.000007169220625800037",
            "extra": "mean: 74.11008694112249 usec\nrounds: 5636"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "8004b9d1934b545739f974dc0074c3d4f3d14f82",
          "message": "docs: add ADR-0019 for Console runtime client architecture (merges PR #715, addresses #714)\n\nDocuments three coupled decisions for the Console SaaS runtime client\nthat issue #713 will implement:\n\n1. Console primary access is org-scoped, not via ClusterEntry.console.\n   Console SaaS is org-scoped (one org owns many clusters); reusing the\n   per-cluster namespace pattern from ADR-0010 would force a per-cluster\n   shape onto an org-scoped resource.\n\n2. ConsoleAPIClient wraps two APIWrapper instances internally (one per\n   x-token-type), preserving APIWrapper's existing static auth_header\n   contract. The dispatch lives in operation methods, not in APIWrapper\n   itself, so DII / ONTAP / AIQUM are untouched.\n\n3. v1 hand-authors only the operation methods actually consumed; future\n   expansion (past ~10 endpoints) generates them by extending the Console\n   codegen pipeline from ADR-0008. The two-wrapper internal design is\n   preserved at scale; only the source of dispatch methods changes.\n\nStatus: Proposed. Will be marked Accepted when issue #713 ships the v1\nimplementation. The ADR is the runtime counterpart to ADR-0008, which\nrecords the codegen split (models-only via datamodel-code-generator,\nseparate from tools/codegen/).\n\nAddresses #714",
          "timestamp": "2026-05-14T03:04:35+01:00",
          "tree_id": "58a2614b271aa68d0082e271632434d9e0649384",
          "url": "https://github.com/endavis/pynetappfoundry/commit/8004b9d1934b545739f974dc0074c3d4f3d14f82"
        },
        "date": 1778724349624,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1137306.494809421,
            "unit": "iter/sec",
            "range": "stddev: 3.1055124122948715e-7",
            "extra": "mean: 879.2704557337206 nsec\nrounds: 115261"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 772399.7670375111,
            "unit": "iter/sec",
            "range": "stddev: 2.1331350150369716e-7",
            "extra": "mean: 1.2946663666606668 usec\nrounds: 189754"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 450273.49441556673,
            "unit": "iter/sec",
            "range": "stddev: 5.12556825306219e-7",
            "extra": "mean: 2.220872452858794 usec\nrounds: 164990"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 447056.0757457011,
            "unit": "iter/sec",
            "range": "stddev: 5.427550961472052e-7",
            "extra": "mean: 2.236855853780701 usec\nrounds: 168891"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 497888.26536476216,
            "unit": "iter/sec",
            "range": "stddev: 5.244476582861403e-7",
            "extra": "mean: 2.0084827652392683 usec\nrounds: 90253"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 157295.88955760907,
            "unit": "iter/sec",
            "range": "stddev: 0.000001103972791536112",
            "extra": "mean: 6.35744521241131 usec\nrounds: 61200"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 134475.22187932945,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017830223901428583",
            "extra": "mean: 7.43631418505741 usec\nrounds: 72591"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 71900.26170672163,
            "unit": "iter/sec",
            "range": "stddev: 0.000001538811217641842",
            "extra": "mean: 13.908155217556246 usec\nrounds: 47282"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 231257.56916014806,
            "unit": "iter/sec",
            "range": "stddev: 7.739900438984904e-7",
            "extra": "mean: 4.324182787320966 usec\nrounds: 48953"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31757.6645662641,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024688305050607064",
            "extra": "mean: 31.48846156219849 usec\nrounds: 3148"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 82.86953355913724,
            "unit": "iter/sec",
            "range": "stddev: 0.00016581222936254227",
            "extra": "mean: 12.067160958331947 msec\nrounds: 72"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 82.97759704225712,
            "unit": "iter/sec",
            "range": "stddev: 0.000285886572543698",
            "extra": "mean: 12.051445638884198 msec\nrounds: 72"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 93.18065891476496,
            "unit": "iter/sec",
            "range": "stddev: 0.00014180463127356555",
            "extra": "mean: 10.73184083098971 msec\nrounds: 71"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.860638491584478,
            "unit": "iter/sec",
            "range": "stddev: 0.005293927465544765",
            "extra": "mean: 92.07561790910032 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 316.6490242628484,
            "unit": "iter/sec",
            "range": "stddev: 0.00005666708790209833",
            "extra": "mean: 3.158070681973446 msec\nrounds: 283"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 84.75065742141274,
            "unit": "iter/sec",
            "range": "stddev: 0.00012692595042231806",
            "extra": "mean: 11.799318500004276 msec\nrounds: 76"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.3329289177234005,
            "unit": "iter/sec",
            "range": "stddev: 0.128762282886954",
            "extra": "mean: 750.2275528000155 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.3271784988057964,
            "unit": "iter/sec",
            "range": "stddev: 0.13039854451984723",
            "extra": "mean: 753.4781500000236 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 413576.5993237733,
            "unit": "iter/sec",
            "range": "stddev: 6.0296706984273e-7",
            "extra": "mean: 2.4179317728204883 usec\nrounds: 12605"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 399608.39047345833,
            "unit": "iter/sec",
            "range": "stddev: 6.06480993841631e-7",
            "extra": "mean: 2.5024499581082225 usec\nrounds: 79663"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 394677.8257247428,
            "unit": "iter/sec",
            "range": "stddev: 7.188149006444179e-7",
            "extra": "mean: 2.5337121439840464 usec\nrounds: 98049"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 171358.19760066646,
            "unit": "iter/sec",
            "range": "stddev: 8.553678565422762e-7",
            "extra": "mean: 5.835728981757863 usec\nrounds: 47875"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 202845.15393761828,
            "unit": "iter/sec",
            "range": "stddev: 7.454956597445785e-7",
            "extra": "mean: 4.929868821552097 usec\nrounds: 40624"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 441133.25994726014,
            "unit": "iter/sec",
            "range": "stddev: 4.897907873919384e-7",
            "extra": "mean: 2.26688869508401 usec\nrounds: 103221"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 452936.88473481406,
            "unit": "iter/sec",
            "range": "stddev: 5.823295945740087e-7",
            "extra": "mean: 2.2078131273973876 usec\nrounds: 108261"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34557.29345838027,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021776674564304524",
            "extra": "mean: 28.937451400942866 usec\nrounds: 16307"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 601455.7723905612,
            "unit": "iter/sec",
            "range": "stddev: 4.955855204070305e-7",
            "extra": "mean: 1.662632642173131 usec\nrounds: 21328"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 261990.96565131898,
            "unit": "iter/sec",
            "range": "stddev: 6.440893121936835e-7",
            "extra": "mean: 3.8169255092974823 usec\nrounds: 74600"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 378173.0879571211,
            "unit": "iter/sec",
            "range": "stddev: 6.390784610648935e-7",
            "extra": "mean: 2.644291811990028 usec\nrounds: 79726"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 229405.32052070033,
            "unit": "iter/sec",
            "range": "stddev: 7.146262087909002e-7",
            "extra": "mean: 4.3590968061691715 usec\nrounds: 55482"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 207525.00027521295,
            "unit": "iter/sec",
            "range": "stddev: 7.158225719977468e-7",
            "extra": "mean: 4.818696536194832 usec\nrounds: 78530"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52342.637881128154,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018314556279170112",
            "extra": "mean: 19.104883522894525 usec\nrounds: 24683"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26240.34429347337,
            "unit": "iter/sec",
            "range": "stddev: 0.00004097712785124514",
            "extra": "mean: 38.10925606828737 usec\nrounds: 14914"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35393.686400929386,
            "unit": "iter/sec",
            "range": "stddev: 0.000003383572182326126",
            "extra": "mean: 28.253626612167235 usec\nrounds: 10311"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 332.9853400220862,
            "unit": "iter/sec",
            "range": "stddev: 0.00019164090180988182",
            "extra": "mean: 3.003135212900581 msec\nrounds: 310"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 33.2811873940413,
            "unit": "iter/sec",
            "range": "stddev: 0.0002565171721644868",
            "extra": "mean: 30.047004878769478 msec\nrounds: 33"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25561.660798301185,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033794330182701547",
            "extra": "mean: 39.121088723095 usec\nrounds: 10561"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 193.10341170546272,
            "unit": "iter/sec",
            "range": "stddev: 0.011777347700176686",
            "extra": "mean: 5.17857240930203 msec\nrounds: 215"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.825425055718487,
            "unit": "iter/sec",
            "range": "stddev: 0.06829263705753273",
            "extra": "mean: 72.33050672726904 msec\nrounds: 22"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13526.928122080804,
            "unit": "iter/sec",
            "range": "stddev: 0.000007168989676792459",
            "extra": "mean: 73.92661445192725 usec\nrounds: 6850"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "25650e1f8114d68f22c251cb898f4d2f1e292d41",
          "message": "chore: add docs/decisions/README.md to sync-exclude.toml (merges PR #730, addresses #725)\n\nProject owns the \"Project-level ADRs (0001+)\" table in\ndocs/decisions/README.md. Upstream pyproject-template ships a generic\nplaceholder under that section:\n\n  _(No project-level ADRs yet.)_\n\nPhase B's bulk-copy sync (#723) applied the upstream version,\nclobbering the project's ADR-0001..ADR-NNNN list. The clobber surfaced\nas a rebase conflict on PR #715 (Console runtime ADR), where the branch\nhad ADR-0019 layered on the pre-Phase-B README. The merge of #715\nrestored the project ADR table on main, but the sync-exclude rule was\nstill missing — meaning the next template sync would clobber the\nREADME again.\n\nAdding docs/decisions/README.md to sync-exclude.toml prevents the\nre-clobber. Following the same pattern used for docs/index.md,\ndocs/reference/api.md, etc. (added in Phase B tail commit ad2ebfd6).\n\nAfter this change, `manage.py --show-excluded check` reports 10\ndifferent files and 56 skipped per project policy (was 9 / 55).\n\nAddresses #725\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-14T03:13:02+01:00",
          "tree_id": "c740ed58216a07bfce99892a0c8d8f3c595f596b",
          "url": "https://github.com/endavis/pynetappfoundry/commit/25650e1f8114d68f22c251cb898f4d2f1e292d41"
        },
        "date": 1778724859438,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1233160.4087456404,
            "unit": "iter/sec",
            "range": "stddev: 2.647081305797587e-7",
            "extra": "mean: 810.9245098269016 nsec\nrounds: 43966"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 731382.3478151791,
            "unit": "iter/sec",
            "range": "stddev: 5.461180521538913e-7",
            "extra": "mean: 1.36727390671548 usec\nrounds: 187688"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 482419.4915752389,
            "unit": "iter/sec",
            "range": "stddev: 5.562451092113742e-7",
            "extra": "mean: 2.0728847350978943 usec\nrounds: 80328"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 485319.2254523359,
            "unit": "iter/sec",
            "range": "stddev: 5.472595473708898e-7",
            "extra": "mean: 2.0604994559363727 usec\nrounds: 164501"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 528786.2385706753,
            "unit": "iter/sec",
            "range": "stddev: 5.974628149071846e-7",
            "extra": "mean: 1.8911233444785351 usec\nrounds: 77466"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 167817.18902991843,
            "unit": "iter/sec",
            "range": "stddev: 8.425799600196283e-7",
            "extra": "mean: 5.958865154282379 usec\nrounds: 41744"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 147665.3787272212,
            "unit": "iter/sec",
            "range": "stddev: 8.926194350077424e-7",
            "extra": "mean: 6.772068094900408 usec\nrounds: 72722"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 79434.28923355072,
            "unit": "iter/sec",
            "range": "stddev: 0.000001368231257686138",
            "extra": "mean: 12.589021814745832 usec\nrounds: 45428"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 245451.11616355964,
            "unit": "iter/sec",
            "range": "stddev: 7.364810926624578e-7",
            "extra": "mean: 4.074130994513941 usec\nrounds: 40704"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32212.829813387405,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020639192092816863",
            "extra": "mean: 31.043531592632938 usec\nrounds: 3102"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 79.58475651456743,
            "unit": "iter/sec",
            "range": "stddev: 0.0005221403207563787",
            "extra": "mean: 12.565220323529632 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 77.39450030720467,
            "unit": "iter/sec",
            "range": "stddev: 0.000908783411729378",
            "extra": "mean: 12.920814735293403 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 88.93970566513683,
            "unit": "iter/sec",
            "range": "stddev: 0.0005133094482106822",
            "extra": "mean: 11.24357217647041 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 12.337764307250922,
            "unit": "iter/sec",
            "range": "stddev: 0.0005045480439948802",
            "extra": "mean: 81.05196169230584 msec\nrounds: 13"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 305.8835558688143,
            "unit": "iter/sec",
            "range": "stddev: 0.00003550554500095994",
            "extra": "mean: 3.269217912547331 msec\nrounds: 263"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 76.61278547323293,
            "unit": "iter/sec",
            "range": "stddev: 0.0013283763507206956",
            "extra": "mean: 13.052651640624413 msec\nrounds: 64"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2062586608059969,
            "unit": "iter/sec",
            "range": "stddev: 0.16007514203072035",
            "extra": "mean: 829.0095918000048 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2036343675212504,
            "unit": "iter/sec",
            "range": "stddev: 0.15574903600199325",
            "extra": "mean: 830.8170877999999 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 404743.34957448475,
            "unit": "iter/sec",
            "range": "stddev: 4.962528987415591e-7",
            "extra": "mean: 2.470701497754864 usec\nrounds: 11484"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 387530.8850521628,
            "unit": "iter/sec",
            "range": "stddev: 5.199696192662007e-7",
            "extra": "mean: 2.580439491591482 usec\nrounds: 72775"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 386362.7881714459,
            "unit": "iter/sec",
            "range": "stddev: 5.195649400908573e-7",
            "extra": "mean: 2.5882409761373206 usec\nrounds: 84332"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176044.7080615689,
            "unit": "iter/sec",
            "range": "stddev: 7.558564600048609e-7",
            "extra": "mean: 5.6803752354218195 usec\nrounds: 40889"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 206180.93475238286,
            "unit": "iter/sec",
            "range": "stddev: 8.997363557057981e-7",
            "extra": "mean: 4.850108964735125 usec\nrounds: 51870"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 424954.9023797322,
            "unit": "iter/sec",
            "range": "stddev: 4.720008940058975e-7",
            "extra": "mean: 2.3531908783732955 usec\nrounds: 84546"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 439709.1571299303,
            "unit": "iter/sec",
            "range": "stddev: 4.735451171088275e-7",
            "extra": "mean: 2.274230553957985 usec\nrounds: 72881"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34847.32602753679,
            "unit": "iter/sec",
            "range": "stddev: 0.00008132532937197216",
            "extra": "mean: 28.696606425692107 usec\nrounds: 15438"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 558405.8349587088,
            "unit": "iter/sec",
            "range": "stddev: 5.989765431038185e-7",
            "extra": "mean: 1.7908122326013027 usec\nrounds: 50946"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 252684.59014903783,
            "unit": "iter/sec",
            "range": "stddev: 6.456542575347888e-7",
            "extra": "mean: 3.9575029067272465 usec\nrounds: 30103"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 364557.6594667681,
            "unit": "iter/sec",
            "range": "stddev: 6.490856840637098e-7",
            "extra": "mean: 2.7430503077693715 usec\nrounds: 69532"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 223361.7450352023,
            "unit": "iter/sec",
            "range": "stddev: 7.88862498157372e-7",
            "extra": "mean: 4.477042386297607 usec\nrounds: 49851"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 199679.54387385264,
            "unit": "iter/sec",
            "range": "stddev: 9.823062887853861e-7",
            "extra": "mean: 5.008024260270491 usec\nrounds: 68672"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 51908.325037737464,
            "unit": "iter/sec",
            "range": "stddev: 0.000001517277809793783",
            "extra": "mean: 19.26473256983341 usec\nrounds: 21830"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25963.506043800033,
            "unit": "iter/sec",
            "range": "stddev: 0.000035512342138810015",
            "extra": "mean: 38.51559948463876 usec\nrounds: 14359"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34894.459019333735,
            "unit": "iter/sec",
            "range": "stddev: 0.000002022363159752646",
            "extra": "mean: 28.657845059180794 usec\nrounds: 8855"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 327.65769886383686,
            "unit": "iter/sec",
            "range": "stddev: 0.0002587311649756206",
            "extra": "mean: 3.0519655221517175 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.83478131337374,
            "unit": "iter/sec",
            "range": "stddev: 0.00023097122500570966",
            "extra": "mean: 31.412183741934538 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25417.731434673868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024353361342749878",
            "extra": "mean: 39.34261413415673 usec\nrounds: 14518"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 179.63646755682842,
            "unit": "iter/sec",
            "range": "stddev: 0.016037508618386036",
            "extra": "mean: 5.566798399014653 msec\nrounds: 203"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 12.275071882397198,
            "unit": "iter/sec",
            "range": "stddev: 0.08383662032149118",
            "extra": "mean: 81.46591804761881 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 14535.731878724113,
            "unit": "iter/sec",
            "range": "stddev: 0.000004673487876734267",
            "extra": "mean: 68.79598553022952 usec\nrounds: 4423"
          }
        ]
      }
    ]
  }
}