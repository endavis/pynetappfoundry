window.BENCHMARK_DATA = {
  "lastUpdate": 1793033601471,
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
          "id": "bf04008b2fa520d3d09753f8a8515bf92b2d488b",
          "message": "feat: add -h short alias for --help in CLI (merges PR #731, addresses #719)\n\nAdds the near-universal `-h` short alias for `--help` across the entire\n`nf` CLI. A single-argument addition to the top-level `@click.group()`\ndecorator:\n\n    @click.group(context_settings={\"help_option_names\": [\"-h\", \"--help\"]})\n\nClick propagates `context_settings` to every subcommand and nested\ngroup automatically, so `nf -h`, `nf cache -h`, `nf events -h`, and\n`nf cache show -h` all work without per-command edits.\n\nTests added under `tests/unit/cli/test_main.py` (TestHelpShortAlias, 8\ntests) cover top-level, two distinct subcommands, and one deep-nested\nsubcommand — each verifies exit code 0 plus output equivalence with\nthe `--help` invocation.\n\nThis issue was split out of the Phase B template sync (PR #723)\nbecause the upstream change (endavis/pyproject-template#569) targeted\n`src/package_name/cli.py`, a file path that does not exist in this\nproject (CLI lives at `src/pynetappfoundry/cli/main.py`).\n\nAddresses #719\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-14T03:27:20+01:00",
          "tree_id": "b63c297953301e1f7577742d0bc3a3f38049daf2",
          "url": "https://github.com/endavis/pynetappfoundry/commit/bf04008b2fa520d3d09753f8a8515bf92b2d488b"
        },
        "date": 1778725705492,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1165675.091851709,
            "unit": "iter/sec",
            "range": "stddev: 3.908375345287863e-7",
            "extra": "mean: 857.8719807862332 nsec\nrounds: 55390"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 734425.5791226088,
            "unit": "iter/sec",
            "range": "stddev: 4.751489437973879e-7",
            "extra": "mean: 1.361608348656188 usec\nrounds: 187266"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 446864.6385754984,
            "unit": "iter/sec",
            "range": "stddev: 8.186394284582774e-7",
            "extra": "mean: 2.23781412462568 usec\nrounds: 154991"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 465415.9666389176,
            "unit": "iter/sec",
            "range": "stddev: 5.240007959350145e-7",
            "extra": "mean: 2.148615586228539 usec\nrounds: 145731"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 511112.4343895732,
            "unit": "iter/sec",
            "range": "stddev: 5.655772178858496e-7",
            "extra": "mean: 1.9565166736636144 usec\nrounds: 82495"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162134.41946024972,
            "unit": "iter/sec",
            "range": "stddev: 8.986953274499216e-7",
            "extra": "mean: 6.167721840489081 usec\nrounds: 54307"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 142486.5761900506,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011968653161919352",
            "extra": "mean: 7.018204989824345 usec\nrounds: 71706"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 73511.60953879115,
            "unit": "iter/sec",
            "range": "stddev: 0.000001496592760464859",
            "extra": "mean: 13.603293497094668 usec\nrounds: 44900"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 234395.90606952857,
            "unit": "iter/sec",
            "range": "stddev: 8.195745829768362e-7",
            "extra": "mean: 4.2662861172300985 usec\nrounds: 42528"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31241.516464200027,
            "unit": "iter/sec",
            "range": "stddev: 0.000002579014275774704",
            "extra": "mean: 32.008689499624964 usec\nrounds: 3095"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 61.57915983173169,
            "unit": "iter/sec",
            "range": "stddev: 0.0005870492724578225",
            "extra": "mean: 16.239260209664327 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 62.05439321985879,
            "unit": "iter/sec",
            "range": "stddev: 0.0007131800750815731",
            "extra": "mean: 16.11489450000742 msec\nrounds: 60"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 63.011292139815055,
            "unit": "iter/sec",
            "range": "stddev: 0.0033016742238490514",
            "extra": "mean: 15.870171298520766 msec\nrounds: 67"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.438731277009873,
            "unit": "iter/sec",
            "range": "stddev: 0.00030649451884911193",
            "extra": "mean: 87.42228274999775 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 306.435687567445,
            "unit": "iter/sec",
            "range": "stddev: 0.00005344353259947318",
            "extra": "mean: 3.263327479701283 msec\nrounds: 271"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 62.72500975967772,
            "unit": "iter/sec",
            "range": "stddev: 0.0011985265612267885",
            "extra": "mean: 15.942604135596998 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2643365511126532,
            "unit": "iter/sec",
            "range": "stddev: 0.13505909418212192",
            "extra": "mean: 790.9286488000134 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.285908080108056,
            "unit": "iter/sec",
            "range": "stddev: 0.13290319706110082",
            "extra": "mean: 777.6605618000076 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 424668.2768030238,
            "unit": "iter/sec",
            "range": "stddev: 8.278565035104295e-7",
            "extra": "mean: 2.354779140858302 usec\nrounds: 12963"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 407920.56901692844,
            "unit": "iter/sec",
            "range": "stddev: 6.419843700967983e-7",
            "extra": "mean: 2.4514576512039055 usec\nrounds: 78101"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 406663.1279606591,
            "unit": "iter/sec",
            "range": "stddev: 6.831835778621373e-7",
            "extra": "mean: 2.459037791340504 usec\nrounds: 89518"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177748.01641624662,
            "unit": "iter/sec",
            "range": "stddev: 0.000001275451170292362",
            "extra": "mean: 5.62594182574854 usec\nrounds: 42510"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 206181.58507661798,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021624362408881204",
            "extra": "mean: 4.850093666844183 usec\nrounds: 58783"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 458775.7370827985,
            "unit": "iter/sec",
            "range": "stddev: 5.332791318589658e-7",
            "extra": "mean: 2.1797142245548238 usec\nrounds: 86491"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 469657.4534429988,
            "unit": "iter/sec",
            "range": "stddev: 5.762967504442757e-7",
            "extra": "mean: 2.1292113915559687 usec\nrounds: 82761"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 36116.75421255359,
            "unit": "iter/sec",
            "range": "stddev: 0.000002617257403981679",
            "extra": "mean: 27.68798087765086 usec\nrounds: 16630"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 583120.5817138123,
            "unit": "iter/sec",
            "range": "stddev: 4.658934030057576e-7",
            "extra": "mean: 1.7149111716498913 usec\nrounds: 61388"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 266863.8105285457,
            "unit": "iter/sec",
            "range": "stddev: 6.628378365668315e-7",
            "extra": "mean: 3.747229712486747 usec\nrounds: 29254"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 378522.26894983446,
            "unit": "iter/sec",
            "range": "stddev: 5.912098817575419e-7",
            "extra": "mean: 2.6418524933140195 usec\nrounds: 65109"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 224366.15640075348,
            "unit": "iter/sec",
            "range": "stddev: 8.665463145003079e-7",
            "extra": "mean: 4.457000182388656 usec\nrounds: 49293"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 212636.56426408238,
            "unit": "iter/sec",
            "range": "stddev: 8.030490119398071e-7",
            "extra": "mean: 4.702860034730704 usec\nrounds: 67124"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 51932.25710412609,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017240510578994213",
            "extra": "mean: 19.255854756995507 usec\nrounds: 23409"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25919.120823362307,
            "unit": "iter/sec",
            "range": "stddev: 0.000035608886497266533",
            "extra": "mean: 38.581555555643924 usec\nrounds: 14670"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35359.756142308914,
            "unit": "iter/sec",
            "range": "stddev: 0.00000282395620238401",
            "extra": "mean: 28.280738022496507 usec\nrounds: 8516"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 335.20093103686145,
            "unit": "iter/sec",
            "range": "stddev: 0.000060760695732345854",
            "extra": "mean: 2.983285269843215 msec\nrounds: 315"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.955902042687576,
            "unit": "iter/sec",
            "range": "stddev: 0.00048280873265722383",
            "extra": "mean: 31.293123838725386 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25258.014486137552,
            "unit": "iter/sec",
            "range": "stddev: 0.0000050040932436513194",
            "extra": "mean: 39.59139387416353 usec\nrounds: 9795"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 181.37109640287053,
            "unit": "iter/sec",
            "range": "stddev: 0.01456081627078972",
            "extra": "mean: 5.5135576717182655 msec\nrounds: 198"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.311672347599268,
            "unit": "iter/sec",
            "range": "stddev: 0.08644453964719222",
            "extra": "mean: 88.40425794442632 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13638.25389267943,
            "unit": "iter/sec",
            "range": "stddev: 0.0000071901733952828086",
            "extra": "mean: 73.32316936384117 usec\nrounds: 6489"
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
          "id": "4025dca943621c9d1dbd6b2643d038e42f264279",
          "message": "feat: add Console SaaS v1 runtime client and cache integration (merges PR #732, addresses #713)\n\nOrg-scoped Console facade, two-wrapper ConsoleAPIClient, hand-authored\nOrganization model, ConsoleInfo cache field (schema v5 → v6), and\nconsoleapi.toml example config. ADR-0019 flipped to Accepted.\nAdds consoleapi.toml to config-schema.md reference.\n\nAddresses #713",
          "timestamp": "2026-05-14T17:55:41+01:00",
          "tree_id": "9f1b5f614a33022157b63278720ef6243ded901b",
          "url": "https://github.com/endavis/pynetappfoundry/commit/4025dca943621c9d1dbd6b2643d038e42f264279"
        },
        "date": 1778777809160,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1506262.2514855142,
            "unit": "iter/sec",
            "range": "stddev: 2.1423617041754557e-7",
            "extra": "mean: 663.8950149708488 nsec\nrounds: 54122"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 1037472.1722429963,
            "unit": "iter/sec",
            "range": "stddev: 1.228131596239572e-7",
            "extra": "mean: 963.8812748471294 nsec\nrounds: 169234"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 601047.6543929266,
            "unit": "iter/sec",
            "range": "stddev: 4.753345296157969e-7",
            "extra": "mean: 1.6637615881057308 usec\nrounds: 178955"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 634240.1689816349,
            "unit": "iter/sec",
            "range": "stddev: 1.8076295528127962e-7",
            "extra": "mean: 1.576689791827039 usec\nrounds: 154107"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 658921.7023213594,
            "unit": "iter/sec",
            "range": "stddev: 4.0292066012060343e-7",
            "extra": "mean: 1.5176309969409612 usec\nrounds: 91609"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 211231.48859604375,
            "unit": "iter/sec",
            "range": "stddev: 6.434234919344909e-7",
            "extra": "mean: 4.7341426538558675 usec\nrounds: 68158"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 185116.8805535573,
            "unit": "iter/sec",
            "range": "stddev: 6.654648883819253e-7",
            "extra": "mean: 5.401992497981208 usec\nrounds: 91442"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 97648.811392371,
            "unit": "iter/sec",
            "range": "stddev: 9.709233284659486e-7",
            "extra": "mean: 10.240780053961075 usec\nrounds: 55941"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 303132.46795150376,
            "unit": "iter/sec",
            "range": "stddev: 5.316921620269867e-7",
            "extra": "mean: 3.2988877989802914 usec\nrounds: 50971"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 41528.521963472456,
            "unit": "iter/sec",
            "range": "stddev: 0.000001392511114456785",
            "extra": "mean: 24.07983604327593 usec\nrounds: 3690"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 107.95542648445426,
            "unit": "iter/sec",
            "range": "stddev: 0.00024585446034483673",
            "extra": "mean: 9.263082297618467 msec\nrounds: 84"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 106.7264330766238,
            "unit": "iter/sec",
            "range": "stddev: 0.0002709447632045822",
            "extra": "mean: 9.369750034483529 msec\nrounds: 87"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 117.91054095461406,
            "unit": "iter/sec",
            "range": "stddev: 0.00047274721421492963",
            "extra": "mean: 8.481005955056371 msec\nrounds: 89"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 15.040240222876987,
            "unit": "iter/sec",
            "range": "stddev: 0.0006249741710458875",
            "extra": "mean: 66.48829973333457 msec\nrounds: 15"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 400.5789723602215,
            "unit": "iter/sec",
            "range": "stddev: 0.00006613795960280754",
            "extra": "mean: 2.49638665281898 msec\nrounds: 337"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 108.28245201070534,
            "unit": "iter/sec",
            "range": "stddev: 0.000250241639675118",
            "extra": "mean: 9.23510671794849 msec\nrounds: 78"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.3956277628300828,
            "unit": "iter/sec",
            "range": "stddev: 0.148043079215943",
            "extra": "mean: 716.5234359999971 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.3630820598730644,
            "unit": "iter/sec",
            "range": "stddev: 0.14590888204696995",
            "extra": "mean: 733.6315467999952 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 489579.67361517926,
            "unit": "iter/sec",
            "range": "stddev: 7.030868511360632e-7",
            "extra": "mean: 2.0425684600337854 usec\nrounds: 9721"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 469280.36141576635,
            "unit": "iter/sec",
            "range": "stddev: 6.799943315483479e-7",
            "extra": "mean: 2.1309223275039932 usec\nrounds: 91358"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 471172.04218011524,
            "unit": "iter/sec",
            "range": "stddev: 6.646299159848784e-7",
            "extra": "mean: 2.1223670134861896 usec\nrounds: 90449"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 215608.1037656505,
            "unit": "iter/sec",
            "range": "stddev: 8.933531496329766e-7",
            "extra": "mean: 4.6380445935692824 usec\nrounds: 44558"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 260341.31230176933,
            "unit": "iter/sec",
            "range": "stddev: 7.040886185671492e-7",
            "extra": "mean: 3.8411114669379494 usec\nrounds: 62763"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 551459.587377783,
            "unit": "iter/sec",
            "range": "stddev: 3.534071191226821e-7",
            "extra": "mean: 1.8133695068301348 usec\nrounds: 93844"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 561818.1809041592,
            "unit": "iter/sec",
            "range": "stddev: 3.784095680335479e-7",
            "extra": "mean: 1.779935277976685 usec\nrounds: 73638"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 45528.16609720639,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022253226744036654",
            "extra": "mean: 21.964425227779163 usec\nrounds: 18543"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 709147.4631175394,
            "unit": "iter/sec",
            "range": "stddev: 5.338532876544507e-7",
            "extra": "mean: 1.4101439432693177 usec\nrounds: 59190"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 318573.00196266687,
            "unit": "iter/sec",
            "range": "stddev: 7.054137411557132e-7",
            "extra": "mean: 3.1389979497295526 usec\nrounds: 76576"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 471658.0499735395,
            "unit": "iter/sec",
            "range": "stddev: 5.250386265985785e-7",
            "extra": "mean: 2.1201800754934665 usec\nrounds: 75535"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 292083.4418235682,
            "unit": "iter/sec",
            "range": "stddev: 6.380559905563736e-7",
            "extra": "mean: 3.423679184813379 usec\nrounds: 58395"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 263184.05215282267,
            "unit": "iter/sec",
            "range": "stddev: 6.476762458663754e-7",
            "extra": "mean: 3.7996223244535035 usec\nrounds: 81713"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 67621.79502909322,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014490823240400054",
            "extra": "mean: 14.788131542053351 usec\nrounds: 27839"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 33624.97467653346,
            "unit": "iter/sec",
            "range": "stddev: 0.00003531271971122584",
            "extra": "mean: 29.739799349139442 usec\nrounds: 19053"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 45866.534844303125,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013819128102392099",
            "extra": "mean: 21.802388242202372 usec\nrounds: 10563"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 425.8436549897094,
            "unit": "iter/sec",
            "range": "stddev: 0.00011390210513973068",
            "extra": "mean: 2.3482796756104425 msec\nrounds: 410"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 41.76693668739497,
            "unit": "iter/sec",
            "range": "stddev: 0.00009959812649491028",
            "extra": "mean: 23.942383121953842 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 33002.72902805719,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016521863314985754",
            "extra": "mean: 30.300524515710578 usec\nrounds: 17397"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 238.3182959328277,
            "unit": "iter/sec",
            "range": "stddev: 0.012929484921189238",
            "extra": "mean: 4.196068942528272 msec\nrounds: 261"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.938979303497014,
            "unit": "iter/sec",
            "range": "stddev: 0.08531339567444128",
            "extra": "mean: 71.74126442307866 msec\nrounds: 26"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 18945.853062881346,
            "unit": "iter/sec",
            "range": "stddev: 0.000002822864114278711",
            "extra": "mean: 52.78199913622242 usec\nrounds: 8104"
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
          "id": "718390273cd2f1cc146533afde348a502156eb7a",
          "message": "chore: remove legacy slash commands replaced by /<ai>:<action> and /multi-* (merges PR #739, addresses #738)\n\nThe upstream pyproject-template removed the pre-cutover top-level slash\ncommands in favor of the /<ai>:<action> self-action naming and the\n/multi-* orchestrators. This project still shipped the legacy wrappers,\nwhich were not referenced anywhere outside themselves.\n\nRemoves 8 files from .claude/commands/ (close-issue, finalize,\ngemini-review, implement, plan-both, plan-issue, review-both,\nwhere-am-i) and 2 files from .gemini/commands/ (plan-issue, review-pr).\n\nAddresses #738",
          "timestamp": "2026-05-15T00:42:38+01:00",
          "tree_id": "ab946b9383a9cfeff76c70059afd9f8aa642ed4a",
          "url": "https://github.com/endavis/pynetappfoundry/commit/718390273cd2f1cc146533afde348a502156eb7a"
        },
        "date": 1778802227874,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1180365.0321565652,
            "unit": "iter/sec",
            "range": "stddev: 2.6851200144688894e-7",
            "extra": "mean: 847.1955477814921 nsec\nrounds: 59162"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 751365.8291062921,
            "unit": "iter/sec",
            "range": "stddev: 3.611971215979002e-7",
            "extra": "mean: 1.3309096065620183 usec\nrounds: 153728"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 477906.72730386385,
            "unit": "iter/sec",
            "range": "stddev: 4.1000312713105654e-7",
            "extra": "mean: 2.0924585130691775 usec\nrounds: 134681"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 479241.44226056006,
            "unit": "iter/sec",
            "range": "stddev: 3.7136261300898666e-7",
            "extra": "mean: 2.0866308958654445 usec\nrounds: 134355"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 534938.9791202608,
            "unit": "iter/sec",
            "range": "stddev: 3.6400751370425376e-7",
            "extra": "mean: 1.8693720948220296 usec\nrounds: 72675"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162857.63815240274,
            "unit": "iter/sec",
            "range": "stddev: 5.884305473952115e-7",
            "extra": "mean: 6.140332202682422 usec\nrounds: 51881"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 142711.77619227988,
            "unit": "iter/sec",
            "range": "stddev: 6.328532768596365e-7",
            "extra": "mean: 7.007130222054485 usec\nrounds: 60274"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 77005.54543167338,
            "unit": "iter/sec",
            "range": "stddev: 8.601623156160669e-7",
            "extra": "mean: 12.986077747962902 usec\nrounds: 39821"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 241373.05051395253,
            "unit": "iter/sec",
            "range": "stddev: 5.243851504360911e-7",
            "extra": "mean: 4.142964584781577 usec\nrounds: 41197"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 33513.3551530971,
            "unit": "iter/sec",
            "range": "stddev: 0.000001217679191334524",
            "extra": "mean: 29.83885067405989 usec\nrounds: 2893"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 80.40808728745992,
            "unit": "iter/sec",
            "range": "stddev: 0.00006286901000429066",
            "extra": "mean: 12.436559974682488 msec\nrounds: 79"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 77.88624386961364,
            "unit": "iter/sec",
            "range": "stddev: 0.00010771990063118271",
            "extra": "mean: 12.83923771794749 msec\nrounds: 78"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 87.21149030798337,
            "unit": "iter/sec",
            "range": "stddev: 0.00007569675297145824",
            "extra": "mean: 11.466378988233615 msec\nrounds: 85"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 16.253569559947962,
            "unit": "iter/sec",
            "range": "stddev: 0.00021520619234586887",
            "extra": "mean: 61.524946647055266 msec\nrounds: 17"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 320.093740139334,
            "unit": "iter/sec",
            "range": "stddev: 0.00010330991926450028",
            "extra": "mean: 3.124084837037765 msec\nrounds: 270"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 79.65411519876648,
            "unit": "iter/sec",
            "range": "stddev: 0.00011280500179163267",
            "extra": "mean: 12.554279179482819 msec\nrounds: 78"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.3674890796315349,
            "unit": "iter/sec",
            "range": "stddev: 0.12050236201355917",
            "extra": "mean: 731.2672655999904 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.3480018520154085,
            "unit": "iter/sec",
            "range": "stddev: 0.125519369908448",
            "extra": "mean: 741.8387434000124 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 434530.8270728866,
            "unit": "iter/sec",
            "range": "stddev: 4.886204657094227e-7",
            "extra": "mean: 2.3013326965459777 usec\nrounds: 13087"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 423154.14710106363,
            "unit": "iter/sec",
            "range": "stddev: 3.1692158549635134e-7",
            "extra": "mean: 2.363205008980252 usec\nrounds: 56300"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 414006.2406862105,
            "unit": "iter/sec",
            "range": "stddev: 6.578507275726742e-7",
            "extra": "mean: 2.4154225268259526 usec\nrounds: 73406"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 181229.15586257284,
            "unit": "iter/sec",
            "range": "stddev: 6.038470177456241e-7",
            "extra": "mean: 5.517875946838852 usec\nrounds: 41579"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 215569.20134863636,
            "unit": "iter/sec",
            "range": "stddev: 5.585555254422939e-7",
            "extra": "mean: 4.638881592286076 usec\nrounds: 52978"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 463006.38084265887,
            "unit": "iter/sec",
            "range": "stddev: 3.06623658725471e-7",
            "extra": "mean: 2.1597974485362976 usec\nrounds: 78543"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 474356.27615587774,
            "unit": "iter/sec",
            "range": "stddev: 3.279542811128061e-7",
            "extra": "mean: 2.1081200993141094 usec\nrounds: 79834"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 37587.026314749564,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013174266148746012",
            "extra": "mean: 26.604924572274264 usec\nrounds: 16307"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 612582.7708390593,
            "unit": "iter/sec",
            "range": "stddev: 2.60898618591705e-7",
            "extra": "mean: 1.6324324607273764 usec\nrounds: 56234"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 273739.9941787677,
            "unit": "iter/sec",
            "range": "stddev: 4.4125733853698485e-7",
            "extra": "mean: 3.653101560844424 usec\nrounds: 53623"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 403395.6213781808,
            "unit": "iter/sec",
            "range": "stddev: 3.968425944324348e-7",
            "extra": "mean: 2.478956009942672 usec\nrounds: 59309"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 241556.596661046,
            "unit": "iter/sec",
            "range": "stddev: 7.220909798551942e-7",
            "extra": "mean: 4.139816563996418 usec\nrounds: 41693"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 217752.6383058046,
            "unit": "iter/sec",
            "range": "stddev: 8.893794493953703e-7",
            "extra": "mean: 4.5923668607662655 usec\nrounds: 58191"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 55872.12069770414,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018938870907305682",
            "extra": "mean: 17.898014027613083 usec\nrounds: 22313"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 28230.305442980418,
            "unit": "iter/sec",
            "range": "stddev: 0.000048703364809864965",
            "extra": "mean: 35.422925268017394 usec\nrounds: 13796"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 37679.77714957437,
            "unit": "iter/sec",
            "range": "stddev: 0.000001630158887073245",
            "extra": "mean: 26.539435093535204 usec\nrounds: 8235"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 349.06875363630627,
            "unit": "iter/sec",
            "range": "stddev: 0.0002897994019209248",
            "extra": "mean: 2.864765148936525 msec\nrounds: 329"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 33.872928182648565,
            "unit": "iter/sec",
            "range": "stddev: 0.000585582902859057",
            "extra": "mean: 29.5221007941159 msec\nrounds: 34"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 27622.152478085227,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015224169886154842",
            "extra": "mean: 36.20282672732969 usec\nrounds: 14255"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 202.33450590153205,
            "unit": "iter/sec",
            "range": "stddev: 0.012214643126372863",
            "extra": "mean: 4.942310732143034 msec\nrounds: 224"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.496287417638364,
            "unit": "iter/sec",
            "range": "stddev: 0.06984265614576983",
            "extra": "mean: 74.09445050000159 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 14518.27271642642,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028357518344593523",
            "extra": "mean: 68.87871715404334 usec\nrounds: 6774"
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
          "id": "591c64f9801a121823d20bcae75ed1c955548925",
          "message": "chore: add doit audit_legacy task to surface non-DataSource call sites (merges PR #746, addresses #744)\n\nClosed phase issues captured manual audit snapshots in comments, but\nthose age out the moment subsequent migration PRs land. There was no\nsingle command to re-derive the current state of the migration. This\ntask makes the answer one command away, machine-readable, and always\ncurrent. --strict provides a future CI gate.\n\nAddresses #744",
          "timestamp": "2026-05-18T14:22:49+01:00",
          "tree_id": "eacdd9ecdf9b44dd7f42f8bea4485faeabcc1636",
          "url": "https://github.com/endavis/pynetappfoundry/commit/591c64f9801a121823d20bcae75ed1c955548925"
        },
        "date": 1779110640171,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1173046.7479126854,
            "unit": "iter/sec",
            "range": "stddev: 1.6572472029090028e-7",
            "extra": "mean: 852.4809448382139 nsec\nrounds: 60456"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 751648.0609533277,
            "unit": "iter/sec",
            "range": "stddev: 2.957473389288575e-7",
            "extra": "mean: 1.3304098712523562 usec\nrounds: 145392"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 473912.829958446,
            "unit": "iter/sec",
            "range": "stddev: 4.088229102902734e-7",
            "extra": "mean: 2.1100926938139297 usec\nrounds: 94796"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 475159.88514917163,
            "unit": "iter/sec",
            "range": "stddev: 3.7897500489820936e-7",
            "extra": "mean: 2.104554764100215 usec\nrounds: 142776"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 538988.0669216365,
            "unit": "iter/sec",
            "range": "stddev: 4.390306390048081e-7",
            "extra": "mean: 1.8553286452358322 usec\nrounds: 77430"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162302.7678623585,
            "unit": "iter/sec",
            "range": "stddev: 8.688548907499091e-7",
            "extra": "mean: 6.161324376476769 usec\nrounds: 50762"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141843.35662408083,
            "unit": "iter/sec",
            "range": "stddev: 0.000001141961760112388",
            "extra": "mean: 7.050030567524156 usec\nrounds: 61863"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 75901.50347622109,
            "unit": "iter/sec",
            "range": "stddev: 9.977972666434433e-7",
            "extra": "mean: 13.174969588228072 usec\nrounds: 41793"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 241617.34516336303,
            "unit": "iter/sec",
            "range": "stddev: 5.68563200332011e-7",
            "extra": "mean: 4.138775712993109 usec\nrounds: 26368"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 34799.84062617687,
            "unit": "iter/sec",
            "range": "stddev: 0.000002422235394886694",
            "extra": "mean: 28.73576378530273 usec\nrounds: 2684"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 77.9749502778534,
            "unit": "iter/sec",
            "range": "stddev: 0.00006589327933231116",
            "extra": "mean: 12.824631454545756 msec\nrounds: 77"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 75.76809435894091,
            "unit": "iter/sec",
            "range": "stddev: 0.00014718105535809425",
            "extra": "mean: 13.198167493333509 msec\nrounds: 75"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 84.76165123752158,
            "unit": "iter/sec",
            "range": "stddev: 0.00008761677961644536",
            "extra": "mean: 11.797788096385364 msec\nrounds: 83"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 15.80514689452209,
            "unit": "iter/sec",
            "range": "stddev: 0.000311841729249662",
            "extra": "mean: 63.27052868749927 msec\nrounds: 16"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 308.35060724854424,
            "unit": "iter/sec",
            "range": "stddev: 0.00011559073512758121",
            "extra": "mean: 3.2430615555556725 msec\nrounds: 261"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 76.03955955450184,
            "unit": "iter/sec",
            "range": "stddev: 0.0006334118238565666",
            "extra": "mean: 13.151049346665975 msec\nrounds: 75"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.3929582015269284,
            "unit": "iter/sec",
            "range": "stddev: 0.11675231674614174",
            "extra": "mean: 717.8966309999993 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.357062924779506,
            "unit": "iter/sec",
            "range": "stddev: 0.11428639886234698",
            "extra": "mean: 736.8855060000101 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 443596.5159634218,
            "unit": "iter/sec",
            "range": "stddev: 3.7787881701465715e-7",
            "extra": "mean: 2.2543008432520204 usec\nrounds: 12096"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 420031.84147032455,
            "unit": "iter/sec",
            "range": "stddev: 3.827601695688349e-7",
            "extra": "mean: 2.380771887434754 usec\nrounds: 51685"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 413382.72982904286,
            "unit": "iter/sec",
            "range": "stddev: 4.606515431597155e-7",
            "extra": "mean: 2.4190657418454724 usec\nrounds: 74823"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 181725.76379007654,
            "unit": "iter/sec",
            "range": "stddev: 5.097062131538243e-7",
            "extra": "mean: 5.502797067097026 usec\nrounds: 39619"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 213930.81084799438,
            "unit": "iter/sec",
            "range": "stddev: 7.14486325256728e-7",
            "extra": "mean: 4.674408497009514 usec\nrounds: 49288"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 454926.3093660802,
            "unit": "iter/sec",
            "range": "stddev: 3.2011520430703415e-7",
            "extra": "mean: 2.198158205871751 usec\nrounds: 76116"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 467476.98005616845,
            "unit": "iter/sec",
            "range": "stddev: 3.1962718218077574e-7",
            "extra": "mean: 2.139142765660563 usec\nrounds: 67110"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 37577.66979420783,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016482505991062497",
            "extra": "mean: 26.6115489724735 usec\nrounds: 15815"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 603027.0917166407,
            "unit": "iter/sec",
            "range": "stddev: 2.544155337581598e-7",
            "extra": "mean: 1.6583002882230287 usec\nrounds: 53422"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 271381.1144639573,
            "unit": "iter/sec",
            "range": "stddev: 4.0595000456309175e-7",
            "extra": "mean: 3.6848547916653653 usec\nrounds: 51099"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 399992.6653759203,
            "unit": "iter/sec",
            "range": "stddev: 4.0913815286006205e-7",
            "extra": "mean: 2.500045842241087 usec\nrounds: 50063"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 237925.26691485796,
            "unit": "iter/sec",
            "range": "stddev: 5.116422590164394e-7",
            "extra": "mean: 4.203000433568294 usec\nrounds: 41508"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 219391.18802053225,
            "unit": "iter/sec",
            "range": "stddev: 4.85734280487533e-7",
            "extra": "mean: 4.558068211501789 usec\nrounds: 55064"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 56327.81495910846,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010808400926982017",
            "extra": "mean: 17.753218382888747 usec\nrounds: 21618"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 28114.34393670119,
            "unit": "iter/sec",
            "range": "stddev: 0.00004507516104830018",
            "extra": "mean: 35.56903203046379 usec\nrounds: 14174"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 37753.04026850402,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015845906516114258",
            "extra": "mean: 26.487932968785653 usec\nrounds: 9324"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 354.87598131862455,
            "unit": "iter/sec",
            "range": "stddev: 0.00020615637362318345",
            "extra": "mean: 2.8178858323526614 msec\nrounds: 340"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 34.136665286055766,
            "unit": "iter/sec",
            "range": "stddev: 0.00011472897267270275",
            "extra": "mean: 29.29401544117675 msec\nrounds: 34"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 27268.059862647522,
            "unit": "iter/sec",
            "range": "stddev: 0.000001687529269292487",
            "extra": "mean: 36.67294281430801 usec\nrounds: 13972"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 206.63721299631013,
            "unit": "iter/sec",
            "range": "stddev: 0.011458525623764955",
            "extra": "mean: 4.839399377777403 msec\nrounds: 225"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 14.216270968384915,
            "unit": "iter/sec",
            "range": "stddev: 0.06521061728887897",
            "extra": "mean: 70.34193440909125 msec\nrounds: 22"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 14588.411604901361,
            "unit": "iter/sec",
            "range": "stddev: 0.000004047954691637428",
            "extra": "mean: 68.54755864332918 usec\nrounds: 6369"
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
          "id": "3feeee73a2eaafd7a08fc09d036d16c72acc6cfa",
          "message": "chore: tighten AI-agent verification discipline in AGENTS.md and CONTRIBUTING.md (merges PR #747, addresses #743, #745)\n\nTwo complementary protocol additions driven by the #510 incident\n(the events-migration deferral that aged out invisibly):\n\n- Pre-Action Checks rows for refactor/migration proposals and issue\n  filing force a verification read of docs/decisions/, docs/usage/,\n  and closed-issue history before recommending. (#743)\n- A tracking-issue deferral convention: deferred work must produce a\n  filed follow-up issue before the tracker is closed, so deferrals\n  remain searchable via gh issue list --state open. (#745)\n\nAddresses #743\nAddresses #745",
          "timestamp": "2026-05-18T14:46:40+01:00",
          "tree_id": "77536912b49b9a5fe4cd07e6bb458156323894bc",
          "url": "https://github.com/endavis/pynetappfoundry/commit/3feeee73a2eaafd7a08fc09d036d16c72acc6cfa"
        },
        "date": 1779112078403,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1211868.5866577916,
            "unit": "iter/sec",
            "range": "stddev: 2.81090515487397e-7",
            "extra": "mean: 825.1719790492274 nsec\nrounds: 51076"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 728228.0672844737,
            "unit": "iter/sec",
            "range": "stddev: 4.571290274546462e-7",
            "extra": "mean: 1.37319617977504 usec\nrounds: 173341"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 462916.00110115396,
            "unit": "iter/sec",
            "range": "stddev: 6.086896555685156e-7",
            "extra": "mean: 2.160219127490228 usec\nrounds: 150830"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 469345.40383750654,
            "unit": "iter/sec",
            "range": "stddev: 5.429218496974725e-7",
            "extra": "mean: 2.1306270218557692 usec\nrounds: 155304"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 520072.7197280185,
            "unit": "iter/sec",
            "range": "stddev: 5.634322349579393e-7",
            "extra": "mean: 1.922808026775502 usec\nrounds: 77042"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 163604.85228291625,
            "unit": "iter/sec",
            "range": "stddev: 9.17511109088049e-7",
            "extra": "mean: 6.112288150663981 usec\nrounds: 53944"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 142427.80231587632,
            "unit": "iter/sec",
            "range": "stddev: 9.702289367518525e-7",
            "extra": "mean: 7.021101103436255 usec\nrounds: 69147"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 72205.19565976028,
            "unit": "iter/sec",
            "range": "stddev: 0.000003711748545747155",
            "extra": "mean: 13.849418879939364 usec\nrounds: 45784"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 219402.3253447651,
            "unit": "iter/sec",
            "range": "stddev: 0.000002021771206812892",
            "extra": "mean: 4.557836834357234 usec\nrounds: 39702"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30795.69048352078,
            "unit": "iter/sec",
            "range": "stddev: 0.000007980589114626176",
            "extra": "mean: 32.47207593981744 usec\nrounds: 2660"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 59.66028870802814,
            "unit": "iter/sec",
            "range": "stddev: 0.001947149628487567",
            "extra": "mean: 16.761568233333673 msec\nrounds: 60"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 63.93116446555453,
            "unit": "iter/sec",
            "range": "stddev: 0.0011694108640601351",
            "extra": "mean: 15.641823645161194 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 68.91941048483372,
            "unit": "iter/sec",
            "range": "stddev: 0.0006609320149122656",
            "extra": "mean: 14.509700430767007 msec\nrounds: 65"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 12.140683309482876,
            "unit": "iter/sec",
            "range": "stddev: 0.000788013846272733",
            "extra": "mean: 82.3676867692379 msec\nrounds: 13"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 309.3499375880734,
            "unit": "iter/sec",
            "range": "stddev: 0.00010261301715494255",
            "extra": "mean: 3.232585103448729 msec\nrounds: 261"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 61.210131174168836,
            "unit": "iter/sec",
            "range": "stddev: 0.0010353393294288947",
            "extra": "mean: 16.337164793105494 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.1513806267845987,
            "unit": "iter/sec",
            "range": "stddev: 0.17155814725178162",
            "extra": "mean: 868.5225170000024 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.129269644022065,
            "unit": "iter/sec",
            "range": "stddev: 0.17259365949023842",
            "extra": "mean: 885.5280980000032 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 409153.4358088647,
            "unit": "iter/sec",
            "range": "stddev: 6.009197230121636e-7",
            "extra": "mean: 2.4440708851022532 usec\nrounds: 11173"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 393978.7118719923,
            "unit": "iter/sec",
            "range": "stddev: 4.916980375676687e-7",
            "extra": "mean: 2.5382082073635246 usec\nrounds: 73470"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 386894.6706396134,
            "unit": "iter/sec",
            "range": "stddev: 5.036478916390514e-7",
            "extra": "mean: 2.584682798413331 usec\nrounds: 82591"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 170480.82454557624,
            "unit": "iter/sec",
            "range": "stddev: 8.751997925045229e-7",
            "extra": "mean: 5.865762338172295 usec\nrounds: 42855"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 203980.54700830166,
            "unit": "iter/sec",
            "range": "stddev: 7.659428923686468e-7",
            "extra": "mean: 4.902428269100101 usec\nrounds: 58120"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 437369.5722327634,
            "unit": "iter/sec",
            "range": "stddev: 4.831258724972006e-7",
            "extra": "mean: 2.2863959074588087 usec\nrounds: 84055"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 445487.24344067276,
            "unit": "iter/sec",
            "range": "stddev: 5.209192628934131e-7",
            "extra": "mean: 2.2447331875916525 usec\nrounds: 66305"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 36309.89664522542,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019762639759820105",
            "extra": "mean: 27.540700811427268 usec\nrounds: 16020"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 575826.7327708413,
            "unit": "iter/sec",
            "range": "stddev: 4.4979239969440383e-7",
            "extra": "mean: 1.7366335098547163 usec\nrounds: 47592"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 255924.6796958115,
            "unit": "iter/sec",
            "range": "stddev: 6.742901626264292e-7",
            "extra": "mean: 3.9073996348792392 usec\nrounds: 55876"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 364341.2568905018,
            "unit": "iter/sec",
            "range": "stddev: 5.146327170749804e-7",
            "extra": "mean: 2.744679558210278 usec\nrounds: 55411"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 218289.66219584268,
            "unit": "iter/sec",
            "range": "stddev: 9.491070775794801e-7",
            "extra": "mean: 4.581068979358404 usec\nrounds: 47188"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 203760.20925793925,
            "unit": "iter/sec",
            "range": "stddev: 8.144808408401485e-7",
            "extra": "mean: 4.907729549561386 usec\nrounds: 62407"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52016.26734201893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015603885035504395",
            "extra": "mean: 19.224755083342867 usec\nrounds: 21787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25456.054570340264,
            "unit": "iter/sec",
            "range": "stddev: 0.00004257400095821558",
            "extra": "mean: 39.283385303751466 usec\nrounds: 13296"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35504.36655060872,
            "unit": "iter/sec",
            "range": "stddev: 0.000002133164669210553",
            "extra": "mean: 28.16554968174344 usec\nrounds: 9118"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 335.55192550199376,
            "unit": "iter/sec",
            "range": "stddev: 0.00005279555905886505",
            "extra": "mean: 2.9801646898731873 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.52990106193584,
            "unit": "iter/sec",
            "range": "stddev: 0.0006266639268487187",
            "extra": "mean: 31.71592571875337 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25411.85454166497,
            "unit": "iter/sec",
            "range": "stddev: 0.000002713683020322647",
            "extra": "mean: 39.351712735503504 usec\nrounds: 13639"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 175.45012631896827,
            "unit": "iter/sec",
            "range": "stddev: 0.017892271999066314",
            "extra": "mean: 5.699625420514091 msec\nrounds: 195"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 10.68242969157084,
            "unit": "iter/sec",
            "range": "stddev: 0.10331611311834447",
            "extra": "mean: 93.61166222222532 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 14773.951083010914,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036167154040160115",
            "extra": "mean: 67.686700353972 usec\nrounds: 6501"
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
          "id": "9d23ee3b5c11d3b4695d15aed31de0d0ee9f8bab",
          "message": "fix: look up cluster IP from config in OntapBackend._get_api_client (merges PR #748, addresses #740)\n\n_get_api_client was passing the cluster name in the IP slot of\nClusterConfig, so ONTAPAPIClient built base_url=https://<name>/ and\nevery live request died with NameResolutionError on clusters that\nweren't DNS-resolvable hostnames. Mirror the existing _get_cli_client\npattern: look up the IP from Config.data[\"clusters\"][name][\"ip\"] and\nfall back to the cluster name when no IP is configured.\n\nAddresses #740",
          "timestamp": "2026-05-18T16:39:10+01:00",
          "tree_id": "8b89dc2f9519cb29d7d43651ba973cd3213f43f9",
          "url": "https://github.com/endavis/pynetappfoundry/commit/9d23ee3b5c11d3b4695d15aed31de0d0ee9f8bab"
        },
        "date": 1779118831770,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1159101.6508131833,
            "unit": "iter/sec",
            "range": "stddev: 3.325890768214984e-7",
            "extra": "mean: 862.7371027367932 nsec\nrounds: 64025"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 777826.2123734328,
            "unit": "iter/sec",
            "range": "stddev: 2.2474115917715848e-7",
            "extra": "mean: 1.2856342253478878 usec\nrounds: 190115"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 458652.27117540204,
            "unit": "iter/sec",
            "range": "stddev: 6.073117393264788e-7",
            "extra": "mean: 2.180300988017065 usec\nrounds: 170040"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 468318.08110540797,
            "unit": "iter/sec",
            "range": "stddev: 5.43200055361285e-7",
            "extra": "mean: 2.1353008571431227 usec\nrounds: 185151"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 513948.6471570558,
            "unit": "iter/sec",
            "range": "stddev: 5.188822281824785e-7",
            "extra": "mean: 1.945719685286794 usec\nrounds: 93024"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 164149.56130463356,
            "unit": "iter/sec",
            "range": "stddev: 9.801068027658066e-7",
            "extra": "mean: 6.092005315470631 usec\nrounds: 59450"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 143720.24539298262,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010690954128806834",
            "extra": "mean: 6.957961957730046 usec\nrounds: 77256"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 75347.87829938934,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013612746924002467",
            "extra": "mean: 13.27177383849579 usec\nrounds: 46060"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 237926.22350753314,
            "unit": "iter/sec",
            "range": "stddev: 7.555966784878384e-7",
            "extra": "mean: 4.202983535223213 usec\nrounds: 45309"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31111.821955461815,
            "unit": "iter/sec",
            "range": "stddev: 0.000002657725764873405",
            "extra": "mean: 32.14212274136666 usec\nrounds: 2656"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 76.09065633260147,
            "unit": "iter/sec",
            "range": "stddev: 0.0005122807312768975",
            "extra": "mean: 13.142218088235158 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 74.19015192835985,
            "unit": "iter/sec",
            "range": "stddev: 0.0006959499606331382",
            "extra": "mean: 13.478877910448665 msec\nrounds: 67"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 85.12298512353236,
            "unit": "iter/sec",
            "range": "stddev: 0.0007268726530328294",
            "extra": "mean: 11.747708313433533 msec\nrounds: 67"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.79701422642633,
            "unit": "iter/sec",
            "range": "stddev: 0.0008247775912251587",
            "extra": "mean: 84.76721150000088 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 312.4048809348917,
            "unit": "iter/sec",
            "range": "stddev: 0.00011291251548094415",
            "extra": "mean: 3.200974315789931 msec\nrounds: 285"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 76.67037753289004,
            "unit": "iter/sec",
            "range": "stddev: 0.0006867959923586027",
            "extra": "mean: 13.04284695312763 msec\nrounds: 64"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.272577454543608,
            "unit": "iter/sec",
            "range": "stddev: 0.15452308264432837",
            "extra": "mean: 785.8067863999963 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.3145609313933175,
            "unit": "iter/sec",
            "range": "stddev: 0.13309694721030518",
            "extra": "mean: 760.7102691999899 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 416343.9130480671,
            "unit": "iter/sec",
            "range": "stddev: 6.073950595887878e-7",
            "extra": "mean: 2.4018605020041437 usec\nrounds: 10122"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 392172.9458998238,
            "unit": "iter/sec",
            "range": "stddev: 6.20245424093872e-7",
            "extra": "mean: 2.5498954235752884 usec\nrounds: 86052"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 394096.538288826,
            "unit": "iter/sec",
            "range": "stddev: 5.287480589344846e-7",
            "extra": "mean: 2.5374493375202363 usec\nrounds: 97192"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 173303.5113828579,
            "unit": "iter/sec",
            "range": "stddev: 9.32579680216551e-7",
            "extra": "mean: 5.770223534541227 usec\nrounds: 44284"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 200837.44138640707,
            "unit": "iter/sec",
            "range": "stddev: 8.901026811648494e-7",
            "extra": "mean: 4.979151263314596 usec\nrounds: 37881"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 409511.709242783,
            "unit": "iter/sec",
            "range": "stddev: 9.089142484080989e-7",
            "extra": "mean: 2.4419326173824745 usec\nrounds: 46555"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 450957.59695872164,
            "unit": "iter/sec",
            "range": "stddev: 5.29737784490619e-7",
            "extra": "mean: 2.217503389995079 usec\nrounds: 84660"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34703.586773438496,
            "unit": "iter/sec",
            "range": "stddev: 0.000002684640981286682",
            "extra": "mean: 28.815465286872946 usec\nrounds: 16377"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 591440.0297573463,
            "unit": "iter/sec",
            "range": "stddev: 4.10554120234277e-7",
            "extra": "mean: 1.6907884987261956 usec\nrounds: 62775"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 259586.70466984148,
            "unit": "iter/sec",
            "range": "stddev: 6.857055269390313e-7",
            "extra": "mean: 3.852277416410298 usec\nrounds: 62736"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 378666.0117297205,
            "unit": "iter/sec",
            "range": "stddev: 5.536960275301485e-7",
            "extra": "mean: 2.640849638001753 usec\nrounds: 61691"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 231182.67674061374,
            "unit": "iter/sec",
            "range": "stddev: 6.986630193924817e-7",
            "extra": "mean: 4.325583621137829 usec\nrounds: 49784"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 207594.40776434634,
            "unit": "iter/sec",
            "range": "stddev: 8.71984229715913e-7",
            "extra": "mean: 4.817085444494073 usec\nrounds: 67857"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52515.162839565586,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018553009437204712",
            "extra": "mean: 19.04211937902604 usec\nrounds: 23840"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26282.338651583068,
            "unit": "iter/sec",
            "range": "stddev: 0.000034911451514490454",
            "extra": "mean: 38.04836446469602 usec\nrounds: 15140"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34976.45938451615,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030066406563559425",
            "extra": "mean: 28.590658334122107 usec\nrounds: 9641"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 329.05250427890655,
            "unit": "iter/sec",
            "range": "stddev: 0.00004291004602554489",
            "extra": "mean: 3.039028686900359 msec\nrounds: 313"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.67129810972821,
            "unit": "iter/sec",
            "range": "stddev: 0.0002711299124159932",
            "extra": "mean: 30.60790534375002 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25341.541675061337,
            "unit": "iter/sec",
            "range": "stddev: 0.000003847343434580447",
            "extra": "mean: 39.460898347163386 usec\nrounds: 13674"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 189.05593172199477,
            "unit": "iter/sec",
            "range": "stddev: 0.012892917893770697",
            "extra": "mean: 5.289439960394853 msec\nrounds: 202"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.297193225353126,
            "unit": "iter/sec",
            "range": "stddev: 0.07340915676558336",
            "extra": "mean: 75.20384061903736 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13547.915848410015,
            "unit": "iter/sec",
            "range": "stddev: 0.0000071793687271720315",
            "extra": "mean: 73.81209118724782 usec\nrounds: 5889"
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
          "id": "ca800505f7e48688937e81c3369cee84de44c08c",
          "message": "docs: demote netapp_ontap SDK from \"preferred pattern\" in ONTAP access patterns guide (merges PR #749, addresses #742)\n\ndocs: demote netapp_ontap SDK from preferred pattern; flip ADR-0013 to Accepted\n\nontap-access-patterns.md claimed the netapp_ontap SDK was the\n\"preferred pattern for most operations\" — contradicting ADR-0010,\nADR-0013, and the Phase 3f/4 migration. Correct that page (6 edits),\nadd a \"Preferred ONTAP Access Patterns\" pointer to docs/index.md as\nalways-loaded ground truth, and flip ADR-0013 from Proposed to\nAccepted (its content has been the implemented direction since\nPhase 3; ADR-0012 already declares itself superseded by it).\n\nAddresses #742",
          "timestamp": "2026-05-18T17:25:14+01:00",
          "tree_id": "8d5933c8fc812ff3cd96a5d491760ab17132562d",
          "url": "https://github.com/endavis/pynetappfoundry/commit/ca800505f7e48688937e81c3369cee84de44c08c"
        },
        "date": 1779121584367,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1212240.0682356388,
            "unit": "iter/sec",
            "range": "stddev: 3.39284065091999e-7",
            "extra": "mean: 824.919111488746 nsec\nrounds: 50378"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 754504.4879098198,
            "unit": "iter/sec",
            "range": "stddev: 4.385221781764402e-7",
            "extra": "mean: 1.3253731634788135 usec\nrounds: 159745"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 486708.21767982555,
            "unit": "iter/sec",
            "range": "stddev: 5.483534898612169e-7",
            "extra": "mean: 2.054619099646755 usec\nrounds: 156495"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 487737.1298510952,
            "unit": "iter/sec",
            "range": "stddev: 5.322393652732524e-7",
            "extra": "mean: 2.0502847513481233 usec\nrounds: 154584"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 529967.867290943,
            "unit": "iter/sec",
            "range": "stddev: 5.136050956057637e-7",
            "extra": "mean: 1.886906851752613 usec\nrounds: 77586"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 170581.04858496785,
            "unit": "iter/sec",
            "range": "stddev: 8.611265328276638e-7",
            "extra": "mean: 5.862315938935571 usec\nrounds: 52469"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 149703.96511126246,
            "unit": "iter/sec",
            "range": "stddev: 9.630373715525214e-7",
            "extra": "mean: 6.679849790596953 usec\nrounds: 68531"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 80581.91704490012,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012830321540700414",
            "extra": "mean: 12.409732067342125 usec\nrounds: 45866"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 246349.94693714762,
            "unit": "iter/sec",
            "range": "stddev: 7.101189572206145e-7",
            "extra": "mean: 4.059266147336068 usec\nrounds: 40053"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32810.23003500033,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020990107683623296",
            "extra": "mean: 30.47829896142909 usec\nrounds: 2696"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 77.15174721888556,
            "unit": "iter/sec",
            "range": "stddev: 0.0014513533211981558",
            "extra": "mean: 12.96146926087003 msec\nrounds: 69"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 81.38728420765545,
            "unit": "iter/sec",
            "range": "stddev: 0.0007467518240549754",
            "extra": "mean: 12.28693167164236 msec\nrounds: 67"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 93.16961552964436,
            "unit": "iter/sec",
            "range": "stddev: 0.0002615073966381839",
            "extra": "mean: 10.73311287499972 msec\nrounds: 72"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.937704700528608,
            "unit": "iter/sec",
            "range": "stddev: 0.008924688165536444",
            "extra": "mean: 83.7681970769238 msec\nrounds: 13"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 305.17192708273126,
            "unit": "iter/sec",
            "range": "stddev: 0.000045147742923205586",
            "extra": "mean: 3.2768413843285877 msec\nrounds: 268"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 83.19554529942216,
            "unit": "iter/sec",
            "range": "stddev: 0.00037054607194929366",
            "extra": "mean: 12.019874338235097 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2461493486666484,
            "unit": "iter/sec",
            "range": "stddev: 0.14424186140763692",
            "extra": "mean: 802.4720319999986 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2186757258275416,
            "unit": "iter/sec",
            "range": "stddev: 0.1511319987879278",
            "extra": "mean: 820.5628279999999 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 413631.15789273,
            "unit": "iter/sec",
            "range": "stddev: 6.100500963252709e-7",
            "extra": "mean: 2.4176128439998643 usec\nrounds: 11445"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 392878.5257085161,
            "unit": "iter/sec",
            "range": "stddev: 5.691393991536216e-7",
            "extra": "mean: 2.54531600625563 usec\nrounds: 72834"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 387969.51716449816,
            "unit": "iter/sec",
            "range": "stddev: 5.329397756208383e-7",
            "extra": "mean: 2.5775220880974583 usec\nrounds: 83348"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177727.5216929178,
            "unit": "iter/sec",
            "range": "stddev: 8.206498082779664e-7",
            "extra": "mean: 5.626590583577854 usec\nrounds: 42309"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 208646.78370527714,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010311874788779887",
            "extra": "mean: 4.792788952896319 usec\nrounds: 55689"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 434885.9476553438,
            "unit": "iter/sec",
            "range": "stddev: 4.775851405177303e-7",
            "extra": "mean: 2.2994534668030266 usec\nrounds: 86304"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 442563.0362934026,
            "unit": "iter/sec",
            "range": "stddev: 4.986897149611974e-7",
            "extra": "mean: 2.259565119525793 usec\nrounds: 78187"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 36533.052056372166,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019560108676259727",
            "extra": "mean: 27.372473519511985 usec\nrounds: 15653"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 556695.6967844851,
            "unit": "iter/sec",
            "range": "stddev: 4.3279077594537925e-7",
            "extra": "mean: 1.796313508036927 usec\nrounds: 53198"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 254264.89671417634,
            "unit": "iter/sec",
            "range": "stddev: 8.479510966243038e-7",
            "extra": "mean: 3.9329062443256473 usec\nrounds: 60007"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 350029.41403998854,
            "unit": "iter/sec",
            "range": "stddev: 5.265472759526873e-7",
            "extra": "mean: 2.8569027627082697 usec\nrounds: 57951"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 220508.71213015929,
            "unit": "iter/sec",
            "range": "stddev: 7.030891338599125e-7",
            "extra": "mean: 4.534968212093732 usec\nrounds: 47754"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 201942.64246706126,
            "unit": "iter/sec",
            "range": "stddev: 9.898568739380748e-7",
            "extra": "mean: 4.951901132833346 usec\nrounds: 57026"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 48798.35095239914,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064580921913223166",
            "extra": "mean: 20.49249576026576 usec\nrounds: 22761"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25818.10471563671,
            "unit": "iter/sec",
            "range": "stddev: 0.00003688637774033158",
            "extra": "mean: 38.732510035655366 usec\nrounds: 14299"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35260.5785675047,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024066517345329686",
            "extra": "mean: 28.360283371004464 usec\nrounds: 8840"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 331.9770990087074,
            "unit": "iter/sec",
            "range": "stddev: 0.00002592170801213848",
            "extra": "mean: 3.0122559748429243 msec\nrounds: 318"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.882183122484694,
            "unit": "iter/sec",
            "range": "stddev: 0.001373442426584574",
            "extra": "mean: 31.36548071875156 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 24222.702066488033,
            "unit": "iter/sec",
            "range": "stddev: 0.00001111190474818642",
            "extra": "mean: 41.28358583840629 usec\nrounds: 14038"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 173.24137143122854,
            "unit": "iter/sec",
            "range": "stddev: 0.018509013614880686",
            "extra": "mean: 5.772293256157748 msec\nrounds: 203"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 12.281764493312922,
            "unit": "iter/sec",
            "range": "stddev: 0.08538604663132457",
            "extra": "mean: 81.42152542857113 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 14866.211132031971,
            "unit": "iter/sec",
            "range": "stddev: 0.000004699539758720984",
            "extra": "mean: 67.26663513108038 usec\nrounds: 6564"
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
          "id": "f0b21cc63f05a2123e5e809e175fffd4eaf7bb20",
          "message": "chore: resolve doit audit vulnerabilities (idna, pymdown-extensions) (merges PR #760, addresses #759)\n\nUpgrade transitive deps flagged by pip-audit to non-vulnerable versions:\n- idna 3.11 -> 3.16 (CVE-2026-45409)\n- pymdown-extensions 10.21.2 -> 10.21.3 (CVE-2026-46338)\n\nBoth are transitive dependencies, so this is a uv.lock-only change with no\npyproject.toml constraint changes.\n\nAddresses #759\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-05-26T14:33:23+01:00",
          "tree_id": "06a97f3883d102f2433dfb5ce0616aade94bb5ed",
          "url": "https://github.com/endavis/pynetappfoundry/commit/f0b21cc63f05a2123e5e809e175fffd4eaf7bb20"
        },
        "date": 1779802475002,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1189809.4182757088,
            "unit": "iter/sec",
            "range": "stddev: 2.8427992985067917e-7",
            "extra": "mean: 840.4707381197371 nsec\nrounds: 69852"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 720512.4619071092,
            "unit": "iter/sec",
            "range": "stddev: 6.316028372173042e-7",
            "extra": "mean: 1.3879010466427202 usec\nrounds: 70892"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 470805.77751523705,
            "unit": "iter/sec",
            "range": "stddev: 4.925282837074257e-7",
            "extra": "mean: 2.124018114810913 usec\nrounds: 168039"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 467217.0634435303,
            "unit": "iter/sec",
            "range": "stddev: 5.317365361630484e-7",
            "extra": "mean: 2.1403327879972944 usec\nrounds: 164420"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 517624.8665375356,
            "unit": "iter/sec",
            "range": "stddev: 5.133445710255118e-7",
            "extra": "mean: 1.9319010052379022 usec\nrounds: 83459"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 163000.3329502247,
            "unit": "iter/sec",
            "range": "stddev: 8.679880890966128e-7",
            "extra": "mean: 6.134956793648816 usec\nrounds: 57399"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141998.6481960801,
            "unit": "iter/sec",
            "range": "stddev: 9.8406093790433e-7",
            "extra": "mean: 7.042320562229163 usec\nrounds: 70289"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74724.2478620007,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012990257157728752",
            "extra": "mean: 13.38253684194695 usec\nrounds: 46211"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 234666.97765518082,
            "unit": "iter/sec",
            "range": "stddev: 7.429196420196643e-7",
            "extra": "mean: 4.261357989062262 usec\nrounds: 46169"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31186.510617626314,
            "unit": "iter/sec",
            "range": "stddev: 0.000002826418645519357",
            "extra": "mean: 32.06514548103402 usec\nrounds: 3485"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 69.15327417190514,
            "unit": "iter/sec",
            "range": "stddev: 0.0014758048420140516",
            "extra": "mean: 14.460631285716758 msec\nrounds: 63"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 69.34880776027002,
            "unit": "iter/sec",
            "range": "stddev: 0.0012836825024162277",
            "extra": "mean: 14.419858571424507 msec\nrounds: 63"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 78.49292763550241,
            "unit": "iter/sec",
            "range": "stddev: 0.0009718222697078127",
            "extra": "mean: 12.74000129850806 msec\nrounds: 67"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.635647794386363,
            "unit": "iter/sec",
            "range": "stddev: 0.0005982459915971098",
            "extra": "mean: 85.94278700000284 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 312.24504293696634,
            "unit": "iter/sec",
            "range": "stddev: 0.0000429403365764832",
            "extra": "mean: 3.2026128920864005 msec\nrounds: 278"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 67.9914374948659,
            "unit": "iter/sec",
            "range": "stddev: 0.0013856573397222885",
            "extra": "mean: 14.707734338982183 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.3077261204600823,
            "unit": "iter/sec",
            "range": "stddev: 0.1301690225203358",
            "extra": "mean: 764.686109999991 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2870115963451416,
            "unit": "iter/sec",
            "range": "stddev: 0.13425915149832232",
            "extra": "mean: 776.9937760000005 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 414131.59981817845,
            "unit": "iter/sec",
            "range": "stddev: 6.546514656109001e-7",
            "extra": "mean: 2.4146913696975623 usec\nrounds: 11969"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 399256.78252585273,
            "unit": "iter/sec",
            "range": "stddev: 6.087510399855668e-7",
            "extra": "mean: 2.504653756095547 usec\nrounds: 81948"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 393276.54724694183,
            "unit": "iter/sec",
            "range": "stddev: 5.764301093734608e-7",
            "extra": "mean: 2.5427399803021844 usec\nrounds: 95612"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 174421.23320014955,
            "unit": "iter/sec",
            "range": "stddev: 9.181265183001046e-7",
            "extra": "mean: 5.733246931309637 usec\nrounds: 41712"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 207212.36069505403,
            "unit": "iter/sec",
            "range": "stddev: 8.976619617000306e-7",
            "extra": "mean: 4.825966929027266 usec\nrounds: 56424"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 441969.73017380456,
            "unit": "iter/sec",
            "range": "stddev: 5.376323160226102e-7",
            "extra": "mean: 2.2625983901810427 usec\nrounds: 87712"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 446651.95454954234,
            "unit": "iter/sec",
            "range": "stddev: 6.123651009709939e-7",
            "extra": "mean: 2.238879713419189 usec\nrounds: 88098"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35079.35809135533,
            "unit": "iter/sec",
            "range": "stddev: 0.000002421220307973195",
            "extra": "mean: 28.50679300903262 usec\nrounds: 16450"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 593055.6640276485,
            "unit": "iter/sec",
            "range": "stddev: 4.5372584822929865e-7",
            "extra": "mean: 1.6861823613801274 usec\nrounds: 58066"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263349.253030062,
            "unit": "iter/sec",
            "range": "stddev: 6.792202279292868e-7",
            "extra": "mean: 3.7972387940885755 usec\nrounds: 60169"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 378618.26798596355,
            "unit": "iter/sec",
            "range": "stddev: 5.806445262046396e-7",
            "extra": "mean: 2.6411826490027495 usec\nrounds: 65322"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 230553.46125850346,
            "unit": "iter/sec",
            "range": "stddev: 7.923524912961756e-7",
            "extra": "mean: 4.337388797120552 usec\nrounds: 47827"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209120.37464328692,
            "unit": "iter/sec",
            "range": "stddev: 7.775548880297864e-7",
            "extra": "mean: 4.781934814844219 usec\nrounds: 68037"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52876.43282081618,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018304276048367867",
            "extra": "mean: 18.912017067957805 usec\nrounds: 22967"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26057.884173233244,
            "unit": "iter/sec",
            "range": "stddev: 0.000043165241632808296",
            "extra": "mean: 38.37610119655086 usec\nrounds: 11117"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34798.761487852826,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029436199266942817",
            "extra": "mean: 28.73665490506233 usec\nrounds: 9296"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 328.9605322007146,
            "unit": "iter/sec",
            "range": "stddev: 0.00010913950071625076",
            "extra": "mean: 3.039878350482033 msec\nrounds: 311"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.05644412444737,
            "unit": "iter/sec",
            "range": "stddev: 0.00038616136296072424",
            "extra": "mean: 32.199436483869974 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25644.074213693515,
            "unit": "iter/sec",
            "range": "stddev: 0.000003965987257990331",
            "extra": "mean: 38.995363672205265 usec\nrounds: 12635"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 184.93980864421292,
            "unit": "iter/sec",
            "range": "stddev: 0.014483718749350014",
            "extra": "mean: 5.407164673365697 msec\nrounds: 199"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 12.805608905483867,
            "unit": "iter/sec",
            "range": "stddev: 0.07794563428968632",
            "extra": "mean: 78.09078095238101 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13748.81237151649,
            "unit": "iter/sec",
            "range": "stddev: 0.000006146842453706396",
            "extra": "mean: 72.73355494120402 usec\nrounds: 6689"
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
          "id": "235e3a64b7e34ac280b8f1d96c7abe7e52370a63",
          "message": "chore(deps): bump cryptography to 48.0.1 for GHSA-537c-gmf6-5ccf (merges PR #777, addresses #776)\n\nchore(deps): bump cryptography to >=48.0.1 for GHSA-537c-gmf6-5ccf\n\npip-audit flagged cryptography 47.0.0 as vulnerable to\nGHSA-537c-gmf6-5ccf (fix 48.0.1). Bump the pyproject floor and\nrefresh uv.lock; resolver picked cryptography 49.0.0.\n\nAddresses #776\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-06-17T15:26:46+01:00",
          "tree_id": "3850af0bbb24cfeb2afa9957b3d804011f513da7",
          "url": "https://github.com/endavis/pynetappfoundry/commit/235e3a64b7e34ac280b8f1d96c7abe7e52370a63"
        },
        "date": 1781706477334,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1076340.2668897985,
            "unit": "iter/sec",
            "range": "stddev: 3.1696189686835515e-7",
            "extra": "mean: 929.0742256532018 nsec\nrounds: 55237"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 720434.8304081501,
            "unit": "iter/sec",
            "range": "stddev: 4.5873633973243087e-7",
            "extra": "mean: 1.388050601930874 usec\nrounds: 185151"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 453828.4853486572,
            "unit": "iter/sec",
            "range": "stddev: 5.715260707638482e-7",
            "extra": "mean: 2.203475613109086 usec\nrounds: 155473"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 451153.42453757644,
            "unit": "iter/sec",
            "range": "stddev: 5.473433125665334e-7",
            "extra": "mean: 2.2165408608501216 usec\nrounds: 162576"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 488689.63445127726,
            "unit": "iter/sec",
            "range": "stddev: 5.762356225340878e-7",
            "extra": "mean: 2.0462885428761854 usec\nrounds: 86566"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 156653.8872588303,
            "unit": "iter/sec",
            "range": "stddev: 9.786782580718336e-7",
            "extra": "mean: 6.38349942984662 usec\nrounds: 53491"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 136104.13639318952,
            "unit": "iter/sec",
            "range": "stddev: 0.000001113554618820028",
            "extra": "mean: 7.347315272704958 usec\nrounds: 69267"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 71731.73530578983,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013552239319558069",
            "extra": "mean: 13.940831010668232 usec\nrounds: 44920"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 230358.2533393284,
            "unit": "iter/sec",
            "range": "stddev: 8.575990615870623e-7",
            "extra": "mean: 4.3410643443582355 usec\nrounds: 46018"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 29181.43084233535,
            "unit": "iter/sec",
            "range": "stddev: 0.000003714469531239744",
            "extra": "mean: 34.26836762744467 usec\nrounds: 2984"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 56.14908198906918,
            "unit": "iter/sec",
            "range": "stddev: 0.0003134768527900539",
            "extra": "mean: 17.80973017857487 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 56.34458691839482,
            "unit": "iter/sec",
            "range": "stddev: 0.0005084576711845755",
            "extra": "mean: 17.747933824562836 msec\nrounds: 57"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 63.95357402375669,
            "unit": "iter/sec",
            "range": "stddev: 0.0003862376889290762",
            "extra": "mean: 15.63634269491385 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.109977533356524,
            "unit": "iter/sec",
            "range": "stddev: 0.0012725205296236144",
            "extra": "mean: 90.00918291667166 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 315.32478296838246,
            "unit": "iter/sec",
            "range": "stddev: 0.000049667527345824476",
            "extra": "mean: 3.1713333490196036 msec\nrounds: 255"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 56.651963727582135,
            "unit": "iter/sec",
            "range": "stddev: 0.0003249999279886815",
            "extra": "mean: 17.651638781819138 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2624740379063009,
            "unit": "iter/sec",
            "range": "stddev: 0.1382227949799542",
            "extra": "mean: 792.0954966000011 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2799435576429032,
            "unit": "iter/sec",
            "range": "stddev: 0.14065628195009947",
            "extra": "mean: 781.2844511999913 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 415060.5972402223,
            "unit": "iter/sec",
            "range": "stddev: 5.621530871633047e-7",
            "extra": "mean: 2.40928675631726 usec\nrounds: 11379"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 392396.24267164426,
            "unit": "iter/sec",
            "range": "stddev: 5.892722615933765e-7",
            "extra": "mean: 2.548444381606366 usec\nrounds: 72485"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 386105.33890581044,
            "unit": "iter/sec",
            "range": "stddev: 7.284791265244228e-7",
            "extra": "mean: 2.589966776512116 usec\nrounds: 97762"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 171247.84652552876,
            "unit": "iter/sec",
            "range": "stddev: 8.995623384303719e-7",
            "extra": "mean: 5.839489490169589 usec\nrounds: 31114"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 195882.68944236368,
            "unit": "iter/sec",
            "range": "stddev: 0.000001331141119918425",
            "extra": "mean: 5.105096335193207 usec\nrounds: 59376"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 428411.1956315274,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010492506740156405",
            "extra": "mean: 2.3342060389572334 usec\nrounds: 78291"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 444725.5793520599,
            "unit": "iter/sec",
            "range": "stddev: 5.423441331075875e-7",
            "extra": "mean: 2.2485776542400453 usec\nrounds: 79854"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 33894.099030008634,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025947561838353783",
            "extra": "mean: 29.50366077335867 usec\nrounds: 13914"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 570521.7269920332,
            "unit": "iter/sec",
            "range": "stddev: 4.346966157622026e-7",
            "extra": "mean: 1.7527816254646582 usec\nrounds: 58679"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 243903.9238384045,
            "unit": "iter/sec",
            "range": "stddev: 7.349968887072715e-7",
            "extra": "mean: 4.099975040428368 usec\nrounds: 47597"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 370727.7618893632,
            "unit": "iter/sec",
            "range": "stddev: 5.52072814389019e-7",
            "extra": "mean: 2.697397127486858 usec\nrounds: 63292"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 224373.76222400324,
            "unit": "iter/sec",
            "range": "stddev: 8.05348878109313e-7",
            "extra": "mean: 4.456849098967513 usec\nrounds: 23585"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 197657.33141822688,
            "unit": "iter/sec",
            "range": "stddev: 8.102746121761991e-7",
            "extra": "mean: 5.059260857286802 usec\nrounds: 67259"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 51201.72930945459,
            "unit": "iter/sec",
            "range": "stddev: 0.000001783548507623563",
            "extra": "mean: 19.53059034307551 usec\nrounds: 18474"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25193.135410872077,
            "unit": "iter/sec",
            "range": "stddev: 0.00003997522371465422",
            "extra": "mean: 39.69335232360363 usec\nrounds: 10953"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34792.64162562259,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029549603685728538",
            "extra": "mean: 28.741709547675246 usec\nrounds: 9196"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 330.4966991104697,
            "unit": "iter/sec",
            "range": "stddev: 0.00005086204582079313",
            "extra": "mean: 3.025748828026105 msec\nrounds: 314"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.768097220614013,
            "unit": "iter/sec",
            "range": "stddev: 0.00046414419358503135",
            "extra": "mean: 32.5011973548374 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25348.4559927387,
            "unit": "iter/sec",
            "range": "stddev: 0.000003801355655401043",
            "extra": "mean: 39.4501345678198 usec\nrounds: 12581"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 183.50341041090263,
            "unit": "iter/sec",
            "range": "stddev: 0.014582979890587572",
            "extra": "mean: 5.449489999999402 msec\nrounds: 204"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 12.693382020407467,
            "unit": "iter/sec",
            "range": "stddev: 0.07966295191370375",
            "extra": "mean: 78.78121042857413 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13486.154089223855,
            "unit": "iter/sec",
            "range": "stddev: 0.0000067536655766904435",
            "extra": "mean: 74.15012414837025 usec\nrounds: 5872"
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
          "id": "b27a7dbd63168b003644b60ab662fba1d1b8f5a0",
          "message": "feat: add cifs session command to query active CIFS sessions (merges PR #778, addresses #775)\n\n* feat: add cifs session command to query active CIFS sessions\n\nAdd `nf cifs session` under a new `cifs` command group, using\nDataSource (ADR-0012/0013) to list active CIFS/SMB sessions across\nin-scope clusters. Supports --user (glob), --ip (glob or CIDR), and\noptional CSV export. Always queries live because CIFS sessions are\ntransient and the model has no cache table.\n\nRemoves the previously uncommitted SDK-based find_user.py — the new\nsession command supersedes it, and tests/template/test_doit_audit_legacy.py\nnow enforces the NetApp-SDK candidate count.\n\nAddresses #775\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n\n* test: harden cifs session csv assertion against rich line-wrap\n\nRich wraps the resolved CSV path at narrow terminal widths (macOS CI\nrunners default to 80 cols), inserting whitespace inside the path and\nbreaking the substring check. Collapse all whitespace from both haystack\nand needle before comparing.\n\nAddresses #775\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n\n---------\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-06-17T16:26:28+01:00",
          "tree_id": "d9d65537b40c259a3c06ab4d799a3457a90496ef",
          "url": "https://github.com/endavis/pynetappfoundry/commit/b27a7dbd63168b003644b60ab662fba1d1b8f5a0"
        },
        "date": 1781710067762,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1106534.3369577564,
            "unit": "iter/sec",
            "range": "stddev: 3.1568970604961176e-7",
            "extra": "mean: 903.7225204862093 nsec\nrounds: 57561"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 702249.4390903598,
            "unit": "iter/sec",
            "range": "stddev: 4.966291819950573e-7",
            "extra": "mean: 1.4239954414136997 usec\nrounds: 177905"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 443417.4421487237,
            "unit": "iter/sec",
            "range": "stddev: 5.946275079488529e-7",
            "extra": "mean: 2.255211241024201 usec\nrounds: 165536"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 442999.89314005146,
            "unit": "iter/sec",
            "range": "stddev: 6.406419699544642e-7",
            "extra": "mean: 2.257336887627322 usec\nrounds: 154274"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 479878.114088912,
            "unit": "iter/sec",
            "range": "stddev: 7.913108205314236e-7",
            "extra": "mean: 2.083862486411955 usec\nrounds: 83599"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 152863.41214452224,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010482689574264855",
            "extra": "mean: 6.541787769689233 usec\nrounds: 39688"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 134874.75453412908,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011639804357345636",
            "extra": "mean: 7.414285968149489 usec\nrounds: 68088"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 70162.43636713666,
            "unit": "iter/sec",
            "range": "stddev: 0.000001624131424460657",
            "extra": "mean: 14.252640754481973 usec\nrounds: 44741"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 222875.95268626264,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013368195487705567",
            "extra": "mean: 4.486800787376452 usec\nrounds: 39375"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 28956.83232350496,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031881880594142307",
            "extra": "mean: 34.53416412499912 usec\nrounds: 2754"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 55.27270691336946,
            "unit": "iter/sec",
            "range": "stddev: 0.001376987079276426",
            "extra": "mean: 18.092111927272338 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 56.24759333166754,
            "unit": "iter/sec",
            "range": "stddev: 0.0012631641082775627",
            "extra": "mean: 17.778538436363593 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 62.30867674846093,
            "unit": "iter/sec",
            "range": "stddev: 0.0009503139559553198",
            "extra": "mean: 16.049129145158755 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.3034074353227,
            "unit": "iter/sec",
            "range": "stddev: 0.008545593133261921",
            "extra": "mean: 97.05527091666255 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 308.2688026891709,
            "unit": "iter/sec",
            "range": "stddev: 0.00034328190400996955",
            "extra": "mean: 3.2439221590914777 msec\nrounds: 264"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 63.30779891852344,
            "unit": "iter/sec",
            "range": "stddev: 0.0015880913958073607",
            "extra": "mean: 15.795842172415295 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2723085551489917,
            "unit": "iter/sec",
            "range": "stddev: 0.13589700700798688",
            "extra": "mean: 785.9728647999987 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2690477622349063,
            "unit": "iter/sec",
            "range": "stddev: 0.13551947094414965",
            "extra": "mean: 787.9924063999852 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 428347.1852230319,
            "unit": "iter/sec",
            "range": "stddev: 8.943153919463598e-7",
            "extra": "mean: 2.334554852926884 usec\nrounds: 12807"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 398048.6425743627,
            "unit": "iter/sec",
            "range": "stddev: 8.534976365670717e-7",
            "extra": "mean: 2.5122557723913905 usec\nrounds: 79473"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 400111.3579219126,
            "unit": "iter/sec",
            "range": "stddev: 5.631008681512005e-7",
            "extra": "mean: 2.499304206693288 usec\nrounds: 89929"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 174226.0561772866,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010752196438478902",
            "extra": "mean: 5.739669610511263 usec\nrounds: 42913"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 206616.70533445248,
            "unit": "iter/sec",
            "range": "stddev: 8.919554499937653e-7",
            "extra": "mean: 4.839879710506903 usec\nrounds: 59415"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 447593.63090536476,
            "unit": "iter/sec",
            "range": "stddev: 5.629151890004636e-7",
            "extra": "mean: 2.2341694138436727 usec\nrounds: 90819"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 461259.102187696,
            "unit": "iter/sec",
            "range": "stddev: 5.416296101829736e-7",
            "extra": "mean: 2.1679788978843373 usec\nrounds: 76959"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35052.63572718797,
            "unit": "iter/sec",
            "range": "stddev: 0.000002837274036701633",
            "extra": "mean: 28.52852515237156 usec\nrounds: 16241"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 566093.9231612146,
            "unit": "iter/sec",
            "range": "stddev: 4.856786999708254e-7",
            "extra": "mean: 1.7664913172283176 usec\nrounds: 59025"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 248678.4330618401,
            "unit": "iter/sec",
            "range": "stddev: 6.855834807706507e-7",
            "extra": "mean: 4.021257443548894 usec\nrounds: 66904"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 371778.2583150319,
            "unit": "iter/sec",
            "range": "stddev: 6.297720784478463e-7",
            "extra": "mean: 2.689775363767063 usec\nrounds: 71342"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 223710.906811509,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010788401429039301",
            "extra": "mean: 4.47005474276033 usec\nrounds: 37594"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 200524.0510009715,
            "unit": "iter/sec",
            "range": "stddev: 8.451137059621284e-7",
            "extra": "mean: 4.986932963942341 usec\nrounds: 63533"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 51587.21104671707,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020586462042626878",
            "extra": "mean: 19.38464940650515 usec\nrounds: 22325"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25579.0710676248,
            "unit": "iter/sec",
            "range": "stddev: 0.00003709252821154805",
            "extra": "mean: 39.09446114584243 usec\nrounds: 14696"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34703.28493149323,
            "unit": "iter/sec",
            "range": "stddev: 0.000003087874994959684",
            "extra": "mean: 28.8157159177891 usec\nrounds: 9015"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 329.4874860124977,
            "unit": "iter/sec",
            "range": "stddev: 0.000043638706094304226",
            "extra": "mean: 3.035016631745672 msec\nrounds: 315"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.143736003009856,
            "unit": "iter/sec",
            "range": "stddev: 0.0003724047633782411",
            "extra": "mean: 32.10918561290642 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25474.888729092105,
            "unit": "iter/sec",
            "range": "stddev: 0.000004171729349227739",
            "extra": "mean: 39.25434221261224 usec\nrounds: 12989"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 181.6705585840058,
            "unit": "iter/sec",
            "range": "stddev: 0.014560476649198214",
            "extra": "mean: 5.504469231527092 msec\nrounds: 203"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.867910629411552,
            "unit": "iter/sec",
            "range": "stddev: 0.0843643309098231",
            "extra": "mean: 84.26082999999664 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13412.363612043684,
            "unit": "iter/sec",
            "range": "stddev: 0.000007906667219395638",
            "extra": "mean: 74.5580740968017 usec\nrounds: 6505"
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
          "id": "d62fc0ed2fdf24b21b3478cadb03b44a5a8476da",
          "message": "chore: bump msgpack and pydantic-settings to resolve audit CVEs (merges PR #791, addresses #790)\n\nBump transitive deps in uv.lock to clear pip-audit findings:\n- msgpack 1.1.2 -> 1.2.1 (GHSA-6v7p-g79w-8964, Unpacker SEGV/DoS)\n- pydantic-settings 2.14.1 -> 2.14.2 (GHSA-4xgf-cpjx-pc3j, symlink\n  traversal in NestedSecretsSettingsSource)\n\nAddresses #790\n\nCo-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-07-01T10:50:25+01:00",
          "tree_id": "cd85b88eaba1efb27bec59f71f075c10977fd553",
          "url": "https://github.com/endavis/pynetappfoundry/commit/d62fc0ed2fdf24b21b3478cadb03b44a5a8476da"
        },
        "date": 1782899497686,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1114949.9088149648,
            "unit": "iter/sec",
            "range": "stddev: 5.013377988269677e-7",
            "extra": "mean: 896.9012796842682 nsec\nrounds: 65326"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 713328.1355188765,
            "unit": "iter/sec",
            "range": "stddev: 5.627898862253577e-7",
            "extra": "mean: 1.401879373890948 usec\nrounds: 145922"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 454511.37552500376,
            "unit": "iter/sec",
            "range": "stddev: 6.507928660772304e-7",
            "extra": "mean: 2.2001649548262794 usec\nrounds: 147016"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 450509.37833644566,
            "unit": "iter/sec",
            "range": "stddev: 6.128411326495791e-7",
            "extra": "mean: 2.2197096177944347 usec\nrounds: 149410"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 493753.58389536693,
            "unit": "iter/sec",
            "range": "stddev: 6.151781414862546e-7",
            "extra": "mean: 2.0253017549983263 usec\nrounds: 84446"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 155912.81149385788,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012465991821835133",
            "extra": "mean: 6.413841110416988 usec\nrounds: 54541"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 129573.37344964198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000050343949888665906",
            "extra": "mean: 7.717634984541363 usec\nrounds: 67304"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 72864.77041444468,
            "unit": "iter/sec",
            "range": "stddev: 0.000001683489919986249",
            "extra": "mean: 13.724053397988344 usec\nrounds: 43953"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232469.93043778965,
            "unit": "iter/sec",
            "range": "stddev: 8.443857034267313e-7",
            "extra": "mean: 4.301631605071633 usec\nrounds: 44303"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30594.717512741612,
            "unit": "iter/sec",
            "range": "stddev: 0.00000281625330480739",
            "extra": "mean: 32.68538104931139 usec\nrounds: 2955"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 71.0210246150403,
            "unit": "iter/sec",
            "range": "stddev: 0.0007893469959982883",
            "extra": "mean: 14.080337553849194 msec\nrounds: 65"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 55.980798828910764,
            "unit": "iter/sec",
            "range": "stddev: 0.0019177699345157197",
            "extra": "mean: 17.863267779658038 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 65.03503020412907,
            "unit": "iter/sec",
            "range": "stddev: 0.0011809284364919582",
            "extra": "mean: 15.376328677963926 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.10184290203552,
            "unit": "iter/sec",
            "range": "stddev: 0.0009770351728904192",
            "extra": "mean: 90.07513516667132 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 305.8474898275904,
            "unit": "iter/sec",
            "range": "stddev: 0.00004554893760289506",
            "extra": "mean: 3.269603424123935 msec\nrounds: 257"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 67.65050093165603,
            "unit": "iter/sec",
            "range": "stddev: 0.0015976332417016233",
            "extra": "mean: 14.781856545456343 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.259152518064872,
            "unit": "iter/sec",
            "range": "stddev: 0.13933636775554606",
            "extra": "mean: 794.1849662000038 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2627399774632004,
            "unit": "iter/sec",
            "range": "stddev: 0.13983118840530337",
            "extra": "mean: 791.9286772000078 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 397695.6529092332,
            "unit": "iter/sec",
            "range": "stddev: 9.380553603422626e-7",
            "extra": "mean: 2.5144856190525973 usec\nrounds: 9596"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 387944.59185916645,
            "unit": "iter/sec",
            "range": "stddev: 6.030969389252665e-7",
            "extra": "mean: 2.577687692996697 usec\nrounds: 77078"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 379948.0439982142,
            "unit": "iter/sec",
            "range": "stddev: 6.933816862626024e-7",
            "extra": "mean: 2.6319388026766632 usec\nrounds: 87177"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 167021.10568234968,
            "unit": "iter/sec",
            "range": "stddev: 9.585304767450561e-7",
            "extra": "mean: 5.987267273286152 usec\nrounds: 44303"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 199440.35007125043,
            "unit": "iter/sec",
            "range": "stddev: 9.001994117734861e-7",
            "extra": "mean: 5.01403050908579 usec\nrounds: 55885"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 426419.5260227241,
            "unit": "iter/sec",
            "range": "stddev: 7.887207672678507e-7",
            "extra": "mean: 2.3451083709208698 usec\nrounds: 90827"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 427829.3255664257,
            "unit": "iter/sec",
            "range": "stddev: 6.647866806672595e-7",
            "extra": "mean: 2.3373806801954204 usec\nrounds: 78407"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 33843.8135871676,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027097670896142313",
            "extra": "mean: 29.54749757808515 usec\nrounds: 15897"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 582320.4012744946,
            "unit": "iter/sec",
            "range": "stddev: 5.962195967627065e-7",
            "extra": "mean: 1.7172676722494207 usec\nrounds: 60533"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263397.7420106348,
            "unit": "iter/sec",
            "range": "stddev: 8.186365632076661e-7",
            "extra": "mean: 3.7965397590979526 usec\nrounds: 63256"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 377525.13859433075,
            "unit": "iter/sec",
            "range": "stddev: 6.566647012398316e-7",
            "extra": "mean: 2.6488302308115936 usec\nrounds: 59734"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 228427.10498365024,
            "unit": "iter/sec",
            "range": "stddev: 8.028886070821925e-7",
            "extra": "mean: 4.377764189024658 usec\nrounds: 48857"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209123.79233310302,
            "unit": "iter/sec",
            "range": "stddev: 8.999593834029773e-7",
            "extra": "mean: 4.781856664148234 usec\nrounds: 66543"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52421.33103233511,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019664332320208486",
            "extra": "mean: 19.07620390987724 usec\nrounds: 22456"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26181.7287122609,
            "unit": "iter/sec",
            "range": "stddev: 0.00003862197288060473",
            "extra": "mean: 38.19457496447513 usec\nrounds: 14827"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35167.19123638988,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028173884617689944",
            "extra": "mean: 28.435594792831566 usec\nrounds: 9679"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 327.44012698184207,
            "unit": "iter/sec",
            "range": "stddev: 0.0003376992028048137",
            "extra": "mean: 3.0539934406251135 msec\nrounds: 320"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.25874279521557,
            "unit": "iter/sec",
            "range": "stddev: 0.0010989454566082168",
            "extra": "mean: 30.999348187503273 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25613.25870572398,
            "unit": "iter/sec",
            "range": "stddev: 0.000004466370630373502",
            "extra": "mean: 39.04227929328347 usec\nrounds: 14039"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 186.16523151426537,
            "unit": "iter/sec",
            "range": "stddev: 0.01405146620622573",
            "extra": "mean: 5.3715722955678356 msec\nrounds: 203"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.374259702809185,
            "unit": "iter/sec",
            "range": "stddev: 0.07359134483580869",
            "extra": "mean: 74.77049363636597 msec\nrounds: 22"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13819.676810679539,
            "unit": "iter/sec",
            "range": "stddev: 0.000006659949136980737",
            "extra": "mean: 72.36059234230588 usec\nrounds: 7104"
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
          "id": "b32974814ac6541fc316851323bf81109d18a5e1",
          "message": "chore(deps): Bump codecov/codecov-action from 6 to 7 (merges PR #765)\n\nBumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 6 to 7.\n- [Release notes](https://github.com/codecov/codecov-action/releases)\n- [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/codecov/codecov-action/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: codecov/codecov-action\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-07-01T11:48:25+01:00",
          "tree_id": "5cd5d7587c54e3b8164a88bfb111203243989e03",
          "url": "https://github.com/endavis/pynetappfoundry/commit/b32974814ac6541fc316851323bf81109d18a5e1"
        },
        "date": 1782903008171,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1142307.509425186,
            "unit": "iter/sec",
            "range": "stddev: 2.917760632436266e-7",
            "extra": "mean: 875.4210155750479 nsec\nrounds: 63943"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 731349.4080323883,
            "unit": "iter/sec",
            "range": "stddev: 4.4758063698197765e-7",
            "extra": "mean: 1.3673354883685285 usec\nrounds: 181127"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 452428.91740406264,
            "unit": "iter/sec",
            "range": "stddev: 5.5466024188463e-7",
            "extra": "mean: 2.2102919630729607 usec\nrounds: 113302"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 456657.7099391373,
            "unit": "iter/sec",
            "range": "stddev: 5.715659246079409e-7",
            "extra": "mean: 2.1898239715109127 usec\nrounds: 161525"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 499258.34051463683,
            "unit": "iter/sec",
            "range": "stddev: 5.47896226658539e-7",
            "extra": "mean: 2.002971044948788 usec\nrounds: 84303"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 158479.1214495916,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013015827519775008",
            "extra": "mean: 6.309979452517826 usec\nrounds: 28568"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 138423.2166634262,
            "unit": "iter/sec",
            "range": "stddev: 9.83429418750781e-7",
            "extra": "mean: 7.224221659517449 usec\nrounds: 68321"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 73843.98986014789,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019665423383950767",
            "extra": "mean: 13.542063502986311 usec\nrounds: 44801"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 233229.89558626313,
            "unit": "iter/sec",
            "range": "stddev: 8.845353393538157e-7",
            "extra": "mean: 4.287615005299083 usec\nrounds: 43398"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 29557.13106577036,
            "unit": "iter/sec",
            "range": "stddev: 0.00000778829677503676",
            "extra": "mean: 33.8327829509165 usec\nrounds: 3050"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 69.31086758110955,
            "unit": "iter/sec",
            "range": "stddev: 0.0011089360228500945",
            "extra": "mean: 14.42775187931058 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 70.5255319326524,
            "unit": "iter/sec",
            "range": "stddev: 0.0009124441855028656",
            "extra": "mean: 14.179262071428818 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 83.96072764951575,
            "unit": "iter/sec",
            "range": "stddev: 0.000587962923740876",
            "extra": "mean: 11.91033031745965 msec\nrounds: 63"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.299144357227886,
            "unit": "iter/sec",
            "range": "stddev: 0.0004351347420015308",
            "extra": "mean: 88.50227666666773 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 306.7454981599547,
            "unit": "iter/sec",
            "range": "stddev: 0.00034201555747730063",
            "extra": "mean: 3.2600315440604857 msec\nrounds: 261"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 73.4834776934615,
            "unit": "iter/sec",
            "range": "stddev: 0.0025139860257831293",
            "extra": "mean: 13.60850127659349 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2867481457175645,
            "unit": "iter/sec",
            "range": "stddev: 0.12376338090006077",
            "extra": "mean: 777.1528587999967 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.3448050124676099,
            "unit": "iter/sec",
            "range": "stddev: 0.12172957605481607",
            "extra": "mean: 743.6022254000079 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 418891.2503358641,
            "unit": "iter/sec",
            "range": "stddev: 6.062728431789099e-7",
            "extra": "mean: 2.3872544465853776 usec\nrounds: 12875"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 401030.87832469685,
            "unit": "iter/sec",
            "range": "stddev: 5.649733049241262e-7",
            "extra": "mean: 2.493573572632341 usec\nrounds: 77556"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 393915.7686998242,
            "unit": "iter/sec",
            "range": "stddev: 5.334251487608728e-7",
            "extra": "mean: 2.5386137836031395 usec\nrounds: 93546"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177157.43816428917,
            "unit": "iter/sec",
            "range": "stddev: 8.742864652318621e-7",
            "extra": "mean: 5.644696662821673 usec\nrounds: 23914"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 206883.04230495886,
            "unit": "iter/sec",
            "range": "stddev: 8.188663393738276e-7",
            "extra": "mean: 4.833648948984113 usec\nrounds: 62461"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 440159.3254944261,
            "unit": "iter/sec",
            "range": "stddev: 5.767400485641845e-7",
            "extra": "mean: 2.2719046083522394 usec\nrounds: 88645"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 453882.7264264681,
            "unit": "iter/sec",
            "range": "stddev: 5.104767711638289e-7",
            "extra": "mean: 2.203212287617221 usec\nrounds: 83043"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 33541.05830576666,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025843009678708475",
            "extra": "mean: 29.814205350463602 usec\nrounds: 16372"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 583782.0541472659,
            "unit": "iter/sec",
            "range": "stddev: 7.551090331901029e-7",
            "extra": "mean: 1.71296803815031 usec\nrounds: 62074"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 266427.79831428424,
            "unit": "iter/sec",
            "range": "stddev: 6.807911015691324e-7",
            "extra": "mean: 3.753362097825758 usec\nrounds: 57965"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 373318.8335975688,
            "unit": "iter/sec",
            "range": "stddev: 6.006662931289986e-7",
            "extra": "mean: 2.6786754645172355 usec\nrounds: 67669"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 231686.09866508748,
            "unit": "iter/sec",
            "range": "stddev: 7.641844660173041e-7",
            "extra": "mean: 4.31618472477084 usec\nrounds: 48667"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 203053.40531186713,
            "unit": "iter/sec",
            "range": "stddev: 0.000002371578433859323",
            "extra": "mean: 4.924812752901695 usec\nrounds: 70196"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52058.02391900614,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017738515899886144",
            "extra": "mean: 19.209334598559447 usec\nrounds: 22920"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25969.197253204362,
            "unit": "iter/sec",
            "range": "stddev: 0.00003666454339354702",
            "extra": "mean: 38.50715870228176 usec\nrounds: 14858"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35788.66247481173,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026725137440525547",
            "extra": "mean: 27.94180980369987 usec\nrounds: 8160"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 337.1765191172877,
            "unit": "iter/sec",
            "range": "stddev: 0.000036427477754543956",
            "extra": "mean: 2.965805574533936 msec\nrounds: 322"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 33.49951195982144,
            "unit": "iter/sec",
            "range": "stddev: 0.0002257742911653151",
            "extra": "mean: 29.851181151515803 msec\nrounds: 33"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25818.391352233735,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033152389810996355",
            "extra": "mean: 38.73208002610444 usec\nrounds: 13808"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 183.50949954507269,
            "unit": "iter/sec",
            "range": "stddev: 0.012793833645965346",
            "extra": "mean: 5.449309177339809 msec\nrounds: 203"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.318705724405232,
            "unit": "iter/sec",
            "range": "stddev: 0.07324379161057797",
            "extra": "mean: 75.082370666663 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13649.9745112324,
            "unit": "iter/sec",
            "range": "stddev: 0.000007670891808082422",
            "extra": "mean: 73.26021005952151 usec\nrounds: 4851"
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
          "id": "31585076423223734ee1ab5b4655f5ec3646f2cc",
          "message": "docs: refresh cache.md SQLite schema section to reflect v6 (merges PR #792, addresses #696)\n\nUpdate the SQLite schema versioning table in docs/reference/cache.md to\nmatch src/pynetappfoundry/cache/db.py: bump the reported SCHEMA_VERSION\nfrom 4 to 6 and add migration rows for v4 → v5 (_upgrade_to_v5, adds\nvm_name column to cloudmetadata) and v5 → v6 (_upgrade_to_v6, creates\nconsoleinfo table).\n\nAddresses #696\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-07-01T12:44:25+01:00",
          "tree_id": "b43154a6b62d7f6156aa5eef53be0a7c81fc2c61",
          "url": "https://github.com/endavis/pynetappfoundry/commit/31585076423223734ee1ab5b4655f5ec3646f2cc"
        },
        "date": 1782906340876,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1086652.8492353503,
            "unit": "iter/sec",
            "range": "stddev: 5.188584923557195e-7",
            "extra": "mean: 920.2571002355301 nsec\nrounds: 55667"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 699867.934622754,
            "unit": "iter/sec",
            "range": "stddev: 6.721147474452907e-7",
            "extra": "mean: 1.4288410006082426 usec\nrounds: 185529"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 425176.87099673046,
            "unit": "iter/sec",
            "range": "stddev: 8.409376566701133e-7",
            "extra": "mean: 2.351962367227849 usec\nrounds: 151012"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 443672.3636104283,
            "unit": "iter/sec",
            "range": "stddev: 5.754101779073902e-7",
            "extra": "mean: 2.253915461090251 usec\nrounds: 153799"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 487018.6634827573,
            "unit": "iter/sec",
            "range": "stddev: 6.823403567777285e-7",
            "extra": "mean: 2.0533094006065835 usec\nrounds: 82899"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 151591.77239615563,
            "unit": "iter/sec",
            "range": "stddev: 0.000001349777547809191",
            "extra": "mean: 6.5966640813902115 usec\nrounds: 55701"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 138988.69497322125,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011407713676627547",
            "extra": "mean: 7.194829767936655 usec\nrounds: 67079"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 69551.28790205538,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018704054713842274",
            "extra": "mean: 14.377878974839918 usec\nrounds: 43933"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 223287.2443552955,
            "unit": "iter/sec",
            "range": "stddev: 8.306409262866031e-7",
            "extra": "mean: 4.478536169351422 usec\nrounds: 44264"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31103.696222060287,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031454277186952247",
            "extra": "mean: 32.150519760116175 usec\nrounds: 2834"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 58.3865733948997,
            "unit": "iter/sec",
            "range": "stddev: 0.0009230246502659048",
            "extra": "mean: 17.12722535087757 msec\nrounds: 57"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 55.789046107311556,
            "unit": "iter/sec",
            "range": "stddev: 0.00017084521821481117",
            "extra": "mean: 17.92466567857203 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 66.11546492587544,
            "unit": "iter/sec",
            "range": "stddev: 0.0005167953466458708",
            "extra": "mean: 15.125054344261782 msec\nrounds: 61"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.41930278289705,
            "unit": "iter/sec",
            "range": "stddev: 0.0014166939238532798",
            "extra": "mean: 87.57102066666651 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 304.9028102534964,
            "unit": "iter/sec",
            "range": "stddev: 0.0003489177320694087",
            "extra": "mean: 3.2797336278029032 msec\nrounds: 223"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 64.13455633410219,
            "unit": "iter/sec",
            "range": "stddev: 0.0015257630083197675",
            "extra": "mean: 15.59221825423732 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2695640048009058,
            "unit": "iter/sec",
            "range": "stddev: 0.13608019230989332",
            "extra": "mean: 787.6719852000065 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.247742959943303,
            "unit": "iter/sec",
            "range": "stddev: 0.14631179602957062",
            "extra": "mean: 801.4471186000037 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 411876.3835505583,
            "unit": "iter/sec",
            "range": "stddev: 5.3785644565708e-7",
            "extra": "mean: 2.4279129368369063 usec\nrounds: 11417"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 393517.8832284121,
            "unit": "iter/sec",
            "range": "stddev: 5.485731291311459e-7",
            "extra": "mean: 2.541180573030181 usec\nrounds: 73228"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 390516.42011826584,
            "unit": "iter/sec",
            "range": "stddev: 5.766446509933252e-7",
            "extra": "mean: 2.5607117869644385 usec\nrounds: 91075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 168260.00464968968,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010637879148587778",
            "extra": "mean: 5.9431830046715985 usec\nrounds: 31950"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 195923.65233274037,
            "unit": "iter/sec",
            "range": "stddev: 0.000001266090191154044",
            "extra": "mean: 5.1040289831963905 usec\nrounds: 37953"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 430993.7646585434,
            "unit": "iter/sec",
            "range": "stddev: 5.373930615195835e-7",
            "extra": "mean: 2.320219181807083 usec\nrounds: 87635"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 443875.46710332966,
            "unit": "iter/sec",
            "range": "stddev: 5.295341836800605e-7",
            "extra": "mean: 2.2528841400626685 usec\nrounds: 75902"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34247.85322887251,
            "unit": "iter/sec",
            "range": "stddev: 0.000003135241410012632",
            "extra": "mean: 29.198910463589414 usec\nrounds: 15033"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 588335.5230280288,
            "unit": "iter/sec",
            "range": "stddev: 4.319989339309672e-7",
            "extra": "mean: 1.6997103877957733 usec\nrounds: 55267"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263573.9803766906,
            "unit": "iter/sec",
            "range": "stddev: 8.115066116425059e-7",
            "extra": "mean: 3.794001208202856 usec\nrounds: 60420"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 378800.4823324763,
            "unit": "iter/sec",
            "range": "stddev: 5.856984725368698e-7",
            "extra": "mean: 2.6399121612582626 usec\nrounds: 55636"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 224023.2084624806,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011694734149114215",
            "extra": "mean: 4.463823221099344 usec\nrounds: 38155"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 205591.2872961388,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010196809370123454",
            "extra": "mean: 4.8640193519464425 usec\nrounds: 64438"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52097.850188176286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018084556569737963",
            "extra": "mean: 19.19464999780264 usec\nrounds: 22157"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25800.92684459182,
            "unit": "iter/sec",
            "range": "stddev: 0.000034582995577102667",
            "extra": "mean: 38.75829756129911 usec\nrounds: 14229"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35545.401653142006,
            "unit": "iter/sec",
            "range": "stddev: 0.00000297707509146844",
            "extra": "mean: 28.133034189855774 usec\nrounds: 9301"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 336.20026572102165,
            "unit": "iter/sec",
            "range": "stddev: 0.00017850357232495535",
            "extra": "mean: 2.9744176372239934 msec\nrounds: 317"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.16524614354844,
            "unit": "iter/sec",
            "range": "stddev: 0.0002477529043245724",
            "extra": "mean: 32.087023968748966 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25424.70665503218,
            "unit": "iter/sec",
            "range": "stddev: 0.00008963933187169605",
            "extra": "mean: 39.33182056210962 usec\nrounds: 14055"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 176.4047421342086,
            "unit": "iter/sec",
            "range": "stddev: 0.01614772334823312",
            "extra": "mean: 5.6687818473678036 msec\nrounds: 190"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.249691631186941,
            "unit": "iter/sec",
            "range": "stddev: 0.09176549322440178",
            "extra": "mean: 88.8913254500018 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13643.404749523961,
            "unit": "iter/sec",
            "range": "stddev: 0.0000078087869402716",
            "extra": "mean: 73.2954873331667 usec\nrounds: 5842"
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
          "id": "4156e08e6615620961805d94d2071355bec739c8",
          "message": "chore(deps): Bump the dev-dependencies group across 1 directory with 3 updates (merges PR #783)\n\nBumps the dev-dependencies group with 3 updates in the / directory: [pytest](https://github.com/pytest-dev/pytest), [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy).\n\n\nUpdates `pytest` from 9.0.3 to 9.1.1\n- [Release notes](https://github.com/pytest-dev/pytest/releases)\n- [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)\n- [Commits](https://github.com/pytest-dev/pytest/compare/9.0.3...9.1.1)\n\nUpdates `ruff` from 0.15.12 to 0.15.19\n- [Release notes](https://github.com/astral-sh/ruff/releases)\n- [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/astral-sh/ruff/compare/0.15.12...0.15.19)\n\nUpdates `mypy` from 1.20.2 to 2.1.0\n- [Changelog](https://github.com/python/mypy/blob/master/CHANGELOG.md)\n- [Commits](https://github.com/python/mypy/compare/v1.20.2...v2.1.0)\n\n---\nupdated-dependencies:\n- dependency-name: mypy\n  dependency-version: 2.1.0\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n  dependency-group: dev-dependencies\n- dependency-name: pytest\n  dependency-version: 9.1.0\n  dependency-type: direct:production\n  update-type: version-update:semver-minor\n  dependency-group: dev-dependencies\n- dependency-name: ruff\n  dependency-version: 0.15.17\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n  dependency-group: dev-dependencies\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-07-01T13:03:18+01:00",
          "tree_id": "bcb9a422413b1db6139d9adde62fcfbe206c6388",
          "url": "https://github.com/endavis/pynetappfoundry/commit/4156e08e6615620961805d94d2071355bec739c8"
        },
        "date": 1782907473224,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1168183.1052997762,
            "unit": "iter/sec",
            "range": "stddev: 3.265175414782823e-7",
            "extra": "mean: 856.0301852194503 nsec\nrounds: 60460"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 733448.7353697733,
            "unit": "iter/sec",
            "range": "stddev: 5.491959929688861e-7",
            "extra": "mean: 1.3634218068367696 usec\nrounds: 168039"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 450264.1679164424,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013019099361167286",
            "extra": "mean: 2.2209184546649836 usec\nrounds: 151241"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 450072.59878967877,
            "unit": "iter/sec",
            "range": "stddev: 6.655199006926337e-7",
            "extra": "mean: 2.221863767510328 usec\nrounds: 157679"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 494353.30489658867,
            "unit": "iter/sec",
            "range": "stddev: 6.045967256971005e-7",
            "extra": "mean: 2.0228447753761554 usec\nrounds: 28739"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 161873.1220476244,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011687550437800991",
            "extra": "mean: 6.177677846392509 usec\nrounds: 52953"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 140766.59468361927,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010624343439142187",
            "extra": "mean: 7.103958167401544 usec\nrounds: 35905"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 71418.76754019514,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024101518464248877",
            "extra": "mean: 14.001921825900887 usec\nrounds: 34372"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232570.0425546967,
            "unit": "iter/sec",
            "range": "stddev: 0.00000119607045327423",
            "extra": "mean: 4.299779924427783 usec\nrounds: 42081"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30202.224839416533,
            "unit": "iter/sec",
            "range": "stddev: 0.000004659641385960294",
            "extra": "mean: 33.11014355124305 usec\nrounds: 2264"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 53.39051357675082,
            "unit": "iter/sec",
            "range": "stddev: 0.0008980151595402776",
            "extra": "mean: 18.729919100000103 msec\nrounds: 50"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 51.377349778474795,
            "unit": "iter/sec",
            "range": "stddev: 0.0004203871624745167",
            "extra": "mean: 19.46382996226409 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 58.302565126292734,
            "unit": "iter/sec",
            "range": "stddev: 0.0004169287566230756",
            "extra": "mean: 17.151904000001355 msec\nrounds: 57"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.255755169450646,
            "unit": "iter/sec",
            "range": "stddev: 0.0009710779687413299",
            "extra": "mean: 97.50622781818663 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 260.59283190699466,
            "unit": "iter/sec",
            "range": "stddev: 0.00040713903278149816",
            "extra": "mean: 3.837404093896562 msec\nrounds: 213"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 51.413655039740455,
            "unit": "iter/sec",
            "range": "stddev: 0.00036565376369264056",
            "extra": "mean: 19.450085764706763 msec\nrounds: 51"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.1784371383447887,
            "unit": "iter/sec",
            "range": "stddev: 0.16312465655407352",
            "extra": "mean: 848.5815385999985 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.1775893050020423,
            "unit": "iter/sec",
            "range": "stddev: 0.1511223434496425",
            "extra": "mean: 849.1924949999998 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 410872.522597852,
            "unit": "iter/sec",
            "range": "stddev: 7.938840686433026e-7",
            "extra": "mean: 2.4338449153942716 usec\nrounds: 11987"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 395324.0063879155,
            "unit": "iter/sec",
            "range": "stddev: 6.123350404229363e-7",
            "extra": "mean: 2.529570640389444 usec\nrounds: 63618"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 393392.1909383011,
            "unit": "iter/sec",
            "range": "stddev: 6.136009253141911e-7",
            "extra": "mean: 2.5419925027358716 usec\nrounds: 82830"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 173478.82499973945,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011672633641270896",
            "extra": "mean: 5.764392282467338 usec\nrounds: 42008"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 204198.91661172823,
            "unit": "iter/sec",
            "range": "stddev: 9.464152967808197e-7",
            "extra": "mean: 4.897185629546894 usec\nrounds: 50590"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 434137.7860093449,
            "unit": "iter/sec",
            "range": "stddev: 5.545714329851314e-7",
            "extra": "mean: 2.3034161785182063 usec\nrounds: 69994"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 440272.189701868,
            "unit": "iter/sec",
            "range": "stddev: 7.364091307527278e-7",
            "extra": "mean: 2.271322203378673 usec\nrounds: 76191"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34267.59182448581,
            "unit": "iter/sec",
            "range": "stddev: 0.000003071718830295618",
            "extra": "mean: 29.182091496883448 usec\nrounds: 15312"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 594261.8008864078,
            "unit": "iter/sec",
            "range": "stddev: 4.504733506597742e-7",
            "extra": "mean: 1.6827600200928081 usec\nrounds: 53692"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 254186.64745064845,
            "unit": "iter/sec",
            "range": "stddev: 0.000001222382091199083",
            "extra": "mean: 3.934116957084281 usec\nrounds: 62151"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 377485.46659477893,
            "unit": "iter/sec",
            "range": "stddev: 6.828284996923728e-7",
            "extra": "mean: 2.6491086107785833 usec\nrounds: 61725"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 232515.6218674841,
            "unit": "iter/sec",
            "range": "stddev: 7.96945822992673e-7",
            "extra": "mean: 4.300786295425443 usec\nrounds: 48057"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209783.8067051638,
            "unit": "iter/sec",
            "range": "stddev: 9.074583233634815e-7",
            "extra": "mean: 4.7668121563139945 usec\nrounds: 62190"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52069.59703162908,
            "unit": "iter/sec",
            "range": "stddev: 0.000002159878587252793",
            "extra": "mean: 19.20506508611084 usec\nrounds: 20035"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25340.754775087466,
            "unit": "iter/sec",
            "range": "stddev: 0.000040921188087859805",
            "extra": "mean: 39.46212371634256 usec\nrounds: 14412"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35460.83717980875,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032691596086028172",
            "extra": "mean: 28.20012384167275 usec\nrounds: 9496"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 333.9609583412672,
            "unit": "iter/sec",
            "range": "stddev: 0.00004578546064610376",
            "extra": "mean: 2.9943619905956864 msec\nrounds: 319"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.450048427147795,
            "unit": "iter/sec",
            "range": "stddev: 0.0002891682192008486",
            "extra": "mean: 32.840670266666905 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 26107.2694641263,
            "unit": "iter/sec",
            "range": "stddev: 0.000004148795183715258",
            "extra": "mean: 38.30350781701198 usec\nrounds: 13816"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 180.93919644934397,
            "unit": "iter/sec",
            "range": "stddev: 0.01550640222785931",
            "extra": "mean: 5.52671847572818 msec\nrounds: 206"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.523858155259243,
            "unit": "iter/sec",
            "range": "stddev: 0.08842139413031175",
            "extra": "mean: 86.77649329999966 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13451.444393657099,
            "unit": "iter/sec",
            "range": "stddev: 0.000007816423600327452",
            "extra": "mean: 74.34145886010134 usec\nrounds: 5773"
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
          "id": "f9ab6266ffdd0b9686430498395267ec049bb649",
          "message": "chore(deps): Bump actions/cache from 5 to 6 (merges PR #784)\n\nBumps [actions/cache](https://github.com/actions/cache) from 5 to 6.\n- [Release notes](https://github.com/actions/cache/releases)\n- [Changelog](https://github.com/actions/cache/blob/main/RELEASES.md)\n- [Commits](https://github.com/actions/cache/compare/v5...v6)\n\n---\nupdated-dependencies:\n- dependency-name: actions/cache\n  dependency-version: '6'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-07-01T13:07:42+01:00",
          "tree_id": "17edad311bec5f0cc95f17688960dc2a70e230cd",
          "url": "https://github.com/endavis/pynetappfoundry/commit/f9ab6266ffdd0b9686430498395267ec049bb649"
        },
        "date": 1782907730068,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1168121.6964614328,
            "unit": "iter/sec",
            "range": "stddev: 2.922126884283806e-7",
            "extra": "mean: 856.0751872251664 nsec\nrounds: 57297"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 739181.2701284034,
            "unit": "iter/sec",
            "range": "stddev: 4.4240596648224845e-7",
            "extra": "mean: 1.352848131320061 usec\nrounds: 193799"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 457990.77276985714,
            "unit": "iter/sec",
            "range": "stddev: 5.403490581108719e-7",
            "extra": "mean: 2.1834501030493585 usec\nrounds: 157184"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 449100.9889418155,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011509983648614173",
            "extra": "mean: 2.226670670123057 usec\nrounds: 155449"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 500590.81980178726,
            "unit": "iter/sec",
            "range": "stddev: 5.410962624511951e-7",
            "extra": "mean: 1.99763951004127 usec\nrounds: 86044"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 159383.03285494584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010152685520194702",
            "extra": "mean: 6.274193570592284 usec\nrounds: 56584"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141195.90216050393,
            "unit": "iter/sec",
            "range": "stddev: 0.000001040085234356924",
            "extra": "mean: 7.082358515357292 usec\nrounds: 73121"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 72962.51949523625,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013321748516676871",
            "extra": "mean: 13.705667059171255 usec\nrounds: 46708"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 235073.2809808591,
            "unit": "iter/sec",
            "range": "stddev: 8.247657257839236e-7",
            "extra": "mean: 4.2539926095702265 usec\nrounds: 45870"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30595.48139564351,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030630865184123453",
            "extra": "mean: 32.68456498750793 usec\nrounds: 3216"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 58.52660458130277,
            "unit": "iter/sec",
            "range": "stddev: 0.00039794120199916947",
            "extra": "mean: 17.086246625000104 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 59.359675545400684,
            "unit": "iter/sec",
            "range": "stddev: 0.0005840939999278106",
            "extra": "mean: 16.84645326666517 msec\nrounds: 60"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 60.07074020472381,
            "unit": "iter/sec",
            "range": "stddev: 0.0008087869704327712",
            "extra": "mean: 16.64703975000066 msec\nrounds: 60"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.214557533398763,
            "unit": "iter/sec",
            "range": "stddev: 0.001755497748191808",
            "extra": "mean: 89.1698131666665 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 308.1351835029397,
            "unit": "iter/sec",
            "range": "stddev: 0.00003941332716262474",
            "extra": "mean: 3.245328847656437 msec\nrounds: 256"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 57.18264118439566,
            "unit": "iter/sec",
            "range": "stddev: 0.00044419661213430413",
            "extra": "mean: 17.487824614034896 msec\nrounds: 57"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2704577898537857,
            "unit": "iter/sec",
            "range": "stddev: 0.14047035371164399",
            "extra": "mean: 787.1178468000011 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2597905777457883,
            "unit": "iter/sec",
            "range": "stddev: 0.13972860867356982",
            "extra": "mean: 793.7827268000007 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 422561.8793981313,
            "unit": "iter/sec",
            "range": "stddev: 7.260460479773935e-7",
            "extra": "mean: 2.36651730493137 usec\nrounds: 13031"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 404920.8227006929,
            "unit": "iter/sec",
            "range": "stddev: 5.766897612343719e-7",
            "extra": "mean: 2.46961861168393 usec\nrounds: 82905"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 398677.2464263381,
            "unit": "iter/sec",
            "range": "stddev: 6.49276015773332e-7",
            "extra": "mean: 2.5082946392446446 usec\nrounds: 90901"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 174280.02857856275,
            "unit": "iter/sec",
            "range": "stddev: 0.000001029036669717699",
            "extra": "mean: 5.7378921047698555 usec\nrounds: 42912"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 206603.73868713508,
            "unit": "iter/sec",
            "range": "stddev: 8.388116032445118e-7",
            "extra": "mean: 4.840183465964881 usec\nrounds: 58921"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 442650.005669191,
            "unit": "iter/sec",
            "range": "stddev: 5.053023600423738e-7",
            "extra": "mean: 2.2591211729190346 usec\nrounds: 90408"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 454270.2817529769,
            "unit": "iter/sec",
            "range": "stddev: 6.163365880388594e-7",
            "extra": "mean: 2.2013326430712454 usec\nrounds: 81613"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35136.456427321675,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025191839742489765",
            "extra": "mean: 28.460468176933528 usec\nrounds: 15759"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 556792.2570327383,
            "unit": "iter/sec",
            "range": "stddev: 4.56691337327876e-7",
            "extra": "mean: 1.796001987041285 usec\nrounds: 55359"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263783.4180030588,
            "unit": "iter/sec",
            "range": "stddev: 6.96703831647558e-7",
            "extra": "mean: 3.7909888634030966 usec\nrounds: 51003"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 366809.7078274061,
            "unit": "iter/sec",
            "range": "stddev: 6.019196571884935e-7",
            "extra": "mean: 2.7262091996499915 usec\nrounds: 61611"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 223671.1729286161,
            "unit": "iter/sec",
            "range": "stddev: 8.479685775137662e-7",
            "extra": "mean: 4.470848821985418 usec\nrounds: 51317"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209189.146562029,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011004556161996468",
            "extra": "mean: 4.780362731215976 usec\nrounds: 66989"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 51040.854548228686,
            "unit": "iter/sec",
            "range": "stddev: 0.000001828964547670897",
            "extra": "mean: 19.592148463249107 usec\nrounds: 23036"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25637.594570860583,
            "unit": "iter/sec",
            "range": "stddev: 0.00003798399345169498",
            "extra": "mean: 39.00521935613216 usec\nrounds: 14538"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34507.78139255874,
            "unit": "iter/sec",
            "range": "stddev: 0.000004256823593324712",
            "extra": "mean: 28.978971108691443 usec\nrounds: 9380"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 332.5304317004144,
            "unit": "iter/sec",
            "range": "stddev: 0.000045322778523903226",
            "extra": "mean: 3.0072435623002676 msec\nrounds: 313"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.019758190080747,
            "unit": "iter/sec",
            "range": "stddev: 0.0023312954989903063",
            "extra": "mean: 32.23751758064226 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 25168.309683647003,
            "unit": "iter/sec",
            "range": "stddev: 0.000003790065660595678",
            "extra": "mean: 39.73250538353577 usec\nrounds: 13467"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 183.64236707230216,
            "unit": "iter/sec",
            "range": "stddev: 0.014380520287959764",
            "extra": "mean: 5.44536653465313 msec\nrounds: 202"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 12.597459533323104,
            "unit": "iter/sec",
            "range": "stddev: 0.07859198199672864",
            "extra": "mean: 79.3810845238102 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13550.858018966528,
            "unit": "iter/sec",
            "range": "stddev: 0.000007433858305367025",
            "extra": "mean: 73.79606506099796 usec\nrounds: 5564"
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
          "id": "785cdb50fe536aebf28d55860f9b756f16fddf54",
          "message": "chore(deps): Bump types-paramiko from 4.0.0.20260518 to 5.0.0.20260617 (merges PR #785)\n\nBumps [types-paramiko](https://github.com/python/typeshed) from 4.0.0.20260518 to 5.0.0.20260617.\n- [Commits](https://github.com/python/typeshed/commits)\n\n---\nupdated-dependencies:\n- dependency-name: types-paramiko\n  dependency-version: 5.0.0.20260617\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-07-01T13:15:20+01:00",
          "tree_id": "832cf742e27c16e07c5907aff37322fef0668a96",
          "url": "https://github.com/endavis/pynetappfoundry/commit/785cdb50fe536aebf28d55860f9b756f16fddf54"
        },
        "date": 1782908189857,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1256944.9858336379,
            "unit": "iter/sec",
            "range": "stddev: 2.5121487900901746e-7",
            "extra": "mean: 795.5797678263338 nsec\nrounds: 47983"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 753557.9981781292,
            "unit": "iter/sec",
            "range": "stddev: 6.223448237145646e-7",
            "extra": "mean: 1.327037868906828 usec\nrounds: 176398"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 479224.22260405676,
            "unit": "iter/sec",
            "range": "stddev: 5.472061952258748e-7",
            "extra": "mean: 2.0867058734345676 usec\nrounds: 145349"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 483961.73591944226,
            "unit": "iter/sec",
            "range": "stddev: 5.327951969009119e-7",
            "extra": "mean: 2.0662790584056725 usec\nrounds: 145328"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 524263.70412609814,
            "unit": "iter/sec",
            "range": "stddev: 6.236930687753162e-7",
            "extra": "mean: 1.9074370247830008 usec\nrounds: 76284"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 164260.18504492872,
            "unit": "iter/sec",
            "range": "stddev: 9.404890884791145e-7",
            "extra": "mean: 6.087902553661913 usec\nrounds: 51259"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 143940.73678255503,
            "unit": "iter/sec",
            "range": "stddev: 9.85905403750663e-7",
            "extra": "mean: 6.947303608085988 usec\nrounds: 50608"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 78836.8274144542,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012947527275972004",
            "extra": "mean: 12.684427225145502 usec\nrounds: 43930"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 242193.62437404454,
            "unit": "iter/sec",
            "range": "stddev: 0.000001582820366926593",
            "extra": "mean: 4.128927846818945 usec\nrounds: 41107"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30993.925632636332,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029324443861422235",
            "extra": "mean: 32.264386636683696 usec\nrounds: 2664"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 56.96769920356224,
            "unit": "iter/sec",
            "range": "stddev: 0.00029447381814695384",
            "extra": "mean: 17.553807051724306 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 55.278975132383145,
            "unit": "iter/sec",
            "range": "stddev: 0.0003675365841080958",
            "extra": "mean: 18.090060418182155 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 63.415944908568356,
            "unit": "iter/sec",
            "range": "stddev: 0.0006412081523970927",
            "extra": "mean: 15.768904830508745 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.275767394220415,
            "unit": "iter/sec",
            "range": "stddev: 0.0005940267522515692",
            "extra": "mean: 88.68575991666579 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 302.6126945261859,
            "unit": "iter/sec",
            "range": "stddev: 0.00010579225342156042",
            "extra": "mean: 3.3045540325588263 msec\nrounds: 215"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 54.639367009648815,
            "unit": "iter/sec",
            "range": "stddev: 0.0002528468915164444",
            "extra": "mean: 18.30182256363638 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.099787506118699,
            "unit": "iter/sec",
            "range": "stddev: 0.17898323528812068",
            "extra": "mean: 909.2665578000037 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.095775814303936,
            "unit": "iter/sec",
            "range": "stddev: 0.17690974025919048",
            "extra": "mean: 912.5954296000089 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 407374.607751486,
            "unit": "iter/sec",
            "range": "stddev: 6.815084484359327e-7",
            "extra": "mean: 2.4547430816062006 usec\nrounds: 10443"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 389021.4693664056,
            "unit": "iter/sec",
            "range": "stddev: 4.906217654598051e-7",
            "extra": "mean: 2.5705522156108436 usec\nrounds: 59015"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 386020.8993820997,
            "unit": "iter/sec",
            "range": "stddev: 5.30831712788822e-7",
            "extra": "mean: 2.590533314648744 usec\nrounds: 74907"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177190.20832841223,
            "unit": "iter/sec",
            "range": "stddev: 7.57973302049032e-7",
            "extra": "mean: 5.643652713283995 usec\nrounds: 40874"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 207662.85866010588,
            "unit": "iter/sec",
            "range": "stddev: 8.308668402714263e-7",
            "extra": "mean: 4.815497612101928 usec\nrounds: 55907"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 416685.6269541511,
            "unit": "iter/sec",
            "range": "stddev: 5.141462071733423e-7",
            "extra": "mean: 2.399890793713488 usec\nrounds: 90123"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 444433.1459507653,
            "unit": "iter/sec",
            "range": "stddev: 4.969070795655261e-7",
            "extra": "mean: 2.250057200078369 usec\nrounds: 81381"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 36244.77154145852,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018878913556225273",
            "extra": "mean: 27.590186321250552 usec\nrounds: 14899"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 589888.2966725111,
            "unit": "iter/sec",
            "range": "stddev: 5.459479520803755e-7",
            "extra": "mean: 1.695236209365196 usec\nrounds: 46789"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 265441.88155388826,
            "unit": "iter/sec",
            "range": "stddev: 6.422411268644748e-7",
            "extra": "mean: 3.7673030124185076 usec\nrounds: 51021"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 371625.0836143213,
            "unit": "iter/sec",
            "range": "stddev: 5.055296236458618e-7",
            "extra": "mean: 2.690884022882096 usec\nrounds: 53683"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 226259.1000116915,
            "unit": "iter/sec",
            "range": "stddev: 6.792902402081398e-7",
            "extra": "mean: 4.419711737332673 usec\nrounds: 34420"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 207498.88362999007,
            "unit": "iter/sec",
            "range": "stddev: 8.181341574027952e-7",
            "extra": "mean: 4.819303036748813 usec\nrounds: 60920"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52690.518955365165,
            "unit": "iter/sec",
            "range": "stddev: 0.000001707117975922817",
            "extra": "mean: 18.978746458107825 usec\nrounds: 16305"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26418.909621512557,
            "unit": "iter/sec",
            "range": "stddev: 0.000040903552758658654",
            "extra": "mean: 37.85167572494035 usec\nrounds: 14793"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35901.7417756977,
            "unit": "iter/sec",
            "range": "stddev: 0.000001779024984984575",
            "extra": "mean: 27.853801808493632 usec\nrounds: 8184"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 335.6406648268259,
            "unit": "iter/sec",
            "range": "stddev: 0.00009986722608390413",
            "extra": "mean: 2.9793767704397522 msec\nrounds: 318"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.56274578674773,
            "unit": "iter/sec",
            "range": "stddev: 0.00009981671724227522",
            "extra": "mean: 32.71957326666666 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 26244.66506197011,
            "unit": "iter/sec",
            "range": "stddev: 0.000002297764591219378",
            "extra": "mean: 38.10298198276694 usec\nrounds: 13154"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 178.37337123301762,
            "unit": "iter/sec",
            "range": "stddev: 0.017976299900997344",
            "extra": "mean: 5.606217974619386 msec\nrounds: 197"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 10.52826222892915,
            "unit": "iter/sec",
            "range": "stddev: 0.10351383309485866",
            "extra": "mean: 94.98243663158757 msec\nrounds: 19"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 15034.698826495354,
            "unit": "iter/sec",
            "range": "stddev: 0.000003615523956673297",
            "extra": "mean: 66.51280557996411 usec\nrounds: 5663"
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
          "id": "994df2b6ec9404a0fef13001ed74651589ccd493",
          "message": "chore: bump dependencies to resolve audit CVEs (merges PR #819, addresses #818)\n\nBump 8 packages flagged by pip-audit:\n- cryptography 49.0.0 -> 50.0.2, floor raised to >=50.0.0\n  (GHSA-g6cj-pr64-35w5)\n- urllib3 2.7.0 -> 2.8.0 (GHSA-vxq7-64xx-v4gw, GHSA-gh4c-6fx4-qh6g,\n  GHSA-8988-9cw3-xx77)\n- certifi 2026.1.4 -> 2026.10.23 (GHSA-6q48-6c7w-9gw2)\n- pip 26.1.2 -> 26.2.2 (GHSA-qwm4-qh6w-59xr)\n- virtualenv 20.36.1 -> 21.14.13 (15 advisories)\n- black 26.3.1 -> 26.10.1 (GHSA-cg8m-r9f2-5wm2)\n- mkdocs-material 9.7.6 -> 9.8.0 (GHSA-xvg9-69gf-fjrf)\n- pymdown-extensions 10.21.3 -> 11.0.2 (GHSA-9xwg-3r6f-jcx2,\n  GHSA-gm37-52c6-37mw)\n\npymdown-extensions is held at 11.x because 12.x breaks the docs build\nwith mkdocstrings 1.0.4; moving to 12.x needs mkdocstrings >= 1.0.7.\nvirtualenv 21 also pulls in filelock 4.2.4, distlib 0.4.4, packaging\n26.3 and the new python-discovery 1.6.4.\n\nAddresses #818\n\n\nClaude-Session: https://claude.ai/code/session_01QAhsGhfKSCD67omHGamv8i\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-25T11:26:42Z",
          "tree_id": "b40ac9017ba3d20abf1880db9cb70c61b06c6ea3",
          "url": "https://github.com/endavis/pynetappfoundry/commit/994df2b6ec9404a0fef13001ed74651589ccd493"
        },
        "date": 1792927662929,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1425897.321773661,
            "unit": "iter/sec",
            "range": "stddev: 2.0469487222812332e-7",
            "extra": "mean: 701.3127696713175 nsec\nrounds: 49359"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 915724.3734408783,
            "unit": "iter/sec",
            "range": "stddev: 3.6501402843777226e-7",
            "extra": "mean: 1.0920316516665949 usec\nrounds: 147038"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 594777.2965453988,
            "unit": "iter/sec",
            "range": "stddev: 3.936069941022682e-7",
            "extra": "mean: 1.6813015658267834 usec\nrounds: 114509"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 590760.2700394556,
            "unit": "iter/sec",
            "range": "stddev: 4.1513369625974726e-7",
            "extra": "mean: 1.6927340085568248 usec\nrounds: 111075"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 650769.8217282759,
            "unit": "iter/sec",
            "range": "stddev: 5.060195851481093e-7",
            "extra": "mean: 1.5366416305910737 usec\nrounds: 76929"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 203567.527913318,
            "unit": "iter/sec",
            "range": "stddev: 6.751367559762704e-7",
            "extra": "mean: 4.912374828395099 usec\nrounds: 51709"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 181348.75099493924,
            "unit": "iter/sec",
            "range": "stddev: 6.983564005742057e-7",
            "extra": "mean: 5.514237040584339 usec\nrounds: 74907"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 98340.03319308575,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011496369986892188",
            "extra": "mean: 10.168798682796352 usec\nrounds: 50865"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 295849.751848671,
            "unit": "iter/sec",
            "range": "stddev: 5.494078978113845e-7",
            "extra": "mean: 3.3800940975996023 usec\nrounds: 45761"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 40369.37531402379,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016894538135373714",
            "extra": "mean: 24.77125276824913 usec\nrounds: 3161"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 74.28107855098106,
            "unit": "iter/sec",
            "range": "stddev: 0.0003790004681628531",
            "extra": "mean: 13.462378569445162 msec\nrounds: 72"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 72.73160606166527,
            "unit": "iter/sec",
            "range": "stddev: 0.00021970566166112153",
            "extra": "mean: 13.749180777778413 msec\nrounds: 72"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 90.45718568103645,
            "unit": "iter/sec",
            "range": "stddev: 0.0010893642668651623",
            "extra": "mean: 11.05495370512772 msec\nrounds: 78"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 14.199329769105775,
            "unit": "iter/sec",
            "range": "stddev: 0.0003954670454851539",
            "extra": "mean: 70.42585926666428 msec\nrounds: 15"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 401.7867289580512,
            "unit": "iter/sec",
            "range": "stddev: 0.000024065073042638765",
            "extra": "mean: 2.4888826034480735 msec\nrounds: 290"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 72.57529383077228,
            "unit": "iter/sec",
            "range": "stddev: 0.0005534415484617411",
            "extra": "mean: 13.778793680556825 msec\nrounds: 72"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2838746642225156,
            "unit": "iter/sec",
            "range": "stddev: 0.15332432955724545",
            "extra": "mean: 778.8922297999989 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.34485657153887,
            "unit": "iter/sec",
            "range": "stddev: 0.16527274371298786",
            "extra": "mean: 743.573717199996 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 498957.0584762106,
            "unit": "iter/sec",
            "range": "stddev: 4.458600029244733e-7",
            "extra": "mean: 2.0041804861002452 usec\nrounds: 12012"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 483560.34588948474,
            "unit": "iter/sec",
            "range": "stddev: 3.523702911418071e-7",
            "extra": "mean: 2.067994219336887 usec\nrounds: 76635"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 474106.8418117363,
            "unit": "iter/sec",
            "range": "stddev: 4.216654787970878e-7",
            "extra": "mean: 2.1092292112441005 usec\nrounds: 84481"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 214107.21790819286,
            "unit": "iter/sec",
            "range": "stddev: 5.495114636375755e-7",
            "extra": "mean: 4.670557161827167 usec\nrounds: 48284"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 251984.75728266724,
            "unit": "iter/sec",
            "range": "stddev: 4.916242863024184e-7",
            "extra": "mean: 3.9684940104461823 usec\nrounds: 69537"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 533251.9923572621,
            "unit": "iter/sec",
            "range": "stddev: 3.424150278914228e-7",
            "extra": "mean: 1.8752860079893177 usec\nrounds: 91938"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 543947.3977749306,
            "unit": "iter/sec",
            "range": "stddev: 4.1134550904839915e-7",
            "extra": "mean: 1.8384130599587327 usec\nrounds: 88285"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 44157.68877591167,
            "unit": "iter/sec",
            "range": "stddev: 0.000001339813259167352",
            "extra": "mean: 22.646112777204657 usec\nrounds: 17273"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 692791.1809166261,
            "unit": "iter/sec",
            "range": "stddev: 4.089700333336588e-7",
            "extra": "mean: 1.4434363882590255 usec\nrounds: 56161"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 289709.69325727085,
            "unit": "iter/sec",
            "range": "stddev: 0.000001076528045302335",
            "extra": "mean: 3.4517312443252295 usec\nrounds: 52944"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 454079.0940256322,
            "unit": "iter/sec",
            "range": "stddev: 4.5619001985507984e-7",
            "extra": "mean: 2.2022595031506804 usec\nrounds: 70319"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 279442.7405949553,
            "unit": "iter/sec",
            "range": "stddev: 5.676512202792805e-7",
            "extra": "mean: 3.5785506464434262 usec\nrounds: 59866"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 254531.9965595863,
            "unit": "iter/sec",
            "range": "stddev: 8.459881987799803e-7",
            "extra": "mean: 3.9287791457130177 usec\nrounds: 76512"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 63230.179144780814,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026972839017622453",
            "extra": "mean: 15.815232750017325 usec\nrounds: 27768"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 31389.890652065922,
            "unit": "iter/sec",
            "range": "stddev: 0.00004232275610079515",
            "extra": "mean: 31.85739036444159 usec\nrounds: 14156"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 43034.20939779982,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032619046091648616",
            "extra": "mean: 23.23732709380566 usec\nrounds: 10471"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 397.9577403648844,
            "unit": "iter/sec",
            "range": "stddev: 0.00025489742099346407",
            "extra": "mean: 2.512829626289233 msec\nrounds: 388"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 37.188063271328126,
            "unit": "iter/sec",
            "range": "stddev: 0.0010800685515905733",
            "extra": "mean: 26.890348999997443 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 31026.94161456484,
            "unit": "iter/sec",
            "range": "stddev: 0.000003316921263491445",
            "extra": "mean: 32.23005388099788 usec\nrounds: 17186"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 221.66448096252492,
            "unit": "iter/sec",
            "range": "stddev: 0.015151621046799934",
            "extra": "mean: 4.511322678571413 msec\nrounds: 252"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 12.556162805908896,
            "unit": "iter/sec",
            "range": "stddev: 0.0929973982567575",
            "extra": "mean: 79.64216580000084 msec\nrounds: 25"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 18198.212317061356,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027533840566949634",
            "extra": "mean: 54.95045241682727 usec\nrounds: 7303"
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
          "id": "e7cb401896006e5105a3cade2d98d201ed9a8b97",
          "message": "chore: bump paramiko to 5.1.0 and remove audit suppression (merges PR #820, addresses #737)\n\nparamiko never shipped 4.0.1; the fix for GHSA-r374-rxx8-8654\n(CVE-2026-44405, rsakey.py SHA-1 acceptance) landed in 5.0.0. Raise the\nfloor to >=5.1.0 and drop the --ignore-vuln flag added for #701.\n\nparamiko 5.0 removes SHA-1 key exchange and ssh-rsa (SHA-1) signatures;\nclients/ontap/cli.py uses none of the removed APIs.\n\nAddresses #737\n\n\nClaude-Session: https://claude.ai/code/session_01QAhsGhfKSCD67omHGamv8i\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-25T15:44:53Z",
          "tree_id": "31363836ac7b48a0afe548f13a747275a847f75c",
          "url": "https://github.com/endavis/pynetappfoundry/commit/e7cb401896006e5105a3cade2d98d201ed9a8b97"
        },
        "date": 1792943159519,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1081038.2084254946,
            "unit": "iter/sec",
            "range": "stddev: 3.134137350628867e-7",
            "extra": "mean: 925.0366843707358 nsec\nrounds: 68367"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 667765.5204207819,
            "unit": "iter/sec",
            "range": "stddev: 5.995104976382696e-7",
            "extra": "mean: 1.497531647590708 usec\nrounds: 188324"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 406753.08666873776,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018274665044046362",
            "extra": "mean: 2.458493943315558 usec\nrounds: 121271"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 408964.41389786114,
            "unit": "iter/sec",
            "range": "stddev: 0.000005075491306181281",
            "extra": "mean: 2.445200526052983 usec\nrounds: 112918"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 467141.2632522886,
            "unit": "iter/sec",
            "range": "stddev: 5.269820715633834e-7",
            "extra": "mean: 2.1406800868711326 usec\nrounds: 79656"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 144501.36846700037,
            "unit": "iter/sec",
            "range": "stddev: 9.381489607481334e-7",
            "extra": "mean: 6.9203496867115755 usec\nrounds: 53465"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 128285.7003804323,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010225876647520089",
            "extra": "mean: 7.79510106765206 usec\nrounds: 64066"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 66687.34154217018,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013483127743540662",
            "extra": "mean: 14.995349595209813 usec\nrounds: 42492"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 199482.97741547984,
            "unit": "iter/sec",
            "range": "stddev: 8.050199418641818e-7",
            "extra": "mean: 5.012959065260072 usec\nrounds: 43435"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 27865.3918199975,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024320294406798895",
            "extra": "mean: 35.88680921695684 usec\nrounds: 3103"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 58.41514477803095,
            "unit": "iter/sec",
            "range": "stddev: 0.00072865474483234",
            "extra": "mean: 17.118848267856812 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 61.91106525921427,
            "unit": "iter/sec",
            "range": "stddev: 0.001490495654604158",
            "extra": "mean: 16.152201481481846 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 67.75480536044786,
            "unit": "iter/sec",
            "range": "stddev: 0.0007082478252157347",
            "extra": "mean: 14.75910077049316 msec\nrounds: 61"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.703488660453585,
            "unit": "iter/sec",
            "range": "stddev: 0.0005406654288978105",
            "extra": "mean: 93.42748254545472 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 283.9633730565336,
            "unit": "iter/sec",
            "range": "stddev: 0.00004706735555848438",
            "extra": "mean: 3.521580932203226 msec\nrounds: 236"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 63.330877293933696,
            "unit": "iter/sec",
            "range": "stddev: 0.0010118962253789538",
            "extra": "mean: 15.790086016948125 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2805971249412844,
            "unit": "iter/sec",
            "range": "stddev: 0.13566651475967353",
            "extra": "mean: 780.8857137999979 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2265012984974084,
            "unit": "iter/sec",
            "range": "stddev: 0.1505590897749343",
            "extra": "mean: 815.3273064000047 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 391838.29677120486,
            "unit": "iter/sec",
            "range": "stddev: 7.922586449688597e-7",
            "extra": "mean: 2.5520731593622203 usec\nrounds: 12876"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 367695.4503672068,
            "unit": "iter/sec",
            "range": "stddev: 6.05644093241525e-7",
            "extra": "mean: 2.7196420271214365 usec\nrounds: 78654"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 371266.4285787172,
            "unit": "iter/sec",
            "range": "stddev: 6.366321090023194e-7",
            "extra": "mean: 2.693483501398717 usec\nrounds: 91735"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 153609.63262800532,
            "unit": "iter/sec",
            "range": "stddev: 9.792711904896824e-7",
            "extra": "mean: 6.510008408272732 usec\nrounds: 44242"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 183596.14544198697,
            "unit": "iter/sec",
            "range": "stddev: 9.291957269137605e-7",
            "extra": "mean: 5.446737444256321 usec\nrounds: 49121"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 403154.07916580513,
            "unit": "iter/sec",
            "range": "stddev: 5.732599146664495e-7",
            "extra": "mean: 2.4804412299862406 usec\nrounds: 93985"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 417333.47439686296,
            "unit": "iter/sec",
            "range": "stddev: 6.529738595962088e-7",
            "extra": "mean: 2.3961653242535026 usec\nrounds: 31163"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 32500.243294526146,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026793351112199456",
            "extra": "mean: 30.769000432942143 usec\nrounds: 11550"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 555139.5029961196,
            "unit": "iter/sec",
            "range": "stddev: 4.172759838218948e-7",
            "extra": "mean: 1.8013490205667997 usec\nrounds: 59985"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 246158.82366805972,
            "unit": "iter/sec",
            "range": "stddev: 7.182872141554524e-7",
            "extra": "mean: 4.062417853233163 usec\nrounds: 38346"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 356382.8646128801,
            "unit": "iter/sec",
            "range": "stddev: 5.714166136729297e-7",
            "extra": "mean: 2.805971047699634 usec\nrounds: 66765"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 212205.30572305372,
            "unit": "iter/sec",
            "range": "stddev: 8.968012997045037e-7",
            "extra": "mean: 4.712417517519975 usec\nrounds: 41330"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 194865.55664477337,
            "unit": "iter/sec",
            "range": "stddev: 9.813814152741372e-7",
            "extra": "mean: 5.131743224498785 usec\nrounds: 64940"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 49521.235759004136,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018693058077024616",
            "extra": "mean: 20.193357146144645 usec\nrounds: 21823"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 24733.86268932623,
            "unit": "iter/sec",
            "range": "stddev: 0.00003363494739656482",
            "extra": "mean: 40.43040153334177 usec\nrounds: 12913"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 33219.808616336646,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028992945485752362",
            "extra": "mean: 30.102521406707492 usec\nrounds: 9810"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 310.9634891600287,
            "unit": "iter/sec",
            "range": "stddev: 0.0000632629897589191",
            "extra": "mean: 3.2158116140939548 msec\nrounds: 298"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.55583483588547,
            "unit": "iter/sec",
            "range": "stddev: 0.0004521861709284102",
            "extra": "mean: 32.72697360000052 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 24211.70594801155,
            "unit": "iter/sec",
            "range": "stddev: 0.000003875411401393595",
            "extra": "mean: 41.30233541359062 usec\nrounds: 13139"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 176.24063988028016,
            "unit": "iter/sec",
            "range": "stddev: 0.01378549767513441",
            "extra": "mean: 5.6740601979163126 msec\nrounds: 192"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 12.432496400986532,
            "unit": "iter/sec",
            "range": "stddev: 0.07722557698628417",
            "extra": "mean: 80.43436875000012 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 12801.518743526942,
            "unit": "iter/sec",
            "range": "stddev: 0.000007076547607388055",
            "extra": "mean: 78.11573142488642 usec\nrounds: 6393"
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
          "id": "7c8fd3f259314d36577f7ddb8366fcda7fd4aa01",
          "message": "chore(deps): Bump actions/setup-python from 6 to 7 (merges PR #800)\n\nBumps [actions/setup-python](https://github.com/actions/setup-python) from 6 to 7.\n- [Release notes](https://github.com/actions/setup-python/releases)\n- [Commits](https://github.com/actions/setup-python/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/setup-python\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-10-25T18:59:51Z",
          "tree_id": "4e538c814beff36a521e6cbaf1c9aa5f1bb62c0a",
          "url": "https://github.com/endavis/pynetappfoundry/commit/7c8fd3f259314d36577f7ddb8366fcda7fd4aa01"
        },
        "date": 1792954859551,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1062423.8073293257,
            "unit": "iter/sec",
            "range": "stddev: 3.136556252122988e-7",
            "extra": "mean: 941.2439678980427 nsec\nrounds: 152393"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 680876.1605155452,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012729146458002572",
            "extra": "mean: 1.4686958627583921 usec\nrounds: 190151"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 428775.2577910581,
            "unit": "iter/sec",
            "range": "stddev: 5.578396644363889e-7",
            "extra": "mean: 2.3322241240125363 usec\nrounds: 158680"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 424413.5026011157,
            "unit": "iter/sec",
            "range": "stddev: 5.701450375525438e-7",
            "extra": "mean: 2.35619270798707 usec\nrounds: 116456"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 472339.2722011661,
            "unit": "iter/sec",
            "range": "stddev: 5.435085889290713e-7",
            "extra": "mean: 2.117122286571392 usec\nrounds: 50259"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 146731.4724726406,
            "unit": "iter/sec",
            "range": "stddev: 9.782750720402188e-7",
            "extra": "mean: 6.815170482164002 usec\nrounds: 56393"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 130281.47890987447,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010515064630645594",
            "extra": "mean: 7.6756881205791 usec\nrounds: 64355"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 68818.59405196029,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014521803027213351",
            "extra": "mean: 14.530956549983676 usec\nrounds: 23084"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 210855.919189809,
            "unit": "iter/sec",
            "range": "stddev: 8.570742376811962e-7",
            "extra": "mean: 4.7425749480611765 usec\nrounds: 44284"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 27948.301039290327,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026993346972763145",
            "extra": "mean: 35.7803502472003 usec\nrounds: 3035"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 62.90825941887399,
            "unit": "iter/sec",
            "range": "stddev: 0.00047490152004224306",
            "extra": "mean: 15.896163862069532 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 58.64513424415166,
            "unit": "iter/sec",
            "range": "stddev: 0.0005754929178520928",
            "extra": "mean: 17.051713034482894 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 69.0811754965582,
            "unit": "iter/sec",
            "range": "stddev: 0.0006865785990152487",
            "extra": "mean: 14.475723564516104 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.731155704261687,
            "unit": "iter/sec",
            "range": "stddev: 0.0005162707567391892",
            "extra": "mean: 93.1866080000002 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 292.51051926503885,
            "unit": "iter/sec",
            "range": "stddev: 0.00003359517567731409",
            "extra": "mean: 3.418680471774476 msec\nrounds: 248"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 60.71232631068602,
            "unit": "iter/sec",
            "range": "stddev: 0.0009709414163478705",
            "extra": "mean: 16.471119799999975 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2571804167511953,
            "unit": "iter/sec",
            "range": "stddev: 0.13642251681605033",
            "extra": "mean: 795.4307803999995 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2373439379634839,
            "unit": "iter/sec",
            "range": "stddev: 0.13792223506245588",
            "extra": "mean: 808.1827286000021 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 383780.5022974464,
            "unit": "iter/sec",
            "range": "stddev: 7.54689430340898e-7",
            "extra": "mean: 2.605656082092875 usec\nrounds: 12093"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 357766.66994916584,
            "unit": "iter/sec",
            "range": "stddev: 6.016101723710403e-7",
            "extra": "mean: 2.7951178351580026 usec\nrounds: 69750"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 362131.3697973003,
            "unit": "iter/sec",
            "range": "stddev: 6.249510148783148e-7",
            "extra": "mean: 2.761428816729522 usec\nrounds: 86200"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 149162.0535522605,
            "unit": "iter/sec",
            "range": "stddev: 0.000001007711976335047",
            "extra": "mean: 6.704117945450781 usec\nrounds: 42384"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 178364.46689829745,
            "unit": "iter/sec",
            "range": "stddev: 9.044715847459689e-7",
            "extra": "mean: 5.606497848981295 usec\nrounds: 53462"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 397169.06310142303,
            "unit": "iter/sec",
            "range": "stddev: 5.799023397815421e-7",
            "extra": "mean: 2.5178194701046874 usec\nrounds: 81150"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 406690.6964347133,
            "unit": "iter/sec",
            "range": "stddev: 6.104466167288265e-7",
            "extra": "mean: 2.458871099748729 usec\nrounds: 72591"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 31562.06957827899,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032579171181120593",
            "extra": "mean: 31.68360039001371 usec\nrounds: 11281"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 549672.9918056973,
            "unit": "iter/sec",
            "range": "stddev: 4.885672030666361e-7",
            "extra": "mean: 1.8192634801192629 usec\nrounds: 60274"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 245058.78128872073,
            "unit": "iter/sec",
            "range": "stddev: 7.376512220967095e-7",
            "extra": "mean: 4.080653607845338 usec\nrounds: 50847"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 357530.98523384216,
            "unit": "iter/sec",
            "range": "stddev: 6.779497854718962e-7",
            "extra": "mean: 2.7969603791009967 usec\nrounds: 64688"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 214406.94029201657,
            "unit": "iter/sec",
            "range": "stddev: 8.304400938080589e-7",
            "extra": "mean: 4.664028126319169 usec\nrounds: 51162"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 195195.19298379394,
            "unit": "iter/sec",
            "range": "stddev: 8.204472407949036e-7",
            "extra": "mean: 5.123076981117178 usec\nrounds: 67627"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 48676.13097710563,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021217861041849176",
            "extra": "mean: 20.543949979720878 usec\nrounds: 22231"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 24283.875315265363,
            "unit": "iter/sec",
            "range": "stddev: 0.00003376647895331085",
            "extra": "mean: 41.17958880193141 usec\nrounds: 14431"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 32947.81925665053,
            "unit": "iter/sec",
            "range": "stddev: 0.000003135830950386404",
            "extra": "mean: 30.351022391205742 usec\nrounds: 9334"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 310.6495299792157,
            "unit": "iter/sec",
            "range": "stddev: 0.000043285975881929854",
            "extra": "mean: 3.2190616868691415 msec\nrounds: 297"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 29.070384821342053,
            "unit": "iter/sec",
            "range": "stddev: 0.0005134582939483762",
            "extra": "mean: 34.399269433332336 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 23930.076565863306,
            "unit": "iter/sec",
            "range": "stddev: 0.000004115523536494045",
            "extra": "mean: 41.78841623208672 usec\nrounds: 13233"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 175.57170184722804,
            "unit": "iter/sec",
            "range": "stddev: 0.014485045969886484",
            "extra": "mean: 5.695678685567107 msec\nrounds: 194"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.460033912520458,
            "unit": "iter/sec",
            "range": "stddev: 0.08271274302436818",
            "extra": "mean: 87.25977668420926 msec\nrounds: 19"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 12750.444467263853,
            "unit": "iter/sec",
            "range": "stddev: 0.000007136051302551857",
            "extra": "mean: 78.42863851275548 usec\nrounds: 5245"
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
          "id": "6562a002d9dad67961315a5b74852691a22fd49e",
          "message": "test: compare CodeQL workflow action versions repo-wide (merges PR #822, addresses #821)\n\ntests/test_codeql_workflow.py hard-coded actions/checkout@v6 and\ngithub/codeql-action init/analyze @v4, so any major bump failed CI even\nwhen applied to every workflow (Dependabot #779, checkout v6 -> v7).\n\nRequire one checkout version across all workflows and one\ncodeql-action version across its steps instead. Drift and half-applied\nbumps still fail; full bumps pass.\n\nAddresses #821\n\n\nClaude-Session: https://claude.ai/code/session_01QAhsGhfKSCD67omHGamv8i\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-25T19:07:15Z",
          "tree_id": "fee3cf5f9768bd592ca547d2941e9cddd14eb71d",
          "url": "https://github.com/endavis/pynetappfoundry/commit/6562a002d9dad67961315a5b74852691a22fd49e"
        },
        "date": 1792955309878,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 874127.6748411945,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012991188718114433",
            "extra": "mean: 1.1439976433438892 usec\nrounds: 126024"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 531062.1636881465,
            "unit": "iter/sec",
            "range": "stddev: 0.0000076123422658792815",
            "extra": "mean: 1.883018728081005 usec\nrounds: 172682"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 397843.70380766754,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013685529125566993",
            "extra": "mean: 2.513549895170484 usec\nrounds: 137288"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 415050.85063980636,
            "unit": "iter/sec",
            "range": "stddev: 7.025013507066903e-7",
            "extra": "mean: 2.409343333373457 usec\nrounds: 143001"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 464994.7981183358,
            "unit": "iter/sec",
            "range": "stddev: 6.703219972695148e-7",
            "extra": "mean: 2.150561692403087 usec\nrounds: 78778"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 145469.1740559493,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010405527455447606",
            "extra": "mean: 6.874308639543023 usec\nrounds: 52699"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 130446.36227606294,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011532029101897235",
            "extra": "mean: 7.665986099970389 usec\nrounds: 64604"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 67262.57836777707,
            "unit": "iter/sec",
            "range": "stddev: 0.000002055646115840968",
            "extra": "mean: 14.867107747969735 usec\nrounds: 43379"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 206914.303919596,
            "unit": "iter/sec",
            "range": "stddev: 8.787023552768773e-7",
            "extra": "mean: 4.832918657902868 usec\nrounds: 31890"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 27351.964159000378,
            "unit": "iter/sec",
            "range": "stddev: 0.000005507610466111373",
            "extra": "mean: 36.560445684517404 usec\nrounds: 1703"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 49.87571485577102,
            "unit": "iter/sec",
            "range": "stddev: 0.0009121322534114882",
            "extra": "mean: 20.049837940002817 msec\nrounds: 50"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 47.66998625948457,
            "unit": "iter/sec",
            "range": "stddev: 0.0009459870899921351",
            "extra": "mean: 20.97756006382395 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 53.387233998064964,
            "unit": "iter/sec",
            "range": "stddev: 0.0009981491599850088",
            "extra": "mean: 18.73106967924664 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.762661394366361,
            "unit": "iter/sec",
            "range": "stddev: 0.0019609206372346024",
            "extra": "mean: 102.43108509090152 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 285.6923697198424,
            "unit": "iter/sec",
            "range": "stddev: 0.000060469513260175836",
            "extra": "mean: 3.5002684915268367 msec\nrounds: 236"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 47.81649888364409,
            "unit": "iter/sec",
            "range": "stddev: 0.0007325983101078363",
            "extra": "mean: 20.91328355999849 msec\nrounds: 50"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.1247643187405243,
            "unit": "iter/sec",
            "range": "stddev: 0.1609392836775075",
            "extra": "mean: 889.0751451999904 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.0916600236734284,
            "unit": "iter/sec",
            "range": "stddev: 0.16433885098473178",
            "extra": "mean: 916.036108600008 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 382130.491236271,
            "unit": "iter/sec",
            "range": "stddev: 7.197343981889239e-7",
            "extra": "mean: 2.616907111402688 usec\nrounds: 7762"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 362735.1279219643,
            "unit": "iter/sec",
            "range": "stddev: 6.804687392271821e-7",
            "extra": "mean: 2.756832528817367 usec\nrounds: 70842"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 370022.65244280745,
            "unit": "iter/sec",
            "range": "stddev: 6.372612118799084e-7",
            "extra": "mean: 2.7025372457556904 usec\nrounds: 79284"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 152252.1605336982,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012848561756095502",
            "extra": "mean: 6.56805129394974 usec\nrounds: 38991"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 181129.07047187173,
            "unit": "iter/sec",
            "range": "stddev: 8.978908527228112e-7",
            "extra": "mean: 5.520924926047662 usec\nrounds: 52122"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 402116.93737144454,
            "unit": "iter/sec",
            "range": "stddev: 5.878344352090827e-7",
            "extra": "mean: 2.4868387950450277 usec\nrounds: 80103"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 411318.97506521305,
            "unit": "iter/sec",
            "range": "stddev: 6.082142033545986e-7",
            "extra": "mean: 2.431203179579677 usec\nrounds: 70637"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 31978.34246446996,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031803199594590694",
            "extra": "mean: 31.27116426097024 usec\nrounds: 14617"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 535890.8896271012,
            "unit": "iter/sec",
            "range": "stddev: 4.809232522657162e-7",
            "extra": "mean: 1.8660515029390556 usec\nrounds: 51531"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 238903.47547390294,
            "unit": "iter/sec",
            "range": "stddev: 8.314362158868936e-7",
            "extra": "mean: 4.185790926717752 usec\nrounds: 64982"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 356707.6060023524,
            "unit": "iter/sec",
            "range": "stddev: 6.540671684006188e-7",
            "extra": "mean: 2.803416532680846 usec\nrounds: 60898"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 214737.1770999039,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010422990991922697",
            "extra": "mean: 4.656855480291436 usec\nrounds: 38493"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 194063.08212987016,
            "unit": "iter/sec",
            "range": "stddev: 0.000001251157017337682",
            "extra": "mean: 5.1529636086619695 usec\nrounds: 66142"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 48986.43100155523,
            "unit": "iter/sec",
            "range": "stddev: 0.000002203826026562788",
            "extra": "mean: 20.413816225318634 usec\nrounds: 21374"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 24487.520579920565,
            "unit": "iter/sec",
            "range": "stddev: 0.000044164548448681435",
            "extra": "mean: 40.83712749668852 usec\nrounds: 14118"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 32657.059485393107,
            "unit": "iter/sec",
            "range": "stddev: 0.000003269515641610112",
            "extra": "mean: 30.621250527693146 usec\nrounds: 8047"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 304.5101369965502,
            "unit": "iter/sec",
            "range": "stddev: 0.0004018510380005522",
            "extra": "mean: 3.2839629243979123 msec\nrounds: 291"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 28.24916774445712,
            "unit": "iter/sec",
            "range": "stddev: 0.0007578220893596503",
            "extra": "mean: 35.39927296428808 msec\nrounds: 28"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 24001.968758702777,
            "unit": "iter/sec",
            "range": "stddev: 0.000004313742096258617",
            "extra": "mean: 41.66324896316741 usec\nrounds: 12054"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 166.65205939018912,
            "unit": "iter/sec",
            "range": "stddev: 0.017609361742649227",
            "extra": "mean: 6.000525908045697 msec\nrounds: 174"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.834154622851372,
            "unit": "iter/sec",
            "range": "stddev: 0.08687867227287602",
            "extra": "mean: 84.5011774705928 msec\nrounds: 17"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 12858.579565857144,
            "unit": "iter/sec",
            "range": "stddev: 0.000007528775739006765",
            "extra": "mean: 77.7690875479947 usec\nrounds: 5951"
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
          "id": "4d4f213e8bb3fae4d9868b7a9c1fb25a8d484f07",
          "message": "chore: bump actions/checkout from v6 to v7 (merges PR #824, addresses #823)\n\nReplace all 13 actions/checkout@v6 references in the 9 workflow files\nwith @v7, the same change as Dependabot #779. #779 can't land: its only\nCI run is from July and can't be re-run, and Dependabot ignored both\nrebase and recreate on it.\n\nThe v7 tag points at v7.0.1. v7's only behavior change (refusing to\ncheck out fork PR code under pull_request_target or workflow_run when\nref is set) doesn't affect the one pull_request_target checkout here,\nwhich sets no ref.\n\nAddresses #823\n\n\nClaude-Session: https://claude.ai/code/session_01QAhsGhfKSCD67omHGamv8i\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-25T19:55:49Z",
          "tree_id": "c3d1a9cac924b508479363df91b7edc7f3a5df11",
          "url": "https://github.com/endavis/pynetappfoundry/commit/4d4f213e8bb3fae4d9868b7a9c1fb25a8d484f07"
        },
        "date": 1792958205357,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1664557.822807854,
            "unit": "iter/sec",
            "range": "stddev: 3.0489312032495653e-7",
            "extra": "mean: 600.7601456062087 nsec\nrounds: 112906"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 1019917.0261859996,
            "unit": "iter/sec",
            "range": "stddev: 5.614038554172824e-7",
            "extra": "mean: 980.4719151905134 nsec\nrounds: 125993"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 671674.9896380559,
            "unit": "iter/sec",
            "range": "stddev: 4.7278141108730396e-7",
            "extra": "mean: 1.4888152982127083 usec\nrounds: 126263"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 675238.6535174621,
            "unit": "iter/sec",
            "range": "stddev: 4.056399269222574e-7",
            "extra": "mean: 1.480957872880628 usec\nrounds: 133833"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 750126.2338035156,
            "unit": "iter/sec",
            "range": "stddev: 4.148528440205181e-7",
            "extra": "mean: 1.3331089554480708 usec\nrounds: 64017"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 227002.03953550244,
            "unit": "iter/sec",
            "range": "stddev: 8.055534799608257e-7",
            "extra": "mean: 4.405246763624795 usec\nrounds: 26033"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 198365.11821847956,
            "unit": "iter/sec",
            "range": "stddev: 8.195600026317858e-7",
            "extra": "mean: 5.0412089029614515 usec\nrounds: 67797"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 113600.58254886139,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010457301226753106",
            "extra": "mean: 8.802771760170195 usec\nrounds: 53952"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 318973.38858591835,
            "unit": "iter/sec",
            "range": "stddev: 6.978314417185654e-7",
            "extra": "mean: 3.13505776902966 usec\nrounds: 40108"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 46422.520296427676,
            "unit": "iter/sec",
            "range": "stddev: 0.000002093907248718358",
            "extra": "mean: 21.541269056797685 usec\nrounds: 3096"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 109.53262263294684,
            "unit": "iter/sec",
            "range": "stddev: 0.0005724610583803215",
            "extra": "mean: 9.129700138296563 msec\nrounds: 94"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 107.72114237243431,
            "unit": "iter/sec",
            "range": "stddev: 0.0009054529058371526",
            "extra": "mean: 9.283228695650173 msec\nrounds: 92"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 136.9457328058079,
            "unit": "iter/sec",
            "range": "stddev: 0.00047027488879802174",
            "extra": "mean: 7.3021625392156055 msec\nrounds: 102"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 17.570239782348438,
            "unit": "iter/sec",
            "range": "stddev: 0.003120503390207223",
            "extra": "mean: 56.9144196315766 msec\nrounds: 19"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 472.357988404941,
            "unit": "iter/sec",
            "range": "stddev: 0.00006726610074246055",
            "extra": "mean: 2.1170383999999682 msec\nrounds: 360"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 101.62462304132724,
            "unit": "iter/sec",
            "range": "stddev: 0.0005885799508269977",
            "extra": "mean: 9.840134901099061 msec\nrounds: 91"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.4738645377594302,
            "unit": "iter/sec",
            "range": "stddev: 0.13007512582374556",
            "extra": "mean: 678.4884053999974 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.4860858214020833,
            "unit": "iter/sec",
            "range": "stddev: 0.12631346729685355",
            "extra": "mean: 672.9086474000042 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 613559.1872879169,
            "unit": "iter/sec",
            "range": "stddev: 4.64283865875279e-7",
            "extra": "mean: 1.6298346120775191 usec\nrounds: 10297"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 590828.6557906028,
            "unit": "iter/sec",
            "range": "stddev: 4.444855692203679e-7",
            "extra": "mean: 1.6925380822327831 usec\nrounds: 28189"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 588740.6244552957,
            "unit": "iter/sec",
            "range": "stddev: 4.4083248470240305e-7",
            "extra": "mean: 1.6985408488249005 usec\nrounds: 74433"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 228928.60865781325,
            "unit": "iter/sec",
            "range": "stddev: 6.756450123236873e-7",
            "extra": "mean: 4.368174016619877 usec\nrounds: 43266"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 273145.5580033486,
            "unit": "iter/sec",
            "range": "stddev: 6.345656300438887e-7",
            "extra": "mean: 3.6610516653093095 usec\nrounds: 55124"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 660091.0285851134,
            "unit": "iter/sec",
            "range": "stddev: 4.264656240617241e-7",
            "extra": "mean: 1.5149425710927658 usec\nrounds: 72333"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 672834.5563038026,
            "unit": "iter/sec",
            "range": "stddev: 9.754978945361424e-7",
            "extra": "mean: 1.4862494659808667 usec\nrounds: 82857"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 52256.13073692337,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015661970693493348",
            "extra": "mean: 19.136510604552196 usec\nrounds: 17681"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 857799.5394899042,
            "unit": "iter/sec",
            "range": "stddev: 3.763634717329765e-7",
            "extra": "mean: 1.1657735332833778 usec\nrounds: 46806"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 403288.4663374923,
            "unit": "iter/sec",
            "range": "stddev: 5.324134386961337e-7",
            "extra": "mean: 2.479614676515815 usec\nrounds: 46387"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 536477.2068119589,
            "unit": "iter/sec",
            "range": "stddev: 4.268738065356227e-7",
            "extra": "mean: 1.8640120909191038 usec\nrounds: 56323"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 302840.2856585597,
            "unit": "iter/sec",
            "range": "stddev: 6.430862552118462e-7",
            "extra": "mean: 3.302070587555382 usec\nrounds: 36352"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 302716.6617228164,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011965910840032403",
            "extra": "mean: 3.303419092655209 usec\nrounds: 63752"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 73631.73289049222,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014025883327921176",
            "extra": "mean: 13.58110098382767 usec\nrounds: 26430"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 36233.2458312926,
            "unit": "iter/sec",
            "range": "stddev: 0.000036488635575819134",
            "extra": "mean: 27.598962694541612 usec\nrounds: 17799"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 50058.41555206027,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015968833708206548",
            "extra": "mean: 19.976661046333152 usec\nrounds: 10379"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 478.5754762875249,
            "unit": "iter/sec",
            "range": "stddev: 0.0000222240766187211",
            "extra": "mean: 2.0895345657018307 msec\nrounds: 449"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 44.70183186308697,
            "unit": "iter/sec",
            "range": "stddev: 0.00012986638503282772",
            "extra": "mean: 22.370447883719972 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 34901.86986544666,
            "unit": "iter/sec",
            "range": "stddev: 0.000002115583480996952",
            "extra": "mean: 28.651760030485185 usec\nrounds: 17123"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 256.1001863347615,
            "unit": "iter/sec",
            "range": "stddev: 0.011966779918541358",
            "extra": "mean: 3.904721875886687 msec\nrounds: 282"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 14.731970330946957,
            "unit": "iter/sec",
            "range": "stddev: 0.07719431088388652",
            "extra": "mean: 67.87958280769365 msec\nrounds: 26"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 20246.045891336154,
            "unit": "iter/sec",
            "range": "stddev: 0.000003438263508141078",
            "extra": "mean: 49.392360630177556 usec\nrounds: 7742"
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
          "id": "29d6be1062210cbb59b1afd95e4ce39f5ac25266",
          "message": "chore: sync with pyproject-template (36bcb77 → 72dd3cd), phase A (merges PR #832, addresses #826)\n\nThis is phase A of the template sync: tooling, CI and config. Phase B\n(#827) covers the AI agent workflow. Phase C (#828) brings the\nroot-level template tests and records the new sync point; until then,\n.config/pyproject_template still records 36bcb77.\n\nUpstream changes adopted:\n- tools/pyproject_template/ refreshed by bootstrap, and\n  migrate_existing_project.py removed.\n- ruff runs in preview mode with explicit-preview-rules, opting into\n  PLW1514 (explicit encoding on text-mode file I/O).\n- mypy excludes the agent config directories.\n- pytest gains the benchmark addopts and pythonpath = [\".\"].\n- The build requires hatchling>=1.32.4.\n- Coverage measures pynetappfoundry and tools/, excluding\n  tools/pyproject_template/.\n- vulture scans src/, tests/ and tools/.\n- GitHub Actions are pinned to commit SHAs.\n- A new daily-check workflow runs doit check on main.\n- CI runs doit deadcode and doit wheel_check.\n- Dependabot groups the codeql-action updates.\n- New doit tasks: wheel_check, worktree, delegation_context and\n  install_jq.\n- doit check now also runs deadcode, wheel_check and docs_build, which\n  now builds with mkdocs --strict.\n- pre-commit installs the commit-msg hook stage, and a new\n  check-commit-issue-ref hook checks that a commit references its\n  branch's issue.\n- Template-owned tests under tests/template/ are refreshed. The tests\n  for the removed pyproject_template modules are deleted.\n- Refreshed from the template: .github/CONTRIBUTING.md, SECURITY.md,\n  the PR template, the actionlint config, .gitignore, ADRs 9001-9004\n  and 9006-9017 (9017 is new), the new ADRs 9020-9022, and the docs\n  under docs/template/ and docs/development/.\n\nProject changes needed to adopt them:\n- Fix placeholders that were left on main: `import package_name` in\n  release.yml and testpypi.yml, and username/package_name in\n  SECURITY.md and CONTRIBUTING.md.\n- Keep doit type_check and the pre-commit mypy hook at\n  src/ tools/doit/ until #829. Skip the two template tests that assert\n  the wider scope until then.\n- Ruff fixes:\n  - noqa the side-effect imports in cache/__init__.py, which F401 now\n    flags in preview mode.\n  - Add encoding=\"utf-8\" at 21 sites. Behavior changes only on non-UTF-8\n    locales.\n  - Use enumerate in the inventory report (SIM113).\n  - Limit the ANN401 ignore to src/** and two tools/ files, so the\n    template code's noqa: ANN401 comments stay in use.\n- tools/doit/audit_legacy.py computes its counts before printing, to\n  satisfy test_doit_markup_escaping.\n- mkdocs.yml ports the template's not_in_nav and validation block, with\n  anchors and omitted_files left at info until #827 and #831. The nav\n  now points at decisions/90xx, and the stale docs/template/decisions/\n  is deleted (ADR-9016).\n- Raise coverage fail_under from 10 to 75. Measured coverage is 77.75%.\n\nAddresses #826\n\n\nClaude-Session: https://claude.ai/code/session_01QAhsGhfKSCD67omHGamv8i\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-25T21:11:07Z",
          "tree_id": "dfbb03ebf677afdfeb55460bbe900de8c1aa28e7",
          "url": "https://github.com/endavis/pynetappfoundry/commit/29d6be1062210cbb59b1afd95e4ce39f5ac25266"
        },
        "date": 1792962950621,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1764435.6308083152,
            "unit": "iter/sec",
            "range": "stddev: 7.594172054032536e-8",
            "extra": "mean: 566.7534607323048 nsec\nrounds: 186290"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 1071696.0163145745,
            "unit": "iter/sec",
            "range": "stddev: 9.790011701905403e-8",
            "extra": "mean: 933.1004172609245 nsec\nrounds: 113598"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 654773.0826564672,
            "unit": "iter/sec",
            "range": "stddev: 1.4497025524204684e-7",
            "extra": "mean: 1.5272466545859207 usec\nrounds: 68437"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 653520.0744617264,
            "unit": "iter/sec",
            "range": "stddev: 1.952102325146769e-7",
            "extra": "mean: 1.530174877678628 usec\nrounds: 68672"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 721452.0516464668,
            "unit": "iter/sec",
            "range": "stddev: 1.1532254669766262e-7",
            "extra": "mean: 1.3860935009025797 usec\nrounds: 74795"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 213454.43368896723,
            "unit": "iter/sec",
            "range": "stddev: 5.762142521646585e-7",
            "extra": "mean: 4.684840613135912 usec\nrounds: 111198"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 184809.23342791575,
            "unit": "iter/sec",
            "range": "stddev: 7.640646723236858e-7",
            "extra": "mean: 5.410985054434777 usec\nrounds: 196580"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 99606.11696109327,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016100449257013472",
            "extra": "mean: 10.039544061240795 usec\nrounds: 108179"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 298280.24956588895,
            "unit": "iter/sec",
            "range": "stddev: 5.703772818575243e-7",
            "extra": "mean: 3.352551841616667 usec\nrounds: 164231"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 41284.34567554211,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014504525634667854",
            "extra": "mean: 24.222256248387758 usec\nrounds: 41971"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 102.48959629724197,
            "unit": "iter/sec",
            "range": "stddev: 0.0005195202457101559",
            "extra": "mean: 9.757087900900537 msec\nrounds: 111"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 94.84955990485965,
            "unit": "iter/sec",
            "range": "stddev: 0.0014035138899652529",
            "extra": "mean: 10.543011491071397 msec\nrounds: 112"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 116.43286124540738,
            "unit": "iter/sec",
            "range": "stddev: 0.0006939720480291775",
            "extra": "mean: 8.588640606300006 msec\nrounds: 127"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 14.828989186512535,
            "unit": "iter/sec",
            "range": "stddev: 0.0005537548175332344",
            "extra": "mean: 67.43547974999764 msec\nrounds: 16"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 392.84067195714874,
            "unit": "iter/sec",
            "range": "stddev: 0.00003942758022934833",
            "extra": "mean: 2.5455612704712016 msec\nrounds: 403"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 99.20146070724913,
            "unit": "iter/sec",
            "range": "stddev: 0.0007230099348094201",
            "extra": "mean: 10.080496727271733 msec\nrounds: 110"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 3.237252094738983,
            "unit": "iter/sec",
            "range": "stddev: 0.00030539634465727",
            "extra": "mean: 308.90396259999306 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 3.2633583562453223,
            "unit": "iter/sec",
            "range": "stddev: 0.000793800812737448",
            "extra": "mean: 306.43278819999296 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 546819.0258128311,
            "unit": "iter/sec",
            "range": "stddev: 1.492929586268975e-7",
            "extra": "mean: 1.8287586071342854 usec\nrounds: 56732"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 512879.5682115143,
            "unit": "iter/sec",
            "range": "stddev: 1.3075862697432546e-7",
            "extra": "mean: 1.9497754677324066 usec\nrounds: 53770"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 519992.4880924266,
            "unit": "iter/sec",
            "range": "stddev: 1.2908701553781883e-7",
            "extra": "mean: 1.9231047042015226 usec\nrounds: 53973"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 218549.15347553956,
            "unit": "iter/sec",
            "range": "stddev: 3.9908768183950766e-7",
            "extra": "mean: 4.575629711198684 usec\nrounds: 116239"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 255533.29736426243,
            "unit": "iter/sec",
            "range": "stddev: 3.7769645731913614e-7",
            "extra": "mean: 3.91338432335298 usec\nrounds: 136968"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 571786.0390614563,
            "unit": "iter/sec",
            "range": "stddev: 1.2098351019289758e-7",
            "extra": "mean: 1.7489059397837423 usec\nrounds: 59716"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 581501.2815382971,
            "unit": "iter/sec",
            "range": "stddev: 1.1933012801449044e-7",
            "extra": "mean: 1.7196866657879257 usec\nrounds: 60296"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 44878.82740150791,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014974362981509544",
            "extra": "mean: 22.282222105615897 usec\nrounds: 46703"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 707682.9098063421,
            "unit": "iter/sec",
            "range": "stddev: 1.0065463559922079e-7",
            "extra": "mean: 1.4130622431925772 usec\nrounds: 74572"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 328763.754758584,
            "unit": "iter/sec",
            "range": "stddev: 3.1905752507469324e-7",
            "extra": "mean: 3.0416978317281793 usec\nrounds: 173041"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 448911.95419158594,
            "unit": "iter/sec",
            "range": "stddev: 4.953304383229602e-7",
            "extra": "mean: 2.227608310856479 usec\nrounds: 48214"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 275274.40721095743,
            "unit": "iter/sec",
            "range": "stddev: 6.88966309498313e-7",
            "extra": "mean: 3.6327387283542376 usec\nrounds: 145986"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 261654.6811606817,
            "unit": "iter/sec",
            "range": "stddev: 3.6392356852294265e-7",
            "extra": "mean: 3.821831107947584 usec\nrounds: 135483"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 63391.50771818084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011124289989111045",
            "extra": "mean: 15.774983684655249 usec\nrounds: 66747"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 32590.119365778784,
            "unit": "iter/sec",
            "range": "stddev: 0.000001605208319664735",
            "extra": "mean: 30.684146589841856 usec\nrounds: 33870"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 43895.15616209715,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013380579136939479",
            "extra": "mean: 22.78155695145894 usec\nrounds: 45530"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 417.2347487097024,
            "unit": "iter/sec",
            "range": "stddev: 0.000017539441912274216",
            "extra": "mean: 2.3967323026006295 msec\nrounds: 423"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 40.02299588584745,
            "unit": "iter/sec",
            "range": "stddev: 0.0002897497050956801",
            "extra": "mean: 24.985635829266105 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 32071.095339413052,
            "unit": "iter/sec",
            "range": "stddev: 0.000001754218910403263",
            "extra": "mean: 31.180724868198453 usec\nrounds: 33384"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 290.52214401632455,
            "unit": "iter/sec",
            "range": "stddev: 0.00002795081023761424",
            "extra": "mean: 3.44207841156442 msec\nrounds: 294"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 27.737867529674727,
            "unit": "iter/sec",
            "range": "stddev: 0.0004247311652172024",
            "extra": "mean: 36.05179810344731 msec\nrounds: 29"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 18230.640664034458,
            "unit": "iter/sec",
            "range": "stddev: 0.000002733895849550644",
            "extra": "mean: 54.85270750647877 usec\nrounds: 18797"
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
          "id": "a9e8e58fcd8e81706363b41ccd11a6d18f72ee12",
          "message": "chore: sync with pyproject-template (36bcb77 → 72dd3cd), phase B (merges PR #843, addresses #827)\n\nPhase B of the template sync brings in the AI agent workflow. Phase C\n(#828) brings the remaining root-level template tests and records the\nnew sync point.\n\nUpstream changes adopted:\n- implement-issue replaces the per-agent plan and implement commands,\n  their delegate skills, and ghi-finalize (ADR-9024).\n- Shared workflow skills now live once in .agents/skills/, and\n  `doit skills_sync` generates the Claude copies under .claude/skills/\n  (ADR-9023). Checkpoint, restore, ghi-status and the multi-*\n  orchestrators move there from .claude/commands/.\n- Antigravity replaces Gemini CLI. This removes .gemini/, GEMINI.md and\n  every Gemini bridge, and adds .agents/hooks.json, the Antigravity\n  review bridges and the agy statusline.\n- Copilot's command surface moves from .copilot/commands/ to\n  .github/skills/.\n- AGENTS.md is restructured to carry only shared, always-on\n  instructions (ADR-9018).\n- New skills:\n  - add-dependency\n  - dead-code-triage\n  - deprecate-api\n  - mutation-triage\n  - perf-change\n  - property-tests\n  - python-version-bump\n  - security-triage\n  - template-migrate\n  - template-sync\n  - typing-branch-narrowing\n  - verified-claims\n- New rule files: typing-branch-narrowing and verified-claims, for both\n  Claude and Copilot.\n- The subagent model and the pre-compact checkpoint hook pin\n  claude-sonnet-5.\n- The dangerous-command hook now also checks Claude's file edits and\n  Codex's apply_patch, and gains a shell wrapper for Antigravity.\n- .codex/config.toml switches to approval_policy = \"on-request\" and\n  hooks = true, because codex-cli 0.128 refuses the old values.\n- New ADRs 9018, 9019, 9023, 9024 and 9025. ADR-9005, the AI docs and\n  AI_SETUP.md are refreshed.\n- New tests: tests/agent_roster.py, four tests under tests/template/,\n  and 32 root-level tests for the hooks, statusline, skills and agent\n  structure.\n\nProject changes needed to adopt them:\n- AGENTS.md keeps the project's own content:\n  - the Cache Schema Pitfalls section;\n  - the Pre-Action rows and the tracking-issue reminder from #747;\n  - the doit audit_legacy row.\n- Fill in the package placeholders in AGENTS.md, CLAUDE.md and two AI\n  docs, as configure.py would.\n- README's AI Agent Support intro now describes Antigravity and\n  \"implement issue N\". The other README placeholders are #842.\n- Drop .gemini from the mypy and bandit excludes and from .gitignore.\n- Untrack .claude/scheduled_tasks.lock, a runtime lock committed by\n  accident in #608, and ignore it.\n- Index the new ADRs. Add the AI docs and the new ADRs to the mkdocs\n  nav, and set validation.links.anchors to warn. This needed the\n  data-source.md link to #cache-only-constraint fixed.\n- Set pytest pythonpath to [\".\", \"tests\"]. tests/ is a package here, so\n  pytest doesn't put it on sys.path the way upstream's layout does, and\n  the template tests import agent_roster as a top-level module.\n- Mark the 8 files upstream ships as executable as executable here too.\n  Extracting the template zip had dropped their exec bits.\n- The CBM and context-mode hooks stay excluded, pending #717 and #718.\n\nAddresses #827\n\n\nClaude-Session: https://claude.ai/code/session_01QAhsGhfKSCD67omHGamv8i\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-25T21:44:13Z",
          "tree_id": "b40e5c7965d8ba69546d754ad5a9c7a9aaa54a39",
          "url": "https://github.com/endavis/pynetappfoundry/commit/a9e8e58fcd8e81706363b41ccd11a6d18f72ee12"
        },
        "date": 1792964813594,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 2309451.999419976,
            "unit": "iter/sec",
            "range": "stddev: 2.3330457146367048e-7",
            "extra": "mean: 433.0031541037234 nsec\nrounds: 194667"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 1355879.2023285876,
            "unit": "iter/sec",
            "range": "stddev: 1.0891133842119029e-7",
            "extra": "mean: 737.5288287353324 nsec\nrounds: 146628"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 899169.0904975679,
            "unit": "iter/sec",
            "range": "stddev: 1.2139005229747933e-7",
            "extra": "mean: 1.112137873252111 usec\nrounds: 92799"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 894261.3560435695,
            "unit": "iter/sec",
            "range": "stddev: 2.441398276401362e-7",
            "extra": "mean: 1.1182413208865962 usec\nrounds: 94376"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 875783.648574823,
            "unit": "iter/sec",
            "range": "stddev: 1.861589166059072e-7",
            "extra": "mean: 1.1418345177228602 usec\nrounds: 92115"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 277147.1784132138,
            "unit": "iter/sec",
            "range": "stddev: 5.035011803179714e-7",
            "extra": "mean: 3.608191162996599 usec\nrounds: 145117"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 237156.3219111897,
            "unit": "iter/sec",
            "range": "stddev: 4.528422071404011e-7",
            "extra": "mean: 4.216628053349891 usec\nrounds: 127033"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 130181.24342708664,
            "unit": "iter/sec",
            "range": "stddev: 8.830864881667916e-7",
            "extra": "mean: 7.6815981601841985 usec\nrounds: 139471"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 398343.8529464937,
            "unit": "iter/sec",
            "range": "stddev: 5.407046029172244e-7",
            "extra": "mean: 2.5103939538746234 usec\nrounds: 42060"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 56739.82474237642,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026713187692625408",
            "extra": "mean: 17.62430540701239 usec\nrounds: 62641"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 108.42751384391006,
            "unit": "iter/sec",
            "range": "stddev: 0.001276745039671403",
            "extra": "mean: 9.222751352941456 msec\nrounds: 136"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 97.3943594320254,
            "unit": "iter/sec",
            "range": "stddev: 0.0009307606990071229",
            "extra": "mean: 10.267535058823725 msec\nrounds: 119"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 113.84898530429079,
            "unit": "iter/sec",
            "range": "stddev: 0.0009863294739139437",
            "extra": "mean: 8.783565328467724 msec\nrounds: 137"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 17.973692319002204,
            "unit": "iter/sec",
            "range": "stddev: 0.0005438215489593117",
            "extra": "mean: 55.63687094736661 msec\nrounds: 19"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 569.8938792664984,
            "unit": "iter/sec",
            "range": "stddev: 0.000038364274871713214",
            "extra": "mean: 1.7547126515678402 msec\nrounds: 574"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 86.760268872167,
            "unit": "iter/sec",
            "range": "stddev: 0.0018460290044884007",
            "extra": "mean: 11.526013150943605 msec\nrounds: 106"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 4.3323013265921455,
            "unit": "iter/sec",
            "range": "stddev: 0.0009618273930368198",
            "extra": "mean: 230.82420279999667 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 4.536806913051336,
            "unit": "iter/sec",
            "range": "stddev: 0.00321242794064895",
            "extra": "mean: 220.4193432000011 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 743493.4134361614,
            "unit": "iter/sec",
            "range": "stddev: 8.257133832184851e-8",
            "extra": "mean: 1.3450018277611322 usec\nrounds: 76104"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 693217.6799128272,
            "unit": "iter/sec",
            "range": "stddev: 8.361753378873142e-8",
            "extra": "mean: 1.442548320645473 usec\nrounds: 73153"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 699533.0523432741,
            "unit": "iter/sec",
            "range": "stddev: 8.56792196756912e-8",
            "extra": "mean: 1.4295250190827025 usec\nrounds: 73368"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 302919.50949228136,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013447971821770032",
            "extra": "mean: 3.3012069829245543 usec\nrounds: 168096"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 355628.2307143787,
            "unit": "iter/sec",
            "range": "stddev: 3.316601588877218e-7",
            "extra": "mean: 2.81192524561737 usec\nrounds: 184230"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 753414.3024819341,
            "unit": "iter/sec",
            "range": "stddev: 4.2366604583887087e-7",
            "extra": "mean: 1.3272909695313073 usec\nrounds: 79121"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 777510.7438052061,
            "unit": "iter/sec",
            "range": "stddev: 1.1212709004749218e-7",
            "extra": "mean: 1.2861558608256805 usec\nrounds: 82659"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 59229.856018054204,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029902844778728424",
            "extra": "mean: 16.883377188949844 usec\nrounds: 63557"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 1072095.7310046286,
            "unit": "iter/sec",
            "range": "stddev: 8.896221845269601e-8",
            "extra": "mean: 932.752524872877 nsec\nrounds: 111075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 464425.2248168626,
            "unit": "iter/sec",
            "range": "stddev: 4.939823339028481e-7",
            "extra": "mean: 2.1531991514766045 usec\nrounds: 49262"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 649642.9667875329,
            "unit": "iter/sec",
            "range": "stddev: 1.3239074164494563e-7",
            "extra": "mean: 1.5393070519103338 usec\nrounds: 68251"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 396810.32082668104,
            "unit": "iter/sec",
            "range": "stddev: 1.581450830403851e-7",
            "extra": "mean: 2.520095742259638 usec\nrounds: 41313"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 371273.5504544751,
            "unit": "iter/sec",
            "range": "stddev: 3.142935211565001e-7",
            "extra": "mean: 2.6934318342254717 usec\nrounds: 136036"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 89106.15278418649,
            "unit": "iter/sec",
            "range": "stddev: 8.982226735384651e-7",
            "extra": "mean: 11.222569584190017 usec\nrounds: 94109"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 45626.04377775343,
            "unit": "iter/sec",
            "range": "stddev: 0.000001440779879523712",
            "extra": "mean: 21.917306809922994 usec\nrounds: 48121"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 63633.4197111214,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011992344305184558",
            "extra": "mean: 15.715012717212602 usec\nrounds: 68018"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 606.1733224825044,
            "unit": "iter/sec",
            "range": "stddev: 0.000042446481814695136",
            "extra": "mean: 1.6496931866031803 msec\nrounds: 627"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 54.5900778255873,
            "unit": "iter/sec",
            "range": "stddev: 0.0008271855597174541",
            "extra": "mean: 18.318347213113572 msec\nrounds: 61"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 46712.160555924354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013394900930106826",
            "extra": "mean: 21.40770172261221 usec\nrounds: 48589"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 413.7068228946793,
            "unit": "iter/sec",
            "range": "stddev: 0.000051716315598931846",
            "extra": "mean: 2.417170674157767 msec\nrounds: 445"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 34.93986122755613,
            "unit": "iter/sec",
            "range": "stddev: 0.0007608298311246164",
            "extra": "mean: 28.620605945948256 msec\nrounds: 37"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 25876.796720921473,
            "unit": "iter/sec",
            "range": "stddev: 0.000005464940339492802",
            "extra": "mean: 38.64465956837296 usec\nrounds: 28223"
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
          "id": "e4c6bab6df83de749b39899f1db2f82c056863e3",
          "message": "feat: label nf cache query wildcard results with their source item (merges PR #849, addresses #848)\n\nWildcard ([*]) and filter-predicate paths now return each value labelled\nwith the array item it came from. The label is the first non-empty field\namong name, svm.name and uuid, falling back to the index [i]. --key\noverrides the order. Nested wildcards compose labels as outer/inner.\n\nAdds get_nested_value_with_identifiers() to utils/dict_path.py;\nget_nested_value() is unchanged. Records the decision in ADR-0020.\n\nBREAKING CHANGE: for wildcard and filter-predicate fields, --json now\nreturns a list of {\"key\": ..., \"value\": ...} records instead of a flat\nlist of values, --csv adds a \"key\" column after \"cluster\", and --raw\nprints \"key<TAB>value\" per line. Scripts parsing the old flat output must\nread the \"value\" field (JSON) or the second column (raw). Queries with\nno wildcard or filter field are unchanged.\n\nAddresses #848\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T10:35:47Z",
          "tree_id": "e945ff43df1f3961e5592a304de3346cfab4d2e6",
          "url": "https://github.com/endavis/pynetappfoundry/commit/e4c6bab6df83de749b39899f1db2f82c056863e3"
        },
        "date": 1793011112383,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 2276040.5269427197,
            "unit": "iter/sec",
            "range": "stddev: 7.42785426879981e-8",
            "extra": "mean: 439.359487743061 nsec\nrounds: 193088"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 1284665.6882064715,
            "unit": "iter/sec",
            "range": "stddev: 1.2816120615237356e-7",
            "extra": "mean: 778.4126323137851 nsec\nrounds: 153234"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 759797.0242291254,
            "unit": "iter/sec",
            "range": "stddev: 1.9214072302196777e-7",
            "extra": "mean: 1.316140979907864 usec\nrounds: 93968"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 806572.2917125967,
            "unit": "iter/sec",
            "range": "stddev: 1.29268444751584e-7",
            "extra": "mean: 1.2398144720254374 usec\nrounds: 93546"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 899474.3742899866,
            "unit": "iter/sec",
            "range": "stddev: 1.2690497450138228e-7",
            "extra": "mean: 1.1117604109504118 usec\nrounds: 102786"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 248955.61791402125,
            "unit": "iter/sec",
            "range": "stddev: 5.375608320016471e-7",
            "extra": "mean: 4.016780213191886 usec\nrounds: 148412"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 201069.1403976988,
            "unit": "iter/sec",
            "range": "stddev: 7.199461087553938e-7",
            "extra": "mean: 4.9734136129595985 usec\nrounds: 127195"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 114068.2591365842,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013286821989969058",
            "extra": "mean: 8.766680648668531 usec\nrounds: 139179"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 330131.2327766338,
            "unit": "iter/sec",
            "range": "stddev: 4.0780853869033306e-7",
            "extra": "mean: 3.0290984333390782 usec\nrounds: 198256"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 49681.98028254147,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015736013981917607",
            "extra": "mean: 20.12802215839624 usec\nrounds: 56051"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 132.67901438424553,
            "unit": "iter/sec",
            "range": "stddev: 0.0005053686205819796",
            "extra": "mean: 7.5369869503548355 msec\nrounds: 141"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 134.24836636279238,
            "unit": "iter/sec",
            "range": "stddev: 0.0002072799930915501",
            "extra": "mean: 7.448880214285834 msec\nrounds: 140"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 150.27166171114223,
            "unit": "iter/sec",
            "range": "stddev: 0.00012502525602561907",
            "extra": "mean: 6.654614639999371 msec\nrounds: 150"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 19.400642769874345,
            "unit": "iter/sec",
            "range": "stddev: 0.00030516911120229595",
            "extra": "mean: 51.54468394999867 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 449.9122922852558,
            "unit": "iter/sec",
            "range": "stddev: 0.00014772280833154404",
            "extra": "mean: 2.2226554311745157 msec\nrounds: 494"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 135.01808335972635,
            "unit": "iter/sec",
            "range": "stddev: 0.0003869710264518921",
            "extra": "mean: 7.406415312056514 msec\nrounds: 141"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 3.754383630528805,
            "unit": "iter/sec",
            "range": "stddev: 0.0014006109210739706",
            "extra": "mean: 266.35530579999624 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 3.8708043490407085,
            "unit": "iter/sec",
            "range": "stddev: 0.0021269719058263823",
            "extra": "mean: 258.344237999998 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 686332.1108910204,
            "unit": "iter/sec",
            "range": "stddev: 2.8155372742418314e-7",
            "extra": "mean: 1.4570205650173718 usec\nrounds: 77520"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 656502.6732705558,
            "unit": "iter/sec",
            "range": "stddev: 1.4037055156392123e-7",
            "extra": "mean: 1.5232230434313603 usec\nrounds: 73036"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 650443.4522085566,
            "unit": "iter/sec",
            "range": "stddev: 1.3491133118236592e-7",
            "extra": "mean: 1.5374126630140361 usec\nrounds: 72234"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 212160.34286312244,
            "unit": "iter/sec",
            "range": "stddev: 6.802310992498109e-7",
            "extra": "mean: 4.713416213911198 usec\nrounds: 135649"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 285660.40076151484,
            "unit": "iter/sec",
            "range": "stddev: 4.3332490220540497e-7",
            "extra": "mean: 3.500660215186268 usec\nrounds: 151309"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 738423.0319288997,
            "unit": "iter/sec",
            "range": "stddev: 1.3882152483685822e-7",
            "extra": "mean: 1.3542372823716131 usec\nrounds: 82366"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 762749.8475836416,
            "unit": "iter/sec",
            "range": "stddev: 1.2799545150801163e-7",
            "extra": "mean: 1.3110458208126248 usec\nrounds: 84861"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 49542.965488428854,
            "unit": "iter/sec",
            "range": "stddev: 0.000002502585135516379",
            "extra": "mean: 20.18450026439289 usec\nrounds: 58627"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 934645.3716380469,
            "unit": "iter/sec",
            "range": "stddev: 1.33200488465772e-7",
            "extra": "mean: 1.0699245193365838 usec\nrounds: 96638"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 421645.05297772505,
            "unit": "iter/sec",
            "range": "stddev: 2.675728261266653e-7",
            "extra": "mean: 2.371663068113427 usec\nrounds: 48714"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 574323.9863098415,
            "unit": "iter/sec",
            "range": "stddev: 1.5945803928291e-7",
            "extra": "mean: 1.7411774953458254 usec\nrounds: 67115"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 298025.24719013384,
            "unit": "iter/sec",
            "range": "stddev: 5.624067495704207e-7",
            "extra": "mean: 3.355420419673441 usec\nrounds: 195199"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 299850.4857407218,
            "unit": "iter/sec",
            "range": "stddev: 5.374459780805252e-7",
            "extra": "mean: 3.3349954312386596 usec\nrounds: 189001"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 71478.8881641681,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017119671352774062",
            "extra": "mean: 13.99014486212019 usec\nrounds: 88850"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 35989.265894535696,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030269829891620815",
            "extra": "mean: 27.786062736884876 usec\nrounds: 42750"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 53120.652352877725,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017652110725953837",
            "extra": "mean: 18.825070019039902 usec\nrounds: 59798"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 501.2361621139493,
            "unit": "iter/sec",
            "range": "stddev: 0.00003246683372360551",
            "extra": "mean: 1.9950675461693113 msec\nrounds: 509"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 49.005398247467944,
            "unit": "iter/sec",
            "range": "stddev: 0.00013528819160154795",
            "extra": "mean: 20.40591518000099 msec\nrounds: 50"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 35128.79921513955,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018897869158827504",
            "extra": "mean: 28.466671857346817 usec\nrounds: 39879"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 333.3506158214538,
            "unit": "iter/sec",
            "range": "stddev: 0.000022317409786116657",
            "extra": "mean: 2.9998444656709764 msec\nrounds: 335"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 33.04763776841178,
            "unit": "iter/sec",
            "range": "stddev: 0.00014530838693388435",
            "extra": "mean: 30.259348852940978 msec\nrounds: 34"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 20652.575993916234,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027155694233231757",
            "extra": "mean: 48.420109931786556 usec\nrounds: 22614"
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
          "id": "47bbebbd014263e64cc395cad12b5f3420540ab7",
          "message": "feat: support dotted field paths in nf cache query filter predicates (merges PR #851, addresses #850)\n\nA filter predicate's field is now resolved as a dotted path inside each\nitem, so protocols.cifs_services[\"security.session_security=none\"]\nmatches nested values. A missing or non-dict intermediate key counts as\nno match. Top-level fields, glob values and || OR behave as before.\n\nPath parsing now splits only on dots outside brackets. Before this, the\ndot inside a predicate like [\"svm.name=svm1\"] was split off before the\npredicate was parsed.\n\nAddresses #850\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T11:31:05Z",
          "tree_id": "fd514d91dbc8ad4a4182b0682fc6111f43a083f4",
          "url": "https://github.com/endavis/pynetappfoundry/commit/47bbebbd014263e64cc395cad12b5f3420540ab7"
        },
        "date": 1793014439129,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 773243.6812662197,
            "unit": "iter/sec",
            "range": "stddev: 1.544724325360248e-7",
            "extra": "mean: 1.2932533743598875 usec\nrounds: 80756"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 480505.22788413794,
            "unit": "iter/sec",
            "range": "stddev: 1.7550992278223177e-7",
            "extra": "mean: 2.0811428096285467 usec\nrounds: 50206"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 253742.9877334345,
            "unit": "iter/sec",
            "range": "stddev: 6.006385973333957e-7",
            "extra": "mean: 3.9409956071398256 usec\nrounds: 135447"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 255261.85923048996,
            "unit": "iter/sec",
            "range": "stddev: 7.419208984222356e-7",
            "extra": "mean: 3.9175457039080994 usec\nrounds: 135612"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 311166.67176087474,
            "unit": "iter/sec",
            "range": "stddev: 5.562987750601718e-7",
            "extra": "mean: 3.21371178455924 usec\nrounds: 168322"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 97921.31364044294,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014994849295066664",
            "extra": "mean: 10.212281298348364 usec\nrounds: 105397"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 72854.58915187143,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017358417411675307",
            "extra": "mean: 13.725971303131187 usec\nrounds: 77256"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 40174.19150810126,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021160347321202994",
            "extra": "mean: 24.891602356163073 usec\nrounds: 42528"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 115771.48035048005,
            "unit": "iter/sec",
            "range": "stddev: 0.000001112173425119675",
            "extra": "mean: 8.637705909716766 usec\nrounds: 126519"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 27076.200706332696,
            "unit": "iter/sec",
            "range": "stddev: 0.000006781811932869036",
            "extra": "mean: 36.93280349211312 usec\nrounds: 29724"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 63.87280409741937,
            "unit": "iter/sec",
            "range": "stddev: 0.0011546790051210163",
            "extra": "mean: 15.656115527271842 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 64.21877738960555,
            "unit": "iter/sec",
            "range": "stddev: 0.0008440281304700763",
            "extra": "mean: 15.571769514283217 msec\nrounds: 70"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 74.20227279112108,
            "unit": "iter/sec",
            "range": "stddev: 0.0008742598755657292",
            "extra": "mean: 13.47667615000141 msec\nrounds: 80"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.608510344895432,
            "unit": "iter/sec",
            "range": "stddev: 0.000347530216402816",
            "extra": "mean: 94.26394163636526 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 295.40602530663097,
            "unit": "iter/sec",
            "range": "stddev: 0.0000372966585442364",
            "extra": "mean: 3.385171304349671 msec\nrounds: 299"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 66.11455051580894,
            "unit": "iter/sec",
            "range": "stddev: 0.0007480896184374374",
            "extra": "mean: 15.125263534248571 msec\nrounds: 73"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 2.825248012390879,
            "unit": "iter/sec",
            "range": "stddev: 0.0019494396440206947",
            "extra": "mean: 353.9512267999953 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 2.8270467219215885,
            "unit": "iter/sec",
            "range": "stddev: 0.007891265309044281",
            "extra": "mean: 353.7260251999953 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 429271.74737944145,
            "unit": "iter/sec",
            "range": "stddev: 2.674631282898605e-7",
            "extra": "mean: 2.329526706811387 usec\nrounds: 44498"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 406763.8217807878,
            "unit": "iter/sec",
            "range": "stddev: 1.987876322172664e-7",
            "extra": "mean: 2.4584290599445633 usec\nrounds: 42168"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 406149.9419895377,
            "unit": "iter/sec",
            "range": "stddev: 1.86846241163021e-7",
            "extra": "mean: 2.4621448795522904 usec\nrounds: 42008"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 159443.4239377635,
            "unit": "iter/sec",
            "range": "stddev: 9.409375422132017e-7",
            "extra": "mean: 6.271817145562153 usec\nrounds: 175101"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 192789.01934659388,
            "unit": "iter/sec",
            "range": "stddev: 6.583269435619585e-7",
            "extra": "mean: 5.187017410997934 usec\nrounds: 105508"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 451787.51886831137,
            "unit": "iter/sec",
            "range": "stddev: 2.018026750952036e-7",
            "extra": "mean: 2.21342989400175 usec\nrounds: 47170"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 464652.0495906869,
            "unit": "iter/sec",
            "range": "stddev: 2.0650433642491822e-7",
            "extra": "mean: 2.1521480447162613 usec\nrounds: 48126"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34136.62077572761,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024526635430742613",
            "extra": "mean: 29.29405363729021 usec\nrounds: 35852"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 586010.5456703804,
            "unit": "iter/sec",
            "range": "stddev: 1.507200390702693e-7",
            "extra": "mean: 1.7064539322513843 usec\nrounds: 60754"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 251011.08916116558,
            "unit": "iter/sec",
            "range": "stddev: 5.052963215032683e-7",
            "extra": "mean: 3.983887737158634 usec\nrounds: 133085"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 364957.9103657353,
            "unit": "iter/sec",
            "range": "stddev: 4.5225625611070316e-7",
            "extra": "mean: 2.7400419927817703 usec\nrounds: 196117"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 216510.3719698981,
            "unit": "iter/sec",
            "range": "stddev: 7.473200261068756e-7",
            "extra": "mean: 4.618716373269324 usec\nrounds: 114864"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 200787.79351712056,
            "unit": "iter/sec",
            "range": "stddev: 5.981628149040274e-7",
            "extra": "mean: 4.980382435024533 usec\nrounds: 106758"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 49001.630352743305,
            "unit": "iter/sec",
            "range": "stddev: 0.000002098680522124568",
            "extra": "mean: 20.407484257184844 usec\nrounds: 51611"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 24678.836517446918,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029727119932341704",
            "extra": "mean: 40.52054882299825 usec\nrounds: 25613"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 32990.550816982126,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028733210740731088",
            "extra": "mean: 30.31170972402324 usec\nrounds: 34574"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 311.2786389689217,
            "unit": "iter/sec",
            "range": "stddev: 0.000046130366566722947",
            "extra": "mean: 3.212555809522929 msec\nrounds: 315"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.113681360471844,
            "unit": "iter/sec",
            "range": "stddev: 0.00034219809428964146",
            "extra": "mean: 32.14020187500033 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 26733.431311748613,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033726122863917506",
            "extra": "mean: 37.40634669521556 usec\nrounds: 28140"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 246.52959451595856,
            "unit": "iter/sec",
            "range": "stddev: 0.0000322930318714227",
            "extra": "mean: 4.056308136000553 msec\nrounds: 250"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 24.386649429273753,
            "unit": "iter/sec",
            "range": "stddev: 0.0007787406083282805",
            "extra": "mean: 41.00604319999775 msec\nrounds: 25"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13885.006529236707,
            "unit": "iter/sec",
            "range": "stddev: 0.000005991757388737376",
            "extra": "mean: 72.02013177987122 usec\nrounds: 14638"
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
          "id": "5fd2b187923f647582671f548ab3bf5e74db5cc4",
          "message": "chore: sync with pyproject-template 72dd3cd, phase C: root-level tests (merges PR #854, addresses #828)\n\nFinishes the 36bcb77 -> 72dd3cd template sync and records 72dd3cd as the\nsync point.\n\nsync-exclude.toml now names each root-level test it skips instead of\nexcluding tests/test_*.py, so new upstream tests appear in the drift\nreport. Still skipped: the example-app tests, test_benchmark_settings\n(needs the example benchmark), the mutmut tests (#830),\ntest_python_versions_agree (#852), test_documented_paths (#853) and the\nCBM and context-mode hook tests (#717, #718).\n\nAdopted 16 template tests. Five of them caught project drift, fixed here:\n- test_ci_jobs_doc: the CI doc's test row now names install_tools.\n- test_workflow_action_pinning: SHA-pinned the action samples in\n  production.md and compliance-checks.md.\n- test_docs_frontmatter: added frontmatter to ADRs 0001-0019, the ADR\n  index and the three plans, and regenerated TABLE_OF_CONTENTS.md.\n- test_markdown_links: pointed README's four template doc links at the\n  project's pages.\n- test_docs_dev_sync: development.md now syncs with --all-extras --dev.\n  RUNTIME_SYNCS diverges from upstream: it drops the entry for the\n  template's docs/examples/api.md and allows the compliance CI sample.\n\nAddresses #828\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T12:03:38Z",
          "tree_id": "737e69d7a2cc84b3c04ac8420f8ac54079f47c13",
          "url": "https://github.com/endavis/pynetappfoundry/commit/5fd2b187923f647582671f548ab3bf5e74db5cc4"
        },
        "date": 1793016393912,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 765120.8279079791,
            "unit": "iter/sec",
            "range": "stddev: 1.3211163550177113e-7",
            "extra": "mean: 1.3069831110652628 usec\nrounds: 78809"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 496397.7104295685,
            "unit": "iter/sec",
            "range": "stddev: 3.745855863852374e-7",
            "extra": "mean: 2.014513723551683 usec\nrounds: 52552"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 247880.89099643615,
            "unit": "iter/sec",
            "range": "stddev: 5.443534083922174e-7",
            "extra": "mean: 4.034195600879849 usec\nrounds: 129685"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 247427.08748706523,
            "unit": "iter/sec",
            "range": "stddev: 6.73838080998463e-7",
            "extra": "mean: 4.041594678077748 usec\nrounds: 129333"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 313773.2014724207,
            "unit": "iter/sec",
            "range": "stddev: 4.4376031634123467e-7",
            "extra": "mean: 3.187015319687509 usec\nrounds: 165865"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 101271.49820441112,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012018522239434472",
            "extra": "mean: 9.874446588926268 usec\nrounds: 103574"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 71385.31161575946,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012539373064268514",
            "extra": "mean: 14.008484061575965 usec\nrounds: 74129"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 39092.97094086371,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019099389117980443",
            "extra": "mean: 25.580046129333812 usec\nrounds: 40755"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 119042.29118315432,
            "unit": "iter/sec",
            "range": "stddev: 9.959917917296116e-7",
            "extra": "mean: 8.400375950941962 usec\nrounds: 127373"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32250.37258001929,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020004377779854797",
            "extra": "mean: 31.007393713632617 usec\nrounds: 32610"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 64.35877186349138,
            "unit": "iter/sec",
            "range": "stddev: 0.0015213970512132171",
            "extra": "mean: 15.537897493150691 msec\nrounds: 73"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 65.26785781995993,
            "unit": "iter/sec",
            "range": "stddev: 0.0012554397238668264",
            "extra": "mean: 15.321477269232275 msec\nrounds: 78"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 67.15896203010617,
            "unit": "iter/sec",
            "range": "stddev: 0.0010589638481840235",
            "extra": "mean: 14.890045494623902 msec\nrounds: 93"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 11.909743332139033,
            "unit": "iter/sec",
            "range": "stddev: 0.0006684751908938081",
            "extra": "mean: 83.96486574999902 msec\nrounds: 12"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 311.6150576390685,
            "unit": "iter/sec",
            "range": "stddev: 0.000043597620601705425",
            "extra": "mean: 3.209087544024464 msec\nrounds: 318"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 69.35291190254931,
            "unit": "iter/sec",
            "range": "stddev: 0.0016902734403324404",
            "extra": "mean: 14.419005238095007 msec\nrounds: 84"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 2.8773879267603184,
            "unit": "iter/sec",
            "range": "stddev: 0.0017751824945151167",
            "extra": "mean: 347.53742819999616 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 2.9425878032050745,
            "unit": "iter/sec",
            "range": "stddev: 0.0008846818500765175",
            "extra": "mean: 339.83692820000044 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 407377.4156920865,
            "unit": "iter/sec",
            "range": "stddev: 1.7302213086989322e-7",
            "extra": "mean: 2.4547261617365734 usec\nrounds: 42329"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 375730.60136536165,
            "unit": "iter/sec",
            "range": "stddev: 3.899440140396443e-7",
            "extra": "mean: 2.6614813815167446 usec\nrounds: 196928"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 366776.20063008205,
            "unit": "iter/sec",
            "range": "stddev: 4.183298447055702e-7",
            "extra": "mean: 2.726458255148801 usec\nrounds: 192419"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 158392.23127052904,
            "unit": "iter/sec",
            "range": "stddev: 8.370863683337555e-7",
            "extra": "mean: 6.313440955901625 usec\nrounds: 166418"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 193511.25660677755,
            "unit": "iter/sec",
            "range": "stddev: 5.275578144562727e-7",
            "extra": "mean: 5.167658034653969 usec\nrounds: 102313"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 453152.09631533636,
            "unit": "iter/sec",
            "range": "stddev: 1.7565708318273005e-7",
            "extra": "mean: 2.2067645899272788 usec\nrounds: 47077"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 465634.85534576536,
            "unit": "iter/sec",
            "range": "stddev: 1.695001851214184e-7",
            "extra": "mean: 2.1476055508289478 usec\nrounds: 48191"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34082.82250093158,
            "unit": "iter/sec",
            "range": "stddev: 0.000005907164286352552",
            "extra": "mean: 29.340293045643946 usec\nrounds: 35892"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 592074.8962548266,
            "unit": "iter/sec",
            "range": "stddev: 1.4821992603370782e-7",
            "extra": "mean: 1.688975510236131 usec\nrounds: 61981"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 268406.9433297416,
            "unit": "iter/sec",
            "range": "stddev: 4.5417793531021606e-7",
            "extra": "mean: 3.7256860332837456 usec\nrounds: 140233"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 368178.9437933141,
            "unit": "iter/sec",
            "range": "stddev: 3.900096623707889e-7",
            "extra": "mean: 2.716070587027849 usec\nrounds: 196580"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 226135.83812788152,
            "unit": "iter/sec",
            "range": "stddev: 5.119865151828938e-7",
            "extra": "mean: 4.422120829138513 usec\nrounds: 120149"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 212500.03104052457,
            "unit": "iter/sec",
            "range": "stddev: 5.287211465349033e-7",
            "extra": "mean: 4.705881665538657 usec\nrounds: 111075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52331.639586235964,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015457458678036123",
            "extra": "mean: 19.108898706529647 usec\nrounds: 54505"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26439.396295325027,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036229462019388287",
            "extra": "mean: 37.822346199970475 usec\nrounds: 27591"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 34607.25129918209,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020745254288277046",
            "extra": "mean: 28.89567828877626 usec\nrounds: 35880"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 318.3302035091641,
            "unit": "iter/sec",
            "range": "stddev: 0.0003085893434690556",
            "extra": "mean: 3.1413921424242486 msec\nrounds: 330"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.342819365018535,
            "unit": "iter/sec",
            "range": "stddev: 0.00017061281489704348",
            "extra": "mean: 32.956726531248925 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 28158.30967358984,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021620135257036015",
            "extra": "mean: 35.51349536218493 usec\nrounds: 29324"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 256.0996404291099,
            "unit": "iter/sec",
            "range": "stddev: 0.00012611577511853798",
            "extra": "mean: 3.9047301992476116 msec\nrounds: 266"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 22.490832062124323,
            "unit": "iter/sec",
            "range": "stddev: 0.0002708381194750293",
            "extra": "mean: 44.46256133333767 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 15436.056054919656,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035458109472983407",
            "extra": "mean: 64.7833874431473 usec\nrounds: 16023"
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
          "id": "47ef3016ae39ba39e1d7a3a46401ca28978745b7",
          "message": "chore: harden doit console_models_check and run it in CI (merges PR #855, addresses #825)\n\n- Pin datamodel-codegen's formatters to black and isort, its current\n  default, before a release switches the default to builtin.\n- Clear src/pynetappfoundry/models/console/ before regenerating, so a\n  module the generator stops producing shows up as a deletion.\n- Replace git diff --exit-code with git status --porcelain\n  --untracked-files=all, so a new untracked module also fails the check.\n- Move the hand-authored Console types out of the generated tree, from\n  models/console/types.py to models/console_types.py. Clearing the tree\n  deleted them.\n- Add a console-models job to ci.yml and to ci-complete. It is separate\n  from lint because lint runs exactly the tasks in doit check.\n\nADR-0008 and the CI jobs table in ci-cd-testing.md describe the new check.\n\nAddresses #825\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T12:23:17Z",
          "tree_id": "03c75651e21da11679a165085a2ab1adb936c932",
          "url": "https://github.com/endavis/pynetappfoundry/commit/47ef3016ae39ba39e1d7a3a46401ca28978745b7"
        },
        "date": 1793017571262,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 761245.616485692,
            "unit": "iter/sec",
            "range": "stddev: 2.592652868708454e-7",
            "extra": "mean: 1.3136364641632003 usec\nrounds: 81480"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 479782.14201700594,
            "unit": "iter/sec",
            "range": "stddev: 2.398742740429683e-7",
            "extra": "mean: 2.084279326854468 usec\nrounds: 50539"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 253132.1264809477,
            "unit": "iter/sec",
            "range": "stddev: 5.951635785047154e-7",
            "extra": "mean: 3.9505060614076823 usec\nrounds: 135612"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 253789.60354900843,
            "unit": "iter/sec",
            "range": "stddev: 5.410434778872394e-7",
            "extra": "mean: 3.940271729085598 usec\nrounds: 135245"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 309030.27646594227,
            "unit": "iter/sec",
            "range": "stddev: 5.306000421772958e-7",
            "extra": "mean: 3.2359288916152797 usec\nrounds: 167758"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 97119.9693700968,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013442750797147282",
            "extra": "mean: 10.296543609783093 usec\nrounds: 104965"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 72467.8614637398,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015341306124315948",
            "extra": "mean: 13.799220506877555 usec\nrounds: 77018"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 39849.96395679382,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019262766219680052",
            "extra": "mean: 25.094125582753882 usec\nrounds: 42044"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 114120.04543594152,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014254486599403353",
            "extra": "mean: 8.762702434791139 usec\nrounds: 123993"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 28745.52422777581,
            "unit": "iter/sec",
            "range": "stddev: 0.000003004481148031606",
            "extra": "mean: 34.78802446169113 usec\nrounds: 30047"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 50.55719945098323,
            "unit": "iter/sec",
            "range": "stddev: 0.00016785676266061782",
            "extra": "mean: 19.779576615384542 msec\nrounds: 52"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 48.566105125011475,
            "unit": "iter/sec",
            "range": "stddev: 0.0009631230199955728",
            "extra": "mean: 20.590492019608167 msec\nrounds: 51"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 55.34038329946098,
            "unit": "iter/sec",
            "range": "stddev: 0.00020987601999079554",
            "extra": "mean: 18.06998687719136 msec\nrounds: 57"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.163901533056995,
            "unit": "iter/sec",
            "range": "stddev: 0.00032517566668477203",
            "extra": "mean: 98.38741518181848 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 284.3765047966446,
            "unit": "iter/sec",
            "range": "stddev: 0.00005988549503069041",
            "extra": "mean: 3.5164649087838393 msec\nrounds: 296"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 48.94981253368806,
            "unit": "iter/sec",
            "range": "stddev: 0.0011688131017698383",
            "extra": "mean: 20.42908743137236 msec\nrounds: 51"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 2.758757271351738,
            "unit": "iter/sec",
            "range": "stddev: 0.0028677059185874187",
            "extra": "mean: 362.48205319999727 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 2.8373900018377514,
            "unit": "iter/sec",
            "range": "stddev: 0.0010952168399498959",
            "extra": "mean: 352.43657000000326 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 418435.29217785195,
            "unit": "iter/sec",
            "range": "stddev: 2.5256495889655035e-7",
            "extra": "mean: 2.3898557762545507 usec\nrounds: 43246"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 395412.4236464211,
            "unit": "iter/sec",
            "range": "stddev: 3.596199798993871e-7",
            "extra": "mean: 2.529005008942771 usec\nrounds: 41366"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 397980.8644945068,
            "unit": "iter/sec",
            "range": "stddev: 2.3179864967407487e-7",
            "extra": "mean: 2.512683621787054 usec\nrounds: 41195"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 156234.820734116,
            "unit": "iter/sec",
            "range": "stddev: 0.000001077549347690538",
            "extra": "mean: 6.400621803137105 usec\nrounds: 170911"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 187039.56668429868,
            "unit": "iter/sec",
            "range": "stddev: 7.755894663572155e-7",
            "extra": "mean: 5.346462343381522 usec\nrounds: 100726"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 438798.8838675066,
            "unit": "iter/sec",
            "range": "stddev: 2.1105064464839102e-7",
            "extra": "mean: 2.2789483673845115 usec\nrounds: 45663"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 451145.0308824102,
            "unit": "iter/sec",
            "range": "stddev: 2.0267250676789552e-7",
            "extra": "mean: 2.2165821000933237 usec\nrounds: 47017"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 33236.479515247454,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028273366992850243",
            "extra": "mean: 30.087422452225823 usec\nrounds: 34598"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 585904.3586944679,
            "unit": "iter/sec",
            "range": "stddev: 1.5971113953587224e-7",
            "extra": "mean: 1.7067632031757436 usec\nrounds: 60902"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 249376.0382268298,
            "unit": "iter/sec",
            "range": "stddev: 5.866108386797689e-7",
            "extra": "mean: 4.010008367726215 usec\nrounds: 131338"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 364311.4082581047,
            "unit": "iter/sec",
            "range": "stddev: 4.50447721268954e-7",
            "extra": "mean: 2.744904434317158 usec\nrounds: 192679"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 216825.2547104118,
            "unit": "iter/sec",
            "range": "stddev: 6.18252895141897e-7",
            "extra": "mean: 4.612008879388074 usec\nrounds: 115661"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 199640.69664728403,
            "unit": "iter/sec",
            "range": "stddev: 7.109459121555e-7",
            "extra": "mean: 5.008998750223527 usec\nrounds: 105619"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 49149.45054455285,
            "unit": "iter/sec",
            "range": "stddev: 0.000003157515928437583",
            "extra": "mean: 20.346107411587905 usec\nrounds: 51959"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 24893.427102756323,
            "unit": "iter/sec",
            "range": "stddev: 0.000003929273742143721",
            "extra": "mean: 40.171246645636636 usec\nrounds: 25713"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 32823.61692687125,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032885600566555587",
            "extra": "mean: 30.46586859174999 usec\nrounds: 34526"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 310.8580745934864,
            "unit": "iter/sec",
            "range": "stddev: 0.0000988411015579576",
            "extra": "mean: 3.216902122641384 msec\nrounds: 318"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 28.557433909501125,
            "unit": "iter/sec",
            "range": "stddev: 0.0001523128057414383",
            "extra": "mean: 35.01715186206901 msec\nrounds: 29"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 26877.567704834004,
            "unit": "iter/sec",
            "range": "stddev: 0.000003582035625571513",
            "extra": "mean: 37.205747595238954 usec\nrounds: 28173"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 243.58407550008707,
            "unit": "iter/sec",
            "range": "stddev: 0.0000668720008809477",
            "extra": "mean: 4.105358685484522 msec\nrounds: 248"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 22.376681297001745,
            "unit": "iter/sec",
            "range": "stddev: 0.00020503722173138698",
            "extra": "mean: 44.68937939130367 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 14066.86855164552,
            "unit": "iter/sec",
            "range": "stddev: 0.000006423307990038351",
            "extra": "mean: 71.08902712274379 usec\nrounds: 14969"
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
          "id": "5d9072ef78dc659aa0e2c5273f7760df84490a62",
          "message": "chore: widen doit type_check to tools/ and tests/ (merges PR #856, addresses #829)\n\ndoit type_check and the pre-commit mypy hook now check src/ tools/\ntests/, the template's scope, instead of src/ tools/doit/.\n\nWidening the scope surfaced 315 errors in 48 files, all fixed with no\nper-module ignore_errors overrides:\n- Annotations on test functions and fixtures, plus cast() where a test\n  knows the concrete model type.\n- mypy_path = \"tests\", so the bare `from agent_roster import` resolves.\n  tests/agent_roster.py is excluded from the file walk, so mypy sees it\n  under one module name only.\n- tools/console_openapi/parser/types.py: renamed a lookup that two\n  branches shared, which had made mypy call a real fallback unreachable.\n  The guard stays.\n- SQLiteDB.__enter__ returns Self, so subclass methods type-check inside\n  a `with` block.\n- Removed 8 stale type: ignore comments and corrected 2 error codes.\n- Removed the two #829 skip markers in tests/template/test_doit_quality.py.\n\nAddresses #829\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T12:58:18Z",
          "tree_id": "166793f4efe73c8bedc0e046d449a7c068a08da9",
          "url": "https://github.com/endavis/pynetappfoundry/commit/5d9072ef78dc659aa0e2c5273f7760df84490a62"
        },
        "date": 1793019675542,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 750138.7576889048,
            "unit": "iter/sec",
            "range": "stddev: 2.643683526279638e-7",
            "extra": "mean: 1.3330866986274517 usec\nrounds: 81954"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 474180.76641767746,
            "unit": "iter/sec",
            "range": "stddev: 1.9002800190785652e-7",
            "extra": "mean: 2.108900383190911 usec\nrounds: 50106"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 253042.9795255328,
            "unit": "iter/sec",
            "range": "stddev: 5.130475868823308e-7",
            "extra": "mean: 3.951897823346239 usec\nrounds: 136538"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 231777.60477370193,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012937512395888353",
            "extra": "mean: 4.3144806892639975 usec\nrounds: 134899"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 306621.2252052237,
            "unit": "iter/sec",
            "range": "stddev: 5.368134146591762e-7",
            "extra": "mean: 3.261352828169977 usec\nrounds: 168891"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 96776.02180793074,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013880148089569003",
            "extra": "mean: 10.333138119530046 usec\nrounds: 104844"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 72327.10697428936,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014454507207222111",
            "extra": "mean: 13.826074923133277 usec\nrounds: 78040"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 40176.021142958816,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018756828927485112",
            "extra": "mean: 24.890468780910087 usec\nrounds: 42474"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 113583.93886823907,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011476201654590353",
            "extra": "mean: 8.804061647835892 usec\nrounds: 124611"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 28681.212671508187,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027204210261846143",
            "extra": "mean: 34.866029252431034 usec\nrounds: 29912"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 51.65668587749873,
            "unit": "iter/sec",
            "range": "stddev: 0.0002387385798808281",
            "extra": "mean: 19.358578333334247 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 50.66390250277815,
            "unit": "iter/sec",
            "range": "stddev: 0.00022706239497801578",
            "extra": "mean: 19.737918924527477 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 56.17090640717075,
            "unit": "iter/sec",
            "range": "stddev: 0.00019030932815616115",
            "extra": "mean: 17.80281045762759 msec\nrounds: 59"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.403476890400034,
            "unit": "iter/sec",
            "range": "stddev: 0.0009064670125671087",
            "extra": "mean: 96.12171109091089 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 293.28652364941445,
            "unit": "iter/sec",
            "range": "stddev: 0.00004431334385000252",
            "extra": "mean: 3.409635013422467 msec\nrounds: 298"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 49.93386442108777,
            "unit": "iter/sec",
            "range": "stddev: 0.00028963251148829774",
            "extra": "mean: 20.026489269228 msec\nrounds: 52"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 2.790027626574554,
            "unit": "iter/sec",
            "range": "stddev: 0.0016047796423251564",
            "extra": "mean: 358.41939000000025 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 2.8697657167922106,
            "unit": "iter/sec",
            "range": "stddev: 0.0011870354661714258",
            "extra": "mean: 348.46050120000314 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 416753.4967489201,
            "unit": "iter/sec",
            "range": "stddev: 2.0305084779304824e-7",
            "extra": "mean: 2.399499962930044 usec\nrounds: 43154"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 391556.61047015846,
            "unit": "iter/sec",
            "range": "stddev: 2.1911547182550182e-7",
            "extra": "mean: 2.5539091238920935 usec\nrounds: 40509"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 390877.68634182133,
            "unit": "iter/sec",
            "range": "stddev: 2.230728310459568e-7",
            "extra": "mean: 2.5583450653294726 usec\nrounds: 40641"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 153960.78042014875,
            "unit": "iter/sec",
            "range": "stddev: 9.879317018561413e-7",
            "extra": "mean: 6.495160632929155 usec\nrounds: 171204"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 185773.3545137831,
            "unit": "iter/sec",
            "range": "stddev: 6.71245740593239e-7",
            "extra": "mean: 5.3829032835051 usec\nrounds: 100624"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 434375.4170025684,
            "unit": "iter/sec",
            "range": "stddev: 2.1409094520883364e-7",
            "extra": "mean: 2.3021560632978613 usec\nrounds: 44860"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 447668.74287755723,
            "unit": "iter/sec",
            "range": "stddev: 2.0362305339799588e-7",
            "extra": "mean: 2.2337945543665354 usec\nrounds: 46147"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 32620.673600145954,
            "unit": "iter/sec",
            "range": "stddev: 0.000002832402466535559",
            "extra": "mean: 30.655406208274183 usec\nrounds: 34406"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 573992.8644406035,
            "unit": "iter/sec",
            "range": "stddev: 1.645897187444636e-7",
            "extra": "mean: 1.7421819363112998 usec\nrounds: 59877"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 241035.29806670727,
            "unit": "iter/sec",
            "range": "stddev: 5.518195191170767e-7",
            "extra": "mean: 4.148769943741795 usec\nrounds: 127960"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 368685.46629915666,
            "unit": "iter/sec",
            "range": "stddev: 3.522933753232638e-7",
            "extra": "mean: 2.7123390841465547 usec\nrounds: 132909"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 214022.37852679202,
            "unit": "iter/sec",
            "range": "stddev: 6.141319067596373e-7",
            "extra": "mean: 4.672408590556883 usec\nrounds: 114195"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 194755.48077900766,
            "unit": "iter/sec",
            "range": "stddev: 6.600377775027687e-7",
            "extra": "mean: 5.134643687561825 usec\nrounds: 104080"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 48841.613305178806,
            "unit": "iter/sec",
            "range": "stddev: 0.000002026451794554797",
            "extra": "mean: 20.474344157136336 usec\nrounds: 51584"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25034.671812963366,
            "unit": "iter/sec",
            "range": "stddev: 0.000003324183531660417",
            "extra": "mean: 39.94460192932041 usec\nrounds: 25812"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 32422.40972850161,
            "unit": "iter/sec",
            "range": "stddev: 0.000006570665786029703",
            "extra": "mean: 30.842864807822373 usec\nrounds: 34610"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 312.70481392210723,
            "unit": "iter/sec",
            "range": "stddev: 0.00003673182840055732",
            "extra": "mean: 3.1979040791137088 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 28.871805362522455,
            "unit": "iter/sec",
            "range": "stddev: 0.00012231525055287547",
            "extra": "mean: 34.63586663333729 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 26812.835744236927,
            "unit": "iter/sec",
            "range": "stddev: 0.000003823768414354787",
            "extra": "mean: 37.29557028353247 usec\nrounds: 27944"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 246.47737371966014,
            "unit": "iter/sec",
            "range": "stddev: 0.000041562315763540755",
            "extra": "mean: 4.0571675400005915 msec\nrounds: 250"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 22.61387451499751,
            "unit": "iter/sec",
            "range": "stddev: 0.00024975230512414264",
            "extra": "mean: 44.22063982608555 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13976.304510320508,
            "unit": "iter/sec",
            "range": "stddev: 0.000006156347546080611",
            "extra": "mean: 71.54967175060982 usec\nrounds: 14818"
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
          "id": "9b053445f758115b8b93ae8495f6d6b0e8e2b290",
          "message": "docs: add missing pages to the mkdocs nav and enforce omitted_files (merges PR #857, addresses #831)\n\nAdds the 21 pages that were missing from the nav:\n- ADR-0005 through ADR-0020\n- development/cache-models.md\n- reference/config-schema.md\n- the three plans, in a new Development > Plans section\n\nvalidation.nav.omitted_files is now warn, matching the template, so\n`mkdocs build --strict` fails when a page is missing from the nav.\nAlso drops a comment in mkdocs.yml that still said test_markdown_links\narrives with #828, which has merged.\n\nAddresses #831\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T13:09:01Z",
          "tree_id": "4b4ed393442a9d8c95782e987050efaa276a8311",
          "url": "https://github.com/endavis/pynetappfoundry/commit/9b053445f758115b8b93ae8495f6d6b0e8e2b290"
        },
        "date": 1793020298746,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1274698.2734412388,
            "unit": "iter/sec",
            "range": "stddev: 7.055254717158155e-8",
            "extra": "mean: 784.4993759192521 nsec\nrounds: 133316"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 788675.5292221652,
            "unit": "iter/sec",
            "range": "stddev: 9.480089070788516e-8",
            "extra": "mean: 1.267948557990958 usec\nrounds: 82454"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 432261.6492348277,
            "unit": "iter/sec",
            "range": "stddev: 1.5695031972705402e-7",
            "extra": "mean: 2.313413650667738 usec\nrounds: 44496"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 437447.6920226102,
            "unit": "iter/sec",
            "range": "stddev: 1.9864483852670019e-7",
            "extra": "mean: 2.285987600886264 usec\nrounds: 44979"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 505937.45693385176,
            "unit": "iter/sec",
            "range": "stddev: 1.2945266087641022e-7",
            "extra": "mean: 1.9765288896780453 usec\nrounds: 52832"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 157939.90990185007,
            "unit": "iter/sec",
            "range": "stddev: 9.965262369247537e-7",
            "extra": "mean: 6.331521909955745 usec\nrounds: 169809"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 118435.30838544307,
            "unit": "iter/sec",
            "range": "stddev: 8.753565297475234e-7",
            "extra": "mean: 8.44342800835659 usec\nrounds: 124813"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 63610.84752585155,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035438559324925605",
            "extra": "mean: 15.72058915884745 usec\nrounds: 68720"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 188129.59415745863,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021978655404701898",
            "extra": "mean: 5.315484809705331 usec\nrounds: 102302"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 55585.01401565712,
            "unit": "iter/sec",
            "range": "stddev: 0.000006620882935494919",
            "extra": "mean: 17.99046051725958 usec\nrounds: 59507"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 77.97252575677551,
            "unit": "iter/sec",
            "range": "stddev: 0.001115191865839044",
            "extra": "mean: 12.825030230768224 msec\nrounds: 91"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 77.03127426085989,
            "unit": "iter/sec",
            "range": "stddev: 0.0011219765756364222",
            "extra": "mean: 12.981740333329872 msec\nrounds: 84"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 87.83692222260268,
            "unit": "iter/sec",
            "range": "stddev: 0.0013742708368763637",
            "extra": "mean: 11.384734058255454 msec\nrounds: 103"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 14.344621807166163,
            "unit": "iter/sec",
            "range": "stddev: 0.0032672636621629706",
            "extra": "mean: 69.71253849999925 msec\nrounds: 16"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 528.7662693733722,
            "unit": "iter/sec",
            "range": "stddev: 0.00005825595643107256",
            "extra": "mean: 1.8911947639645683 msec\nrounds: 555"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 71.82046128828819,
            "unit": "iter/sec",
            "range": "stddev: 0.0008256191604091793",
            "extra": "mean: 13.923608705129142 msec\nrounds: 78"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 4.557752866747582,
            "unit": "iter/sec",
            "range": "stddev: 0.0035854553528416326",
            "extra": "mean: 219.4063673999949 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 4.839469984692886,
            "unit": "iter/sec",
            "range": "stddev: 0.002019550292432395",
            "extra": "mean: 206.634198200004 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 731938.1985397151,
            "unit": "iter/sec",
            "range": "stddev: 1.0430944685151067e-7",
            "extra": "mean: 1.3662355674223494 usec\nrounds: 72617"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 634343.5449283259,
            "unit": "iter/sec",
            "range": "stddev: 8.239450802809814e-7",
            "extra": "mean: 1.5764328462000656 usec\nrounds: 70617"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 656048.0235112463,
            "unit": "iter/sec",
            "range": "stddev: 8.82299539665061e-8",
            "extra": "mean: 1.524278656687177 usec\nrounds: 69872"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 299367.3359966275,
            "unit": "iter/sec",
            "range": "stddev: 8.476607168925516e-7",
            "extra": "mean: 3.340377789283148 usec\nrounds: 162629"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 352792.9533003836,
            "unit": "iter/sec",
            "range": "stddev: 3.277510541693075e-7",
            "extra": "mean: 2.834523735933455 usec\nrounds: 186637"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 755482.5535558636,
            "unit": "iter/sec",
            "range": "stddev: 8.434890479270136e-8",
            "extra": "mean: 1.3236573039221824 usec\nrounds: 77520"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 750985.4046035263,
            "unit": "iter/sec",
            "range": "stddev: 5.007246601211849e-7",
            "extra": "mean: 1.3315838015892438 usec\nrounds: 77520"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 56375.0376317306,
            "unit": "iter/sec",
            "range": "stddev: 0.000007893694633666179",
            "extra": "mean: 17.738347360980768 usec\nrounds: 61331"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 1065283.8999748945,
            "unit": "iter/sec",
            "range": "stddev: 2.5179505040012233e-7",
            "extra": "mean: 938.7168998081798 nsec\nrounds: 105877"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 470969.9896082566,
            "unit": "iter/sec",
            "range": "stddev: 1.7363119900194456e-7",
            "extra": "mean: 2.12327753798449 usec\nrounds: 49951"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 643893.9934333825,
            "unit": "iter/sec",
            "range": "stddev: 1.2960692503259496e-7",
            "extra": "mean: 1.553050673244804 usec\nrounds: 67286"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 369791.6718841699,
            "unit": "iter/sec",
            "range": "stddev: 0.000001087110718213567",
            "extra": "mean: 2.7042253139579375 usec\nrounds: 136781"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 364599.7942769584,
            "unit": "iter/sec",
            "range": "stddev: 3.288413612797428e-7",
            "extra": "mean: 2.74273330840219 usec\nrounds: 195008"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 87103.92838134803,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033242820618996694",
            "extra": "mean: 11.480538462305848 usec\nrounds: 94287"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 45169.7370237552,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014379456769412242",
            "extra": "mean: 22.138716448007884 usec\nrounds: 47367"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 60573.807747891915,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010968268009873355",
            "extra": "mean: 16.50878551604347 usec\nrounds: 65907"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 580.2996966355821,
            "unit": "iter/sec",
            "range": "stddev: 0.00015661291345068704",
            "extra": "mean: 1.7232474974529965 msec\nrounds: 589"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 48.59750480971157,
            "unit": "iter/sec",
            "range": "stddev: 0.0003772192766846858",
            "extra": "mean: 20.577188148148775 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 48448.307134598304,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012379596660690589",
            "extra": "mean: 20.64055607189362 usec\nrounds: 52718"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 451.3963115888276,
            "unit": "iter/sec",
            "range": "stddev: 0.00003920741622129229",
            "extra": "mean: 2.215348185899423 msec\nrounds: 468"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 34.2810079147085,
            "unit": "iter/sec",
            "range": "stddev: 0.0031363793798834883",
            "extra": "mean: 29.1706708999925 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 26900.463961799604,
            "unit": "iter/sec",
            "range": "stddev: 0.000004512525787621008",
            "extra": "mean: 37.174080024049566 usec\nrounds: 28254"
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
          "id": "306e9dd54e7fc0875859878e2bbad114b1009560",
          "message": "docs: replace the template placeholders left in README.md (merges PR #858, addresses #842)\n\nRewrite the title, description, badges, Installation and Quick Start\nfor pynetappfoundry's nf CLI and library. Remove the template-only\n\"Quick Setup (Automated)\", \"Using This Template (Manual)\" and\n\"Migrating an Existing Project\" sections, point clone URLs at\nendavis/pynetappfoundry, fix the stale test path, and replace the\ngeneric fork-based Contributing steps with a link to CONTRIBUTING.md.\n\nAddresses #842\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T13:43:03Z",
          "tree_id": "29949b8757061d4cbdf4ae53baddf8908b36a911",
          "url": "https://github.com/endavis/pynetappfoundry/commit/306e9dd54e7fc0875859878e2bbad114b1009560"
        },
        "date": 1793022342309,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1018663.8342443105,
            "unit": "iter/sec",
            "range": "stddev: 9.21054166873571e-8",
            "extra": "mean: 981.6781222451505 nsec\nrounds: 105541"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 616881.0748227168,
            "unit": "iter/sec",
            "range": "stddev: 1.2900100809237866e-7",
            "extra": "mean: 1.6210579977467885 usec\nrounds: 63968"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 327925.47866060486,
            "unit": "iter/sec",
            "range": "stddev: 4.2817784154659943e-7",
            "extra": "mean: 3.049473325721593 usec\nrounds: 170970"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 327912.5921137093,
            "unit": "iter/sec",
            "range": "stddev: 3.5837897658441155e-7",
            "extra": "mean: 3.049593166136276 usec\nrounds: 170416"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 410788.09903224156,
            "unit": "iter/sec",
            "range": "stddev: 1.572289221877711e-7",
            "extra": "mean: 2.4343451096948963 usec\nrounds: 42891"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 125988.2802710613,
            "unit": "iter/sec",
            "range": "stddev: 9.503273881674101e-7",
            "extra": "mean: 7.9372462093181975 usec\nrounds: 134211"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 91618.02528557232,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013867529595844584",
            "extra": "mean: 10.914882708757492 usec\nrounds: 95557"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 51794.799512407524,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024688232866392777",
            "extra": "mean: 19.306957636942844 usec\nrounds: 54505"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 147775.86810718567,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010433335086800595",
            "extra": "mean: 6.767004740413191 usec\nrounds: 158003"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 39438.57097839654,
            "unit": "iter/sec",
            "range": "stddev: 0.00000178185338530175",
            "extra": "mean: 25.355888288847357 usec\nrounds: 41849"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 69.49042968411646,
            "unit": "iter/sec",
            "range": "stddev: 0.0002728031139692124",
            "extra": "mean: 14.390470810811111 msec\nrounds: 74"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 65.29383357740038,
            "unit": "iter/sec",
            "range": "stddev: 0.00028696100217364247",
            "extra": "mean: 15.31538194666704 msec\nrounds: 75"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 77.03426575345388,
            "unit": "iter/sec",
            "range": "stddev: 0.0003153960556162922",
            "extra": "mean: 12.981236209876698 msec\nrounds: 81"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 13.526399863981414,
            "unit": "iter/sec",
            "range": "stddev: 0.0010117313904122354",
            "extra": "mean: 73.92950157142967 msec\nrounds: 14"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 402.57892447041843,
            "unit": "iter/sec",
            "range": "stddev: 0.0000799061351343692",
            "extra": "mean: 2.4839849759037254 msec\nrounds: 415"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 68.74898596509169,
            "unit": "iter/sec",
            "range": "stddev: 0.0009028962031324507",
            "extra": "mean: 14.54566908823593 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 3.477696752072694,
            "unit": "iter/sec",
            "range": "stddev: 0.001627152689855803",
            "extra": "mean: 287.54663539999683 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 3.609344201172672,
            "unit": "iter/sec",
            "range": "stddev: 0.0021597638344537226",
            "extra": "mean: 277.0586412 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 536009.3704012206,
            "unit": "iter/sec",
            "range": "stddev: 1.4636046527789575e-7",
            "extra": "mean: 1.8656390265182623 usec\nrounds: 56190"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 492885.17746502085,
            "unit": "iter/sec",
            "range": "stddev: 1.3933027514021917e-7",
            "extra": "mean: 2.0288701014364916 usec\nrounds: 52250"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 509939.34945041535,
            "unit": "iter/sec",
            "range": "stddev: 1.1854576870942527e-7",
            "extra": "mean: 1.961017523118671 usec\nrounds: 52913"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 218492.6426461695,
            "unit": "iter/sec",
            "range": "stddev: 3.966044800373177e-7",
            "extra": "mean: 4.576813149811255 usec\nrounds: 115036"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 255351.56736833166,
            "unit": "iter/sec",
            "range": "stddev: 4.2930833339063493e-7",
            "extra": "mean: 3.916169422048429 usec\nrounds: 136036"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 558987.0683653398,
            "unit": "iter/sec",
            "range": "stddev: 1.2321645727561422e-7",
            "extra": "mean: 1.78895015035737 usec\nrounds: 58528"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 575651.8769861549,
            "unit": "iter/sec",
            "range": "stddev: 1.1666253003316735e-7",
            "extra": "mean: 1.7371610168901634 usec\nrounds: 59613"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 44578.94492226016,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014998931146503225",
            "extra": "mean: 22.432114572111765 usec\nrounds: 46486"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 746436.3618947775,
            "unit": "iter/sec",
            "range": "stddev: 1.0529082807663266e-7",
            "extra": "mean: 1.3396989362382732 usec\nrounds: 79435"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 340559.2496252535,
            "unit": "iter/sec",
            "range": "stddev: 3.1571723224672814e-7",
            "extra": "mean: 2.936346615457914 usec\nrounds: 178636"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 483803.86250359495,
            "unit": "iter/sec",
            "range": "stddev: 1.4362874263092066e-7",
            "extra": "mean: 2.066953320350082 usec\nrounds: 49799"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 287236.444594757,
            "unit": "iter/sec",
            "range": "stddev: 3.3983804937426015e-7",
            "extra": "mean: 3.4814523672677895 usec\nrounds: 149477"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 270889.7970600074,
            "unit": "iter/sec",
            "range": "stddev: 3.5445193043041546e-7",
            "extra": "mean: 3.6915380750884474 usec\nrounds: 141024"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 66300.12053698077,
            "unit": "iter/sec",
            "range": "stddev: 0.00000107986624198444",
            "extra": "mean: 15.08292883784761 usec\nrounds: 69152"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 33127.15118456829,
            "unit": "iter/sec",
            "range": "stddev: 0.000005214291041786589",
            "extra": "mean: 30.186718876865957 usec\nrounds: 34974"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 44455.4473173321,
            "unit": "iter/sec",
            "range": "stddev: 0.000002357615629054299",
            "extra": "mean: 22.494431174244966 usec\nrounds: 46269"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 425.1483054896478,
            "unit": "iter/sec",
            "range": "stddev: 0.00002467608672561399",
            "extra": "mean: 2.352120394431043 msec\nrounds: 431"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 39.582290463677744,
            "unit": "iter/sec",
            "range": "stddev: 0.000643518015067008",
            "extra": "mean: 25.263823499997784 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 35909.29279109688,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016283125802360393",
            "extra": "mean: 27.847944703827018 usec\nrounds: 37272"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 333.7659237476021,
            "unit": "iter/sec",
            "range": "stddev: 0.00004130314221385756",
            "extra": "mean: 2.996111732353517 msec\nrounds: 340"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 28.11792102506357,
            "unit": "iter/sec",
            "range": "stddev: 0.003768085776301151",
            "extra": "mean: 35.5645070312498 msec\nrounds: 32"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 19666.874128616666,
            "unit": "iter/sec",
            "range": "stddev: 0.000003822241561865253",
            "extra": "mean: 50.84692124738474 usec\nrounds: 20520"
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
          "id": "b0352491318f7567b27de077cd0fe6e227d50483",
          "message": "chore: adopt test_documented_paths and fix the doc paths it reports (merges PR #861, addresses #853)\n\n* chore: adopt test_documented_paths and fix the doc paths it reports\n\nAdopt the template's tests/test_documented_paths.py and drop it from\nsync-exclude.toml.\n\nProject docs named package files relative to src/pynetappfoundry/\n(cache/db.py, utils/dict_path.py, ...); rewrite them as repo-root paths\nso the test's resolution stays identical to upstream. Correct stale\npaths (cache/check.py is cli/commands/cache/check.py; the ADR-0007\ncontainer models live under models/ontap/). Allowlist, with reasons,\nthe template files this project excludes or sheds that template-synced\nskills and docs name, plus user-created and historical paths.\n\nAddresses #853\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\n* fix: skip the CI uv cache in the documented-paths scan\n\nCI sets UV_CACHE_DIR to .uv-cache inside the workspace, and the\ndatamodel-code-generator archive there ships markdown naming paths in\nits own project, so every test job failed. Upstream replaced the skip\nset with a git-based scan (pyproject-template #1014); this holds until\nthe next template sync brings that in.\n\nAddresses #853\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\n---------\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T14:10:41Z",
          "tree_id": "254d517dc1ceed2566b4ef956232098862cf72eb",
          "url": "https://github.com/endavis/pynetappfoundry/commit/b0352491318f7567b27de077cd0fe6e227d50483"
        },
        "date": 1793024015443,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 755623.8814841347,
            "unit": "iter/sec",
            "range": "stddev: 1.4169466666750805e-7",
            "extra": "mean: 1.323409734001368 usec\nrounds: 81354"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 466181.76286688284,
            "unit": "iter/sec",
            "range": "stddev: 5.337395733392953e-7",
            "extra": "mean: 2.1450860579579296 usec\nrounds: 51212"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 250185.50059377518,
            "unit": "iter/sec",
            "range": "stddev: 5.239637546031482e-7",
            "extra": "mean: 3.9970341911368177 usec\nrounds: 133441"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 244819.1500031818,
            "unit": "iter/sec",
            "range": "stddev: 8.065814728624941e-7",
            "extra": "mean: 4.084647789958439 usec\nrounds: 133798"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 306659.7638377259,
            "unit": "iter/sec",
            "range": "stddev: 5.144487081490494e-7",
            "extra": "mean: 3.260942966515707 usec\nrounds: 166639"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 93335.87162362556,
            "unit": "iter/sec",
            "range": "stddev: 0.000002110250239862329",
            "extra": "mean: 10.713994336844829 usec\nrounds: 105065"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 69958.44088678266,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014285345556640675",
            "extra": "mean: 14.294200775834204 usec\nrounds: 78107"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 39544.438496115385,
            "unit": "iter/sec",
            "range": "stddev: 0.000002349211201176824",
            "extra": "mean: 25.28800605167865 usec\nrounds: 41641"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 111059.36634513953,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027608198432473908",
            "extra": "mean: 9.004193278865799 usec\nrounds: 122926"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 28257.399885734565,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028398503822649433",
            "extra": "mean: 35.388960203123254 usec\nrounds: 30128"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 56.54376294592649,
            "unit": "iter/sec",
            "range": "stddev: 0.0013910304160765865",
            "extra": "mean: 17.685416532258607 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 52.75753854248918,
            "unit": "iter/sec",
            "range": "stddev: 0.0001895352932854781",
            "extra": "mean: 18.954637149999577 msec\nrounds: 60"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 56.19319814775828,
            "unit": "iter/sec",
            "range": "stddev: 0.001193958998456569",
            "extra": "mean: 17.79574811475458 msec\nrounds: 61"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.253918855292325,
            "unit": "iter/sec",
            "range": "stddev: 0.0030807286933809304",
            "extra": "mean: 97.52368963636502 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 238.5959093245248,
            "unit": "iter/sec",
            "range": "stddev: 0.00048442419036747353",
            "extra": "mean: 4.191186692307688 msec\nrounds: 299"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 50.789180800024255,
            "unit": "iter/sec",
            "range": "stddev: 0.00020369388996097236",
            "extra": "mean: 19.68923271153691 msec\nrounds: 52"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 2.7359763530657637,
            "unit": "iter/sec",
            "range": "stddev: 0.002404055773282668",
            "extra": "mean: 365.5002350000075 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 2.793868045681527,
            "unit": "iter/sec",
            "range": "stddev: 0.005755674206398604",
            "extra": "mean: 357.92671079999536 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 417626.4072804012,
            "unit": "iter/sec",
            "range": "stddev: 3.149760013521813e-7",
            "extra": "mean: 2.39448459811734 usec\nrounds: 43644"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 391663.75844379084,
            "unit": "iter/sec",
            "range": "stddev: 4.031600646500179e-7",
            "extra": "mean: 2.5532104475873116 usec\nrounds: 40976"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 395825.3083240516,
            "unit": "iter/sec",
            "range": "stddev: 2.5361456322543537e-7",
            "extra": "mean: 2.52636700829985 usec\nrounds: 41077"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 154899.82336176382,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010827323480897718",
            "extra": "mean: 6.455785283011785 usec\nrounds: 170620"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 187222.63767218054,
            "unit": "iter/sec",
            "range": "stddev: 7.219971091931421e-7",
            "extra": "mean: 5.3412344384922115 usec\nrounds: 101854"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 436362.70502170274,
            "unit": "iter/sec",
            "range": "stddev: 2.2022183708103995e-7",
            "extra": "mean: 2.2916715578391704 usec\nrounds: 45640"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 446581.3903019759,
            "unit": "iter/sec",
            "range": "stddev: 4.385885897167724e-7",
            "extra": "mean: 2.239233478412089 usec\nrounds: 46642"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 33063.67143653495,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031539346302883055",
            "extra": "mean: 30.244675093613843 usec\nrounds: 34730"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 580985.8198679261,
            "unit": "iter/sec",
            "range": "stddev: 1.757939662936452e-7",
            "extra": "mean: 1.7212124045081296 usec\nrounds: 60607"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 245265.80221926945,
            "unit": "iter/sec",
            "range": "stddev: 6.272237418418259e-7",
            "extra": "mean: 4.077209260123401 usec\nrounds: 132223"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 366481.7837423024,
            "unit": "iter/sec",
            "range": "stddev: 4.585013461231171e-7",
            "extra": "mean: 2.7286485832626437 usec\nrounds: 195695"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 217033.4243317105,
            "unit": "iter/sec",
            "range": "stddev: 6.539230406275376e-7",
            "extra": "mean: 4.6075852283085 usec\nrounds: 115261"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 196367.16123329315,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011084978249959077",
            "extra": "mean: 5.092501178503846 usec\nrounds: 106068"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 49366.24214402433,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021758629425638176",
            "extra": "mean: 20.256757585123335 usec\nrounds: 51878"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 24807.757936867147,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035007858833794718",
            "extra": "mean: 40.30997087866156 usec\nrounds: 25926"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 32600.93781779523,
            "unit": "iter/sec",
            "range": "stddev: 0.0000042288762126474084",
            "extra": "mean: 30.673964215046283 usec\nrounds: 34372"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 310.5811267836139,
            "unit": "iter/sec",
            "range": "stddev: 0.00009412537403621527",
            "extra": "mean: 3.2197706613921637 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 28.701691409974725,
            "unit": "iter/sec",
            "range": "stddev: 0.00029949179922132685",
            "extra": "mean: 34.84115224137867 msec\nrounds: 29"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 26597.97998052995,
            "unit": "iter/sec",
            "range": "stddev: 0.0000041623200512318015",
            "extra": "mean: 37.59684008830792 usec\nrounds: 28078"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 247.15845201820574,
            "unit": "iter/sec",
            "range": "stddev: 0.00005889763620993198",
            "extra": "mean: 4.045987470120341 msec\nrounds: 251"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 22.431306576423616,
            "unit": "iter/sec",
            "range": "stddev: 0.00021668251742115851",
            "extra": "mean: 44.58055069565356 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 13846.039665469425,
            "unit": "iter/sec",
            "range": "stddev: 0.000007950651711943055",
            "extra": "mean: 72.22281779922207 usec\nrounds: 14731"
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
          "id": "32afdc711d0aef13fa6b4dc444c289f64c3c8764",
          "message": "docs: document the nf CLI in docs/usage/cli.md (merges PR #862, addresses #859)\n\nReplace the template's example CLI (the `greet` command in a single\ncli.py, with __PYPI_NAME__/__PACKAGE_NAME__ placeholders) with the\nproject's `nf` entry point, its cli/ package layout, the eight command\ngroups, @with_config, and how to add and test a command. Exclude the\npage from template sync, like docs/usage/basics.md.\n\nSubstitute the package name for the placeholder in tooling-roles.md,\ndoit-tasks-reference.md and ADR-9002, where the result is accurate.\nextensions.md, add-a-feature.md and ADR-9014 describe the template's\nexample code, so they stay template-owned and unchanged.\n\nAddresses #859\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T14:38:20Z",
          "tree_id": "c8ec05faaf8317a9d4b75e22fb1ea0aa5650d1e2",
          "url": "https://github.com/endavis/pynetappfoundry/commit/32afdc711d0aef13fa6b4dc444c289f64c3c8764"
        },
        "date": 1793025662448,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1045963.2797468273,
            "unit": "iter/sec",
            "range": "stddev: 9.24730482585215e-8",
            "extra": "mean: 956.0565073011428 nsec\nrounds: 109016"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 621196.7550683259,
            "unit": "iter/sec",
            "range": "stddev: 1.7906590238887363e-7",
            "extra": "mean: 1.609795917060142 usec\nrounds: 65394"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 325802.0581694386,
            "unit": "iter/sec",
            "range": "stddev: 4.0001312708339284e-7",
            "extra": "mean: 3.069348320322562 usec\nrounds: 172772"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 326594.5907511092,
            "unit": "iter/sec",
            "range": "stddev: 3.5230280202647507e-7",
            "extra": "mean: 3.0619000691351896 usec\nrounds: 170678"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 412761.09302611504,
            "unit": "iter/sec",
            "range": "stddev: 1.5215303748622727e-7",
            "extra": "mean: 2.4227089638429917 usec\nrounds: 42928"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 124668.6684803173,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011696479390083646",
            "extra": "mean: 8.021261574297476 usec\nrounds: 135300"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 93165.46578086233,
            "unit": "iter/sec",
            "range": "stddev: 9.447733141867034e-7",
            "extra": "mean: 10.733590946157388 usec\nrounds: 96843"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 50420.872341944974,
            "unit": "iter/sec",
            "range": "stddev: 0.00000204664217890696",
            "extra": "mean: 19.833056302917292 usec\nrounds: 54562"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 144147.7345375476,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012262430732767327",
            "extra": "mean: 6.937327202596584 usec\nrounds: 158003"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 40723.17903099531,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025819231119379885",
            "extra": "mean: 24.55603967555868 usec\nrounds: 43150"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 65.93884742179603,
            "unit": "iter/sec",
            "range": "stddev: 0.000600501900730849",
            "extra": "mean: 15.165566871425945 msec\nrounds: 70"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 63.40105897212806,
            "unit": "iter/sec",
            "range": "stddev: 0.00017340287951426883",
            "extra": "mean: 15.772607212122644 msec\nrounds: 66"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 70.01917498126947,
            "unit": "iter/sec",
            "range": "stddev: 0.00023434717732001903",
            "extra": "mean: 14.281802095890244 msec\nrounds: 73"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 13.096319596213966,
            "unit": "iter/sec",
            "range": "stddev: 0.0007743672426782657",
            "extra": "mean: 76.357330214291 msec\nrounds: 14"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 248.51324221077522,
            "unit": "iter/sec",
            "range": "stddev: 0.0003955999552852182",
            "extra": "mean: 4.02393043969808 msec\nrounds: 398"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 61.19708759563818,
            "unit": "iter/sec",
            "range": "stddev: 0.0002482051447353254",
            "extra": "mean: 16.34064690476014 msec\nrounds: 63"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 3.349999415157142,
            "unit": "iter/sec",
            "range": "stddev: 0.005519034625025143",
            "extra": "mean: 298.50751479999644 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 3.5471862215947527,
            "unit": "iter/sec",
            "range": "stddev: 0.0009854109576868783",
            "extra": "mean: 281.91358939999986 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 554888.1880726306,
            "unit": "iter/sec",
            "range": "stddev: 1.1754989019493657e-7",
            "extra": "mean: 1.8021648712210607 usec\nrounds: 57386"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 523589.85246918525,
            "unit": "iter/sec",
            "range": "stddev: 1.2293216184405068e-7",
            "extra": "mean: 1.9098918653295573 usec\nrounds: 54151"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 522751.01657137997,
            "unit": "iter/sec",
            "range": "stddev: 1.1868454594050909e-7",
            "extra": "mean: 1.912956586022159 usec\nrounds: 53773"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 222661.66735455353,
            "unit": "iter/sec",
            "range": "stddev: 4.4198462282763285e-7",
            "extra": "mean: 4.491118798673407 usec\nrounds: 116104"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 261510.89015344356,
            "unit": "iter/sec",
            "range": "stddev: 4.102145607482205e-7",
            "extra": "mean: 3.8239325307379826 usec\nrounds: 138678"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 584119.70944526,
            "unit": "iter/sec",
            "range": "stddev: 1.2236855501220466e-7",
            "extra": "mean: 1.7119778426064456 usec\nrounds: 60332"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 584031.4997621139,
            "unit": "iter/sec",
            "range": "stddev: 2.300883205307478e-7",
            "extra": "mean: 1.712236412603288 usec\nrounds: 61638"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 46655.91836871462,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012747559398730072",
            "extra": "mean: 21.433508008504994 usec\nrounds: 48261"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 761062.276122177,
            "unit": "iter/sec",
            "range": "stddev: 1.0837927887501807e-7",
            "extra": "mean: 1.3139529199834696 usec\nrounds: 80206"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 348862.67199936527,
            "unit": "iter/sec",
            "range": "stddev: 3.2658293427350197e-7",
            "extra": "mean: 2.866457435153221 usec\nrounds: 182216"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 485814.86214261234,
            "unit": "iter/sec",
            "range": "stddev: 3.0371233818501086e-7",
            "extra": "mean: 2.058397298900352 usec\nrounds: 50868"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 289582.7061219912,
            "unit": "iter/sec",
            "range": "stddev: 3.805489664882441e-7",
            "extra": "mean: 3.453244889488444 usec\nrounds: 154584"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 278177.74554113444,
            "unit": "iter/sec",
            "range": "stddev: 4.283100265299285e-7",
            "extra": "mean: 3.5948238708122284 usec\nrounds: 145328"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 66738.9657147793,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011265100152127062",
            "extra": "mean: 14.983750336702485 usec\nrounds: 69057"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 34230.257065713486,
            "unit": "iter/sec",
            "range": "stddev: 0.000001566016044630117",
            "extra": "mean: 29.213920248400456 usec\nrounds: 35598"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 45341.79673752081,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014871896935321105",
            "extra": "mean: 22.054706075917135 usec\nrounds: 46791"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 415.97645772924665,
            "unit": "iter/sec",
            "range": "stddev: 0.000029754178177112736",
            "extra": "mean: 2.403982199999612 msec\nrounds: 425"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 36.84240303856518,
            "unit": "iter/sec",
            "range": "stddev: 0.0002070791163934265",
            "extra": "mean: 27.14263776315674 msec\nrounds: 38"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 36000.61477109803,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016986697912330767",
            "extra": "mean: 27.77730342546313 usec\nrounds: 37426"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 327.4290253092929,
            "unit": "iter/sec",
            "range": "stddev: 0.00004352875655788613",
            "extra": "mean: 3.0540969880583724 msec\nrounds: 335"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 28.066065043554175,
            "unit": "iter/sec",
            "range": "stddev: 0.0005447945471657435",
            "extra": "mean: 35.6302174333365 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 19883.849651540306,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025258081153108093",
            "extra": "mean: 50.29207208487089 usec\nrounds: 20462"
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
          "id": "7934e923abb520a2e3c52f6163941bd1d73aaaa3",
          "message": "chore: run unit tests from tmp_path so they stop writing into data/ (merges PR #865, addresses #864)\n\nConfig and setup_logger write under os.getcwd() / \"data\". Unit tests\nthat ran CLI commands from the repository root left log files in its\ndata/ on every run, and once per mutant under mutmut.\n\nAdd an autouse fixture in tests/unit/conftest.py that chdirs each unit\ntest into its tmp_path. Only tests/unit wrote there; tests/conftest.py\nis template-owned and stays as it is. Runtime behaviour is unchanged.\n\nAdd tests/unit/core/test_logging.py, which fails when the fixture is\nremoved: it checks the working directory and that setup_logger writes\nunder tmp_path and not the repository's data/.\n\nAddresses #864\n\n\nClaude-Session: https://claude.ai/code/session_015WG66RnHdWy7pS3G1ygVjp\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-10-26T16:50:24Z",
          "tree_id": "d38b1a188f3cb6ab000576722b1f9e1f63a2fd4f",
          "url": "https://github.com/endavis/pynetappfoundry/commit/7934e923abb520a2e3c52f6163941bd1d73aaaa3"
        },
        "date": 1793033600317,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 780930.0110134792,
            "unit": "iter/sec",
            "range": "stddev: 1.8025167236900248e-7",
            "extra": "mean: 1.2805244847770867 usec\nrounds: 82974"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 485254.94968453684,
            "unit": "iter/sec",
            "range": "stddev: 1.8777549979481994e-7",
            "extra": "mean: 2.060772385011421 usec\nrounds: 51396"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 253371.9633025195,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012484271745401335",
            "extra": "mean: 3.946766591558618 usec\nrounds: 137118"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 255084.96615249215,
            "unit": "iter/sec",
            "range": "stddev: 5.969451752193323e-7",
            "extra": "mean: 3.920262393677057 usec\nrounds: 136743"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 303260.3543156768,
            "unit": "iter/sec",
            "range": "stddev: 9.517033689779782e-7",
            "extra": "mean: 3.297496641974694 usec\nrounds: 170040"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 97927.43942895898,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015872874131935028",
            "extra": "mean: 10.211642475605068 usec\nrounds: 105397"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 72213.32040916997,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015809379462243733",
            "extra": "mean: 13.847860676311118 usec\nrounds: 78716"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 40342.77874034736,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033572627416124208",
            "extra": "mean: 24.787583583078437 usec\nrounds: 42712"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 110130.42156560182,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012168434780519772",
            "extra": "mean: 9.080143213692558 usec\nrounds: 124611"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 27291.331772408714,
            "unit": "iter/sec",
            "range": "stddev: 0.000003846052338969532",
            "extra": "mean: 36.64167100159586 usec\nrounds: 29374"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 52.70351245579561,
            "unit": "iter/sec",
            "range": "stddev: 0.00038066051715934264",
            "extra": "mean: 18.97406744642944 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 52.535165602437004,
            "unit": "iter/sec",
            "range": "stddev: 0.0007044600192749246",
            "extra": "mean: 19.03486909259142 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 56.27076616354663,
            "unit": "iter/sec",
            "range": "stddev: 0.00027000106890612274",
            "extra": "mean: 17.771217066666146 msec\nrounds: 60"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.552180638298431,
            "unit": "iter/sec",
            "range": "stddev: 0.0005900157178213932",
            "extra": "mean: 94.76714190909195 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 288.0517510135226,
            "unit": "iter/sec",
            "range": "stddev: 0.0001660890350473577",
            "extra": "mean: 3.4715984071662698 msec\nrounds: 307"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 50.12307356612468,
            "unit": "iter/sec",
            "range": "stddev: 0.00019360002506269846",
            "extra": "mean: 19.950891452830675 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 2.771439861261052,
            "unit": "iter/sec",
            "range": "stddev: 0.0029690117038309264",
            "extra": "mean: 360.8232723999947 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 2.837726533843388,
            "unit": "iter/sec",
            "range": "stddev: 0.000881992151908083",
            "extra": "mean: 352.3947738000004 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 420028.2247612236,
            "unit": "iter/sec",
            "range": "stddev: 2.0551554355576318e-7",
            "extra": "mean: 2.380792387388912 usec\nrounds: 43625"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 393342.4651484236,
            "unit": "iter/sec",
            "range": "stddev: 2.0314247248228822e-7",
            "extra": "mean: 2.542313857779532 usec\nrounds: 41161"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 394186.08703740285,
            "unit": "iter/sec",
            "range": "stddev: 2.0037758804980282e-7",
            "extra": "mean: 2.53687289552945 usec\nrounds: 41008"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 156144.06929092793,
            "unit": "iter/sec",
            "range": "stddev: 9.647197173963116e-7",
            "extra": "mean: 6.404341865439655 usec\nrounds: 169751"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 188510.58151742836,
            "unit": "iter/sec",
            "range": "stddev: 6.24713863724581e-7",
            "extra": "mean: 5.304742004138092 usec\nrounds: 101740"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 434526.28697978734,
            "unit": "iter/sec",
            "range": "stddev: 1.7238616015415276e-7",
            "extra": "mean: 2.301356741730372 usec\nrounds: 45515"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 444195.8109091552,
            "unit": "iter/sec",
            "range": "stddev: 1.7474790842564778e-7",
            "extra": "mean: 2.251259411819431 usec\nrounds: 46686"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 32871.16266768657,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024562073389427676",
            "extra": "mean: 30.421801933493295 usec\nrounds: 34549"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 591006.4360379212,
            "unit": "iter/sec",
            "range": "stddev: 1.8064786741272576e-7",
            "extra": "mean: 1.6920289509940907 usec\nrounds: 61725"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 247391.5981931571,
            "unit": "iter/sec",
            "range": "stddev: 5.123279887326559e-7",
            "extra": "mean: 4.0421744606671135 usec\nrounds: 129972"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 363913.6954655378,
            "unit": "iter/sec",
            "range": "stddev: 4.4917495211181593e-7",
            "extra": "mean: 2.747904276371756 usec\nrounds: 197668"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 221255.95984250243,
            "unit": "iter/sec",
            "range": "stddev: 5.917494700574004e-7",
            "extra": "mean: 4.519652264787959 usec\nrounds: 117427"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 199787.59600939957,
            "unit": "iter/sec",
            "range": "stddev: 6.554726316210499e-7",
            "extra": "mean: 5.005315745192471 usec\nrounds: 105175"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 49932.57220410002,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021629544593981253",
            "extra": "mean: 20.027007539537266 usec\nrounds: 52258"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 24967.23985047544,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029670992016591745",
            "extra": "mean: 40.052485015918066 usec\nrounds: 26061"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 32828.27294884352,
            "unit": "iter/sec",
            "range": "stddev: 0.000005499796229729922",
            "extra": "mean: 30.46154762872557 usec\nrounds: 34622"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 314.19508122808634,
            "unit": "iter/sec",
            "range": "stddev: 0.00003806242397140557",
            "extra": "mean: 3.1827360125795905 msec\nrounds: 318"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 29.503839498810958,
            "unit": "iter/sec",
            "range": "stddev: 0.00024246888587628896",
            "extra": "mean: 33.89389370967467 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 27091.56339359738,
            "unit": "iter/sec",
            "range": "stddev: 0.000003548628912731167",
            "extra": "mean: 36.91186017844702 usec\nrounds: 28236"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 248.03805262331707,
            "unit": "iter/sec",
            "range": "stddev: 0.00005447126293702901",
            "extra": "mean: 4.0316394578321 msec\nrounds: 249"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 22.592753419527533,
            "unit": "iter/sec",
            "range": "stddev: 0.0007786240040940731",
            "extra": "mean: 44.26197999999738 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 14138.390842413351,
            "unit": "iter/sec",
            "range": "stddev: 0.00000606678033353082",
            "extra": "mean: 70.72940698457201 usec\nrounds: 14976"
          }
        ]
      }
    ]
  }
}