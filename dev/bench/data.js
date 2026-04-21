window.BENCHMARK_DATA = {
  "lastUpdate": 1776739917566,
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
      }
    ]
  }
}